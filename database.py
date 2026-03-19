"""
Database models and CRUD helpers for the Essay Exam Generator & Grader.

Uses SQLAlchemy ORM with SQLite backend. All tables follow the data model
specified in the product design: contents, questions, exams, exam_questions,
student_responses, and grades.
"""

import json
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, String, Text, Float, DateTime,
    Boolean, ForeignKey, JSON, LargeBinary
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()
engine = create_engine("sqlite:///essay_exam.db", echo=False)
SessionLocal = sessionmaker(bind=engine)


# ── Models ──────────────────────────────────────────────────────────────────

class Content(Base):
    """Uploaded teaching content (PDF, DOCX, MD, TXT) stored as cleaned markdown."""
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    original_content = Column(LargeBinary, nullable=True)
    cleaned_markdown = Column(Text, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    tags = Column(String(500), default="")
    word_count = Column(Integer, default=0)
    file_type = Column(String(10), default="")

    questions = relationship("Question", back_populates="content")


class Question(Base):
    """AI-generated essay question, linked to source content."""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    difficulty = Column(String(20), nullable=False)  # Basic, Intermediate, Advanced
    bloom_level = Column(String(30), nullable=False)
    source_sections = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    content = relationship("Content", back_populates="questions")
    exam_questions = relationship("ExamQuestion", back_populates="question")


class Exam(Base):
    """A curated exam composed of selected questions."""
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    instructions = Column(Text, default="")
    time_limit_minutes = Column(Integer, nullable=True)
    total_points = Column(Float, default=0)
    access_code = Column(String(20), nullable=False)
    is_live = Column(Boolean, default=False)
    show_all_questions = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    exam_questions = relationship("ExamQuestion", back_populates="exam", order_by="ExamQuestion.order")
    student_responses = relationship("StudentResponse", back_populates="exam")


class ExamQuestion(Base):
    """Join table linking exams to questions with ordering."""
    __tablename__ = "exam_questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    order = Column(Integer, nullable=False)
    points = Column(Float, default=10.0)

    exam = relationship("Exam", back_populates="exam_questions")
    question = relationship("Question", back_populates="exam_questions")


class StudentResponse(Base):
    """A student's submitted essay response to an exam question."""
    __tablename__ = "student_responses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    student_name = Column(String(255), nullable=False)
    student_id_str = Column(String(100), default="")
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    response_text = Column(Text, default="")
    submitted_at = Column(DateTime, nullable=True)
    is_submitted = Column(Boolean, default=False)

    exam = relationship("Exam", back_populates="student_responses")
    question = relationship("Question")
    grade = relationship("Grade", back_populates="response", uselist=False)


class Grade(Base):
    """AI-generated grade and feedback for a student response."""
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, autoincrement=True)
    response_id = Column(Integer, ForeignKey("student_responses.id"), nullable=False)
    total_score = Column(Float, default=0)
    score_json = Column(JSON, nullable=True)
    feedback_text = Column(Text, default="")
    strengths = Column(JSON, nullable=True)
    improvements = Column(JSON, nullable=True)
    overall_grade = Column(String(5), default="")
    graded_at = Column(DateTime, default=datetime.utcnow)

    response = relationship("StudentResponse", back_populates="grade")


# ── Initialize DB ───────────────────────────────────────────────────────────

def init_db():
    """Create all tables if they don't exist."""
    Base.metadata.create_all(engine)


def get_session():
    """Return a new database session."""
    return SessionLocal()


# ── CRUD Helpers ────────────────────────────────────────────────────────────

def add_content(filename, original_bytes, cleaned_markdown, file_type, tags=""):
    """Store uploaded content in the database."""
    session = get_session()
    try:
        content = Content(
            filename=filename,
            original_content=original_bytes,
            cleaned_markdown=cleaned_markdown,
            file_type=file_type,
            tags=tags,
            word_count=len(cleaned_markdown.split()),
        )
        session.add(content)
        session.commit()
        session.refresh(content)
        return content.id
    finally:
        session.close()


def get_all_contents():
    """Return all content records."""
    session = get_session()
    try:
        return session.query(Content).order_by(Content.upload_date.desc()).all()
    finally:
        session.close()


def get_content_by_id(content_id):
    session = get_session()
    try:
        return session.query(Content).filter(Content.id == content_id).first()
    finally:
        session.close()


def delete_content(content_id):
    """Delete content and mark linked questions as inactive."""
    session = get_session()
    try:
        session.query(Question).filter(Question.content_id == content_id).update(
            {"is_active": False}
        )
        session.query(Content).filter(Content.id == content_id).delete()
        session.commit()
    finally:
        session.close()


def add_questions(questions_data):
    """Bulk insert generated questions. questions_data is a list of dicts."""
    session = get_session()
    try:
        for q in questions_data:
            question = Question(
                content_id=q["content_id"],
                question_text=q["question"],
                difficulty=q["difficulty"],
                bloom_level=q["bloom_level"],
                source_sections=q.get("source_sections", ""),
            )
            session.add(question)
        session.commit()
    finally:
        session.close()


def get_all_questions(active_only=True):
    session = get_session()
    try:
        query = session.query(Question)
        if active_only:
            query = query.filter(Question.is_active == True)
        return query.order_by(Question.created_at.desc()).all()
    finally:
        session.close()


