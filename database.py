from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///grades.db")
Session = sessionmaker(bind=engine)

Base = declarative_base()


def create_tables():
    from models import Subject, Grade
    Base.metadata.create_all(engine)