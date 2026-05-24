from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///grades.db")
Session = sessionmaker(bind=engine)

Base = declarative_base()


def create_tables():
    from models import Grade, Semester, Subject
    Base.metadata.create_all(engine)

    inspector = inspect(engine)
    subject_columns = [column["name"] for column in inspector.get_columns("subjects")]
    if "semester_id" not in subject_columns:
        with engine.connect() as connection:
            connection.execute(text("ALTER TABLE subjects ADD COLUMN semester_id INTEGER"))
            connection.commit()

    remove_old_subject_unique_constraint()
    add_grade_topic_column()


def add_grade_topic_column():
    inspector = inspect(engine)
    grade_columns = [column["name"] for column in inspector.get_columns("grades")]
    if "topic" not in grade_columns:
        with engine.connect() as connection:
            connection.execute(text("ALTER TABLE grades ADD COLUMN topic VARCHAR DEFAULT ''"))
            connection.commit()


def remove_old_subject_unique_constraint():
    with engine.connect() as connection:
        table = connection.execute(
            text("SELECT sql FROM sqlite_master WHERE type='table' AND name='subjects'")
        ).fetchone()

    if table is None or "UNIQUE (name)" not in table[0]:
        return

    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
        connection.exec_driver_sql("PRAGMA foreign_keys=OFF")
        connection.exec_driver_sql("ALTER TABLE grades RENAME TO grades_old")
        connection.exec_driver_sql("ALTER TABLE subjects RENAME TO subjects_old")
        connection.exec_driver_sql("""
            CREATE TABLE subjects (
                id INTEGER NOT NULL,
                name VARCHAR NOT NULL,
                semester_id INTEGER,
                PRIMARY KEY (id),
                FOREIGN KEY(semester_id) REFERENCES semesters (id)
            )
        """)
        connection.exec_driver_sql("""
            CREATE TABLE grades (
                id INTEGER NOT NULL,
                value FLOAT NOT NULL,
                topic VARCHAR DEFAULT '',
                subject_id INTEGER,
                PRIMARY KEY (id),
                FOREIGN KEY(subject_id) REFERENCES subjects (id)
            )
        """)
        connection.exec_driver_sql("""
            INSERT INTO subjects (id, name, semester_id)
            SELECT id, name, semester_id FROM subjects_old
        """)
        connection.exec_driver_sql("""
            INSERT INTO grades (id, value, subject_id)
            SELECT id, value, subject_id FROM grades_old
        """)
        connection.exec_driver_sql("DROP TABLE grades_old")
        connection.exec_driver_sql("DROP TABLE subjects_old")
        connection.exec_driver_sql("PRAGMA foreign_keys=ON")
