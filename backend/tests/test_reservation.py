import pytest
from datetime import datetime,timedelta
from backend.models import Room,Lesson,User,Role
from backend.exceptions import OverbookingError,DoubleBookingError,UnauthorizeRoleError,ExpiredLessonError,DeleteReservationError,ReservationNotFoundError
from backend.reservation import BookingService

@pytest.fixture
def not_started_lesson() -> Lesson:
    start_time = datetime.now() + timedelta(hours=1)
    end_time = datetime.now() + timedelta(hours=2)
    return Lesson(id=1,name="Deep Learning",start_time=start_time,end_time=end_time,teacher_id=1,room_id=1)

@pytest.fixture
def room_with_standard_capacity() -> Room:
    id = 1
    name = "Aula1"
    capacity = 50
    return Room(id=id, name=name, capacity=capacity)

@pytest.fixture
def standard_student() -> User:
    id = 1
    email = "prova@gmail.com"
    hased_password = "pasw"
    name = "enrico"
    surname = "danieli"
    role = Role.STUDENT
    return User(id=id,email=email,hased_password=hased_password,name=name,surname=surname,role=role)

def test_success_booking_to_lesson(not_started_lesson,room_with_standard_capacity,standard_student):

    #la capacità dell'aula è un valore statico, dopo per calcolare la capacità rimanente controllo le iscrizioni con la capacità dell'aula

    service = BookingService(room=room_with_standard_capacity,lesson=not_started_lesson)
    
    service.book(student=standard_student)

    assert len(service.reservation) == 1
    

def test_booking_to_full_lesson(not_started_lesson):
    room = Room(id=1,name="Aula1",capacity=1)

    student_1 = User(id=1,email="prova@gmail.com",hased_password="psw",name="enrico",surname="danieli",role=Role.STUDENT)

    service = BookingService(room=room,lesson=not_started_lesson)

    service.book(student=student_1)
    
    student_2 = User(id=2,email="prova@gmail.com",hased_password="psw",name="mario",surname="rossi",role=Role.STUDENT)

    with pytest.raises(OverbookingError):
        service.book(student=student_2)


def test_double_booking_to_lesson(not_started_lesson, room_with_standard_capacity,standard_student):

    service = BookingService(room=room_with_standard_capacity,lesson=not_started_lesson)

    service.book(student=standard_student)

    with pytest.raises(DoubleBookingError):
        service.book(student=standard_student)

def test_teacher_booking_to_lesson(not_started_lesson, room_with_standard_capacity):

    teacher = User(id=1,email="prova@gmail.com",hased_password="psw",name="enrico",surname="danieli",role=Role.TEACHER)

    service = BookingService(room=room_with_standard_capacity,lesson=not_started_lesson)

    with pytest.raises(UnauthorizeRoleError):
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






    
