from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Semester(Base):
    __tablename__ = "semesters"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    subjects = relationship("Subject", back_populates="semester", cascade="all, delete")

    def average(self):
        grades = []
        for subject in self.subjects:
            grades = grades + subject.grades

        if len(grades) == 0:
            return None

        total = 0
        for grade in grades:
            total = total + grade.value

        return total / len(grades)


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    semester_id = Column(Integer, ForeignKey("semesters.id"), nullable=True)

    semester = relationship("Semester", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject", cascade="all, delete")

    def average(self):
        if len(self.grades) == 0:
            return None

        total = 0
        for grade in self.grades:
            total = total + grade.value

        return total / len(self.grades)


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True)
    value = Column(Float, nullable=False)
    topic = Column(String, default="")
    subject_id = Column(Integer, ForeignKey("subjects.id"))

    subject = relationship("Subject", back_populates="grades")
