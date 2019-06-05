import datetime

import apps.api.modules.city as mod_city
import apps.db.Message.models as db_msg
import apps.db.Travel.models as db_travel
from apps.api.modules.exceptions import *
from apps.api.modules.user import get_user_instance_by_id, get_user_info_instance_by_id, \
    is_friend, check_friend_relation_existence


# Static Methods
def check_visibility(visibility):
    """
    Return the standard version of visibility.
    """
    assert isinstance(visibility, str)
    visibility = visibility.upper()
    if visibility not in (db_travel.Travel.ME,
                          db_travel.Travel.FRIEND,
                          db_travel.Travel.PUBLIC):
        raise VisibilityError(f'Visibility {visibility} is illegal.')
    return visibility


def get_travel_instance_by_id(travel_id):
    try:
        return db_travel.Travel.objects.get(travel_id=travel_id)
    except db_travel.Travel.DoesNotExist:
        raise TravelDoesNotExistException(f'Travel (ID={travel_id}) does not exist.')


def get_travel_group_instance_by_id(travel_group_id):
    try:
        return db_travel.TravelGroup.objects.get(travel_group_id=travel_group_id)
    except db_travel.TravelGroup.DoesNotExist:
        raise TravelGroupDoesNotExistException(f'Travel Group (ID={travel_group_id}) does not exist.')


def get_travel_group_instance_by_travel_id(travel_id):
    travel = get_travel_instance_by_id(travel_id=travel_id)
    try:
        travel_groups = db_travel.TravelGrouping.objects.filter(travel_id=travel)
        return travel_groups.first().travel_group_id
    except AttributeError:
        TravelDoesNotBelongToTravelGroup(f'Travel (ID={travel_id})'
                                         f' does not belong to any travel group.')


def get_travel_group_owner_user_instance(travel_group_id):
    travel_group = get_travel_group_instance_by_id(travel_group_id=travel_group_id)
    ownership = db_travel.TravelGroupOwnership.objects.get(travel_group_id=travel_group)
    return ownership.user_id


def get_travel_owner_user_instance(travel_id):
    travel_group = get_travel_group_instance_by_travel_id(travel_id=travel_id)
    ownership = db_travel.TravelGroupOwnership.objects.get(travel_group_id=travel_group)
    return ownership.user_id


def get_travel_group_permission_level(user_id, travel_group_id):
    owner_user = get_travel_group_owner_user_instance(travel_group_id=travel_group_id)
    if user_id == owner_user.user_id:
        permission_level = db_travel.Travel.ME
    elif is_friend(user_id=user_id, friend_user_id=owner_user.user_id):
        permission_level = db_travel.Travel.FRIEND
    else:
        permission_level = db_travel.Travel.PUBLIC
    return permission_level


def get_travel_permission_level(user_id, travel_id):
    travel_group = get_travel_group_instance_by_travel_id(travel_id=travel_id)
    return get_travel_group_permission_level(user_id=user_id,
                                             travel_group_id=travel_group.travel_group_id)


def delete_associated_travel(user_id, friend_user_id):
    travel_association_list = db_travel.TravelAssociation.objects.filter(company_user_id=friend_user_id)
    for travel_association in travel_association_list:
        owner_dbobj = get_travel_owner_user_instance(travel_id=travel_association.travel_id)
        if owner_dbobj.user_id == user_id:
            travel_association.delete()


