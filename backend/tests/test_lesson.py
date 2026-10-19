import pytest
from backend.models import Room,Reservation,Lesson,Role,User
from backend.lesson import LessonService
from backend.exceptions.booking_exceptions import UnauthorizeRoleError
from datetime import datetime

def test_success_create_lesson():

    room = Room(id=1,name="Aula1",capacity=50)
    teacher = User(id=1,email="prova@gmail.com",hased_password="psw",name="enrico",surname="danieli",role=Role.TEACHER)
    lesson = Lesson(1,"DeepLearning",datetime.now(),datetime.now(),teacher_id=teacher.id,room_id=room.id)

    service = LessonService(room=room,user=teacher)

    service.create(teacher=teacher, lesson=lesson)

    assert len(service.existing_lesson) == 1
    