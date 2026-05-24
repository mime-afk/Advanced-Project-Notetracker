from services.grade_service import GradeService


class TestGradeServiceEndToEnd:
    def test_grade_flow_updates_semester_and_overall_average(self, test_database):
        service = GradeService()

        service.add_semester("1. Semester")
        semester = service.get_semesters()[0]

        service.add_subject("Math", semester.id)
        subject = service.get_semester(semester.id).subjects[0]

        service.add_grade(subject.id, "1.75", "Algebra Test")

        loaded_semester = service.get_semester(semester.id)
        loaded_subject = loaded_semester.subjects[0]

        assert loaded_semester.name == "1. Semester"
        assert len(loaded_semester.subjects) == 1
        assert loaded_subject.name == "Math"
        assert loaded_subject.grades[0].topic == "Algebra Test"
        assert loaded_subject.average() == 1.75
        assert loaded_semester.average() == 1.75
        assert service.overall_average() == 1.75

    def test_duplicate_subject_in_same_semester_is_rejected(self, test_database):
        service = GradeService()

        service.add_semester("1. Semester")
        semester = service.get_semesters()[0]
        service.add_subject("Math", semester.id)

        try:
            service.add_subject("Math", semester.id)
            raised = False
        except ValueError as error:
            raised = True
            message = str(error)

        assert raised
        assert message == "This subject already exists in this semester."
        assert len(service.get_semester(semester.id).subjects) == 1

    def test_deleting_grade_updates_overall_average(self, test_database):
        service = GradeService()

        service.add_semester("1. Semester")
        semester = service.get_semesters()[0]
        service.add_subject("Math", semester.id)
        subject = service.get_semester(semester.id).subjects[0]
        service.add_grade(subject.id, 2.0, "Quiz")
        service.add_grade(subject.id, 4.0, "Exam")

        loaded_subject = service.get_semester(semester.id).subjects[0]
        grade_ids = sorted(grade.id for grade in loaded_subject.grades)
        service.delete_grade(grade_ids[1])

        refreshed_subject = service.get_semester(semester.id).subjects[0]

        assert len(refreshed_subject.grades) == 1
        assert refreshed_subject.grades[0].value == 2.0
        assert refreshed_subject.average() == 2.0
        assert service.overall_average() == 2.0
