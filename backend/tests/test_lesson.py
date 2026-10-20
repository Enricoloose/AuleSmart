import pytest
from backend.models import Room,Reservation,Lesson,Role,User
from backend.lesson import LessonService
from backend.exceptions.booking_exceptions import UnauthorizeRoleError
from backend.exceptions.lesson_exceptions import MaxDurationLessonError,OverLappingTimeLesson,OverLappingRoomLesson, UnauthorizeDeleteError
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

    service = LessonService()

    service.create(teacher=standard_teacher, lesson=not_started_lesson, room_id=room_with_standard_capacity.id)

    assert len(service.existing_lesson) == 1

def test_only_teacher_create_lesson(room_with_standard_capacity,standard_student, not_started_lesson):

    service = LessonService()

    with pytest.raises(UnauthorizeRoleError):
        service.create(teacher=standard_student,lesson=not_started_lesson, room_id=room_with_standard_capacity.id)

def test_check_lesson_duration(room_with_standard_capacity, standard_teacher):

    service = LessonService()

    start_time = datetime.now()
    end_time = datetime.now() + timedelta(hours=3)

    over_duration_lesson = Lesson(1,"Deep Learning", start_time=start_time, end_time=end_time, teacher_id=standard_teacher.id, room_id=room_with_standard_capacity.id)

    with pytest.raises(MaxDurationLessonError):
        service.create(teacher=standard_teacher,lesson=over_duration_lesson,room_id=room_with_standard_capacity.id)

def test_create_time_overlap_lesson(room_with_standard_capacity,standard_teacher, not_started_lesson):

    #not_started_lesson e overlap_lesson hanno la stessa stanza
    existing_lesson = not_started_lesson

    overlap_start_time = datetime.now() + timedelta(hours=1, minutes=30)
    overlap_end_time = datetime.now() + timedelta(hours=2, minutes=30)

    overlap_lesson = Lesson(id=2,name="Fondamenti di Informatica", start_time=overlap_start_time, end_time=overlap_end_time, teacher_id=standard_teacher.id, room_id=room_with_standard_capacity.id)
    teacher_2 = User(id=2,email="prova2@gmail.com",hased_password="str",name="Marco",surname="Rossi",role=Role.TEACHER)


    service = LessonService(existing_lesson=[existing_lesson])

    with pytest.raises(OverLappingTimeLesson):
        service.create(teacher=teacher_2,lesson=overlap_lesson,room_id=room_with_standard_capacity.id)

    assert len(service.existing_lesson) == 1


def test_create_room_overlap_lesson(standard_teacher,not_started_lesson):

    room_1 = Room(id=1,name="Aula5",capacity=50)
    room_2 = Room(id=2,name="Aula3",capacity=30)

    existing_lesson = Lesson(id=1,name="Deep Learning", start_time=not_started_lesson.start_time, end_time=not_started_lesson.end_time,teacher_id=standard_teacher.id, room_id=room_1.id)

    service = LessonService(existing_lesson=[existing_lesson])

    overlap_room_lesson = Lesson(id=2,name="Fondamenti di Informatica", start_time=not_started_lesson.start_time,end_time=not_started_lesson.end_time,teacher_id=standard_teacher.id,room_id=room_2.id)


    with pytest.raises(OverLappingRoomLesson):
        service.create(teacher=standard_teacher, lesson=overlap_room_lesson,room_id=room_2.id)

    assert len(service.existing_lesson) == 1

def test_success_to_delete_lesson(standard_teacher, not_started_lesson):

    #un professore ha due lezioni e ne cancella una
    lesson_1 = not_started_lesson

    no_overlapping_start_time = not_started_lesson.start_time + timedelta(hours=3)
    no_overlapping_end_time = not_started_lesson.end_time + timedelta(hours=3)

    lesson_2 = Lesson(id=2,name="Fondamenti di Informatica", start_time=no_overlapping_start_time,end_time=no_overlapping_end_time,teacher_id=standard_teacher.id,room_id=not_started_lesson.room_id)

    service = LessonService()

    service.create(teacher=standard_teacher,lesson=lesson_1,room_id=not_started_lesson.room_id)
    service.create(teacher=standard_teacher, lesson=lesson_2,room_id=lesson_2.room_id)

    service.delete(lesson=lesson_2, teacher=standard_teacher)

    assert len(service.existing_lesson) == 1


def test_delete_not_own_lesson(not_started_lesson):

    #docente 1 non può cancellare una lezione di docente 2, indipendetemente da sovrapposizioni temporali o di aula

    teacher_1 = User(id=1,email="prova1@gmail.com",hased_password="psw1",name="Enrico",surname="Danieli",role=Role.TEACHER)
    teacher_2 = User(id=2,email="prova2@gmail.com",hased_password="psw2",name="Mario",surname="Rossi",role=Role.TEACHER)

    lesson_1 = Lesson(id=1,name="Deep Learning",start_time=datetime.now(),end_time=datetime.now(),teacher_id=teacher_1.id,room_id=1)

    service = LessonService()

    service.create(teacher=teacher_1,lesson=lesson_1,room_id=lesson_1.room_id)

    with pytest.raises(UnauthorizeDeleteError):
        service.delete(lesson=lesson_1, teacher=teacher_2)

