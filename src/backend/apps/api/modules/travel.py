import datetime.date as ddate

from apps.api.modules.user import User, FriendInfo

import apps.db.User.models as db_user
import apps.db.Travel.models as db_travel

import apps.api.modules.city as mod_city

from django.core.exceptions import *
from apps.api.modules.exceptions import *


class Travel(object):
    def __init__(self):
        pass


class TravelInfo(object):
    def __init__(self, user_id, travel_id):
        if not db_user.User.objects.filter(user_id=user_id).exists():
            raise UserDoesNotExistException(
                f'User (ID={user_id}) does not exist.')
        try:
            travelinfo = db_travel.Travel.objects.get(travel_id=travel_id)
        except ObjectDoesNotExist:
            raise TravelDoesNotExistException(f"Travel (ID={travel_id}) does not exist.")
        # 是否应该判断这个travel_id是否属于user_id？
        self.travelinfo_dbobj = travelinfo
        self.user_id = user_id

    def get_user_id(self):
        return self.user_id

    def get_travel_id(self):
        return self.travelinfo_dbobj.travel_id

    def get_travel_note(self):
        return self.travelinfo_dbobj.travel_note

    def get_city(self):
        return mod_city.get_city_instance_by_id(self.travelinfo_dbobj.city_id)

    # 这里直接返回model里的DateField对应值，不确定是否可以
    def get_date_start(self):
        return self.travelinfo_dbobj.date_start

    def get_date_end(self):
        return self.travelinfo_dbobj.date_end

    def get_visibility(self):
        return self.travelinfo_dbobj.visibility

    def set_city(self, city_id):
        try:
            resident_city = mod_city.get_city_instance_by_id(city_id)
            self.travelinfo_dbobj.resident_city_id = resident_city
            self.travelinfo_dbobj.save()
            return 0
        except CityIdDoesNotExistException as e:
            raise e
            return 1

    # date_start必须比date_end早，但是这一步检查应该在哪里做？
    def set_date_start(self, year, month, date):
        try:
            d = ddate(year, month, date)
            self.travelinfo_dbobj.date_start = d
            self.travelinfo_dbobj.save()
            return 0
        except ValueError:
            raise DateFormatError(
                f'Illegal Start Date: Year={year}, Month={month}, date={date}')
            return 1

    def set_date_end(self, year, month, date):
        try:
            d = ddate(year, month, date)
            self.travelinfo_dbobj.date_end = d
            self.travelinfo_dbobj.save()
            return 0
        except ValueError:
            raise DateFormatError(
                f'Illegal End Date: Year={year}, Month={month}, date={date}')
            return 1

    def set_travel_note(self, note):
        self.travelinfo_dbobj.travel_note = note
        self.travelinfo_dbobj.save()
        return 0

    def set_visibility(self, visibility):
        '''
            Receive "M"(Only ME),"F" (Friend) or "P"(Public).
        '''
        assert type(visibility) == str
        v = visibility.upper()
        if not v in (db_travel.Travel.ONLY_ME, db_travel.Travel.FRIEND, db_travel.Travel.PUBLIC):
            raise VisibilityError(f"Visibility {visibility} is illegal")


class TravelGroup(object):
    def __init__(self, user_id, travel_group_id):
        if not db_user.User.objects.filter(user_id=user_id).exists():
            raise UserDoesNotExistException(
                f'User (ID={user_id}) does not exist.')
        if not db_travel.TravelGroupOwnership.objects.filter(user_id=user_id, travel_group_id=travel_group_id).exists():
            raise TravelGroupOwnershipMismatch(
                f"TravelGroup (ID={travel_group_id}) doesn't belong to User (ID={user_id}).")
        try:
            travelgroup = db_travel.TravelGroup.objects.get(
                travel_group_id=travel_group_id)
        except ObjectDoesNotExist:
            raise TravelGroupDoseNotExistException(
                f"Travel Group (ID={travel_group_id}) does not exist.")
        try:
            travellist = db_travel.TravelGrouping.objects.get(
                travel_group_id=travel_group_id)
        except ObjectDoesNotExist:
            raise TravelGroupDoseNotExistException(
                f"Travel Grouping (ID={travel_group_id}) does not exist.")

        # 是否应该判断这个travel_group_id是否属于user_id？

        self.travelgroup_dbobj = travelgroup
        self.travelgrouping_dbobj = travellist
        self.user_id = user_id

    def add_travel(self):
        pass

    def remove_travel(self):
        pass

    def get_user_id(self):
        pass

    def get_travel_group_id(self):
        pass

    def get_travel_note(self):
        pass

    def get_travel_list(self):
        pass

    def set_travel_group_note(self):
        pass