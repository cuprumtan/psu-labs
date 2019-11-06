from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, Boolean, Text


Base = declarative_base()


class CeSubjects(Base):
    __tablename__ = 'cesubjects'
    id = Column(Integer, nullable=False, primary_key=True)
    subject_name = Column(String, nullable=False)


class CeQuestions(Base):
    __tablename__ = 'cequestions'
    id = Column(Integer, nullable=False, primary_key=True)
    subject_id = Column(Integer, ForeignKey('cesubjects.id'), nullable=False)
    question_text = Column(Text, nullable=False)


class CeAnswers(Base):
    __tablename__ = 'ceanswers'
    id = Column(Integer, nullable=False, primary_key=True)
    question_id = Column(Integer, ForeignKey('cequestions.id'), nullable=False)
    answer_text = Column(Text, nullable=False)
    is_right = Column(Boolean, nullable=False)


class CeSessions(Base):
    __tablename__ = 'cesessions'
    id = Column(Integer, nullable=False, primary_key=True)
    session_number = Column(Integer, nullable=False)
    session_date = Column(Text, nullable=False)
    student_name = Column(String, nullable=False)
    student_group = Column(String, nullable=True)
    student_grade = Column(Integer, nullable=True)
    answer_id = Column(Integer, ForeignKey('ceanswers.id'), nullable=False)
    is_right = Column(Boolean, nullable=False)
    result_percent = Column(Integer)
