from nicegui import ui

from database import create_tables
from services.grade_service import GradeService

service = GradeService()
selected_semester_id = None


def show_average(value):
    if value is None:
        return "No grades yet"
    return str(round(value, 2))


def open_semester(semester_id):
    global selected_semester_id
    selected_semester_id = semester_id
    show_page.refresh()


def back_to_semesters():
    global selected_semester_id
    selected_semester_id = None
    show_page.refresh()


@ui.refreshable
def show_page():
    ui.query("body").classes("bg-gradient-to-br from-slate-100 to-blue-100")

    with ui.column().classes("w-full max-w-6xl mx-auto p-6 gap-6"):
        with ui.card().classes("w-full p-8 rounded-3xl bg-gradient-to-r from-blue-700 to-indigo-700 text-white shadow-xl"):
            ui.label("Grade Tracker").classes("text-5xl font-extrabold")
            ui.label("Organize your semesters, subjects and grades.").classes("text-blue-100 text-lg")
            ui.label("Overall average: " + show_average(service.overall_average())).classes("text-2xl font-bold mt-4")

        if selected_semester_id is None:
            show_semester_overview()
        else:
            show_semester_details(selected_semester_id)


def show_semester_overview():
    semesters = service.get_semesters()

    with ui.card().classes("w-full p-6 rounded-3xl shadow-lg bg-white"):
        ui.label("Create a semester first").classes("text-2xl font-bold text-slate-800")
        ui.label("Click a semester to open its subjects and grades.").classes("text-slate-500")

        with ui.row().classes("w-full items-end gap-4 mt-2"):
            semester_input = ui.input("Semester name", placeholder="e.g. 1. Semester").classes("grow")

            def add_semester():
                try:
                    service.add_semester(semester_input.value)
                    semester_input.value = ""
                    ui.notify("Semester added")
                    show_page.refresh()
                except ValueError as error:
                    ui.notify(str(error))

            ui.button("Add Semester", on_click=add_semester).props("color=primary").classes("rounded-xl px-5")

    if len(semesters) == 0:
        with ui.card().classes("w-full p-8 rounded-3xl shadow-md bg-white text-center"):
            ui.label("No semesters yet.").classes("text-xl font-bold text-slate-600")
            ui.label("Start by adding your first semester above.").classes("text-slate-400")

    for semester in semesters:
        with ui.card().classes("w-full p-6 rounded-3xl shadow-lg bg-white hover:bg-blue-50 cursor-pointer"):
            with ui.row().classes("w-full items-center justify-between"):
                with ui.column().classes("gap-0").on("click", lambda semester_id=semester.id: open_semester(semester_id)):
                    ui.label(semester.name).classes("text-3xl font-extrabold text-blue-700")
                    ui.label("Semester average: " + show_average(semester.average())).classes("text-slate-500")

                with ui.row().classes("gap-2"):
                    ui.button("Open", on_click=lambda semester_id=semester.id: open_semester(semester_id)).props("color=primary").classes("rounded-xl")

                    def delete_semester(semester_id=semester.id):
                        service.delete_semester(semester_id)
                        ui.notify("Semester deleted")
                        show_page.refresh()

                    ui.button("Delete", on_click=delete_semester).props("flat color=negative").classes("rounded-xl")


def show_semester_details(semester_id):
    semester = service.get_semester(semester_id)

    if semester is None:
        back_to_semesters()
        return

    with ui.row().classes("w-full items-center justify-between"):
        ui.button("← Back to semesters", on_click=back_to_semesters).props("flat color=primary").classes("rounded-xl")

    with ui.card().classes("w-full p-6 rounded-3xl shadow-lg bg-white"):
        with ui.row().classes("w-full items-center justify-between"):
            with ui.column().classes("gap-0"):
                ui.label(semester.name).classes("text-4xl font-extrabold text-blue-700")
                ui.label("Semester average: " + show_average(semester.average())).classes("text-slate-500")

            def delete_semester():
                service.delete_semester(semester.id)
                ui.notify("Semester deleted")
                back_to_semesters()

            ui.button("Delete Semester", on_click=delete_semester).props("flat color=negative").classes("rounded-xl")

        with ui.card().classes("w-full mt-4 p-4 rounded-2xl bg-slate-50 shadow-none"):
            ui.label("Add subject to " + semester.name).classes("font-bold text-slate-700")
            with ui.row().classes("w-full items-end gap-3"):
                subject_input = ui.input("Subject name", placeholder="e.g. Mathe").classes("grow")

                def add_subject():
                    try:
                        service.add_subject(subject_input.value, semester.id)
                        subject_input.value = ""
                        ui.notify("Subject added")
                        show_page.refresh()
                    except ValueError as error:
                        ui.notify(str(error))

                ui.button("Add Subject", on_click=add_subject).props("color=primary").classes("rounded-xl px-5")

    if len(semester.subjects) == 0:
        with ui.card().classes("w-full p-6 rounded-3xl shadow-md bg-white text-center"):
            ui.label("No subjects in this semester yet.").classes("text-slate-400")

    for subject in semester.subjects:
        with ui.card().classes("w-full p-5 rounded-3xl border border-slate-200 shadow-lg bg-white"):
            with ui.row().classes("w-full items-center justify-between"):
                with ui.column().classes("gap-0"):
                    ui.label(subject.name).classes("text-2xl font-bold text-slate-800")
                    ui.label("Average: " + show_average(subject.average())).classes("text-blue-700 font-bold")

                def delete_subject(subject_id=subject.id):
                    service.delete_subject(subject_id)
                    ui.notify("Subject deleted")
                    show_page.refresh()

                ui.button("Delete Subject", on_click=delete_subject).props("flat color=negative").classes("rounded-xl")

            with ui.row().classes("items-end gap-3 mt-3"):
                grade_input = ui.number("New grade", min=1, max=6, step=0.25).classes("w-40")
                topic_input = ui.input("Exam topic", placeholder="e.g. Algebra").classes("grow")

                def add_grade(subject_id=subject.id, grade_input=grade_input, topic_input=topic_input):
                    try:
                        service.add_grade(subject_id, grade_input.value, topic_input.value or "")
                        grade_input.value = None
                        topic_input.value = ""
                        ui.notify("Grade added")
                        show_page.refresh()
                    except ValueError as error:
                        ui.notify(str(error))

                ui.button("Add Grade", on_click=add_grade).props("color=primary").classes("rounded-xl")

            if len(subject.grades) == 0:
                ui.label("No grades for this subject.").classes("text-slate-400 mt-2")

            with ui.column().classes("w-full gap-2 mt-3"):
                for grade in subject.grades:
                    topic = grade.topic or "No topic"
                    with ui.row().classes("w-full items-center justify-between px-4 py-2 bg-blue-50 rounded-2xl"):
                        ui.label(topic).classes("text-slate-700")
                        with ui.row().classes("items-center gap-2"):
                            ui.label(str(grade.value)).classes("text-blue-800 font-bold")

                            def delete_grade(grade_id=grade.id):
                                service.delete_grade(grade_id)
                                ui.notify("Grade deleted")
                                show_page.refresh()

                            ui.button("x", on_click=delete_grade).props("flat dense color=negative")


create_tables()
show_page()
ui.run()