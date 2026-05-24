from sqlalchemy.orm import joinedload

import database
from models import Grade, Semester, Subject


class GetSemestersService:
    def execute(self):
        session = database.Session()
        try:
            return (
                session.query(Semester)
                .options(joinedload(Semester.subjects).joinedload(Subject.grades))
                .order_by(Semester.name)
                .all()
            )
        finally:
            session.close()


class GetSemesterService:
    def execute(self, semester_id):
        session = database.Session()
        try:
            return (
                session.query(Semester)
                .options(joinedload(Semester.subjects).joinedload(Subject.grades))
                .filter_by(id=semester_id)
                .first()
            )
        finally:
            session.close()


class GetSubjectsService:
    def execute(self):
        session = database.Session()
        try:
            return (
                session.query(Subject)
                .options(joinedload(Subject.grades), joinedload(Subject.semester))
                .order_by(Subject.name)
                .all()
            )
        finally:
            session.close()


class AddSemesterService:
    def execute(self, name):
        name = name.strip()

        if name == "":
            raise ValueError("Semester name cannot be empty.")

        session = database.Session()
        try:
            old_semester = session.query(Semester).filter_by(name=name).first()
            if old_semester is not None:
                raise ValueError("This semester already exists.")

            semester = Semester(name=name)
            session.add(semester)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


class DeleteSemesterService:
    def execute(self, semester_id):
        session = database.Session()
        try:
            semester = session.get(Semester, semester_id)

            if semester is not None:
                session.delete(semester)
                session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


class AddSubjectService:
    def execute(self, name, semester_id=None):
        name = name.strip()

        if name == "":
            raise ValueError("Subject name cannot be empty.")

        session = database.Session()
        try:
            old_subject = session.query(Subject).filter_by(name=name, semester_id=semester_id).first()
            if old_subject is not None:
                raise ValueError("This subject already exists in this semester.")

            semester = None
            if semester_id is not None:
                semester = session.get(Semester, semester_id)
                if semester is None:
                    raise ValueError("Semester not found.")

            subject = Subject(name=name, semester=semester)
            session.add(subject)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


class DeleteSubjectService:
    def execute(self, subject_id):
        session = database.Session()
        try:
            subject = session.get(Subject, subject_id)

            if subject is not None:
                session.delete(subject)
                session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


class GradeValidator:
    def validate(self, value):
        try:
            grade = float(value)
        except (TypeError, ValueError):
            raise ValueError("Grade must be a number.")

        if grade < 1 or grade > 6:
            raise ValueError("Grade must be between 1 and 6.")

        return grade


class AddGradeService:
    def __init__(self, grade_validator=None):
        self.grade_validator = grade_validator or GradeValidator()

    def execute(self, subject_id, value, topic=""):
        grade_value = self.grade_validator.validate(value)
        topic = topic.strip()

        session = database.Session()
        try:
            subject = session.get(Subject, subject_id)

            if subject is None:
                raise ValueError("Subject not found.")

            grade = Grade(value=grade_value, topic=topic, subject=subject)
            session.add(grade)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


class DeleteGradeService:
    def execute(self, grade_id):
        session = database.Session()
        try:
            grade = session.get(Grade, grade_id)

            if grade is not None:
                session.delete(grade)
                session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


class OverallAverageService:
    def execute(self):
        session = database.Session()
        try:
            grades = session.query(Grade).all()

            if len(grades) == 0:
                return None

            total = 0
            for grade in grades:
                total = total + grade.value

            return total / len(grades)
        finally:
            session.close()


class GradeService:
    def __init__(self):
        grade_validator = GradeValidator()

        self.get_semesters_service = GetSemestersService()
        self.get_semester_service = GetSemesterService()
        self.get_subjects_service = GetSubjectsService()
        self.add_semester_service = AddSemesterService()
        self.delete_semester_service = DeleteSemesterService()
        self.add_subject_service = AddSubjectService()
        self.delete_subject_service = DeleteSubjectService()
        self.add_grade_service = AddGradeService(grade_validator)
        self.delete_grade_service = DeleteGradeService()
        self.overall_average_service = OverallAverageService()
        self.grade_validator = grade_validator

    def get_semesters(self):
        return self.get_semesters_service.execute()

    def get_semester(self, semester_id):
        return self.get_semester_service.execute(semester_id)

    def get_subjects(self):
        return self.get_subjects_service.execute()

    def add_semester(self, name):
        self.add_semester_service.execute(name)

    def delete_semester(self, semester_id):
        self.delete_semester_service.execute(semester_id)

    def add_subject(self, name, semester_id=None):
        self.add_subject_service.execute(name, semester_id)

    def delete_subject(self, subject_id):
        self.delete_subject_service.execute(subject_id)

    def add_grade(self, subject_id, value, topic=""):
        self.add_grade_service.execute(subject_id, value, topic)

    def delete_grade(self, grade_id):
        self.delete_grade_service.execute(grade_id)

    def overall_average(self):
        return self.overall_average_service.execute()

    def check_grade(self, value):
        return self.grade_validator.validate(value)
