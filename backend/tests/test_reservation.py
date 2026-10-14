import pytest
import datetime
from backend.models import Room,Lesson,User,Role
from backend.exceptions import OverbookingError,DoubleBookingError,UnauthorizeRoleError
from backend.reservation import BookingService

def test_success_booking_to_lesson():

    #la capacità dell'aula è un valore statico, dopo per calcolare la capacità rimanente controllo le iscrizioni con la capacità dell'aula
    room = Room(1,"Aula1",5)

    lesson = Lesson(1,"Deep Learning",datetime.datetime(2026,10,13,),datetime.datetime(2026,10,13),1,1)

    student_1 = User(1,"prova@gmail.com","psw","enrico","danieli",Role.STUDENT)

    service = BookingService(room=room,lesson=lesson)
    
    service.book(student=student_1)

    assert len(service.reservation) == 1
    

def test_booking_to_full_lesson():
    room = Room(1,"Aula1",1)
    
    lesson = Lesson(1,"Deep Learning",datetime.datetime(2026,10,13,),datetime.datetime(2026,10,13),1,1)

    student_1 = User(1,"prova@gmail.com","psw","enrico","danieli",Role.STUDENT)

    service = BookingService(room,lesson)

    service.book(student=student_1)
    
    student_2 = User(2,"prova@gmail.com","psw","mario","rossi",Role.STUDENT)

    with pytest.raises(OverbookingError):
        service.book(student=student_2)


def test_double_booking_to_lesson():

    room = Room(1,"Aula",50)

    lesson = Lesson(1,"Deep Learning",datetime.datetime(2026,10,13,),datetime.datetime(2026,10,13),1,1)

    student_1 = User(1,"prova@gmail.com","psw","enrico","danieli",Role.STUDENT)

    service = BookingService(room,lesson)

    service.book(student=student_1)

    with pytest.raises(DoubleBookingError):
        service.book(student=student_1)







    
