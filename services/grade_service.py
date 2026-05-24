from sqlalchemy.orm import joinedload
from database import Session
from models import Grade, Semester, Subject


class GradeService:
    def get_semesters(self):
        session = Session()
        semesters = (
            session.query(Semester)
            .options(joinedload(Semester.subjects).joinedload(Subject.grades))
            .order_by(Semester.name)
            .all()
        )
        session.close()
        return semesters

    def get_subjects(self):
        session = Session()
        subjects = (
            session.query(Subject)
            .options(joinedload(Subject.grades), joinedload(Subject.semester))
            .order_by(Subject.name)
            .all()
        )
        session.close()
        return subjects

    def add_semester(self, name):
        name = name.strip()

        if name == "":
            raise ValueError("Semester name cannot be empty.")

        session = Session()

        old_semester = session.query(Semester).filter_by(name=name).first()
        if old_semester is not None:
            session.close()
            raise ValueError("This semester already exists.")

        semester = Semester(name=name)
        session.add(semester)
        session.commit()
        session.close()

    def delete_semester(self, semester_id):
        session = Session()
        semester = session.get(Semester, semester_id)

        if semester is not None:
            session.delete(semester)
            session.commit()

        session.close()

    def add_subject(self, name, semester_id=None):
        name = name.strip()

        if name == "":
            raise ValueError("Subject name cannot be empty.")

        session = Session()

        old_subject = session.query(Subject).filter_by(name=name).first()
        if old_subject is not None:
            session.close()
            raise ValueError("This subject already exists.")

        semester = None
        if semester_id is not None:
            semester = session.get(Semester, semester_id)
            if semester is None:
                session.close()
                raise ValueError("Semester not found.")

        subject = Subject(name=name, semester=semester)
        session.add(subject)
        session.commit()
        session.close()

    def delete_subject(self, subject_id):
        session = Session()
        subject = session.get(Subject, subject_id)

        if subject is not None:
            session.delete(subject)
            session.commit()

        session.close()

    def add_grade(self, subject_id, value):
        grade_value = self.check_grade(value)

        session = Session()
        subject = session.get(Subject, subject_id)

        if subject is None:
            session.close()
            raise ValueError("Subject not found.")

        grade = Grade(value=grade_value, subject=subject)
        session.add(grade)
        session.commit()
        session.close()

    def delete_grade(self, grade_id):
        session = Session()
        grade = session.get(Grade, grade_id)

        if grade is not None:
            session.delete(grade)
            session.commit()

        session.close()

    def overall_average(self):
        session = Session()
        grades = session.query(Grade).all()

        if len(grades) == 0:
            session.close()
            return None

        total = 0
        for grade in grades:
            total = total + grade.value

        average = total / len(grades)
        session.close()
        return average

    def check_grade(self, value):
        try:
            grade = float(value)
        except:
            raise ValueError("Grade must be a number.")

        if grade < 1 or grade > 6:
            raise ValueError("Grade must be between 1 and 6.")

        return grade