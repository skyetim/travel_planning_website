import re

import apps.api.modules.city as mod_city
import apps.db.Travel.models as db_travel
import apps.db.User.models as db_user
from apps.api.modules.exceptions import *


# Static Methods
def check_pswd_hash_format(pswd_hash):
    pswd_hash_pattern = r'^[0-9A-Fa-f]{32}$'
    if re.match(pattern=pswd_hash_pattern, string=pswd_hash, flags=re.IGNORECASE) is None:
        raise IllegalPswdHashFormat(f'Illegal password hash, should be like '
                                    f'/{pswd_hash_pattern}/.')


def check_user_existence(user_id, need_existence=True):
    """
    Check the existence of user_id in the database user.User. Raise exceptions when the target user_id exists (or not).
        :param: existence, True checks user_id in the database; other checks user_id not in the database.
    """
    exists = db_user.User.objects.filter(user_id=user_id).exists()
    if need_existence:
        if not exists:
            raise UserDoesNotExistException(f'User (ID={user_id}) does not exist.')
    elif exists:
        raise UserAlreadyExistsException(f'User (ID={user_id}) already exist.')


def is_friend(user_id, friend_user_id):
    return db_user.FriendRelation.objects.filter(user_id=user_id, friend_user_id=friend_user_id).exists()


def check_friend_relation_existence(user_id, friend_user_id, need_existence=True):
    if is_friend(user_id=user_id, friend_user_id=friend_user_id):
        if not need_existence:
            raise FriendAlreadyExistsException(f'The friendship between '
                                               f'User (ID={user_id}) and User (ID={friend_user_id})'
                                               f' already exists.')
    elif need_existence:
        raise FriendDoesNotExistException(f'The friendship between '
                                          f'User (ID={user_id}) and User (ID={friend_user_id})'
                                          f' does not exist')


def get_user_instance_by_id(user_id):
    check_user_existence(user_id=user_id)
    return db_user.User.objects.get(user_id=user_id)


class User(object):
    def __init__(self, email, pswd_hash):
        try:
            user = db_user.User.objects.get(email=email)
            if user.pswd_hash != pswd_hash:
                raise WrongPasswordException('Wrong password.')
        except db_user.User.DoesNotExist:
            raise UserDoesNotExistException(f'User (Email={email}) does not exist.')

        db_user.UserSession.objects.filter(user_id=user.user_id).delete()

        self.user_dbobj = user
        self.user_session_dbobj = db_user.UserSession.objects.create(user_id=user)

        self.user_info = UserInfo(user_id=self.get_user_id())

        self.travel_group_list = self.get_others_travel_group_list(other_user_id=self.get_user_id())

        self.friend_info_list = []
        friend_relations = db_user.FriendRelation.objects.filter(user_id=self.get_user_id())
        for fr_dbobj in friend_relations:
            self.friend_info_list.append(FriendInfo(user_id=self.get_user_id(),
                                                    friend_user_id=fr_dbobj.friend_user_id.user_id))

    def get_user_id(self):
        return self.user_dbobj.user_id

    def get_session_id(self):
        return self.user_session_dbobj.session_id

    def get_email(self):
        return self.user_dbobj.email

    def get_user_info(self):
        return self.user_info

    def get_friend_info_list(self):
        return self.friend_info_list

    def get_travel_group_list(self):
        return self.travel_group_list

    def get_others_travel_group_list(self, other_user_id):
        from apps.api.modules.travel import TravelGroup as mod_travel_TravelGroup

        travel_group_list = []
        others_travel_groups = db_travel.TravelGroupOwnership.objects.filter(user_id=other_user_id)
        for tg_dbobj in others_travel_groups:
            try:
                travel_group = mod_travel_TravelGroup(user_id=self.get_user_id(),
                                                      travel_group_id=tg_dbobj.travel_group_id.travel_group_id)
                travel_group_list.append(travel_group)
            except PermissionDeniedException:
                pass

        return travel_group_list

    def set_email(self, email):
        self.user_dbobj.email = email
        self.user_dbobj.save()
        return self.user_dbobj.email

    def set_friend_note(self, friend_user_id, friend_note):
        # TODO: refactor (use dict)

        friend_exist = False
        for fr in self.friend_info_list:
            if fr.get_user_id() == friend_user_id:
                friend_exist = True
                fr.set_friend_note(friend_note)
        if not friend_exist:
            raise FriendDoesNotExistException(f'User (ID={self.get_user_id()})'
                                              f' does not have friendship with '
                                              f'User (ID={friend_user_id})')

    def reset_password(self, old_pswd_hash, new_pswd_hash):
        if self.user_dbobj.pswd_hash != old_pswd_hash:
            raise WrongPasswordException('Wrong password.')
        check_pswd_hash_format(new_pswd_hash)
        self.user_dbobj.pswd_hash = new_pswd_hash
        self.user_dbobj.save()

    # 和类图定义不一致

    def add_friend(self, friend_user_id, friend_note):
        fr = FriendInfo.new_friend_info(user_id=self.get_user_id(),
                                        friend_user_id=friend_user_id,
                                        friend_note=friend_note)
        self.friend_info_list.append(fr)

    def remove_friend(self, friend_user_id):
        # TODO: refactor (use dict)

        friend_exist = False
        for fr in self.friend_info_list:
            if fr.get_user_id() == friend_user_id:
                friend_exist = True
                fr.delete()
                self.friend_info_list.remove(fr)
        if not friend_exist:
            raise FriendDoesNotExistException(f'User (ID={self.get_user_id()})'
                                              f' does not have friendship with '
                                              f'User (ID={friend_user_id})')

    def add_travel_group(self, travel_group_name, travel_group_note, travel_group_color):
        from apps.api.modules.travel import TravelGroup as mod_travel_TravelGroup

        travel_group = mod_travel_TravelGroup.new_travel_group(user_id=self.get_user_id(),
                                                               travel_group_name=travel_group_name,
                                                               travel_group_note=travel_group_note,
                                                               travel_group_color=travel_group_color)
        self.travel_group_list.append(travel_group)
        return travel_group

    def remove_travel_group(self, travel_group_id):
        # TODO: refactor (use dict)

        travel_group_exist = False
        for tg in self.travel_group_list:
            if tg.get_travel_group_id() == travel_group_id:
                travel_group_exist = True
                tg.delete()
                self.travel_group_list.remove(tg)
        if not travel_group_exist:
            raise TravelGroupDoesNotExistException(f'User (ID={self.get_user_id()})'
                                                   f' does not have the Travel Group '
                                                   f'(ID={travel_group_id})')

    @classmethod
    def new_user(cls, email, pswd_hash, user_name, gender, resident_city_id):
        if db_user.User.objects.filter(email=email).exists():
            raise UserAlreadyExistsException(f'User (Email={email}) already exists, try to login.')

        resident_city = mod_city.get_city_instance_by_id(city_id=resident_city_id)

        user = db_user.User.objects.create(email=email, pswd_hash=pswd_hash)
        user_info = db_user.UserInfo.objects.create(user_id=user,
                                                    user_name=user_name,
                                                    gender=gender,
                                                    comment='',
                                                    resident_city_id=resident_city)

        return cls(email=email, pswd_hash=pswd_hash)

    def keys(self):
        return ['user_id',
                'email']

    def __getitem__(self, item):
        return getattr(self, f'get_{item}')()


