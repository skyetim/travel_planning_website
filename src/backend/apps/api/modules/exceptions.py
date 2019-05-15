class BackendBaseException(Exception):
    CODE = 1


class WrongPasswordException(BackendBaseException):
    CODE = 2


class UserDoNotExistException(BackendBaseException):
    CODE = 3


class UserAlreadyExistsException(BackendBaseException):
    CODE = 4


class UserAuthorizationException(BackendBaseException):
    CODE = 5


class FriendDoNotExistException(BackendBaseException):
    CODE = 6


class CityIdDoNotExistException(BackendBaseException):
    CODE = 7


class GenderDoNotExistException(BackendBaseException):
    CODE = 8
