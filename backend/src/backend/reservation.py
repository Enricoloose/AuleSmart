from backend.models import Room,Lesson,Reservation
from datetime import datetime

class BookingService:
    def __init__(self,room: Room, lesson: Lesson, reservation: list[Reservation] | None = None) -> None:
        self.room = room,
        self.lesson = lesson
        self.reservation = reservation if reservation is not None else []

    def book(self, lesson_id: int, student_id : int) -> Reservation:

        new_reservation = Reservation(id = len(self.reservation)+1, student_id = student_id, lesson_id = lesson_id, created_at=datetime.now())

        self.reservation.append(new_reservation)
        return new_reservation

            