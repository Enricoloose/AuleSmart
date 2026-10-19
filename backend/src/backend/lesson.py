from backend.models import Room,Lesson,Reservation,User,Role
from backend.exceptions.booking_exceptions import UnauthorizeRoleError
from datetime import datetime

class LessonService:
    def __init__(self,room: Room, user: User, existing_lesson: list[Lesson] | None = None) -> None:
        self.room = room
        self.user = user
        self.existing_lesson = existing_lesson if existing_lesson is not None else []

    def create(self, teacher : User, lesson : Lesson) -> Lesson:

        new_lesson = Lesson(id=len(self.existing_lesson)+1, name=lesson.name,start_time=lesson.start_time, end_time=lesson.end_time,teacher_id=teacher.id, room_id=self.room.id)
        self.existing_lesson.append(new_lesson)

        return new_lesson

