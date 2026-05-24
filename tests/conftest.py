import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import database
from models import Grade, Semester, Subject


@pytest.fixture(scope="function")
def test_database(tmp_path):
    original_engine = database.engine
    original_session = database.Session

    database.use_database(f"sqlite:///{tmp_path / 'test_grades.db'}")
    database.Base.metadata.create_all(database.engine)

    yield database.engine

    database.Base.metadata.drop_all(database.engine)
    database.engine.dispose()
    database.engine = original_engine
    database.Session = original_session


@pytest.fixture(scope="function")
def db_session(test_database):
    with database.Session() as session:
        yield session


@pytest.fixture
def seeded_gradebook(db_session):
    semester = Semester(name="1. Semester")
    math = Subject(name="Math", semester=semester)
    physics = Subject(name="Physics", semester=semester)
    db_session.add_all(
        [
            semester,
            math,
            physics,
            Grade(value=1.5, topic="Algebra", subject=math),
            Grade(value=2.5, topic="Vectors", subject=math),
            Grade(value=2.0, topic="Kinematics", subject=physics),
        ]
    )
    db_session.commit()

    return {
        "semester_id": semester.id,
        "math_id": math.id,
        "physics_id": physics.id,
    }
