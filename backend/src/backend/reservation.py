from backend.models import Room,Lesson,Reservation,User,Role
from datetime import datetime
from backend.exceptions import OverbookingError,DoubleBookingError,UnauthorizeRoleError,ExpiredLessonError


class BookingService:
    def __init__(self,room: Room, lesson: Lesson, reservation: list[Reservation] | None = None) -> None:
        self.room = room
        self.lesson = lesson
        self.reservation = reservation if reservation is not None else []

    def book(self, student : User) -> Reservation:

        if(student.role != Role.STUDENT):
            raise UnauthorizeRoleError("Non è possibile registrarsi per il tipo di account")

        current_datetime = datetime.now()
        if(current_datetime >= self.lesson.start_time):
            raise ExpiredLessonError("La lezione è già iniziata")

        if(len(self.reservation)>=self.room.capacity):
            raise OverbookingError("Posti esauriti per questa lezione")

        for res in self.reservation:
            if(res.student_id == student.id):
                raise DoubleBookingError("Utente già iscritto per questa lezione")

        new_reservation = Reservation(id = len(self.reservation)+1, student_id = student.id, lesson_id = self.lesson.id, created_at=datetime.now())

        self.reservation.append(new_reservation)
        return new_reservation

            