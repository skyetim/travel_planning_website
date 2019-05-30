from datetime import date as ddate

import apps.api.modules.city as mod_city
import apps.db.Travel.models as db_travel
from apps.api.modules.exceptions import *
from apps.api.modules.user import get_user_instance_by_id, is_friend


# Static Methods
def check_visibility(visibility):
    """
    Return the standard version of visibility.
    """
    assert isinstance(visibility, str)
    v = visibility.upper()
    if v not in (db_travel.Travel.ME,
                 db_travel.Travel.FRIEND,
                 db_travel.Travel.PUBLIC):
        raise VisibilityError(f'Visibility {visibility} is illegal.')
    return v


def get_travel_instance_by_id(travel_id):
    try:
        return db_travel.Travel.objects.get(travel_id=travel_id)
    except db_travel.Travel.DoesNotExist:
        raise TravelDoesNotExistException(
            f'Travel (ID={travel_id}) does not exist.')


def get_travel_group_instance_by_id(travel_group_id):
    try:
        return db_travel.TravelGroup.objects.get(travel_group_id=travel_group_id)
    except db_travel.TravelGroup.DoesNotExist:
        raise TravelGroupDoesNotExistException(
            f'Travel Group (ID={travel_group_id}) does not exist.')


def get_travel_group_instance_by_travel_id(travel_id):
    travel = get_travel_instance_by_id(travel_id=travel_id)
    try:
        return db_travel.TravelGrouping.objects.get(travel_id=travel).travel_group_id
    except db_travel.TravelGroup.DoesNotExist:
        TravelDoesNotBelongToTravelGroup(f'Travel (ID={travel_id})'
                                         f' does not belong to any travel group.')


def get_travel_group_owner_user_instance(travel_group_id):
    travel_group = get_travel_group_instance_by_id(
        travel_group_id=travel_group_id)
    ownership = db_travel.TravelGroupOwnership.objects.get(
        travel_group_id=travel_group)
    return ownership.user_id


def get_travel_group_permission_level(user_id, travel_group_id):
    owner_user = get_travel_group_owner_user_instance(
        travel_group_id=travel_group_id)
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


class TravelInfo(object):
    def __init__(self, user_id, travel_id):
        travel_info = get_travel_instance_by_id(travel_id=travel_id)

        self.permission_level = get_travel_permission_level(
            user_id=user_id, travel_id=travel_id)
        visibility_list = {self.permission_level, db_travel.Travel.PUBLIC}
        if self.permission_level == db_travel.Travel.ME:
            visibility_list.add(db_travel.Travel.FRIEND)
        if travel_info.visibility not in visibility_list:
            raise PermissionDeniedException(f'No permission to access '
                                            f'Travel (ID={self.get_travel_id()}).')
        self.travel_info_dbobj = travel_info

    @classmethod
    def new_travel_info(cls, user_id, city_id, date_start, date_end, visibility, travel_note):
        city = mod_city.get_city_instance_by_id(city_id)
        try:
            dstart, dend = ddate(date_start), ddate(date_end)
        except Exception:
            raise DateFormatError('Date Format Error.')
        if dstart >= dend:
            raise DateStartLaterThanDateEndError(
                'The Date_Start should be earlier than Date_End.')
        v = check_visibility(visibility)

        travel_info = db_travel.Travel.objects.create(date_start=dstart, date_end=dend, city_id=city,
                                                      visibility=v, travel_note=travel_note)
        travel_id = travel_info.travel_id
        return cls(user_id=user_id, travel_id=travel_id)

    def check_permission(self):
        if self.permission_level != db_travel.Travel.ME:
            raise PermissionDeniedException(f'No permission to modify '
                                            f'Travel (ID={self.get_travel_id()}).')

    def get_travel_id(self):
        return self.travel_info_dbobj.travel_id

    def get_travel_note(self):
        return self.travel_info_dbobj.travel_note

    def get_city_id(self):
        city = mod_city.get_city_instance_by_id(self.travel_info_dbobj.city_id)
        return city.city_id

    # 这里直接返回model里的DateField对应值，不确定是否可以
    def get_date_start(self):
        return self.travel_info_dbobj.date_start

    def get_date_end(self):
        return self.travel_info_dbobj.date_end

    def get_visibility(self):
        return self.travel_info_dbobj.visibility

    def set_city_id(self, city_id):
        self.check_permission()

        # TODO: send message to companies
        city = mod_city.get_city_instance_by_id(city_id=city_id)
        self.travel_info_dbobj.city_id = city
        self.travel_info_dbobj.save()

    # date_start必须比date_end早，但是这一步检查应该在哪里做？
    def set_date_start(self, year, month, date):
        self.check_permission()

        # TODO: send message to companies
        try:
            d = ddate(year, month, date)
            self.travel_info_dbobj.date_start = d
            self.travel_info_dbobj.save()
        except ValueError:
            raise DateFormatError(
                f'Illegal Start Date: Year={year}, Month={month}, date={date}.')

    def set_date_end(self, year, month, date):
        self.check_permission()

        # TODO: send message to companies
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

        # TODO: send message to companies
        # to set visibility ME is same to delete, remove all companies
        self.travel_info_dbobj.visibility = v
        self.travel_info_dbobj.save()

    def keys(self):
        return ['travel_id',
                'date_start',
                'date_end',
                'city_id',
                'visibility',
                'travel_note']

    def __getitem__(self, item):
        return getattr(self, f'get_{item}')()


