from datetime import date as ddate

from django.core.exceptions import *

import apps.api.modules.city as mod_city
import apps.db.Travel.models as db_travel
from apps.api.modules.exceptions import *
from apps.api.modules.user import get_user_instance_by_id, is_friend


# Static Methods
def check_visibility(visibility):
    '''
        Return the standard version of visibility.
    '''
    assert isinstance(visibility, str)
    v = visibility.upper()
    if v not in (db_travel.Travel.ME,
                 db_travel.Travel.FRIEND,
                 db_travel.Travel.PUBLIC):
        raise VisibilityError(f'Visibility {visibility} is illegal.')
    return v


def check_travel_existence(travel_id):
    if not db_travel.Travel.objects.filter(travel_id=travel_id).exists():
        raise TravelDoesNotExistException(f'Travel (ID={travel_id}) does not exist.')

def check_travel_group_existence(travel_group_id):
    if not db_travel.TravelGroup.objects.filter(travel_group_id=travel_group_id).exists():
        raise TravelGroupDoesNotExistException(f'Travel Group (ID={travel_group_id}) does not exist.')

def get_travel_group_instance_by_id(travel_group_id):
    try:
        travel_group = db_travel.TravelGroup.objects.get(travel_group_id=travel_group_id)
    except db_travel.TravelGroup.DoesNotExist:
        raise TravelGroupDoesNotExistException(f'Travel Group (ID={travel_group_id}) does not exist.')
    return travel_group


def get_travel_instance_by_id(travel_id):
    try:
        travel = db_travel.Travel.objects.get(travel_id=travel_id)
    except db_travel.Travel.DoesNotExist:
        raise TravelDoesNotExistException(f'Travel (ID={travel_id}) does not exist.')
    return travel


def get_travel_group_owner_user_instance(travel_group_id):
    travel_group = get_travel_group_instance_by_id(travel_group_id=travel_group_id)
    ownership = db_travel.TravelGroupOwnership.objects.get(travel_group_id=travel_group)
    return ownership.user_id


def get_permission_level(user_id, travel_group_id):
    owner_user = get_travel_group_owner_user_instance(travel_group_id=travel_group_id)
    if user_id == owner_user.user_id:
        permission_level = db_travel.Travel.ME
    elif is_friend(user_id=user_id, friend_user_id=owner_user.user_id):
        permission_level = db_travel.Travel.FRIEND
    else:
        permission_level = db_travel.Travel.PUBLIC
    return permission_level


class TravelInfo(object):
    def __init__(self, travel_id, permission_level):
        travel_info = get_travel_instance_by_id(travel_id)

        permission_level = check_visibility(permission_level)
        self.permission_level = permission_level
        visibility_list = {permission_level, db_travel.Travel.PUBLIC}
        if permission_level == db_travel.Travel.ME:
            visibility_list.add(db_travel.Travel.FRIEND)
            self.read_only = False
        else:
            self.read_only = True
        if travel_info.visibility not in visibility_list:
            raise PermissionDeniedException(f'No permission to access '
                                            f'Travel (ID={self.get_travel_id()}).')
        self.travel_info_dbobj = travel_info

    @classmethod
    def new_travel_info(cls, city_id, date_start, date_end, visibility, travel_note):
        city = mod_city.get_city_instance_by_id(city_id)
        try:
            dstart, dend = ddate(date_start), ddate(date_end)
        except Exception:
            raise DateFormatError('Date Format Error.')
        if dstart >= dend:
            raise DateStartLaterThanDateEndError('The Date_Start should be earlier than Date_End.')
        v = check_visibility(visibility)

        travel_info = db_travel.Travel.objects.create(date_start=dstart, date_end=dend, city_id=city,
                                                      visibility=v, travel_note=travel_note)
        travel_id = travel_info.travel_id
        return cls(travel_id, permission_level=db_travel.Travel.ME)

    def check_permission(self):
        if self.read_only:
            raise PermissionDeniedException(f'No permission to modify '
                                            f'Travel (ID={self.get_travel_id()}).')

    def get_travel_id(self):
        return self.travel_info_dbobj.travel_id

    def get_travel_note(self):
        return self.travel_info_dbobj.travel_note

    def get_city(self):
        return mod_city.get_city_instance_by_id(self.travel_info_dbobj.city_id)

    # 这里直接返回model里的DateField对应值，不确定是否可以
    def get_date_start(self):
        return self.travel_info_dbobj.date_start

    def get_date_end(self):
        return self.travel_info_dbobj.date_end

    def get_visibility(self):
        return self.travel_info_dbobj.visibility

    def set_city(self, city_id):
        self.check_permission()
        resident_city = mod_city.get_city_instance_by_id(city_id)
        self.travel_info_dbobj.resident_city_id = resident_city
        self.travel_info_dbobj.save()


    # date_start必须比date_end早，但是这一步检查应该在哪里做？
    def set_date_start(self, year, month, date):
        self.check_permission()
        try:
            d = ddate(year, month, date)
            self.travel_info_dbobj.date_start = d
            self.travel_info_dbobj.save()
        except ValueError:
            raise DateFormatError(
                    f'Illegal Start Date: Year={year}, Month={month}, date={date}.')

    def set_date_end(self, year, month, date):
        self.check_permission()
        try:
            d = ddate(year, month, date)
            self.travel_info_dbobj.date_end = d
            self.travel_info_dbobj.save()
        except ValueError:
            raise DateFormatError(
                    f'Illegal End Date: Year={year}, Month={month}, date={date}.')

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
        v = check_visibility(visibility)
        self.travel_info_dbobj.visibility = v
        self.travel_info_dbobj.save()