def create_exam(title, instructions, time_limit, access_code, question_ids, points_per_q=10.0, show_all=True):
    """Create an exam with ordered questions."""
    session = get_session()
    try:
        exam = Exam(
            title=title,
            instructions=instructions,
            time_limit_minutes=time_limit if time_limit else None,
            access_code=access_code,
            total_points=len(question_ids) * points_per_q,
            show_all_questions=show_all,
        )
        session.add(exam)
        session.flush()
        for i, qid in enumerate(question_ids):
            eq = ExamQuestion(exam_id=exam.id, question_id=qid, order=i + 1, points=points_per_q)
            session.add(eq)
        session.commit()
        session.refresh(exam)
        return exam.id
    finally:
        session.close()


def get_all_exams():
    session = get_session()
    try:
        return session.query(Exam).order_by(Exam.created_at.desc()).all()
    finally:
        session.close()


def get_exam_by_code(access_code):
    session = get_session()
    try:
        return session.query(Exam).filter(Exam.access_code == access_code).first()
    finally:
        session.close()


def get_exam_by_id(exam_id):
    session = get_session()
    try:
        return session.query(Exam).filter(Exam.id == exam_id).first()
    finally:
        session.close()


def get_exam_questions(exam_id):
    """Return questions for an exam in order."""
    session = get_session()
    try:
        eqs = (
            session.query(ExamQuestion)
            .filter(ExamQuestion.exam_id == exam_id)
            .order_by(ExamQuestion.order)
            .all()
        )
        result = []
        for eq in eqs:
            q = session.query(Question).filter(Question.id == eq.question_id).first()
            result.append({"eq": eq, "question": q})
        return result
    finally:
        session.close()


def publish_exam(exam_id):
    session = get_session()
    try:
        session.query(Exam).filter(Exam.id == exam_id).update({"is_live": True})
        session.commit()
    finally:
        session.close()


def save_student_response(exam_id, student_name, student_id_str, question_id, response_text):
    """Save or update a student's response to a question."""
    session = get_session()
    try:
        existing = (
            session.query(StudentResponse)
            .filter(
                StudentResponse.exam_id == exam_id,
                StudentResponse.student_name == student_name,
                StudentResponse.question_id == question_id,
            )
            .first()
        )
        if existing:
            existing.response_text = response_text
        else:
            sr = StudentResponse(
                exam_id=exam_id,
                student_name=student_name,
                student_id_str=student_id_str,
                question_id=question_id,
                response_text=response_text,
            )
            session.add(sr)
        session.commit()
    finally:
        session.close()


def submit_student_exam(exam_id, student_name):
    """Mark all responses for this student+exam as submitted."""
    session = get_session()
    try:
        session.query(StudentResponse).filter(
            StudentResponse.exam_id == exam_id,
            StudentResponse.student_name == student_name,
        ).update({"is_submitted": True, "submitted_at": datetime.utcnow()})
        session.commit()
    finally:
        session.close()


def get_student_responses(exam_id, student_name=None):
    session = get_session()
    try:
        query = session.query(StudentResponse).filter(
            StudentResponse.exam_id == exam_id,
            StudentResponse.is_submitted == True,
        )
        if student_name:
            query = query.filter(StudentResponse.student_name == student_name)
        return query.all()
    finally:
        session.close()


def get_all_submissions():
    """Return all submitted responses with related data for the gradebook."""
    session = get_session()
    try:
        return (
            session.query(StudentResponse)
            .filter(StudentResponse.is_submitted == True)
            .order_by(StudentResponse.submitted_at.desc())
            .all()
        )
    finally:
        session.close()


def save_grade(response_id, score_json, total_score, feedback_text, strengths, improvements, overall_grade):
    session = get_session()
    try:
        existing = session.query(Grade).filter(Grade.response_id == response_id).first()
        if existing:
            existing.score_json = score_json
            existing.total_score = total_score
            existing.feedback_text = feedback_text
            existing.strengths = strengths
            existing.improvements = improvements
            existing.overall_grade = overall_grade
            existing.graded_at = datetime.utcnow()
        else:
            grade = Grade(
                response_id=response_id,
                score_json=score_json,
                total_score=total_score,
                feedback_text=feedback_text,
                strengths=strengths,
                improvements=improvements,
                overall_grade=overall_grade,
            )
            session.add(grade)
        session.commit()
    finally:
        session.close()


def get_grade_for_response(response_id):
    session = get_session()
    try:
        return session.query(Grade).filter(Grade.response_id == response_id).first()
    finally:
        session.close()


def get_grades_for_exam(exam_id):
    """Return all grades for an exam joined with response data."""
    session = get_session()
    try:
        responses = (
            session.query(StudentResponse)
            .filter(StudentResponse.exam_id == exam_id, StudentResponse.is_submitted == True)
            .all()
        )
        results = []
        for r in responses:
            grade = session.query(Grade).filter(Grade.response_id == r.id).first()
            q = session.query(Question).filter(Question.id == r.question_id).first()
            results.append({
                "student_name": r.student_name,
                "student_id": r.student_id_str,
                "question": q.question_text if q else "",
                "difficulty": q.difficulty if q else "",
                "bloom_level": q.bloom_level if q else "",
                "response": r.response_text,
                "submitted_at": r.submitted_at,
                "grade": grade,
            })
        return results
    finally:
        session.close()
