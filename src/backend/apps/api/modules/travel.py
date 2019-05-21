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

        if db_travel.TravelGrouping.objects.filter(travel_id=travel_id).exists():
            self.travel_group_id = db_travel.TravelGrouping.objects.get(
                travel_id=travel_id)
        else:
            raise TravelDoesNotExistBelongToTravelGroup(
                f"Travel (ID={travel_id}) doen't belong to any travel group.")

        self.travel_dbobj = db_travel.Travel.objects.get(travel_id=travel_id)
        self.travel_info = TravelInfo(user_id=user_id, travel_id=travel_id)
        self.company_user_id_list = db_travel.TravelAssociation.objects.filter(
            travel_id=self.travel_dbobj)#掉了id？
            

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

    def delete(self):
        self.travel_dbobj.delete()

    def add_company(self, company_user_id):
        cuser = mod_user.get_user_instance_by_id(company_user_id)
        if db_travel.TravelAssociation.objects.filter(company_user_id=cuser, travel_id=self.travel_dbobj).exists():
            raise TravelAssociationAlreadyExist(
                f"Travel Association between User(ID={company_user_id} and Travel (ID={self.travel_id}) already exists.")
        db_travel.TravelAssociation.objects.create(
            company_user_id=cuser, travel_id=self.travel_dbobj)
        self.company_user_id_list = db_travel.TravelAssociation.objects.filter(
            travel_id=self.travel_dbobj)

    def remove_company(self, user_id, company_user_id):
        cuser = mod_user.get_user_instance_by_id(company_user_id)
        if not db_travel.TravelAssociation.objects.filter(company_user_id=cuser, travel_id=self.travel_dbobj).exists():
            raise TravelAssociationDoesNotExist(
                f"Travel Association between User(ID={company_user_id} and Travel (ID={self.travel_id}) does not exist.")
        db_travel.TravelAssociation.objects.delete(
            company_user_id=cuser, travel_id=self.travel_dbobj)
        self.company_user_id_list = db_travel.TravelAssociation.objects.filter(
            travel_id=self.travel_dbobj)

    def move_to_travel_group(self, travel_group_id):
        old_travelgrouping = db_travel.TravelGrouping.objects.get(
            travel_id=self.travel_dbobj)
        old_travelgrouping.delete()

        new_travel_group = get_travel_group_instance_by_id(travel_group_id)
        old_travelgrouping = db_travel.TravelGrouping.objects.create(
            travel_group_id=new_travel_group, travel_id=self.travel_dbobj)

    def move_to_new_travel_group(self, travel_group_name, travel_group_note, travel_group_color):
        new_travel_group = TravelGroup.new_travelgroup(
            user_id=self.user_id, travel_group_name=travel_group_name, travel_group_note=travel_group_note, travel_group_color=travel_group_color)
        self.move_to_travel_group(new_travel_group)

    def get_user_id(self):
        return self.user_id

    def get_travel_id(self):
        return self.travel_dbobj.travel_id

    def get_travel_group_id(self):
        return self.travel_group_id

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
        mod_user.check_user_existance(user_id=user_id)
        city = mod_city.get_city_instance_by_id(city_id)
        try:
            dstart, dend = ddate(date_start), ddate(date_end)
        except Exception:
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
        # 这里不对 应该是返回一个List of Travel 而不是返回数据库对象
        try:
            travellist = db_travel.TravelGrouping.objects.filter(
                travel_group_id=travel_group_id)
        except ObjectDoesNotExist:
            raise TravelGroupDoseNotExistException(
                f"Travel Grouping (ID={travel_group_id}) does not exist.")
        self.travel_list = []
        for t in travellist:
            self.travel_list.append(
                Travel(user_id=user_id, travel_id=t.travel_id))

        self.travelgroup_dbobj = travelgroup
        self.user_id = user_id

    @classmethod
    def new_travelgroup(cls, user_id, travel_group_name, travel_group_note, travel_group_color):
        # mod_user.check_user_existance(user_id)
        user = mod_user.get_user_instance_by_id(user_id)
        travel_group = db_travel.TravelGroup.objects.create(
            travel_group_name=travel_group_name, travel_group_note=travel_group_note, travel_group_color=travel_group_color)
        db_travel.TravelGroupOwnership.objects.create(
            travel_group_id=travel_group, user_id=user)
        return cls(user_id, travel_group)

    def delete(self):
        self.travelgroup_dbobj.delete()

    def add_travel(self, travel_id):
        check_travel_existance(travel_id=travel_id)
        if db_travel.TravelGrouping.objects.filter(travel_id=travel_id).exists():
            raise TravelAlreadyExistsInTravelGroup(
                f'Travel (ID={travel_id}) already exists in the travelgrouping database.')
        t = get_travel_instance_by_id(travel_id=travel_id)
        db_travel.TravelGrouping.objects.create(
            travel_id=t, travel_group_id=self.travelgroup_dbobj)
        self.travel_list.append(
            Travel(user_id=self.get_user_id(), travel_id=travel_id))

    def add_new_travel(self, travel_note, city_id, date_start, date_end, visibility, company_user_id_list):
        t = Travel.new_travel(user_id=self.get_user_id(), travel_group_id=self.get_travel_group_id(
        ), travel_note=travel_note, city_id=city_id, date_start=date_start, date_end=date_end, visibility=visibility, company_user_id_list=company_user_id_list)
        self.travel_list.append(t)

    def remove_travel(self, travel_id):
        t = self.get_travel_object_in_group(travel_id)
        t.delete()
        self.travel_list.remove(t)

    def travel_move_to_other_group(self, travel_id, other_travel_group_id):
        t = self.get_travel_object_in_group(travel_id)
        t.move_to_travel_group(other_travel_group_id)

    def travel_move_to_new_group(self, travel_id, travel_group_name, travel_group_note, travel_group_color):
        t = self.get_travel_object_in_group(travel_id)
        t.move_to_new_travel_group(
            travel_group_name, travel_group_note, travel_group_color)

    def get_user_id(self):
        return self.user_id

    def get_travel_group_id(self):
        return self.travelgroup_dbobj.travel_group_id

    def get_travel_group_name(self):
        return self.travelgroup_dbobj.travel_group_name

    def get_travel_group_note(self):
        return self.travelgroup_dbobj.travel_group_note

    def get_travel_group_color(self):
        return self.travelgroup_dbobj.travel_group_color

    def get_travel_list(self):
        return self.travel_list

    def set_travel_group_name(self, name):
        self.travelgroup_dbobj.travel_group_name = name
        self.travelgroup_dbobj.save()

    def set_travel_group_note(self, note):
        self.travelgroup_dbobj.travel_group_note = note
        self.travelgroup_dbobj.save()

    def set_travel_group_color(self, color):
        self.travelgroup_dbobj.travel_group_color = color
        self.travelgroup_dbobj.save()

    def get_travel_object_in_group(self, travel_id):
        travel_exist = False
        for t in self.travel_list:
            if t.get_travel_id() == travel_id:
                travel_exist = True
                return t
        if not travel_exist:
            raise TravelDoesNotExistInTravelGroup(
                f"TravelGroup (ID={self.get_travel_group_id()}) doesn't have the Travel (ID={travel_id}).")


# Static Methods
def check_visibility(visibility):
    assert type(visibility) == str
    v = visibility.upper()
    if not v in (db_travel.Travel.ONLY_ME, db_travel.Travel.FRIEND, db_travel.Travel.PUBLIC):
        raise VisibilityError(f"Visibility {visibility} is illegal.")
    return v


def check_travel_existance(travel_id):
    if not db_travel.Travel.objects.filter(travel_id=travel_id).exists():
        raise TravelDoesNotExistException(
            f'Travel (ID={travel_id}) does not exist.')


def get_travel_group_instance_by_id(travel_group_id):
    if not db_travel.TravelGroup.objects.filter(travel_group_id).exists():
        raise TravelGroupDoseNotExistException(
            f'Travel Group (ID={travel_group_id}) does not exist.')
    # check_travel_group_existance(user_id)
    return db_travel.TravelGroup.objects.get(travel_group_id=travel_group_id)


def get_travel_instance_by_id(travel_id):
    try:
        travelinfo = db_travel.Travel.objects.get(travel_id=travel_id)
    except ObjectDoesNotExist:
        raise TravelDoesNotExistException(
            f"Travel (ID={travel_id}) does not exist.")
    return travelinfo
