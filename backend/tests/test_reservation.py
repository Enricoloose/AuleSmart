import pytest
from datetime import datetime,timedelta
from backend.models import Room,Lesson,User,Role
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


def test_double_booking_to_lesson(not_started_lesson, room_with_standard_capacity,standard_student):

    service = BookingService(room=room_with_standard_capacity,lesson=not_started_lesson)

    service.book(student=standard_student)

    with pytest.raises(DoubleBookingError):
        service.book(student=standard_student)

def test_teacher_booking_to_lesson(not_started_lesson, room_with_standard_capacity):

    teacher = User(id=1,email="prova@gmail.com",hashed_password="psw",name="enrico",surname="danieli",role=Role.TEACHER)

    service = BookingService(room=room_with_standard_capacity,lesson=not_started_lesson)

    with pytest.raises(UnauthorizedRoleError):
        service.book(student=teacher)

def test_booking_to_started_lesson(room_with_standard_capacity,standard_student):

    #Mi serve creare una lezione nel passato 
    start_time = datetime.now() - timedelta(hours=1)
    end_time = datetime.now()
    
    past_lesson = Lesson(id=1,name="Deep Learning",start_time=start_time,end_time=end_time,teacher_id=1,room_id=room_with_standard_capacity.id)

    service = BookingService(room=room_with_standard_capacity,lesson=past_lesson)

    with pytest.raises(ExpiredLessonError):
        service.book(student=standard_student)

def test_fail_to_delete_reservation(room_with_standard_capacity,standard_student):

    #creo una lezione che avverrà tra 15 minuti
    start_time = datetime.now() + timedelta(minutes=15)
    end_time = datetime.now() + timedelta(hours=2)

    future_lesson = Lesson(id=1,name="Deep Learning",start_time=start_time,end_time=end_time,teacher_id=1,room_id=room_with_standard_capacity.id)

    service = BookingService(room=room_with_standard_capacity,lesson=future_lesson)

    with pytest.raises(DeleteReservationError):
        service.delete(standard_student.id)


def test_success_to_delete_reservation(room_with_standard_capacity,not_started_lesson,standard_student):

    service = BookingService(room=room_with_standard_capacity,lesson=not_started_lesson)

    service.book(standard_student)

    service.delete(standard_student.id)

    assert len(service.reservation) == 0

def test_delete_non_existing_reservation(room_with_standard_capacity,not_started_lesson,standard_student):
    
    service = BookingService(room=room_with_standard_capacity,lesson=not_started_lesson)

    with pytest.raises(ReservationNotFoundError):
        service.delete(standard_student.id)






    
