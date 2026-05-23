from nicegui import ui

from database import create_tables
from services.grade_service import GradeService

service = GradeService()


def show_average(value):
    if value is None:
        return "No grades yet"
    return str(round(value, 2))


@ui.refreshable
def show_page():
    subjects = service.get_subjects()

    ui.label("Grade Tracker").classes("text-3xl")
    ui.label("Overall average: " + show_average(service.overall_average()))

    with ui.card():
        ui.label("Add subject")
        subject_input = ui.input("Subject name")

        def add_subject():
            try:
                service.add_subject(subject_input.value)
                subject_input.value = ""
                ui.notify("Subject added")
                show_page.refresh()
            except ValueError as error:
                ui.notify(str(error))

        ui.button("Add Subject", on_click=add_subject)

    if len(subjects) == 0:
        ui.label("No subjects yet.")

    for subject in subjects:
        with ui.card():
            ui.label(subject.name).classes("text-xl")
            ui.label("Average: " + show_average(subject.average()))

            def delete_subject(subject_id=subject.id):
                service.delete_subject(subject_id)
                ui.notify("Subject deleted")
                show_page.refresh()

            ui.button("Delete Subject", on_click=delete_subject)

            grade_input = ui.number("New grade")

            def add_grade(subject_id=subject.id, grade_input=grade_input):
                try:
                    service.add_grade(subject_id, grade_input.value)
                    grade_input.value = None
                    ui.notify("Grade added")
                    show_page.refresh()
                except ValueError as error:
                    ui.notify(str(error))

            ui.button("Add Grade", on_click=add_grade)

            if len(subject.grades) == 0:
                ui.label("No grades for this subject.")

            for grade in subject.grades:
                with ui.row():
                    ui.label(str(grade.value))

                    def delete_grade(grade_id=grade.id):
                        service.delete_grade(grade_id)
                        ui.notify("Grade deleted")
                        show_page.refresh()

                    ui.button("Delete", on_click=delete_grade)


create_tables()
show_page()
ui.run()