class UserInfoBase(object):
    def __init__(self, user_id):
        check_user_existence(user_id=user_id)
        self.user_info_dbobj = db_user.UserInfo.objects.get(user_id=user_id)

    def get_user_id(self):
        return self.user_info_dbobj.user_id.user_id

    def get_user_name(self):
        return self.user_info_dbobj.user_name

    def get_gender(self):
        return self.user_info_dbobj.gender

    def get_comment(self):
        return self.user_info_dbobj.comment

    def get_resident_city_id(self):
        return self.user_info_dbobj.resident_city_id.city_id

    def keys(self):
        return ['user_id',
                'user_name',
                'gender',
                'comment',
                'resident_city_id']

    def __getitem__(self, item):
        return getattr(self, f'get_{item}')()


class UserInfo(UserInfoBase):
    def set_user_name(self, user_name):
        self.user_info_dbobj.user_name = user_name
        self.user_info_dbobj.save()

    def set_gender(self, gender):
        if gender not in (db_user.UserInfo.MALE,
                          db_user.UserInfo.FEMALE,
                          db_user.UserInfo.UNKNOWN):
            gender = db_user.UserInfo.OTHER
        self.user_info_dbobj.gender = gender
        self.user_info_dbobj.save()

    def set_comment(self, comment):
        self.user_info_dbobj.comment = comment
        self.user_info_dbobj.save()

    def set_resident_city_id(self, city_id):
        city = mod_city.get_city_instance_by_id(city_id=city_id)
        self.user_info_dbobj.resident_city_id = city
        self.user_info_dbobj.save()


class FriendInfo(UserInfoBase):
    def __init__(self, user_id, friend_user_id):
        check_friend_relation_existence(user_id=user_id, friend_user_id=friend_user_id)
        self.friend_relation_dbobj = db_user.FriendRelation.objects.get(user_id=user_id,
                                                                        friend_user_id=friend_user_id)
        self.self_user_id = user_id
        super().__init__(user_id=friend_user_id)

    def get_friend_note(self):
        return self.friend_relation_dbobj.friend_note

    def set_friend_note(self, friend_note):
        self.friend_relation_dbobj.friend_note = friend_note
        self.friend_relation_dbobj.save()

    def delete(self):
        # TODO: remove all travel association for both user
        # user1 associate with user2's travel
        # user2 associate with user1's travel
        # do not send message?
        self.friend_relation_dbobj.delete()

    @classmethod
    def new_friend_info(cls, user_id, friend_user_id, friend_note):
        check_user_existence(friend_user_id)
        check_friend_relation_existence(user_id, friend_user_id, need_existence=False)
        db_user.FriendRelation.objects.create(user_id=user_id,
                                              friend_user_id=friend_user_id,
                                              friend_note=friend_note)
        return cls(user_id=user_id, friend_user_id=friend_user_id)

    def keys(self):
        return ['user_id',
                'user_name',
                'friend_note',
                'gender',
                'comment',
                'resident_city_id']
