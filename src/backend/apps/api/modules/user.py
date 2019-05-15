from django.core.exceptions import *

import apps.db.City.models as city_db
import apps.db.User.models as user_db
from apps.api.modules.exceptions import *


class User(object):
    def __init__(self, email, pswd_hash):
        try:
            user = user_db.User.objects.get(email=email)
            if user.pswd_hash != pswd_hash:
                raise WrongPasswordException('Wrong password.')
        except ObjectDoesNotExist:
            raise UserDoNotExistException('User do not exist.')

        self._user_id = user.user_id

        # some code ...
        # self.user_info = UserInfo(...)

    def get_user_id(self):
        return self._user_id

    @classmethod
    def new_user(cls, email, pswd_hash, gender, resident_city_id):
        if user_db.User.objects.filter(email=email).exists():
            raise UserAlreadyExistsException('User already exists, try to login.')
        resident_city = city_db.City.objects.get(city_id=resident_city_id)
        user = user_db.User.objects.create(email=email,
                                           pswd_hash=pswd_hash,
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