class Travel(object):
    def __init__(self, travel_id, permission_level):
        check_travel_existence(travel_id)
        permission_level = check_visibility(permission_level)
        self.permission_level = permission_level
        self.read_only = (permission_level != db_travel.Travel.ME)

        if db_travel.TravelGrouping.objects.filter(travel_id=travel_id).exists():
            self.travel_grouping_dbobj = db_travel.TravelGrouping.objects.get(travel_id=travel_id)
        else:
            raise TravelDoesNotExistBelongToTravelGroup(f'Travel (ID={travel_id})'
                                                        f' does not belong to any travel group.')

        self.travel_dbobj = db_travel.Travel.objects.get(travel_id=travel_id)
        self.travel_info = TravelInfo(travel_id=travel_id,
                                      permission_level=permission_level)
        self.company_user_id_list = db_travel.TravelAssociation.objects.filter(travel_id=self.travel_dbobj)

    @classmethod
    def new_travel(cls, travel_group_id,
                   date_start, date_end, city_id,
                   visibility, travel_note, company_user_id_list):
        travel_id = TravelInfo.new_travel_info(date_start, date_end, city_id,
                                               visibility, travel_note)
        travel_group_id = get_travel_group_instance_by_id(travel_group_id)
        db_travel.TravelGrouping.objects.create(travel_id=travel_id,
                                                travel_group_id=travel_group_id)
        for c_user in company_user_id_list:
            c_user_id = get_user_instance_by_id(c_user)
            db_travel.TravelAssociation.objects.create(travel_id=travel_id,
                                                       company_user_id=c_user_id)

        return cls(travel_id=travel_id, permission_level=db_travel.Travel.ME)

    def check_permission(self):
        if self.read_only:
            raise PermissionDeniedException(f'No permission to modify '
                                            f'Travel (ID={self.get_travel_id()}).')

    def delete(self):
        self.check_permission()
        self.travel_dbobj.delete()

    def add_company(self, company_user_id):
        self.check_permission()
        c_user = get_user_instance_by_id(company_user_id)
        if db_travel.TravelAssociation.objects.filter(company_user_id=c_user,
                                                      travel_id=self.travel_dbobj).exists():
            raise TravelAssociationAlreadyExist(f'Travel Association between '
                                                f'User(ID={company_user_id} and Travel (ID={self.get_travel_id()})'
                                                f' already exists.')
        db_travel.TravelAssociation.objects.create(company_user_id=c_user,
                                                   travel_id=self.travel_dbobj)
        self.company_user_id_list = db_travel.TravelAssociation.objects.filter(travel_id=self.travel_dbobj)

    def remove_company(self, company_user_id):
        self.check_permission()
        c_user = get_user_instance_by_id(company_user_id)
        if not db_travel.TravelAssociation.objects.filter(company_user_id=c_user, travel_id=self.travel_dbobj).exists():
            raise TravelAssociationDoesNotExist(f'Travel Association between '
                                                f'User(ID={company_user_id} and Travel (ID={self.get_travel_id()})'
                                                f' does not exist.')
        db_travel.TravelAssociation.objects.delete(company_user_id=c_user,
                                                   travel_id=self.travel_dbobj)
        self.company_user_id_list = db_travel.TravelAssociation.objects.filter(travel_id=self.travel_dbobj)

    def move_to_travel_group(self, travel_group_id):
        self.check_permission()
        old_travel_grouping = db_travel.TravelGrouping.objects.get(travel_id=self.travel_dbobj)
        old_travel_grouping.delete()

        new_travel_group = get_travel_group_instance_by_id(travel_group_id)
        db_travel.TravelGrouping.objects.create(travel_group_id=new_travel_group,
                                                travel_id=self.travel_dbobj)

    def move_to_new_travel_group(self, travel_group_name, travel_group_note, travel_group_color):
        self.check_permission()
        owner = get_travel_group_owner_user_instance(travel_group_id=self.get_travel_group_id())
        new_travel_group = TravelGroup.new_travel_group(user_id=owner,
                                                        travel_group_name=travel_group_name,
                                                        travel_group_note=travel_group_note,
                                                        travel_group_color=travel_group_color)
        self.move_to_travel_group(new_travel_group)

    def get_travel_id(self):
        return self.travel_dbobj.travel_id

    def get_travel_group_id(self):
        return self.travel_grouping_dbobj.travel_group_id

    def get_travel_info(self):
        return self.travel_info

    def get_company_list(self):
        return self.company_user_id_list


