class BackendBaseException(Exception):
    CODE = 1


class WrongPasswordException(BackendBaseException):
    CODE = 2


class UserDoesNotExistException(BackendBaseException):
    CODE = 3


class UserAlreadyExistsException(BackendBaseException):
    CODE = 4


class UserAuthorizationException(BackendBaseException):
    CODE = 5


class FriendDoesNotExistException(UserDoesNotExistException):
    CODE = 6


class NoCityFoundException(BackendBaseException):
    CODE = 7


class CityIdDoesNotExistException(BackendBaseException):
    CODE = 8


class DateFormatError(BackendBaseException):
    CODE = 9


class VisibilityError(BackendBaseException):
    CODE = 10


class TravelDoesNotExistException(BackendBaseException):
    CODE = 11


class TravelGroupDoseNotExistException(BackendBaseException):
    CODE = 12


class TravelGroupOwnershipMismatch(BackendBaseException):
    CODE = 13


class TravelAlreadyExistsInTravelGroup(BackendBaseException):
    CODE = 14


class TravelDoesNotExistInTravelGroup(BackendBaseException):
    CODE = 15


class TravelAlreadyExistsException(BackendBaseException):
    CODE = 16


class DateStartLaterThanDateEndError(BackendBaseException):
    CODE = 17
