import pytest
import datetime
from backend.models import Room,Lesson,User,Role
from backend.exceptions import SoldOutError
from backend.reservation import BookingService

def test_success_booking_to_lesson():

    room = Room(1,"Aula1",1)

    lesson = Lesson(1,"Deep Learning",datetime.datetime(2026,10,13,),datetime.datetime(2026,10,13),1,1)

    student_1 = User(1,"prova@gmail.com","psw","enrico","danieli",Role.STUDENT)

    service = BookingService(room=room,lesson=lesson)
    
    service.book(lesson_id=lesson.id,student_id=student_1.id)

    assert len(service.reservation) == 1

    