class TravelGroup(object):
    def __init__(self, user_id, travel_group_id):
        travel_group=get_travel_group_instance_by_id(travel_group_id)

        self.permission_level = get_permission_level(user_id=user_id, travel_group_id=travel_group_id)
        self.read_only = (self.permission_level != db_travel.Travel.ME)

        # 这里不对 应该是返回一个List of Travel 而不是返回数据库对象
        self.travel_list = []
        travel_list = db_travel.TravelGrouping.objects.filter(travel_group_id=travel_group_id)
        for travel in travel_list:
            try:
                self.travel_list.append(Travel(travel_id=travel.travel_id,
                                               permission_level=self.permission_level))
            except PermissionDeniedException:
                pass
        if list(self.travel_list) == 0:
            raise PermissionDeniedException(f'No permission to access '
                                            f'TravelGroup (ID={self.get_travel_group_id()}).')

        self.travel_group_dbobj = travel_group

    @classmethod
    def new_travel_group(cls, user_id, travel_group_name, travel_group_note, travel_group_color):
        # mod_user.check_user_existence(user_id)
        user = get_user_instance_by_id(user_id)
        travel_group = db_travel.TravelGroup.objects.create(travel_group_name=travel_group_name,
                                                            travel_group_note=travel_group_note,
                                                            travel_group_color=travel_group_color)
        db_travel.TravelGroupOwnership.objects.create(user_id=user, travel_group_id=travel_group)
        return cls(user_id, travel_group)

    def check_permission(self):
        if self.read_only:
            raise PermissionDeniedException(f'No permission to modify '
                                            f'TravelGroup (ID={self.get_travel_group_id()}).')

    def delete(self):
        self.check_permission()
        self.travel_group_dbobj.delete()

    def add_travel(self, travel_id):
        self.check_permission()
        check_travel_existence(travel_id=travel_id)
        if db_travel.TravelGrouping.objects.filter(travel_id=travel_id).exists():
            raise TravelAlreadyExistsInTravelGroup(
                    f'Travel (ID={travel_id}) already exists in the travelgrouping database.')
        travel = get_travel_instance_by_id(travel_id=travel_id)
        db_travel.TravelGrouping.objects.create(travel_id=travel,
                                                travel_group_id=self.travel_group_dbobj)
        self.travel_list.append(Travel(travel_id=travel_id,
                                       permission_level=db_travel.Travel.ME))

    def add_new_travel(self, travel_note, city_id,
                       date_start, date_end,
                       visibility,
                       company_user_id_list):
        self.check_permission()
        travel = Travel.new_travel(travel_group_id=self.get_travel_group_id(),
                                   date_start=date_start, date_end=date_end,
                                   city_id=city_id,
                                   visibility=visibility,
                                   travel_note=travel_note,
                                   company_user_id_list=company_user_id_list)
        self.travel_list.append(travel)

    def remove_travel(self, travel_id):
        self.check_permission()
        t = self.get_travel_object_in_group(travel_id)
        t.delete()
        self.travel_list.remove(t)

    def travel_move_to_other_group(self, travel_id, other_travel_group_id):
        self.check_permission()
        t = self.get_travel_object_in_group(travel_id)
        t.move_to_travel_group(other_travel_group_id)

    def travel_move_to_new_group(self, travel_id, travel_group_name, travel_group_note, travel_group_color):
        self.check_permission()
        t = self.get_travel_object_in_group(travel_id)
        t.move_to_new_travel_group(travel_group_name,
                                   travel_group_note,
                                   travel_group_color)

    def get_travel_group_id(self):
        return self.travel_group_dbobj.travel_group_id

    def get_travel_group_name(self):
        return self.travel_group_dbobj.travel_group_name

    def get_travel_group_note(self):
        return self.travel_group_dbobj.travel_group_note

    def get_travel_group_color(self):
        return self.travel_group_dbobj.travel_group_color

    def get_travel_list(self):
        return self.travel_list

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

    def get_travel_object_in_group(self, travel_id):
        for t in self.travel_list:
            if t.get_travel_id() == travel_id:
                return t
        raise TravelDoesNotExistInTravelGroup(f'TravelGroup (ID={self.get_travel_group_id()})'
                                              f' does not have the '
                                              f'Travel (ID={travel_id}).')
