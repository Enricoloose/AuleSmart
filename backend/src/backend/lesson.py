from backend.models import Room,Lesson,Reservation,User,Role
from backend.exceptions.booking_exceptions import UnauthorizeRoleError
from backend.exceptions.lesson_exceptions import MaxDurationLessonError,OverLappingTimeLesson,OverLappingRoomLesson, UnauthorizeDeleteError
from datetime import datetime, timedelta

MAX_LESSION_SLOT = timedelta(hours=2,minutes=30)

#gestisce le lezione per tutte le aule, così posso fare il confronto se un docente prenota contemporanemente due aule
class LessonService:
    def __init__(self, existing_lesson: list[Lesson] | None = None) -> None:
        self.existing_lesson = existing_lesson if existing_lesson is not None else []

    def create(self, teacher : User, lesson : Lesson, room_id : int) -> Lesson:

        if(teacher.role != Role.TEACHER):
            raise UnauthorizeRoleError("Non è possibile creare una lezione con questo tipo di account")

        if((lesson.end_time - lesson.start_time) >= MAX_LESSION_SLOT):
            raise MaxDurationLessonError("Durata massima della lezione violata")

        new_lesson_start_time = lesson.start_time
        new_lesson_end_time = lesson.end_time

        for les in self.existing_lesson:
            if(new_lesson_start_time < les.end_time and new_lesson_end_time > les.start_time):
                if(room_id == les.room_id):
                    raise OverLappingTimeLesson("Sovrapposizione temporale della lezione")
                if (teacher.id == les.teacher_id):
                    raise OverLappingRoomLesson("Il docente ha già una lezione programmata")


        new_lesson = Lesson(id=len(self.existing_lesson)+1, name=lesson.name,start_time=lesson.start_time, end_time=lesson.end_time,teacher_id=teacher.id, room_id=room_id)
        self.existing_lesson.append(new_lesson)

        return new_lesson

    def delete(self, lesson: Lesson, teacher : User) -> Lesson:

        if(lesson.teacher_id != teacher.id):
            raise UnauthorizeDeleteError

        for les in self.existing_lesson:
            if (lesson.id == les.id):
                self.existing_lesson.remove(les)
                return

