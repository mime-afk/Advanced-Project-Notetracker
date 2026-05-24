# Advanced-Project-Notetracker (Browser App)
<img width="1873" height="928" alt="image" src="https://github.com/user-attachments/assets/640c1418-e56f-4f2e-83ee-237d3a69c789" />

---
The goal of this project is to develop a browser-based grade tracker using Python, NiceGUI and SQLAlchemy.

The project follows the requirements of the Advanced Programming module:

- Browser-based application instead of a CLI-only application
- NiceGUI as frontend technology
- Server-side Python application logic
- SQLite database for persistent data storage
- ORM-based data access using SQLAlchemy
- Object-oriented structure
- Automated and documented tests
- GitHub-based collaboration
---
## Application Requirements

### Problem

Students often use diffrent apps or spreadsheets to track grades for different subjects, leading to confusion.Calculating averages for each subject or overall performance manually is time-consuming and error-prone.

---

## Scenario

The application allows users to: 
- Add/Delete Subjects: Organize your courses.
- Add/Delete Grades: Log your results for each subject.
- View Averages:
  - Average grade per subject.
  - Overall average across all subjects.
- User-Friendly UI: Simple and intuitive interface powered by NiceGUI.

---

### User Stories

| **ID** | **As a** | **I want to**                     | **So that**                                                    |
| ------ | -------- | --------------------------------- | -------------------------------------------------------------- |
| US_001 | Student  | Add subjects                      | I can organize my courses in one place.                        |
| US_002 | Student  | Delete subjects                   | I can remove courses I no longer take.                         |
| US_003 | Student  | Add grades to my subjects         | I can track my performance in each course.                     |
| US_004 | Student  | Delete grades                     | I can correct mistakes or remove incorrect entries.            |
| US_005 | Student  | See the average grade per subject | I can quickly understand my performance in individual courses. |
| US_006 | Student  | See my overall average            | I can assess my general academic performance.                  |
| US_007 | Student  | Use a simple interface            | I can manage my grades without needing training.               |
| US_008 | Student  | Have my data persist              | I don’t lose my grades when I close the app.                   |

---
## Use Cases

### **Main Use Cases**

- **Manage Subjects** (Add/Delete)
- **Manage Grades** (Add/Delete)
- **View Averages** (Per Subject & Overall)
- **Persist Data** (SQLite Database)

### **Actors**

- **Student**
---
## Architecture

- **UI**: NiceGUI (browser-based interface)
- **Application Logic**: `grade_service.py` (business logic)
- **Persistence**: SQLite + SQLAlchemy ORM

### **Design Decisions**

- **MVC-like structure** (Model–View–Controller)
- **Clear separation of concerns** (UI, logic, database)
- **Business logic independent of UI**

### **Design Patterns Used**

- **Model-View-Controller (MVC)**: Separates UI, logic, and data for maintainability.
- **Facade Pattern**: Simplifies database setup and access

---
##  Database and ORM

The application uses **SQLAlchemy** to map domain objects to a **SQLite database**.

### **Entities**

- `Subject`
- `Grade`

### **Relationships**

- One `Subject` → many `Grade`

### Database Schema

<img src="/database-schema.png" alt="Database Schema" width="50%">

---

##  Project Requirements

The app meets the following criteria:

1. **Browser-based UI** using NiceGUI.
2. **Data validation** (e.g., grade ranges, non-empty subject names).
3. **ORM for database management** (SQLAlchemy).


---

##  Implementation

### **Technology**

- Python 3.8+
- NiceGUI
- SQLAlchemy
- SQLite
- pytest

### **Libraries Used**

- **nicegui** – UI framework
- **sqlalchemy** – ORM and database toolkit
- **pytest** – Testing

---

## Test Cases

The following test cases use the project test-case template and cover both the existing automated tests and manual UI checks.

### Automated Test Cases

#### TC_001

| Field | Value |
| --- | --- |
| Test case title/description | Verify that grade validation rejects text input. |
| Preconditions | Test environment is set up and `GradeValidator` is available. |
| Test steps | Call `GradeValidator.validate("excellent")`. |
| Test data/input | `"excellent"` |
| Expected result | A `ValueError` with the message `Grade must be a number.` is raised. |
| Actual result | A `ValueError` with the correct message is raised. |
| Status | Pass |
| Comments | Covered by `tests/test_unit.py::TestGradeValidator::test_non_numeric_value_raises_clear_error`. |

#### TC_002

| Field | Value |
| --- | --- |
| Test case title/description | Verify that a new grade is stored in the database with the correct relationships. |
| Preconditions | Test database is created and empty. |
| Test steps | Create a subject, add a grade with a topic, commit the transaction, then query the database. |
| Test data/input | Subject `Math`, grade `1.25`, topic `Linear Algebra` |
| Expected result | The grade is stored with value `1.25`, topic `Linear Algebra`, and linked subject `Math`. |
| Actual result | The grade is persisted with the expected values and relationship. |
| Status | Pass |
| Comments | Covered by `tests/test_database.py::test_saving_grade_persists_topic_and_subject_relationship`. |

#### TC_003

| Field | Value |
| --- | --- |
| Test case title/description | Verify the full application flow from creating a semester to calculating the overall average. |
| Preconditions | Isolated test database is available. |
| Test steps | Create a semester, add a subject, add a grade, reload the semester, and read the averages. |
| Test data/input | Semester `1. Semester`, subject `Math`, grade `1.75`, topic `Algebra Test` |
| Expected result | The subject average, semester average, and overall average are all `1.75`. |
| Actual result | All averages are calculated as `1.75`. |
| Status | Pass |
| Comments | Covered by `tests/test_integration.py::TestGradeServiceEndToEnd::test_grade_flow_updates_semester_and_overall_average`. |

### Manual Test Cases

#### TC_004

| Field | Value |
| --- | --- |
| Test case title/description | Verify that a user can create a new semester in the application. |
| Preconditions | Application is running in the browser. |
| Test steps | Enter a semester name in the semester input field and click **Add Semester**. |
| Test data/input | `1. Semester` |
| Expected result | A new semester card appears and a confirmation notification is shown. |
| Actual result | ____________________ |
| Status | ____________________ |
| Comments | Manual UI test for semester creation feedback and rendering. |

#### TC_005

| Field | Value |
| --- | --- |
| Test case title/description | Verify that a subject and its grade are visible inside the selected semester. |
| Preconditions | At least one semester exists and can be opened. |
| Test steps | Open a semester, add a subject, enter a grade and topic, then click **Add Grade**. |
| Test data/input | Subject `Math`, grade `2.0`, topic `Algebra` |
| Expected result | The subject appears in the semester view, the grade row is shown, and the subject average is updated. |
| Actual result | ____________________ |
| Status | ____________________ |
| Comments | Manual UI test for nested subject and grade rendering. |

#### TC_006

| Field | Value |
| --- | --- |
| Test case title/description | Verify that deleting a grade removes it from the list and updates the average. |
| Preconditions | A semester, subject, and at least one grade already exist. |
| Test steps | Open the semester, locate the grade row, click the delete button (`x`), and observe the updated values. |
| Test data/input | Existing grade entry, for example `2.0` with topic `Algebra` |
| Expected result | The selected grade disappears, a notification is shown, and the average is recalculated. |
| Actual result | ____________________ |
| Status | ____________________ |
| Comments | Manual UI test for delete behavior and live refresh. |

---
## Team & Contributions
| Name | Contribution |
|---  | ---  |
|Louie| UI/UX, logic, documentation|
|Michael| Database, logic, documentation|
|Aimen| Testing, logic, documentation|
