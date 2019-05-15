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
            raise UserDoNotExistException('User do not exist.')

        db_user.UserSession.objects.filter(user_id=user).delete()

        self.user_dbobj = user
        self.user_session_dbobj = db_user.UserSession.objects.create(user_id=user)

        # some code ...
        # self.user_info = UserInfo(...)

    def get_user_id(self):
        return self.user_dbobj.user_id

    def get_session_id(self):
        return self.user_session_dbobj.session_id

    @classmethod
    def new_user(cls, email, pswd_hash, user_name, gender, resident_city_id):
        if db_user.User.objects.filter(email=email).exists():
            raise UserAlreadyExistsException('User already exists, try to login.')
        resident_city = db_city.City.objects.get(city_id=resident_city_id)
        user = db_user.User.objects.create(email=email,
                                           pswd_hash=pswd_hash)
        user_info = db_user.UserInfo.objects.create(user_id=user,
                                                    user_name=user_name,
                                                    gender=gender,
                                                    resident_city_id=resident_city)
        return cls(email=email, pswd_hash=pswd_hash)


class UserInfoBase(object):
    def __init__(self):
        pass


class UserInfo(UserInfoBase):
    def __init__(self):
        super().__init__()


class FriendInfo(UserInfoBase):
    def __init__(self):
        super().__init__()
