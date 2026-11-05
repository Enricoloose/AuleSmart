import pytest
from backend.models import Room,Reservation,Lesson,Role,User
from backend.lesson import LessonService
from backend.exceptions.booking_exceptions import UnauthorizedRoleError
from backend.exceptions.lesson_exceptions import MaxDurationLessonError,OverLappingTimeLesson,OverLappingRoomLesson,UnauthorizedDeleteError,TimeDeleteError,MinDurationLessonError,LessonNotFoundError
from datetime import datetime,timedelta
from common_fixture import room_with_standard_capacity,standard_student,not_started_lesson, standard_teacher


def test_success_to_create_lesson(standard_teacher,room_with_standard_capacity,not_started_lesson):

    service = LessonService()

    service.create(teacher=standard_teacher, lesson=not_started_lesson, room_id=room_with_standard_capacity.id)

    assert len(service.existing_lesson) == 1

def test_only_teacher_create_lesson(room_with_standard_capacity,standard_student, not_started_lesson):

    service = LessonService()

    with pytest.raises(UnauthorizedRoleError):
        service.create(teacher=standard_student,lesson=not_started_lesson, room_id=room_with_standard_capacity.id)

@pytest.mark.parametrize(
        "duration_in_minutes, expected_exception",
        [
            (0,MinDurationLessonError),
            (-15,MinDurationLessonError),
            (151,MaxDurationLessonError),
            (250, MaxDurationLessonError),
        ]
)

def test_invalid_lesson_duration(room_with_standard_capacity, standard_teacher, duration_in_minutes, expected_exception):
    
    service = LessonService()
    
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=duration_in_minutes)

    invalid_time_lesson = Lesson(1,"Deep Learning", start_time=start_time, end_time=end_time, teacher_id=standard_teacher.id, room_id=room_with_standard_capacity.id)

    with pytest.raises(expected_exception):
        service.create(teacher=standard_teacher, lesson=invalid_time_lesson, room_id=room_with_standard_capacity.id)

@pytest.mark.parametrize(
        "overlap_start_time, overlap_end_time",
        [
            #la seconda lezione inizia prima ma finisce durante
            (-30,60),
            #la seconda inizia durante ma finisce dopo
            (30,120),
            #inzia e finisce durante la lezione
            (0,60),
            #stessi orari
            (0,120)
        ]
)

def test_create_time_overlap_lesson(room_with_standard_capacity,standard_teacher,not_started_lesson, overlap_start_time, overlap_end_time):

    #not_started_lesson inizia fra un'ora e finisce fra 2 ore
    existing_lesson = not_started_lesson

    service = LessonService(existing_lesson=[existing_lesson])

    base_start_time = not_started_lesson.start_time

    overlap_lesson_start_time = base_start_time + timedelta(minutes=overlap_start_time)
    overlap_lesson_end_time = overlap_lesson_start_time + timedelta(minutes=overlap_end_time)


    overlap_lesson = Lesson(id=2,name="Fondamenti di Informatica", start_time=overlap_lesson_start_time, end_time=overlap_lesson_end_time, teacher_id=standard_teacher.id, room_id=room_with_standard_capacity.id)
    teacher_2 = User(id=2,email="prova2@gmail.com",hashed_password="str",name="Marco",surname="Rossi",role=Role.TEACHER)


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


def test_delete_not_own_lesson():

    #docente 1 non può cancellare una lezione di docente 2, indipendetemente da sovrapposizioni temporali o di aula

    teacher_1 = User(id=1,email="prova1@gmail.com",hashed_password="psw1",name="Enrico",surname="Danieli",role=Role.TEACHER)
    teacher_2 = User(id=2,email="prova2@gmail.com",hashed_password="psw2",name="Mario",surname="Rossi",role=Role.TEACHER)

    lesson_1 = Lesson(id=1,name="Deep Learning",start_time=datetime.now(),end_time=datetime.now() + timedelta(hours=2),teacher_id=teacher_1.id,room_id=1)

    service = LessonService()

    service.create(teacher=teacher_1,lesson=lesson_1,room_id=lesson_1.room_id)

    with pytest.raises(UnauthorizedDeleteError):
        service.delete(lesson=lesson_1, teacher=teacher_2)

def test_fail_to_delete_started_lesson(standard_teacher, room_with_standard_capacity):

    current_start_time = datetime.now()
    current_end_time = current_start_time + timedelta(hours=2)

    current_lesson = Lesson(id=1,name='Deep Learning',start_time=current_start_time,end_time=current_end_time,teacher_id=standard_teacher.id,room_id=room_with_standard_capacity)

    service = LessonService()

    service.create(teacher=standard_teacher,lesson=current_lesson,room_id=room_with_standard_capacity.id)

    with pytest.raises(TimeDeleteError):
        service.delete(lesson=current_lesson,teacher=standard_teacher)

def test_fail_delete_not_existing_lesson(standard_teacher,room_with_standard_capacity,not_started_lesson):

    service = LessonService([not_started_lesson])

    not_reserved_lesson = Lesson(id=2,name="Fondamenti di Informatica",start_time=datetime.now()+timedelta(minutes=30),end_time=datetime.now() + timedelta(hours=2),teacher_id=standard_teacher.id,room_id=room_with_standard_capacity.id)

    with pytest.raises(LessonNotFoundError):
        service.delete(lesson=not_reserved_lesson,teacher=standard_teacher)

    assert len(service.existing_lesson) == 1