class TravelInfo(object):
    def __init__(self, user_id, travel_id):
        travel_info = get_travel_instance_by_id(travel_id=travel_id)

        self.permission_level = get_travel_permission_level(user_id=user_id,
                                                            travel_id=travel_id)

        owner = get_travel_owner_user_instance(travel_id=travel_id)
        self.owner_user_id = owner.user_id
        self.watcher_user_id = user_id

        visibility_list = {self.permission_level, db_travel.Travel.PUBLIC}
        if self.permission_level == db_travel.Travel.ME:
            visibility_list.add(db_travel.Travel.FRIEND)
        if travel_info.visibility not in visibility_list:
            raise PermissionDeniedException(f'No permission to access '
                                            f'Travel (ID={self.get_travel_id()}).')

        self.travel_info_dbobj = travel_info

    @classmethod
    def new_travel_info(cls, user_id, travel_group_id,
                        city_id,
                        date_start, date_end,
                        visibility, travel_note):
        visibility = check_visibility(visibility=visibility)

        if date_start > date_end:
            raise DateStartLaterThanDateEndError('The date_start should be earlier than date_end.')

        city = mod_city.get_city_instance_by_id(city_id=city_id)
        travel = db_travel.Travel.objects.create(city_id=city,
                                                 date_start=date_start, date_end=date_end,
                                                 visibility=visibility,
                                                 travel_note=travel_note)
        travel_group = get_travel_group_instance_by_id(travel_group_id=travel_group_id)
        db_travel.TravelGrouping.objects.create(travel_id=travel,
                                                travel_group_id=travel_group)

        return cls(user_id=user_id, travel_id=travel.travel_id)

    def check_permission(self):
        if self.permission_level != db_travel.Travel.ME:
            raise PermissionDeniedException(f'No permission to modify '
                                            f'Travel (ID={self.get_travel_id()}).')

    def get_owner_user_id(self):
        return self.owner_user_id

    def get_travel_id(self):
        return self.travel_info_dbobj.travel_id

    def get_travel_note(self):
        return self.travel_info_dbobj.travel_note

    def get_city_id(self):
        return self.travel_info_dbobj.city_id.city_id

    def get_date_start(self):
        return self.travel_info_dbobj.date_start.isoformat()

    def get_date_end(self):
        return self.travel_info_dbobj.date_end.isoformat()

    def get_visibility(self):
        return self.travel_info_dbobj.visibility

    def get_company_list(self):
        return Travel(self.watcher_user_id, self.get_travel_id()).get_company_list()

    def set_travel_info(self):
        self.check_permission()

    def set_city_id(self, city_id):
        self.check_permission()

        city = mod_city.get_city_instance_by_id(city_id=city_id)
        self.travel_info_dbobj.city_id = city
        self.travel_info_dbobj.save()

    def set_date_start(self, date_start):
        self.check_permission()

        try:
            self.travel_info_dbobj.date_start = date_start
            self.travel_info_dbobj.save()
        except ValueError:
            raise DateFormatError(f'Illegal Start Date: {date_start}.')

    def set_date_end(self, date_end):
        self.check_permission()

        try:
            self.travel_info_dbobj.date_end = date_end
            self.travel_info_dbobj.save()
        except ValueError:
            raise DateFormatError(f'Illegal End Date: {date_end}.')

    def set_travel_note(self, note):
        self.check_permission()
        self.travel_info_dbobj.travel_note = note
        self.travel_info_dbobj.save()
        return 0

    def set_visibility(self, visibility):
        """
        Receive "M"(ME),"F" (Friend) or "P"(Public).
        """
        self.check_permission()
        visibility = check_visibility(visibility)

        # to set visibility ME is same to delete, remove all companies
        if self.get_visibility() != db_travel.Travel.ME and visibility == db_travel.Travel.ME:
            db_travel.TravelAssociation.objects.filter(travel_id=self.get_travel_id()).delete()
        self.travel_info_dbobj.visibility = visibility
        self.travel_info_dbobj.save()

    def keys(self):
        return ['owner_user_id',
                'travel_id',
                'city_id',
                'city',
                'date_start',
                'date_end',
                'visibility',
                'travel_note']

    def __getitem__(self, item):
        try:
            return getattr(self, f'get_{item}')()
        except AttributeError:
            if item == 'city':
                return dict(mod_city.get_city_instance_by_id(city_id=self.get_city_id()))
            else:
                raise


