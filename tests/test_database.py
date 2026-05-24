from sqlalchemy import select

from models import Grade, Semester, Subject


def test_saving_grade_persists_topic_and_subject_relationship(db_session):
    subject = Subject(name="Math")
    grade = Grade(value=1.25, topic="Linear Algebra", subject=subject)
    db_session.add_all([subject, grade])
    db_session.commit()

    saved_grade = db_session.execute(
        select(Grade).join(Subject).where(Subject.name == "Math")
    ).scalar_one()

    assert saved_grade.value == 1.25
    assert saved_grade.topic == "Linear Algebra"
    assert saved_grade.subject.name == "Math"


def test_saving_subject_persists_semester_relationship(db_session):
    semester = Semester(name="2. Semester")
    subject = Subject(name="History", semester=semester)
    db_session.add_all([semester, subject])
    db_session.commit()

    saved_subject = db_session.execute(
        select(Subject).join(Semester).where(Semester.name == "2. Semester")
    ).scalar_one()

    assert saved_subject.name == "History"
    assert saved_subject.semester.name == "2. Semester"


def test_deleting_subject_cascades_to_grades(db_session):
    subject = Subject(name="Biology")
    grade = Grade(value=2.25, topic="Cells", subject=subject)
    db_session.add_all([subject, grade])
    db_session.commit()

    db_session.delete(subject)
    db_session.commit()

    assert db_session.execute(select(Subject)).scalars().all() == []
    assert db_session.execute(select(Grade)).scalars().all() == []
