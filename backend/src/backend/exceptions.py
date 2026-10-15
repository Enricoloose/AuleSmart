class OverbookingError(Exception):
    pass

class DoubleBookingError(Exception):
    pass

class UnauthorizeRoleError(Exception):
    pass

class ExpiredLessonError(Exception):
    pass

class DeleteError(Exception):
    pass

class ReservationNotFoundError(Exception):
    pass