class Travel(object):
    def __init__(self, user_id, travel_id):
        self.permission_level = get_travel_permission_level(user_id=user_id,
                                                            travel_id=travel_id)
        self.watcher_user_id = user_id
        self.travel_dbobj = get_travel_instance_by_id(travel_id=travel_id)
        self.travel_info = TravelInfo(user_id=user_id, travel_id=travel_id)

        self.company_set = set()
        company_list = db_travel.TravelAssociation.objects.filter(travel_id=self.travel_dbobj)
        for company in company_list:
            self.company_set.add(company.company_user_id.user_id)

    @classmethod
    def new_travel(cls, user_id, travel_group_id,
                   city_id, date_start, date_end,
                   visibility, travel_note):
        travel_info = TravelInfo.new_travel_info(user_id=user_id,
                                                 travel_group_id=travel_group_id,
                                                 city_id=city_id,
                                                 date_start=date_start, date_end=date_end,
                                                 visibility=visibility,
                                                 travel_note=travel_note)

        return cls(user_id=user_id, travel_id=travel_info.get_travel_id())

    def check_permission(self):
        if self.permission_level != db_travel.Travel.ME:
            raise PermissionDeniedException(f'No permission to modify '
                                            f'Travel (ID={self.get_travel_id()}).')

    def delete(self):
        self.check_permission()
        self._send_msg_to_company(msg_type=db_msg.TravelAssociation.DELETE)

        self.travel_dbobj.delete()

    def set_travel_info(self, city_id, date_start, date_end, visibility, travel_note):
        # only when something changed, send one message
        if date_start > date_end:
            raise DateStartLaterThanDateEndError

        travel_info = self.get_travel_info()
        flag = False

        if city_id != travel_info.get_city_id():
            flag = True
            travel_info.set_city_id(city_id)
        if travel_note != travel_info.get_travel_note():
            flag = True
            travel_info.set_travel_note(travel_note)
        if date_start.isoformat() != travel_info.get_date_start():
            flag = True
            travel_info.set_date_start(date_start)
        if date_end.isoformat() != travel_info.get_date_end():
            flag = True
            travel_info.set_date_end(date_end)

        if travel_info.get_visibility() != db_travel.Travel.ME and visibility == db_travel.Travel.ME:
            self._send_msg_to_company(msg_type=db_msg.TravelAssociation.DELETE)
            flag = False
        travel_info.set_visibility(visibility)

        if flag:
            self._send_msg_to_company(msg_type=db_msg.TravelAssociation.MODIFY, modify_term="general")

        return

    def add_company(self, company_user_id):
        self.check_permission()

        if company_user_id in self.company_set:
            raise TravelAssociationAlreadyExist(f'Travel Association between '
                                                f'User(ID={company_user_id} and Travel (ID={self.get_travel_id()})'
                                                f' already exists.')

        company_user_info = get_user_info_instance_by_id(user_id=company_user_id)

        # send messages to existed company users
        target_user_name = company_user_info.user_name
        self._send_msg_to_company(msg_type=db_msg.TravelAssociation.ADD,
                                  content=target_user_name)

        db_travel.TravelAssociation.objects.create(travel_id=self.travel_dbobj,
                                                   company_user_id=company_user_info.user_id)
        self.company_set.add(company_user_id)

    def remove_company(self, company_user_id, actively_leave=False):
        self.check_permission()

        if company_user_id not in self.company_set:
            raise TravelAssociationDoesNotExist(f'Travel Association between '
                                                f'User(ID={company_user_id} and Travel (ID={self.get_travel_id()})'
                                                f' does not exist.')

        company = get_user_instance_by_id(user_id=company_user_id)

        # send message to the user being removed from this trip
        if actively_leave:
            msg_type = db_msg.TravelAssociation.LEAVE
        else:
            msg_type = db_msg.TravelAssociation.REMOVE
        self._send_msg_to_company(msg_type=msg_type,
                                  company_list=[company_user_id])

        db_travel.TravelAssociation.objects.delete(travel_id=self.travel_dbobj,
                                                   company_user_id=company)

        self.company_set.remove(company_user_id)

    def invite_company(self, company_user_id):
        self.check_permission()

        check_friend_relation_existence(user_id=self.watcher_user_id,
                                        friend_user_id=company_user_id,
                                        need_existence=True)

        # send invitation to friend
        self._send_msg_to_company(msg_type=db_msg.TravelAssociation.INVITE,
                                  company_list=[company_user_id])

    def move_to_travel_group(self, new_travel_group_id):
        self.check_permission()

        old_travel_grouping = db_travel.TravelGrouping.objects.get(travel_id=self.travel_dbobj)
        old_travel_grouping.delete()

        new_travel_group = get_travel_group_instance_by_id(travel_group_id=new_travel_group_id)
        db_travel.TravelGrouping.objects.create(travel_group_id=new_travel_group,
                                                travel_id=self.travel_dbobj)

    def get_travel_id(self):
        return self.travel_dbobj.travel_id

    def get_travel_info(self):
        return self.travel_info

    def get_company_list(self):
        return sorted(self.company_set)

    def _send_msg_to_company(self, msg_type, content='', company_list=(), modify_term=''):
        # 仅通知用户将来的关联行程
        travel_info = self.get_travel_info()

        if datetime.date.today().isoformat() > travel_info.get_date_end():
            return

        if len(company_list) > 0:
            target_list = company_list
        else:
            target_list = self.get_company_list()

        if len(target_list) == 0:
            return

        self_user_dbobj = get_user_instance_by_id(user_id=self.watcher_user_id)
        self_user_info_dbobj = get_user_info_instance_by_id(user_id=self.watcher_user_id)
        self_user_name = self_user_info_dbobj.user_name
        travel_dbobj = get_travel_instance_by_id(travel_id=self.get_travel_id())
        city = mod_city.get_city_instance_by_id(travel_info.get_city_id())
        city_name = ' '.join([city.country_name, city.province_name, city.city_name])

        if msg_type == db_msg.TravelAssociation.LEAVE:
            for company_user_id in target_list:
                other_user_dbobj = get_user_instance_by_id(user_id=company_user_id)
                other_user_info_dbobj = get_user_info_instance_by_id(user_id=company_user_id)
                other_user_name = other_user_info_dbobj.user_name
                msg_content = f'Your friend {other_user_name} has leave the travel to {city_name}.'
                db_msg.TravelAssociation.objects.create(user_id=self_user_dbobj,
                                                        friend_user_id=other_user_dbobj,
                                                        travel_id=travel_dbobj,
                                                        msg_type=msg_type,
                                                        msg_content=msg_content)
            return
        elif msg_type == db_msg.TravelAssociation.DELETE:
            msg_content = f'Your friend {self_user_name} has deleted the travel to {city_name}.'
            travel_dbobj = None
        elif msg_type == db_msg.TravelAssociation.ADD:
            msg_content = f'Your friend {self_user_name} has added a new company {content} to the travel to {city_name}.'
        elif msg_type == db_msg.TravelAssociation.REMOVE:
            msg_content = f'Your friend {self_user_name} has removed you from the travel to {city_name}.'
        elif msg_type == db_msg.TravelAssociation.INVITE:
            msg_content = f'Your friend {self_user_name} has invited you to join the travel to {city_name}.'
        elif msg_type == db_msg.TravelAssociation.MODIFY:
            if modify_term == 'city':
                msg_content = f'Your friend {self_user_name}\'s travel\'s destination has been changed from {content} to {city_name}.'
            elif modify_term == 'date_start':
                msg_content = f'Your friend {self_user_name}\'s travel to {city_name}\'s start date has been changed to {content}.'
            elif modify_term == 'date_end':
                msg_content = f'Your friend {self_user_name}\'s travel to {city_name}\'s end date has been changed to {content}.'
            elif modify_term == 'general':
                msg_content = f'Your friend {self_user_name} has updated the travel to {city_name}.'
            else:
                raise MsgTypeError
        else:
            raise MsgTypeError

        for company_user_id in target_list:
            other_user_dbobj = get_user_instance_by_id(company_user_id)
            db_msg.TravelAssociation.objects.create(user_id=other_user_dbobj,
                                                    friend_user_id=self_user_dbobj,
                                                    travel_id=travel_dbobj,
                                                    msg_type=msg_type,
                                                    msg_content=msg_content)


