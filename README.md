# Advanced-Project-Notetracker (Browser App)

---
The goal of this project is to develop a browser-based grade tracker using Python, NiceGUI, SQLite, and SQLModel. 

The project follows the requirements of the Advanced Programming module:

- Browser-based application instead of a CLI-only application
- NiceGUI as frontend technology
- Server-side Python application logic
- SQLite database for persistent data storage
- ORM-based data access using SQLModel
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
