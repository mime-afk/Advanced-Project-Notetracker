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

Students often use diffrent apps or spreadsheets to track their grades.

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

1: As a student, I want to add or delete subjects so that I can organize my courses in one place.

---

2: As a student, I want to add or delete grades to my subjects so that I can track my performance in each course.

---

3: As a student, I want to see the average grade for each subject so that I can quickly understand my performance in individual courses.

---

4: As a student, I want to see my overall average across all subjects so that I can assess my general academic performance.

---
## Architecture

Browser  
↓  
NiceGUI UI (Python)  
↓  
GradeService (Business Logic)  
↓  
SQLite Database (SQLAlchemy ORM)  

---