class TravelGroup(object):
    def __init__(self, user_id, travel_group_id):
        self.permission_level = get_travel_group_permission_level(user_id=user_id,
                                                                  travel_group_id=travel_group_id)

        owner = get_travel_group_owner_user_instance(travel_group_id=travel_group_id)
        self.owner_user_id = owner.user_id
        self.watcher_user_id = user_id

        self.travel_set = set()
        travel_list = db_travel.TravelGrouping.objects.filter(travel_group_id=travel_group_id)
        for travel_dbobj in travel_list:
            try:
                travel = Travel(user_id=user_id, travel_id=travel_dbobj.travel_id.travel_id)
                self.travel_set.add(travel.get_travel_id())
            except PermissionDeniedException:
                pass

        if self.permission_level != db_travel.Travel.ME and len(self.travel_set) == 0:
            raise PermissionDeniedException(f'No permission to access '
                                            f'TravelGroup (ID={self.get_travel_group_id()}).')

        self.travel_group_dbobj = get_travel_group_instance_by_id(travel_group_id=travel_group_id)

    @classmethod
    def new_travel_group(cls, user_id, travel_group_name, travel_group_note, travel_group_color):
        user = get_user_instance_by_id(user_id)

        travel_group = db_travel.TravelGroup.objects.create(travel_group_name=travel_group_name,
                                                            travel_group_note=travel_group_note,
                                                            travel_group_color=travel_group_color)
        db_travel.TravelGroupOwnership.objects.create(user_id=user,
                                                      travel_group_id=travel_group)

        return cls(user_id=user_id, travel_group_id=travel_group.travel_group_id)

    def check_permission(self):
        if self.permission_level != db_travel.Travel.ME:
            raise PermissionDeniedException(f'No permission to modify '
                                            f'TravelGroup (ID={self.get_travel_group_id()}).')

    def delete(self):
        self.check_permission()

        for travel_id in self.get_travel_list():
            self.remove_travel(travel_id)
        self.travel_group_dbobj.delete()

    def add_travel(self,
                   city_id,
                   date_start, date_end,
                   visibility,
                   travel_note):
        self.check_permission()

        travel = Travel.new_travel(user_id=self.get_owner_user_id(),
                                   travel_group_id=self.get_travel_group_id(),
                                   city_id=city_id,
                                   date_start=date_start, date_end=date_end,
                                   visibility=visibility,
                                   travel_note=travel_note)

        self.travel_set.add(travel.get_travel_id())
        return travel

    def remove_travel(self, travel_id):
        self.check_permission()

        try:
            self.travel_set.remove(travel_id)
            travel = Travel(user_id=self.get_owner_user_id(), travel_id=travel_id)
            travel.delete()
        except KeyError:
            raise TravelDoesNotExistInTravelGroup(f'TravelGroup (ID={self.get_travel_group_id()})'
                                                  f' does not have the '
                                                  f'Travel (ID={travel_id}).')

    def move_travel_to_other_group(self, travel_id, other_travel_group_id):
        self.check_permission()

        try:
            self.travel_set.remove(travel_id)
            travel = Travel(user_id=self.get_owner_user_id(), travel_id=travel_id)
            travel.move_to_travel_group(new_travel_group_id=other_travel_group_id)
        except KeyError:
            raise TravelDoesNotExistInTravelGroup(f'TravelGroup (ID={self.get_travel_group_id()})'
                                                  f' does not have the '
                                                  f'Travel (ID={travel_id}).')

    def get_owner_user_id(self):
        return self.owner_user_id

    def get_travel_group_id(self):
        return self.travel_group_dbobj.travel_group_id

    def get_travel_group_name(self):
        return self.travel_group_dbobj.travel_group_name

    def get_travel_group_note(self):
        return self.travel_group_dbobj.travel_group_note

    def get_travel_group_color(self):
        return self.travel_group_dbobj.travel_group_color

    def get_travel_list(self):
        return sorted(self.travel_set)

    def get_travel_group_detail(self):
        travel_group_detail = dict(self)
        travel_group_detail['travel_infos'] = {
            'count': len(self.travel_set),
            'travel_info_list': [dict(TravelInfo(user_id=self.watcher_user_id,
                                                 travel_id=travel_id))
                                 for travel_id in self.travel_set]
        }
        return travel_group_detail

    def set_travel_group_name(self, name):
        self.check_permission()
        self.travel_group_dbobj.travel_group_name = name
        self.travel_group_dbobj.save()

    def set_travel_group_note(self, note):
        self.check_permission()
        self.travel_group_dbobj.travel_group_note = note
        self.travel_group_dbobj.save()

    def set_travel_group_color(self, color):
        self.check_permission()
        self.travel_group_dbobj.travel_group_color = color
        self.travel_group_dbobj.save()

    def keys(self):
        return ['owner_user_id',
                'travel_group_id',
                'travel_group_name',
                'travel_group_note',
                'travel_group_color']

    def __getitem__(self, item):
        return getattr(self, f'get_{item}')()
