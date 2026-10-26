class OverbookingError(Exception):
    pass

class DoubleBookingError(Exception):
    pass

class UnauthorizedRoleError(Exception):
    pass

class ExpiredLessonError(Exception):
    pass

class DeleteReservationError(Exception):
    pass

class ReservationNotFoundError(Exception):
    pass
