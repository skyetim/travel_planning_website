from datetime import date as ddate

from apps.api.modules.user import User, FriendInfo

import apps.db.User.models as db_user
import apps.db.Travel.models as db_travel

import apps.api.modules.user as mod_user
import apps.api.modules.city as mod_city

from django.core.exceptions import *
from apps.api.modules.exceptions import *


class Travel(object):
    def __init__(self, user_id, travel_id):
        mod_user.check_user_existance(user_id)
        check_travel_existance(travel_id)
        self.user_id = user_id
        self.travel_id = travel_id
        self.travel_dbobj = db_travel.Travel.objects.get(travel_id=travel_id)
        self.travel_info = TravelInfo(user_id=user_id, travel_id=travel_id)
        self.company_user_id_list = db_travel.TravelAssociation.objects.filter(
            travel_id=self.travel_dbobj)

    @classmethod
    def new_travel(cls, user_id, travel_group_id, travel_note, city_id, date_start, date_end, visibility, company_user_id_list):
        # mod_user.check_user_existance(user_id)
        user_id = mod_user.get_user_instance_by_id(user_id)
        travel_id = TravelInfo.new_travelinfo(
            user_id, travel_note, city_id, date_start, date_end, visibility)
        travel_group_id = get_travel_group_instance_by_id(travel_group_id)
        db_travel.TravelGrouping.objects.create(
            travel_id=travel_id, travel_group_id=travel_group_id)
        for c_user in company_user_id_list:
            c_user_id = mod_user.get_user_instance_by_id(c_user)
            db_travel.TravelAssociation.objects.create(
                travel_id=travel_id, company_user_id=c_user_id)

        return cls(user_id=user_id, travel_id=travel_id)

    def add_company(self):
        pass

    def remove_company(self):
        pass

    def move_to_travel_group(self):
        pass

    def move_to_new_travel_group(self):
        pass

    def get_user_id(self):
        return self.user_id

    def get_travel_id(self):
        return self.travel_dbobj.travel_id

    def get_travel_group_id(self):
        pass

    def get_travel_info(self):
        return self.travel_info

    def get_company_list(self):
        return self.company_user_id_list


class TravelInfo(object):
    def __init__(self, user_id, travel_id):
        mod_user.check_user_existance(user_id)
        try:
            travelinfo = db_travel.Travel.objects.get(travel_id=travel_id)
        except ObjectDoesNotExist:
            raise TravelDoesNotExistException(
                f"Travel (ID={travel_id}) does not exist.")
        # 是否应该判断这个travel_id是否属于user_id？
        self.travelinfo_dbobj = travelinfo
        self.user_id = user_id

    @classmethod
    def new_travelinfo(cls, user_id, travel_note, city_id, date_start, date_end, visbility):
        if not db_user.User.objects.filter(user_id=user_id).exists():
            raise UserDoesNotExistException(
                f'User (ID={user_id}) does not exist.')
        city = mod_city.get_city_instance_by_id(city_id)
        try:
            dstart, dend = ddate(date_start), ddate(date_end)
        except Exception as e:
            raise DateFormatError("Date Format Error.")
        if dstart >= dend:
            raise DateStartLaterThanDateEndError(
                "The Date_Start should be earlier than Date_End.")
        v = check_visibility(visbility)

        travel_info = db_travel.Travel.objects.create(
            date_start=dstart, date_end=dend, city_id=city, visbility=v, travel_note=travel_note)
        travel_id = travel_info.travel_id
        return cls(user_id, travel_id)

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
                f'Illegal Start Date: Year={year}, Month={month}, date={date}.')
            return 1

    def set_date_end(self, year, month, date):
        try:
            d = ddate(year, month, date)
            self.travelinfo_dbobj.date_end = d
            self.travelinfo_dbobj.save()
            return 0
        except ValueError:
            raise DateFormatError(
                f'Illegal End Date: Year={year}, Month={month}, date={date}.')
            return 1

    def set_travel_note(self, note):
        self.travelinfo_dbobj.travel_note = note
        self.travelinfo_dbobj.save()
        return 0

    def set_visibility(self, visibility):
        '''
            Receive "M"(Only ME),"F" (Friend) or "P"(Public).
        '''
        v = check_visibility(visibility)
        self.travelinfo_dbobj.visbility = v
        self.travelinfo_dbobj.save()


def check_visibility(visibility):
    assert type(visibility) == str
    v = visibility.upper()
    if not v in (db_travel.Travel.ONLY_ME, db_travel.Travel.FRIEND, db_travel.Travel.PUBLIC):
        raise VisibilityError(f"Visibility {visibility} is illegal.")
    return v


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
            travellist = db_travel.TravelGrouping.objects.filter(
                travel_group_id=travel_group_id)
        except ObjectDoesNotExist:
            raise TravelGroupDoseNotExistException(
                f"Travel Grouping (ID={travel_group_id}) does not exist.")

        # 是否应该判断这个travel_group_id是否属于user_id？

        self.travelgroup_dbobj = travelgroup
        self.travel_list = travellist
        self.user_id = user_id

    def add_travel(self, travel_id):
        try:
            travelinfo = db_travel.Travel.objects.get(travel_id=travel_id)
        except ObjectDoesNotExist:
            raise TravelDoesNotExistException(
                f"Travel (ID={travel_id}) does not exist.")

        if db_travel.TravelGrouping.objects.filter(travel_id=travel_id).exists():
            raise TravelAlreadyExistsInTravelGroup(
                f'Travel (ID={travel_id}) already exists in the travelgrouping database.')

        try:
            tg = db_travel.TravelGrouping(
                travel_id=travelinfo, travel_group_id=self.travelgroup_dbobj)
            tg.save()
            return 0
        except Exception as e:
            raise e
            return 1

    def remove_travel(self, travel_id):
        try:
            tg = db_travel.TravelGrouping.objects.get(travel_id=travel_id)
            tg.delete()
            return 0
        except ObjectDoesNotExist:
            raise TravelDoesNotExistInTravelGroup(
                f'Travel (ID={travel_id}) doesn\'t exist in the travelgrouping database.')
            return 1
        except Exception as e:
            raise e
            return 2

    def get_user_id(self):
        return self.user_id

    def get_travel_group_id(self):
        return self.travelgroup_dbobj.travel_group_id

    def get_travel_group_note(self):
        return self.travelgroup_dbobj.travel_group_note

    def get_travel_list(self):
        '''
        Return the QuerySet of Model TravelGrouping.
        '''
        return self.travel_list

    def set_travel_group_note(self, note):
        self.travelgroup_dbobj.travel_group_note = note
        self.travelgroup_dbobj.save()
        return 0


def check_travel_existance(travel_id):
    if not db_travel.Travel.objects.filter(travel_id=travel_id).exists():
        raise TravelDoesNotExistException(
            f'Travel (ID={travel_id}) does not exist.')
    return 0


def get_travel_group_instance_by_id(travel_group_id):
    if not db_travel.TravelGroup.objects.filter(travel_group_id).exists():
        raise TravelGroupDoseNotExistException(
            f'Travel Group (ID={travel_group_id}) does not exist.')
    # check_travel_group_existance(user_id)
    return db_travel.TravelGroup.objects.get(travel_group_id=travel_group_id)
