import pytest
from datetime import datetime,timedelta
from backend.models import Room,Lesson,User,Role
from backend.exceptions import OverbookingError,DoubleBookingError,UnauthorizeRoleError,ExpiredLessonError
from backend.reservation import BookingService

@pytest.fixture
def not_started_lesson() -> Lesson:
    start_time = datetime.now() + timedelta(hours=1)
    end_time = datetime.now() + timedelta(hours=2)
    return Lesson(1,"Deep Learning",start_time,end_time,1,1)

def test_success_booking_to_lesson(not_started_lesson):

    #la capacità dell'aula è un valore statico, dopo per calcolare la capacità rimanente controllo le iscrizioni con la capacità dell'aula
    room = Room(1,"Aula1",5)

    student_1 = User(1,"prova@gmail.com","psw","enrico","danieli",Role.STUDENT)

    service = BookingService(room=room,lesson=not_started_lesson)
    
    service.book(student=student_1)

    assert len(service.reservation) == 1
    

def test_booking_to_full_lesson(not_started_lesson):
    room = Room(1,"Aula1",1)
    
    lesson = Lesson(1,"Deep Learning",datetime(2026,10,13,),datetime(2026,10,13),1,1)

    student_1 = User(1,"prova@gmail.com","psw","enrico","danieli",Role.STUDENT)

    service = BookingService(room=room,lesson=not_started_lesson)

    service.book(student=student_1)
    
    student_2 = User(2,"prova@gmail.com","psw","mario","rossi",Role.STUDENT)

    with pytest.raises(OverbookingError):
        service.book(student=student_2)


def test_double_booking_to_lesson(not_started_lesson):

    room = Room(1,"Aula",50)

    lesson = Lesson(1,"Deep Learning",datetime(2026,10,13,),datetime(2026,10,13),1,1)

    student_1 = User(1,"prova@gmail.com","psw","enrico","danieli",Role.STUDENT)

    service = BookingService(room=room,lesson=not_started_lesson)

    service.book(student=student_1)

    with pytest.raises(DoubleBookingError):
        service.book(student=student_1)

def test_teacher_booking_to_lesson(not_started_lesson):

    room = Room(1,"Aula",50)

    lesson = Lesson(1,"Deep Learning",datetime(2026,10,13,),datetime(2026,10,13),1,1)

    teacher = User(1,"prova@gmail.com","psw","enrico","danieli",Role.TEACHER)

    service = BookingService(room=room,lesson=not_started_lesson)

    with pytest.raises(UnauthorizeRoleError):
        service.book(student=teacher)

def test_booking_to_started_lesson():
    room = Room(1,"Aula",50)

    #Mi serve creare una lezione nel passato 
    start_time = datetime.now() - timedelta(hours=1)
    end_time = datetime.now()
    
    lesson = Lesson(1,"Deep Learning",start_time,end_time,1,1)

    student_1 = User(1,"prova@gmail.com","psw","enrico","danieli",Role.STUDENT)

    service = BookingService(room,lesson)

    with pytest.raises(ExpiredLessonError):
        service.book(student_1)







    
