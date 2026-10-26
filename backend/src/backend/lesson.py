from backend.models import Room,Lesson,Reservation,User,Role
from backend.exceptions.booking_exceptions import UnauthorizedRoleError
from backend.exceptions.lesson_exceptions import MaxDurationLessonError,OverLappingTimeLesson,OverLappingRoomLesson,UnauthorizedDeleteError,TimeDeleteError,MinDurationLessonError,LessonNotFoundError
from datetime import datetime, timedelta

MAX_LESSON_DURATION = timedelta(hours=2,minutes=30)
MIN_LESSON_DURATION = timedelta(hours=1)

#usato solo come catalogo
class LessonArchive:
    def __init__(self, lessons: list[Lesson] | None = None) -> None:
        self.lessons = {l.id: l for l in (lessons or [])}

    def get_by_id(self, lesson_id: int) -> Lesson | None:
        return self.lessons.get(lesson_id)

    def add(self, lesson: Lesson) -> None:
        self.lessons[lesson.id] = lesson

    def remove(self,lesson_id : int) -> None:
        self.lessons.pop(lesson_id,None)

#gestisce le lezione per tutte le aule, così posso fare il confronto se un docente prenota contemporanemente due aule
class LessonService:
    def __init__(self, existing_lesson: list[Lesson] | None = None, lesson_archive : LessonArchive | None = None) -> None:
        self.existing_lesson = existing_lesson if existing_lesson is not None else []
        self.next_id = max((les.id for les in self.existing_lesson),default=0) + 1 
        self.lesson_archive = lesson_archive if lesson_archive is not None else LessonArchive(existing_lesson)

    def create(self, teacher : User, lesson : Lesson, room_id : int) -> Lesson:

        if(teacher.role != Role.TEACHER):
            raise UnauthorizedRoleError("Non è possibile creare una lezione con questo tipo di account")

        if((lesson.end_time - lesson.start_time) > MAX_LESSON_DURATION):
            raise MaxDurationLessonError("Durata massima della lezione violata")

        if((lesson.end_time - lesson.start_time) < MIN_LESSON_DURATION):
            raise MinDurationLessonError("Durata minima della lezione violata")

        new_lesson_start_time = lesson.start_time
        new_lesson_end_time = lesson.end_time

        for les in self.existing_lesson:
            if(new_lesson_start_time < les.end_time and new_lesson_end_time > les.start_time):
                if(room_id == les.room_id):
                    raise OverLappingTimeLesson("Sovrapposizione temporale della lezione")
                if (teacher.id == les.teacher_id):
                    raise OverLappingRoomLesson("Il docente ha già una lezione programmata")


        new_lesson = Lesson(id=self.next_id, name=lesson.name,start_time=lesson.start_time, end_time=lesson.end_time,teacher_id=teacher.id, room_id=room_id)
        self.existing_lesson.append(new_lesson)
        self.next_id +=1

        self.lesson_archive.add(new_lesson)
        return new_lesson

    def delete(self, lesson: Lesson, teacher : User) -> None:

        current_datetime = datetime.now()
    
        if(lesson.teacher_id != teacher.id):
            raise UnauthorizedDeleteError("Impossibile cancellare la lezione per il tipo account")

        if(lesson.start_time <= current_datetime):
            raise TimeDeleteError("Impossibile cancellare la lezione: la lezione è già avviata")

        
        for les in self.existing_lesson:
            if (lesson.id == les.id):
                self.existing_lesson.remove(les)
                self.lesson_archive.remove(les.id)
                return

        raise LessonNotFoundError("Lezione non trovata")
