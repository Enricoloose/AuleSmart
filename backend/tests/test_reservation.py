import pytest
import datetime
from backend.models import Room,Lesson,User,Role
from backend.exceptions import OverbookingError
from backend.reservation import BookingService

def test_success_booking_to_lesson():

    room = Room(1,"Aula1",1)

    lesson = Lesson(1,"Deep Learning",datetime.datetime(2026,10,13,),datetime.datetime(2026,10,13),1,1)

    student_1 = User(1,"prova@gmail.com","psw","enrico","danieli",Role.STUDENT)

    service = BookingService(room=room,lesson=lesson)
    
    service.book(student_id=student_1.id)

    assert len(service.reservation) == 1

def test_booking_to_full_lesson():
    room = Room(1,"Aula1",1)
    
    lesson = Lesson(1,"Deep Learning",datetime.datetime(2026,10,13,),datetime.datetime(2026,10,13),1,1)

    student_1 = User(1,"prova@gmail.com","psw","enrico","danieli",Role.STUDENT)

    service = BookingService(room,lesson)

    service.book(student_id=student_1.id)
    
    student_2 = User(2,"prova@gmail.com","psw","mario","rossi",Role.STUDENT)

    with pytest.raises(OverbookingError):
        service.book(student_id=student_2.id)

    
