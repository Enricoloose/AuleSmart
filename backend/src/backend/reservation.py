from backend.models import Room,Lesson,Reservation,User,Role
from datetime import datetime,timedelta
from backend.exceptions.booking_exceptions import OverbookingError,DoubleBookingError,UnauthorizedRoleError,ExpiredLessonError,DeleteReservationError,ReservationNotFoundError


class BookingService:
    def __init__(self, reservation: list[Reservation] | None = None) -> None:
        self.reservation = reservation if reservation is not None else []
        self.next_id = max((res.id for res in self.reservation),default=0) + 1

    def book(self, student : User, lesson : Lesson, room : Room) -> Reservation:

        if(student.role != Role.STUDENT):
            raise UnauthorizedRoleError("Non è possibile registrarsi per il tipo di account")

        current_datetime = datetime.now()
        if(current_datetime >= lesson.start_time):
            raise ExpiredLessonError("La lezione è già iniziata")

        if(len(self.reservation)>=room.capacity):
            raise OverbookingError("Posti esauriti per questa lezione")

        for res in self.reservation:
            if(res.student_id == student.id):
                raise DoubleBookingError("Utente già iscritto per questa lezione")

        new_reservation = Reservation(id = len(self.reservation)+1, student_id = student.id, lesson_id = lesson.id, created_at=datetime.now())

        self.reservation.append(new_reservation)
        self.next_id += 1
        return new_reservation

    def delete(self,student_id : int, lesson: Lesson) -> None:
        
        current_datetime = datetime.now()
        if(current_datetime > lesson.start_time - timedelta(minutes=30)):
            raise DeleteReservationError("Non puoi cancellare la prenotazione")

        for res in self.reservation:
            if(res.student_id == student_id):
                self.reservation.remove(res)
                return

        raise ReservationNotFoundError("Prenotazione non trovata")


            