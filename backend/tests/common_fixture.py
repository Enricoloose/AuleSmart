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
    email = "enrico.danieli@edu.unife.it"
    hased_password = "pasw"
    name = "enrico"
    surname = "danieli"
    role = Role.STUDENT
    return User(id=id,email=email,hashed_password=hased_password,name=name,surname=surname,role=role)

@pytest.fixture
def standard_teacher() -> User:
    id = 2
    email = "mrorss@edu.it"
    hased_password = "pasw"
    name = "Mario"
    surname = "Rossi"
    role = Role.TEACHER
    return User(id=id,email=email,hashed_password=hased_password,name=name,surname=surname,role=role)

@pytest.fixture
def not_started_lesson(standard_teacher,room_with_standard_capacity) -> Lesson:
    start_time = datetime.now() + timedelta(hours=1)
    end_time = datetime.now() + timedelta(hours=2)
    return Lesson(id=1,name="Deep Learning",start_time=start_time,end_time=end_time,teacher_id=standard_teacher.id,room_id=room_with_standard_capacity.id)