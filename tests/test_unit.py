import pytest

from models import Grade, Semester, Subject
from services.grade_service import GradeValidator


class TestGradeValidator:
    def setup_method(self):
        self.validator = GradeValidator()

    def test_numeric_string_is_converted_to_float(self):
        assert self.validator.validate("1.75") == 1.75

    def test_non_numeric_value_raises_clear_error(self):
        with pytest.raises(ValueError, match="Grade must be a number."):
            self.validator.validate("excellent")

    def test_grade_above_range_raises_clear_error(self):
        with pytest.raises(ValueError, match="Grade must be between 1 and 6."):
            self.validator.validate("6.5")


class TestAverages:
    def test_subject_average_returns_none_without_grades(self):
        subject = Subject(name="Math")

        assert subject.average() is None

    def test_semester_average_uses_all_subject_grades(self):
        semester = Semester(name="1. Semester")
        math = Subject(name="Math", semester=semester)
        physics = Subject(name="Physics", semester=semester)
        math.grades = [Grade(value=1.5), Grade(value=2.5)]
        physics.grades = [Grade(value=2.0)]

        assert semester.average() == 2.0

    def test_subject_average_returns_mean_of_all_grades(self):
        subject = Subject(name="Math")
        subject.grades = [Grade(value=1.0), Grade(value=2.0), Grade(value=3.0)]

        assert subject.average() == 2.0
