import pytest
from datetime import datetime,timedelta
from backend.models import Room,Lesson,User,Role, Reservation
from backend.exceptions.booking_exceptions import OverbookingError,DoubleBookingError,UnauthorizedRoleError,ExpiredLessonError,DeleteReservationError,ReservationNotFoundError
from backend.reservation import BookingService
from common_fixture import room_with_standard_capacity, standard_student, not_started_lesson, standard_teacher


def test_success_booking_to_lesson(not_started_lesson,room_with_standard_capacity,standard_student):

    #la capacità dell'aula è un valore statico, dopo per calcolare la capacità rimanente controllo le iscrizioni con la capacità dell'aula

    service = BookingService()
    
    service.book(student=standard_student, lesson=not_started_lesson, room=room_with_standard_capacity)

    assert len(service.reservation) == 1
    

def test_booking_to_full_lesson(not_started_lesson, standard_student):

    room_without_capacity = Room(id=2,name="Aula1",capacity=1)

    service = BookingService()

    service.book(student=standard_student,lesson=not_started_lesson,room=room_without_capacity)
    
    student_2 = User(id=3,email="pino.vedi@edu.unife.it",hashed_password="psw",name="Pino",surname="Verdi",role=Role.STUDENT)

    with pytest.raises(OverbookingError):
        service.book(student=student_2, lesson=not_started_lesson, room=room_without_capacity)


def test_double_booking_to_lesson(not_started_lesson, room_with_standard_capacity,standard_student, standard_teacher):

    reservation = Reservation(id=1,student_id=standard_student.id,lesson_id=not_started_lesson.id,created_at=datetime.now())
    service = BookingService([reservation])

    #controllo che lo studente non riesca ad iscriversi due volte alla stessa lezione, ma che comunque sia in grado di iscriversi ad un'altra lezione
    lesson_2_start_time = not_started_lesson.end_time + timedelta(hours=1)
    lesson_2_end_time = lesson_2_start_time + timedelta(hours=2)

    lesson_2 = Lesson(id=not_started_lesson.id + 1, name="Fondamenti di informatica", start_time=lesson_2_start_time, end_time=lesson_2_end_time, teacher_id=standard_teacher, room_id=room_with_standard_capacity.id)

    service.book(student=standard_student,lesson=lesson_2,room=room_with_standard_capacity)

    with pytest.raises(DoubleBookingError):
       service.book(student=standard_student, lesson=not_started_lesson, room=room_with_standard_capacity)

    assert len(service.reservation) == 1

"""
def test_booking_to_overlapping_lesson(not_started_lesson,standard_student,room_with_standard_capacity,):
    #voglio impedire che uno studente si possa iscrivere a due lezioni diverse ma che combaciano con gli orari (stessi orari ma aule diverse)

    room_2 = Room(id=room_with_standard_capacity.id + 1, name="Aula3", capacity=25)

    teacher_2 = User(id=standard_student.id+1, email="pino.vedi@edu.it", hashed_password="psw", name="Pino", surname="Verdi", role=Role.TEACHER)

    overlap_start_time = not_started_lesson.start_time
    overlap_end_time = not_started_lesson.end_time
    overlap_lesson = Lesson(id=not_started_lesson.id + 1, name="Fondamenti di informatica", start_time=overlap_start_time, end_time=overlap_end_time, teacher_id=teacher_2.id, room_id=room_2.id)

    service = BookingService()

    #prima prenotazione
    service.book(student=standard_student,lesson=not_started_lesson,room=room_with_standard_capacity)

    #seconda prenotazione
    with pytest.raises(OverLappingTimeLesson):
        service.book(student=standard_student,lesson=overlap_lesson,room=room_2)

"""

def test_teacher_booking_to_lesson(not_started_lesson, room_with_standard_capacity, standard_student):

    teacher = User(id=standard_student.id+1, email="pino.vedi@edu.it", hashed_password="psw", name="Pino", surname="Verdi", role=Role.TEACHER)

    service = BookingService()

    with pytest.raises(UnauthorizedRoleError):
        service.book(student=teacher, lesson=not_started_lesson, room=room_with_standard_capacity)

def test_booking_to_started_lesson(room_with_standard_capacity,standard_student, standard_teacher):

    #Mi serve creare una lezione nel passato 
    past_start_time = datetime.now() - timedelta(hours=1)
    past_end_time = datetime.now()
    
    past_lesson = Lesson(id=1,name="Deep Learning",start_time=past_start_time,end_time=past_end_time,teacher_id=standard_teacher.id,room_id=room_with_standard_capacity.id)

    service = BookingService()

    with pytest.raises(ExpiredLessonError):
        service.book(student=standard_student, lesson=past_lesson, room=room_with_standard_capacity)

def test_delete_already_started_lesson(standard_student,room_with_standard_capacity, standard_teacher):


    future_start_time = datetime.now() + timedelta(minutes=29)
    future_end_time = future_start_time + timedelta(hours=2)
    future_lesson = Lesson(id=2,name="Fondamenti di Informatica", start_time=future_start_time, end_time=future_end_time, teacher_id=standard_teacher.id, room_id=room_with_standard_capacity.id)

    service = BookingService()

    with pytest.raises(DeleteReservationError):
        service.delete(standard_student.id, lesson = future_lesson)


def test_success_to_delete_reservation(room_with_standard_capacity,not_started_lesson,standard_student):

    service = BookingService(room=room_with_standard_capacity,lesson=not_started_lesson)

    service.book(standard_student)

    service.delete(standard_student.id)

    assert len(service.reservation) == 0

def test_delete_non_existing_reservation(room_with_standard_capacity,not_started_lesson,standard_student):
    
    service = BookingService(room=room_with_standard_capacity,lesson=not_started_lesson)

    with pytest.raises(ReservationNotFoundError):
        service.delete(standard_student.id)






    
