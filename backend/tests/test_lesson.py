import pytest
from backend.models import Room,Reservation,Lesson,Role,User
from backend.lesson import LessonService
from backend.exceptions.booking_exceptions import UnauthorizeRoleError
from datetime import datetime
from common_fixture import room_with_standard_capacity,standard_student,not_started_lesson

@pytest.fixture
def standard_teacher() -> User:
    id = 1
    email = "prova@gmail.com"
    hased_password = "pasw"
    name = "enrico"
    surname = "danieli"
    role = Role.TEACHER
    return User(id=id,email=email,hased_password=hased_password,name=name,surname=surname,role=role)

def test_success_to_create_lesson(room_with_standard_capacity):

    teacher = User(id=1,email="prova@gmail.com",hased_password="psw",name="enrico",surname="danieli",role=Role.TEACHER)
    lesson = Lesson(1,"DeepLearning",datetime.now(),datetime.now(),teacher_id=teacher.id,room_id=room_with_standard_capacity.id)

    service = LessonService(room=room_with_standard_capacity,user=teacher)

    service.create(teacher=teacher, lesson=lesson)

    assert len(service.existing_lesson) == 1

def test_only_teacher_create_lesson(room_with_standard_capacity,standard_student):

    service = LessonService(room=room_with_standard_capacity, user=standard_student)

    with pytest.raises(UnauthorizeRoleError):
        service.create(teacher=standard_student,lesson=not_started_lesson)