class Travel(object):
    def __init__(self, user_id, travel_id):
        self.permission_level = get_travel_permission_level(
            user_id=user_id, travel_id=travel_id)

        if db_travel.TravelGrouping.objects.filter(travel_id=travel_id).exists():
            self.travel_grouping_dbobj = db_travel.TravelGrouping.objects.get(
                travel_id=travel_id)
        else:
            raise TravelDoesNotBelongToTravelGroup(f'Travel (ID={travel_id})'
                                                   f' does not belong to any travel group.')

        self.travel_dbobj = get_travel_instance_by_id(travel_id=travel_id)
        self.travel_info = TravelInfo(user_id=user_id, travel_id=travel_id)
        self.company_user_id_list = db_travel.TravelAssociation.objects.filter(
            travel_id=self.travel_dbobj)

    @classmethod
    def new_travel(cls, user_id, travel_group_id,
                   date_start, date_end, city_id,
                   visibility, travel_note):
        travel_id = TravelInfo.new_travel_info(user_id, date_start, date_end, city_id,
                                               visibility, travel_note)
        travel_group_id = get_travel_group_instance_by_id(travel_group_id)
        db_travel.TravelGrouping.objects.create(travel_id=travel_id,
                                                travel_group_id=travel_group_id)

        return cls(user_id=user_id, travel_id=travel_id)

    def check_permission(self):
        if self.permission_level != db_travel.Travel.ME:
            raise PermissionDeniedException(f'No permission to modify '
                                            f'Travel (ID={self.get_travel_id()}).')

    def delete(self):
        self.check_permission()

        # TODO: send message to companies
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
        self.company_user_id_list = db_travel.TravelAssociation.objects.filter(
            travel_id=self.travel_dbobj)

    def remove_company(self, company_user_id):
        self.check_permission()
        c_user = get_user_instance_by_id(company_user_id)
        if not db_travel.TravelAssociation.objects.filter(company_user_id=c_user, travel_id=self.travel_dbobj).exists():
            raise TravelAssociationDoesNotExist(f'Travel Association between '
                                                f'User(ID={company_user_id} and Travel (ID={self.get_travel_id()})'
                                                f' does not exist.')
        db_travel.TravelAssociation.objects.delete(company_user_id=c_user,
                                                   travel_id=self.travel_dbobj)
        self.company_user_id_list = db_travel.TravelAssociation.objects.filter(
            travel_id=self.travel_dbobj)

    def move_to_travel_group(self, travel_group_id):
        self.check_permission()

        # TODO: fix (change TravelGroup object simultaneously)
        old_travel_grouping = db_travel.TravelGrouping.objects.get(
            travel_id=self.travel_dbobj)
        old_travel_grouping.delete()

        new_travel_group = get_travel_group_instance_by_id(travel_group_id)
        db_travel.TravelGrouping.objects.create(travel_group_id=new_travel_group,
                                                travel_id=self.travel_dbobj)

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
        self.permission_level = get_travel_group_permission_level(
            user_id=user_id, travel_group_id=travel_group_id)

        self.travel_list = []  # save only travel_id
        travel_list = db_travel.TravelGrouping.objects.filter(
            travel_group_id=travel_group_id)

        for travel in travel_list:
            try:
                self.travel_list.append(travel.travel_id)
            except PermissionDeniedException:
                pass

        if list(self.travel_list) == 0:
            raise PermissionDeniedException(f'No permission to access '
                                            f'TravelGroup (ID={self.get_travel_group_id()}).')

        self.travel_group_dbobj = get_travel_group_instance_by_id(
            travel_group_id=travel_group_id)

    @classmethod
    def new_travel_group(cls, user_id, travel_group_name, travel_group_note, travel_group_color):

        user = get_user_instance_by_id(user_id)
        travel_group = db_travel.TravelGroup.objects.create(travel_group_name=travel_group_name,
                                                            travel_group_note=travel_group_note,
                                                            travel_group_color=travel_group_color)
        db_travel.TravelGroupOwnership.objects.create(
            user_id=user, travel_group_id=travel_group)
        return cls(user_id, travel_group)

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
                   date_start, date_end,
                   city_id,
                   visibility,
                   travel_note):
        self.check_permission()
        travel = Travel.new_travel(user_id=self.get_owner_user_id(),
                                   travel_group_id=self.get_travel_group_id(),
                                   date_start=date_start, date_end=date_end,
                                   city_id=city_id,
                                   visibility=visibility,
                                   travel_note=travel_note)

        self.travel_list.append(travel.get_travel_id())

    def remove_travel(self, travel_id):
        self.check_permission()
        t = self.get_travel_object_in_group(travel_id)
        t.delete()
        self.travel_list.remove(travel_id)

    def travel_move_to_other_group(self, travel_id, other_travel_group_id):
        self.check_permission()
        t = self.get_travel_object_in_group(travel_id)
        t.move_to_travel_group(other_travel_group_id)

    def travel_move_to_new_group(self, travel_id, travel_group_name, travel_group_note, travel_group_color):
        self.check_permission()
        t = self.get_travel_object_in_group(travel_id)
        tg = TravelGroup.new_travel_group(self.get_owner_user_id(
        ), travel_group_name, travel_group_note, travel_group_color)
        t.move_to_travel_group(tg.get_travel_group_id)
        # TODO: add the new travel_group to user's travel_group_list

    def get_owner_user_id(self):
        owner = get_travel_group_owner_user_instance(
            travel_group_id=self.get_travel_group_id())
        return owner.user_id

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

        # TODO: refactor (use dict)
        if travel_id in self.travel_list:
            return Travel(user_id=self.get_owner_user_id(), travel_id=travel_id)

        raise TravelDoesNotExistInTravelGroup(f'TravelGroup (ID={self.get_travel_group_id()})'
                                              f' does not have the '
                                              f'Travel (ID={travel_id}).')

    def keys(self):
        return ['owner_user_id',
                'travel_group_id',
                'travel_group_name',
                'travel_group_note',
                'travel_group_color',
                'travel_list']

    def __getitem__(self, item):
        return getattr(self, f'get_{item}')()
