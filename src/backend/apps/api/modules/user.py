from django.core.exceptions import *

import apps.db.City.models as db_city
import apps.db.User.models as db_user
from apps.api.modules.exceptions import *


class User(object):
    def __init__(self, email, pswd_hash):
        try:
            user = db_user.User.objects.get(email=email)
            if user.pswd_hash != pswd_hash:
                raise WrongPasswordException('Wrong password.')
        except ObjectDoesNotExist:
            raise UserDoNotExistException(
                'User (Email=%s) do not exist.' % email)

        db_user.UserSession.objects.filter(user_id=user).delete()

        self.user_dbobj = user
        self.user_session_dbobj = db_user.UserSession.objects.create(
            user_id=user)

        # some code ...
        # self.user_info = UserInfo(...)

    def get_user_id(self):
        return self.user_dbobj.user_id

    def get_session_id(self):
        return self.user_session_dbobj.session_id

    @classmethod
    def new_user(cls, email, pswd_hash, user_name, gender, resident_city_id):
        if db_user.User.objects.filter(email=email).exists():
            raise UserAlreadyExistsException(
                'User already exists, try to login.')
        resident_city = db_city.City.objects.get(city_id=resident_city_id)
        user = db_user.User.objects.create(email=email, pswd_hash=pswd_hash)
        user_info = db_user.UserInfo.objects.create(
            user_id=user, user_name=user_name, gender=gender, resident_city_id=resident_city)
        return cls(email=email, pswd_hash=pswd_hash)


class UserInfoBase(object):
    def __init__(self, user_id):
        try:
            userinfo = db_user.UserInfo.objects.get(user_id=user_id)
        except ObjectDoesNotExist:
            raise UserDoNotExistException(
                'User (ID=%s) do not exist.' % user_id)
        self.user_info_dbobj = userinfo

    def get_user_id(self):
        return self.user_info_dbobj.user_id

    def get_user_name(self):
        return self.user_info_dbobj.user_name

    def get_gender(self):
        return self.user_info_dbobj.gender

    def get_resident_city(self):
        try:
            city = db_city.City.objects.get(
                city_id=self.user_info_dbobj.resident_city_id)
        except ObjectDoesNotExist:
            raise CityIdDoNotExistException(
                'City whose ID=%s do not exist.' % self.user_info_dbobj.resident_city_id)
        return city


class UserInfo(UserInfoBase):
    def set_user_name(self, user_name):
        try:
            self.user_info_dbobj.user_name = user_name
            self.user_info_dbobj.save()
            return 0
        except Exception as e:
            raise e
            return 1

    def set_gender(self, gender):
        if not gender in db_user.UserInfo.GENDER_CHOICES:
            raise GenderDoNotExistException
        try:
            self.user_info_dbobj.gender = gender
            self.user_info_dbobj.save()
            return 0
        except Exception as e:
            raise e
            return 1

    def set_resident_city(self, city_id):
        if not db_user.City.objects.filter(city_id=city_id).exists():
            raise CityIdDoNotExistException(
                'City whose ID=%s do not exist.' % city_id)
        try:
            self.user_info_dbobj.resident_city_id = city_id
            self.user_info_dbobj.save()
            return 0
        except Exception as e:
            raise e
            return 1


class FriendInfo(UserInfoBase):
    def __init__(self, user_id, friend_user_id):
        try:
            self.friend_ralation_dbobj = db_user.FriendRelation.objects.get(
                user_id=user_id, friend_user_id=friend_user_id)
        except ObjectDoesNotExist:
            raise FriendDoNotExistException(
                "Friend relation between ID=%d and ID=%d doesn't exist." % (user_id, friend_user_id))
        super().__init__(friend_user_id)

    def get_user_note(self):
        return self.friend_ralation_dbobj.friend_user_note

    def set_user_note(self, user_note):
        try:
            self.friend_ralation_dbobj.friend_user_note = user_note
            self.friend_ralation_dbobj.save()
            return 0
        except Exception as e:
            raise e
            return 1
