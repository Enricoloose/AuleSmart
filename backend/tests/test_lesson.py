import pytest
from backend.models import Room,Reservation,Lesson,Role,User
from backend.lesson import LessonService
from backend.exceptions.booking_exceptions import UnauthorizeRoleError
from backend.exceptions.lesson_exceptions import MaxDurationLessonError,OverLappingTimeLesson,OverLappingRoomLesson
from datetime import datetime,timedelta
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

def test_success_to_create_lesson(standard_teacher,room_with_standard_capacity,not_started_lesson):

    service = LessonService(user=standard_teacher)

    service.create(teacher=standard_teacher, lesson=not_started_lesson, room_id=room_with_standard_capacity.id)

    assert len(service.existing_lesson) == 1

def test_only_teacher_create_lesson(room_with_standard_capacity,standard_student, not_started_lesson):

    service = LessonService(user=standard_student)

    with pytest.raises(UnauthorizeRoleError):
        service.create(teacher=standard_student,lesson=not_started_lesson, room_id=room_with_standard_capacity.id)

def test_check_lesson_duration(room_with_standard_capacity, standard_teacher):

    service = LessonService(user=standard_teacher)

    start_time = datetime.now()
    end_time = datetime.now() + timedelta(hours=3)

    over_duration_lesson = Lesson(1,"Deep Learning", start_time=start_time, end_time=end_time, teacher_id=standard_teacher.id, room_id=room_with_standard_capacity.id)

    with pytest.raises(MaxDurationLessonError):
        service.create(teacher=standard_teacher,lesson=over_duration_lesson,room_id=room_with_standard_capacity.id)

def test_create_time_overlap_lesson(room_with_standard_capacity,standard_teacher, not_started_lesson):

    existing_lesson = not_started_lesson

    overlap_start_time = datetime.now() + timedelta(hours=1, minutes=30)
    overlap_end_time = datetime.now() + timedelta(hours=2, minutes=30)

    overlap_lesson = Lesson(1,"Fondamenti di Informatica", start_time=overlap_start_time, end_time=overlap_end_time, teacher_id=standard_teacher.id, room_id=room_with_standard_capacity.id)

    service = LessonService(user=standard_teacher,existing_lesson=[existing_lesson])

    with pytest.raises(OverLappingTimeLesson):
        service.create(teacher=standard_teacher,lesson=overlap_lesson,room_id=room_with_standard_capacity.id)

    assert len(service.existing_lesson) == 1


def test_create_room_overlap_lesson(standard_teacher,not_started_lesson):

    room_1 = Room(id=1,name="Aula5",capacity=50)
    room_2 = Room(id=2,name="Aula3",capacity=30)

    service_1 = LessonService(room=room_1,user=standard_teacher)
    service_2 = LessonService(room=room_2, user=standard_teacher)

    service_1.create(teacher=standard_teacher,lesson=not_started_lesson)

    with pytest.raises(OverLappingRoomLesson):
        service_2.create(teacher=standard_teacher, lesson=not_started_lesson)

