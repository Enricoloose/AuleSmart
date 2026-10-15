class OverbookingError(Exception):
    pass

class DoubleBookingError(Exception):
    pass

class UnauthorizeRoleError(Exception):
    pass

class ExpiredLessonError(Exception):
    pass

class DeleteReservationError(Exception):
    pass

class ReservationNotFoundError(Exception):
    pass