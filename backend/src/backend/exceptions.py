class OverbookingError(Exception):
    pass

class DoubleBookingError(Exception):
    pass

class UnauthorizeRoleError(Exception):
    pass

class ExpiredLessonError(Exception):
    pass