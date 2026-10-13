from dataclasses import dataclass, field
import datetime
from enum import Enum

@dataclass (frozen=True)
class Room:
    id : int
    name : str
    capacity : int


@dataclass (frozen=True)
class Role(Enum):
    STUDENT = 1
    TEACHER = 2

@dataclass
class User:
    id : int
    email : str
    hased_password : str
    name : str
    surname : str
    role : Role

@dataclass
class Lesson:
    id : int
    name : str
    start_time : datetime
    end_time : datetime
    teacher_id : int
    room_id: int

@dataclass
class Reservation:
    id : int
    student_id : int
    lesson_id : int
    created_at : datetime

    
