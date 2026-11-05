from backend.models import Room,Lesson,Reservation,User,Role
from datetime import datetime,timedelta
from backend.exceptions.booking_exceptions import OverbookingError,DoubleBookingError,UnauthorizedRoleError,ExpiredLessonError,DeleteReservationError,ReservationNotFoundError
from backend.exceptions.lesson_exceptions import OverLappingTimeLesson
from backend.lesson import LessonArchive


class BookingService:
    def __init__(self, reservation: list[Reservation] | None = None, lesson_archive : LessonArchive | None = None) -> None:
        self.reservation = reservation if reservation is not None else []
        self.next_id = max((res.id for res in self.reservation),default=0) + 1
        self.lesson_archive = lesson_archive if lesson_archive is not None else LessonArchive()

    def book(self, student : User, lesson : Lesson, room : Room) -> Reservation:

        if(student.role != Role.STUDENT):
            raise UnauthorizedRoleError("Non è possibile registrarsi per il tipo di account")

        current_datetime = datetime.now()
        if(current_datetime >= lesson.start_time):
            raise ExpiredLessonError("La lezione è già iniziata")

        total_reservation_for_lesson = sum(1 for res in self.reservation if res.lesson_id == lesson.id)
        if(total_reservation_for_lesson >= room.capacity):
            raise OverbookingError("Posti esauriti per questa lezione")

        for res in self.reservation:
            if(res.student_id == student.id):
                if(res.lesson_id == lesson.id):
                    raise DoubleBookingError("Utente già iscritto per questa lezione")
                booked_lesson = self.lesson_archive.get_by_id(res.lesson_id)
                if(booked_lesson and lesson.start_time < booked_lesson.end_time and lesson.end_time > booked_lesson.start_time):
                    raise OverLappingTimeLesson("Hai gia una lezione in questo orario")


        new_reservation = Reservation(id = len(self.reservation)+1, student_id = student.id, lesson_id = lesson.id, created_at=datetime.now())

        self.reservation.append(new_reservation)
        self.lesson_archive.add(lesson)
        self.next_id += 1
        return new_reservation

    def delete(self,student_id : int, lesson: Lesson) -> None:
        
        current_datetime = datetime.now()
        if(current_datetime > lesson.start_time - timedelta(minutes=30)):
            raise DeleteReservationError("Non puoi cancellare la prenotazione")

        for res in self.reservation:
            if(res.student_id == student_id and res.lesson_id == lesson.id):
                self.reservation.remove(res)
                return
            

        raise ReservationNotFoundError("Prenotazione non trovata")




            