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
    semesters = service.get_semesters()
    semester_options = {semester.id: semester.name for semester in semesters}

    ui.query("body").classes("bg-slate-100")

    with ui.column().classes("w-full max-w-5xl mx-auto p-6 gap-4"):
        with ui.card().classes("w-full bg-blue-700 text-white shadow-lg"):
            ui.label("Grade Tracker").classes("text-4xl font-bold")
            ui.label("Overall average: " + show_average(service.overall_average())).classes("text-lg")

        with ui.row().classes("w-full gap-4"):
            with ui.card().classes("grow shadow-md"):
                ui.label("Add semester").classes("text-xl font-bold")
                semester_input = ui.input("Semester name", placeholder="e.g. Semester 1").classes("w-full")

                def add_semester():
                    try:
                        service.add_semester(semester_input.value)
                        semester_input.value = ""
                        ui.notify("Semester added")
                        show_page.refresh()
                    except ValueError as error:
                        ui.notify(str(error))

                ui.button("Add Semester", on_click=add_semester).props("color=primary")

            with ui.card().classes("grow shadow-md"):
                ui.label("Add subject").classes("text-xl font-bold")
                subject_input = ui.input("Subject name").classes("w-full")
                semester_select = ui.select(semester_options, label="Semester", clearable=True).classes("w-full")

                def add_subject():
                    try:
                        service.add_subject(subject_input.value, semester_select.value)
                        subject_input.value = ""
                        semester_select.value = None
                        ui.notify("Subject added")
                        show_page.refresh()
                    except ValueError as error:
                        ui.notify(str(error))

                ui.button("Add Subject", on_click=add_subject).props("color=primary")

        if len(subjects) == 0:
            ui.label("No subjects yet.").classes("text-slate-500")

        for semester in semesters:
            with ui.card().classes("w-full shadow-md"):
                with ui.row().classes("w-full items-center justify-between"):
                    ui.label(semester.name).classes("text-2xl font-bold text-blue-700")
                    ui.label("Semester average: " + show_average(semester.average())).classes("text-slate-600")

                    def delete_semester(semester_id=semester.id):
                        service.delete_semester(semester_id)
                        ui.notify("Semester deleted")
                        show_page.refresh()

                    ui.button("Delete Semester", on_click=delete_semester).props("flat color=negative")

        for subject in subjects:
            with ui.card().classes("w-full shadow-md"):
                with ui.row().classes("w-full items-center justify-between"):
                    ui.label(subject.name).classes("text-xl font-bold")
                    ui.label("Semester: " + (subject.semester.name if subject.semester else "No semester"))
                    ui.label("Average: " + show_average(subject.average())).classes("text-blue-700 font-bold")

                def delete_subject(subject_id=subject.id):
                    service.delete_subject(subject_id)
                    ui.notify("Subject deleted")
                    show_page.refresh()

                ui.button("Delete Subject", on_click=delete_subject).props("flat color=negative")

                with ui.row().classes("items-end"):
                    grade_input = ui.number("New grade", min=1, max=6, step=0.25)

                    def add_grade(subject_id=subject.id, grade_input=grade_input):
                        try:
                            service.add_grade(subject_id, grade_input.value)
                            grade_input.value = None
                            ui.notify("Grade added")
                            show_page.refresh()
                        except ValueError as error:
                            ui.notify(str(error))

                    ui.button("Add Grade", on_click=add_grade).props("color=primary")

                if len(subject.grades) == 0:
                    ui.label("No grades for this subject.").classes("text-slate-500")

                for grade in subject.grades:
                    with ui.row().classes("items-center"):
                        ui.label(str(grade.value)).classes("px-3 py-1 bg-slate-200 rounded-full")

                        def delete_grade(grade_id=grade.id):
                            service.delete_grade(grade_id)
                            ui.notify("Grade deleted")
                            show_page.refresh()

                        ui.button("Delete", on_click=delete_grade).props("flat color=negative")


create_tables()
show_page()
ui.run()