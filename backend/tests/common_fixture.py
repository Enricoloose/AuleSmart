import pytest
from backend.models import Room, User, Role, Lesson
from datetime import datetime,timedelta

@pytest.fixture
def room_with_standard_capacity() -> Room:
    id = 1
    name = "Aula1"
    capacity = 50
    return Room(id=id, name=name, capacity=capacity)

@pytest.fixture
def standard_student() -> User:
    id = 1
    email = "prova@gmail.com"
    hased_password = "pasw"
    name = "enrico"
    surname = "danieli"
    role = Role.STUDENT
    return User(id=id,email=email,hashed_password=hased_password,name=name,surname=surname,role=role)

@pytest.fixture
def not_started_lesson() -> Lesson:
    start_time = datetime.now() + timedelta(hours=1)
    end_time = datetime.now() + timedelta(hours=2)
    return Lesson(id=1,name="Deep Learning",start_time=start_time,end_time=end_time,teacher_id=1,room_id=1)