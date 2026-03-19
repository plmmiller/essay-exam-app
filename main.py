"""
AI-Powered Essay Exam Generator & Grader
=========================================

A Streamlit-based platform for teachers to upload content, generate essay
questions using Bloom's Taxonomy, build exams, administer them to students,
and automatically grade responses with detailed AI feedback.

Run with: streamlit run main.py
"""

import os
import json
import string
import random
import time
from datetime import datetime, timedelta

import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from database import (
    init_db, add_content, get_all_contents, get_content_by_id, delete_content,
    add_questions, get_all_questions, create_exam, get_all_exams, get_exam_by_code,
    get_exam_by_id, get_exam_questions, publish_exam, save_student_response,
    submit_student_exam, get_student_responses, get_all_submissions,
    save_grade, get_grade_for_response, get_grades_for_exam,
)
from content_processor import process_file
from ai_engine import generate_questions, grade_response

# ── App Config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Essay Exam Generator & Grader",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()

# ── Session State Defaults ──────────────────────────────────────────────────

defaults = {
    "authenticated": False,
    "role": None,           # "teacher" or "student"
    "student_name": "",
    "student_id": "",
    "exam_code": "",
    "current_exam_id": None,
    "exam_start_time": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── Authentication ──────────────────────────────────────────────────────────

def login_page():
    """Landing page with role selection and authentication."""
    st.title("Essay Exam Generator & Grader")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Teacher Login")
        teacher_pw = st.text_input("Password", type="password", key="teacher_pw")
        if st.button("Login as Teacher", use_container_width=True):
            expected = os.environ.get("TEACHER_PASSWORD", "admin")
            if teacher_pw == expected:
                st.session_state.authenticated = True
                st.session_state.role = "teacher"
                st.rerun()
            else:
                st.error("Incorrect password.")

    with col2:
        st.subheader("Student Exam Portal")
        sname = st.text_input("Your Name", key="s_name")
        sid = st.text_input("Student ID (optional)", key="s_id")
        scode = st.text_input("Exam Access Code", key="s_code")
        if st.button("Enter Exam", use_container_width=True):
            if not sname.strip():
                st.error("Please enter your name.")
            elif not scode.strip():
                st.error("Please enter the exam access code.")
            else:
                exam = get_exam_by_code(scode.strip())
                if exam and exam.is_live:
                    st.session_state.authenticated = True
                    st.session_state.role = "student"
                    st.session_state.student_name = sname.strip()
                    st.session_state.student_id = sid.strip()
                    st.session_state.exam_code = scode.strip()
                    st.session_state.current_exam_id = exam.id
                    st.session_state.exam_start_time = datetime.utcnow().isoformat()
                    st.rerun()
                elif exam and not exam.is_live:
                    st.error("This exam is not yet live. Please contact your teacher.")
                else:
                    st.error("Invalid access code.")


# ── Teacher Pages ───────────────────────────────────────────────────────────

def content_library_page():
    """Upload and manage teaching content (MD, PDF, TXT, DOCX)."""
    st.header("Content Library")

    # Upload section
    with st.expander("Upload New Content", expanded=True):
        uploaded = st.file_uploader(
            "Drag & drop or select files",
            type=["md", "pdf", "txt", "docx"],
            accept_multiple_files=True,
        )
        tags = st.text_input("Tags (comma-separated)", placeholder="biology, chapter3, ecology")
        if uploaded and st.button("Process & Upload"):
            for f in uploaded:
                with st.spinner(f"Processing {f.name}..."):
                    try:
                        cleaned, raw = process_file(f)
                        ext = os.path.splitext(f.name)[1].lower().lstrip(".")
                        add_content(f.name, raw, cleaned, ext, tags)
                        st.success(f"Uploaded: {f.name} ({len(cleaned.split())} words)")
                    except Exception as e:
                        st.error(f"Error processing {f.name}: {e}")

    # Library view
    st.markdown("---")
    contents = get_all_contents()
    if not contents:
        st.info("No content uploaded yet. Upload files above to get started.")
        return

    for c in contents:
        with st.container():
            col1, col2, col3 = st.columns([4, 2, 1])
            with col1:
                badge = {"md": "Markdown", "pdf": "PDF", "txt": "Text", "docx": "Word"}.get(c.file_type, c.file_type)
                st.markdown(f"**{c.filename}** `{badge}` — {c.word_count} words")
                if c.tags:
                    st.caption(f"Tags: {c.tags}")
            with col2:
                st.caption(f"Uploaded: {c.upload_date.strftime('%Y-%m-%d %H:%M') if c.upload_date else 'N/A'}")
            with col3:
                if st.button("Delete", key=f"del_{c.id}"):
                    delete_content(c.id)
                    st.rerun()

            # Preview
            with st.expander("Preview"):
                preview = c.cleaned_markdown[:2000]
                if len(c.cleaned_markdown) > 2000:
                    preview += "\n\n*[Preview truncated...]*"
                st.markdown(preview)
            st.markdown("---")


def question_generator_page():
    """Generate essay questions from uploaded content using AI."""
    st.header("Generate Questions")

    contents = get_all_contents()
    if not contents:
        st.warning("Upload content in the Content Library first.")
        return

    content_options = {c.id: f"{c.filename} ({c.word_count} words)" for c in contents}
    selected_ids = st.multiselect(
        "Select content to generate questions from",
        options=list(content_options.keys()),
        format_func=lambda x: content_options[x],
    )

    col1, col2 = st.columns(2)
    with col1:
        difficulty = st.selectbox("Difficulty Level", ["Basic", "Intermediate", "Advanced", "All Levels"])
    with col2:
        num_q = st.slider("Number of questions", 3, 15, 5)

    custom = st.text_area("Custom instructions (optional)", placeholder="e.g., Focus on Chapter 3 themes")

    if st.button("Generate Questions", type="primary", disabled=not selected_ids):
        # Combine selected content
        combined = ""
        for cid in selected_ids:
            c = get_content_by_id(cid)
            if c:
                combined += f"\n\n--- Source: {c.filename} ---\n\n{c.cleaned_markdown}"

        if difficulty == "All Levels":
            per_level = max(1, num_q // 3)
            levels = ["Basic", "Intermediate", "Advanced"]
            all_questions = []
            for level in levels:
                count = per_level if level != "Advanced" else num_q - 2 * per_level
                with st.spinner(f"Generating {count} {level} questions..."):
                    try:
                        qs = generate_questions(combined, count, level, custom)
                        for q in qs:
                            q["content_id"] = selected_ids[0]
                        all_questions.extend(qs)
                    except Exception as e:
                        st.error(f"Error generating {level} questions: {e}")
        else:
            with st.spinner(f"Generating {num_q} {difficulty} questions..."):
                try:
                    all_questions = generate_questions(combined, num_q, difficulty, custom)
                    for q in all_questions:
                        q["content_id"] = selected_ids[0]
                except Exception as e:
                    st.error(f"Error: {e}")
                    return

        if all_questions:
            add_questions(all_questions)
            st.success(f"Generated {len(all_questions)} questions!")
            for q in all_questions:
                with st.container():
                    st.markdown(f"**Q{q['id']}** [{q['difficulty']} / {q['bloom_level']}]")
                    st.write(q["question"])
                    if q.get("source_sections"):
                        st.caption(f"Source: {q['source_sections']}")
                    st.markdown("---")


def question_bank_page():
    """View and manage generated questions."""
    st.header("Question Bank")

    questions = get_all_questions()
    if not questions:
        st.info("No questions yet. Generate some from the Question Generator page.")
        return

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        diff_filter = st.selectbox("Filter by Difficulty", ["All", "Basic", "Intermediate", "Advanced"])
    with col2:
        bloom_filter = st.text_input("Filter by Bloom Level", placeholder="e.g., Analyze")

    filtered = questions
    if diff_filter != "All":
        filtered = [q for q in filtered if q.difficulty == diff_filter]
    if bloom_filter.strip():
        filtered = [q for q in filtered if bloom_filter.lower() in q.bloom_level.lower()]

    st.markdown(f"Showing {len(filtered)} of {len(questions)} questions")
    st.markdown("---")

    for q in filtered:
        with st.container():
            cols = st.columns([5, 1, 1])
            with cols[0]:
                st.markdown(f"**Q#{q.id}** — `{q.difficulty}` / `{q.bloom_level}`")
                st.write(q.question_text)
                if q.source_sections:
                    st.caption(f"Source: {q.source_sections}")
            with cols[1]:
                content = get_content_by_id(q.content_id)
                if content:
                    st.caption(f"From: {content.filename}")
            with cols[2]:
                st.caption(f"Created: {q.created_at.strftime('%m/%d') if q.created_at else ''}")
            st.markdown("---")


def exam_builder_page():
    """Build exams by selecting questions from the question bank."""
    st.header("Exam Builder")

    questions = get_all_questions()
    if not questions:
        st.warning("Generate questions first before building an exam.")
        return

    # Exam metadata
    title = st.text_input("Exam Title", placeholder="Midterm Essay Exam")
    instructions = st.text_area("Instructions for Students",
                                value="Read each question carefully. Write a well-organized essay of 400-600 words for each question. Support your arguments with specific references to the source material.")
    col1, col2, col3 = st.columns(3)
    with col1:
        time_limit = st.number_input("Time Limit (minutes, 0 = unlimited)", min_value=0, value=0, step=5)
    with col2:
        points_per = st.number_input("Points per Question", min_value=1.0, value=10.0, step=0.5)
    with col3:
        show_all = st.checkbox("Show all questions at once", value=True)

    # Question selection
    st.subheader("Select Questions")
    q_options = {}
    for q in questions:
        label = f"[{q.difficulty}/{q.bloom_level}] {q.question_text[:80]}..."
        q_options[q.id] = label

    selected_q_ids = st.multiselect(
        "Choose questions for this exam",
        options=list(q_options.keys()),
        format_func=lambda x: q_options[x],
    )

    if selected_q_ids:
        st.markdown(f"**{len(selected_q_ids)} questions selected** — Total: {len(selected_q_ids) * points_per} points")

        # Preview
        with st.expander("Preview Exam"):
            st.markdown(f"## {title or 'Untitled Exam'}")
            st.markdown(instructions)
            for i, qid in enumerate(selected_q_ids):
                q = next((q for q in questions if q.id == qid), None)
                if q:
                    st.markdown(f"**Question {i+1}** ({points_per} pts) — *{q.difficulty}*")
                    st.write(q.question_text)
                    st.markdown("---")

    if st.button("Create Exam", type="primary", disabled=not (title and selected_q_ids)):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        exam_id = create_exam(
            title=title,
            instructions=instructions,
            time_limit=time_limit if time_limit > 0 else None,
            access_code=code,
            question_ids=selected_q_ids,
            points_per_q=points_per,
            show_all=show_all,
        )
        st.success(f"Exam created! Access Code: **{code}**")
        st.info("Go to Manage Exams to publish it for students.")


def manage_exams_page():
    """View, publish, and manage exams."""
    st.header("Manage Exams")

    exams = get_all_exams()
    if not exams:
        st.info("No exams yet. Build one in the Exam Builder.")
        return

    for exam in exams:
        with st.container():
            col1, col2, col3 = st.columns([4, 2, 2])
            with col1:
                status = "LIVE" if exam.is_live else "Draft"
                st.markdown(f"**{exam.title}** — `{status}`")
                st.caption(f"Code: `{exam.access_code}` | Points: {exam.total_points} | "
                           f"Time: {exam.time_limit_minutes or 'Unlimited'} min")
            with col2:
                eq = get_exam_questions(exam.id)
                st.caption(f"{len(eq)} questions")
            with col3:
                if not exam.is_live:
                    if st.button("Publish", key=f"pub_{exam.id}"):
                        publish_exam(exam.id)
                        st.rerun()
                else:
                    st.success("Live")

            # Show submissions count
            subs = get_student_responses(exam.id)
            students = set(s.student_name for s in subs)
            if students:
                st.caption(f"Submissions from: {', '.join(students)}")

            st.markdown("---")


def gradebook_page():
    """View grades, trigger grading, and export analytics."""
    st.header("Gradebook & Analytics")

    exams = get_all_exams()
    if not exams:
        st.info("No exams yet.")
        return

    exam_options = {e.id: e.title for e in exams}
    selected_exam_id = st.selectbox(
        "Select Exam",
        options=list(exam_options.keys()),
        format_func=lambda x: exam_options[x],
    )

    if not selected_exam_id:
        return

    exam = get_exam_by_id(selected_exam_id)
    responses = get_student_responses(selected_exam_id)

    if not responses:
        st.info("No submissions yet for this exam.")
        return

    # Group by student
    students = {}
    for r in responses:
        if r.student_name not in students:
            students[r.student_name] = []
        students[r.student_name].append(r)

    # Grade button
    ungraded = [r for r in responses if get_grade_for_response(r.id) is None]
    if ungraded:
        st.warning(f"{len(ungraded)} responses need grading.")
        if st.button("Grade All Ungraded Responses", type="primary"):
            progress = st.progress(0)
            for i, resp in enumerate(ungraded):
                with st.spinner(f"Grading response {i+1}/{len(ungraded)}..."):
                    try:
                        q = next((eq["question"] for eq in get_exam_questions(selected_exam_id)
                                  if eq["question"].id == resp.question_id), None)
                        if q:
                            source_content = get_content_by_id(q.content_id)
                            source_md = source_content.cleaned_markdown if source_content else ""
                            result = grade_response(q.question_text, resp.response_text, source_md)
                            save_grade(
                                response_id=resp.id,
                                score_json=result.get("rubric_scores", {}),
                                total_score=result.get("score", 0),
                                feedback_text=result.get("detailed_feedback", ""),
                                strengths=result.get("strengths", []),
                                improvements=result.get("improvements", []),
                                overall_grade=result.get("overall_grade", ""),
                            )
                    except Exception as e:
                        st.error(f"Error grading response {resp.id}: {e}")
                progress.progress((i + 1) / len(ungraded))
            st.success("All responses graded!")
            st.rerun()

    # Display grades table
    st.subheader("Results")
    grade_data = get_grades_for_exam(selected_exam_id)

    if grade_data:
        rows = []
        for g in grade_data:
            grade = g["grade"]
            rows.append({
                "Student": g["student_name"],
                "Question": g["question"][:60] + "..." if len(g["question"]) > 60 else g["question"],
                "Difficulty": g["difficulty"],
                "Bloom Level": g["bloom_level"],
                "Score": grade.total_score if grade else "Ungraded",
                "Grade": grade.overall_grade if grade else "—",
                "Submitted": g["submitted_at"].strftime("%Y-%m-%d %H:%M") if g["submitted_at"] else "",
            })

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)

        # Export CSV
        csv = df.to_csv(index=False)
        st.download_button("Export CSV", csv, f"grades_{exam.title}.csv", "text/csv")

        # Analytics
        st.subheader("Analytics")
        graded_rows = [r for r in rows if isinstance(r["Score"], (int, float))]
        if graded_rows:
            scores = [r["Score"] for r in graded_rows]
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average Score", f"{sum(scores)/len(scores):.1f}/10")
            with col2:
                st.metric("Highest", f"{max(scores):.1f}/10")
            with col3:
                st.metric("Lowest", f"{min(scores):.1f}/10")

            # By difficulty
            st.markdown("**Average by Difficulty:**")
            diff_scores = {}
            for r in graded_rows:
                d = r["Difficulty"]
                if d not in diff_scores:
                    diff_scores[d] = []
                diff_scores[d].append(r["Score"])
            for d, s in diff_scores.items():
                st.write(f"- {d}: {sum(s)/len(s):.1f}/10 ({len(s)} responses)")

            # By Bloom level
            st.markdown("**Average by Bloom Level:**")
            bloom_scores = {}
            for r in graded_rows:
                b = r["Bloom Level"]
                if b not in bloom_scores:
                    bloom_scores[b] = []
                bloom_scores[b].append(r["Score"])
            for b, s in bloom_scores.items():
                st.write(f"- {b}: {sum(s)/len(s):.1f}/10 ({len(s)} responses)")

        # Detailed feedback view
        st.subheader("Detailed Feedback")
        for g in grade_data:
            grade = g["grade"]
            if not grade:
                continue
            with st.expander(f"{g['student_name']} — Q: {g['question'][:50]}... — {grade.overall_grade}"):
                st.markdown(f"**Score:** {grade.total_score}/10 ({grade.overall_grade})")
                if grade.score_json:
                    st.markdown("**Rubric Breakdown:**")
                    for dim, score in grade.score_json.items():
                        st.write(f"- {dim.replace('_', ' ').title()}: {score}")
                st.markdown(f"**Feedback:** {grade.feedback_text}")
                if grade.strengths:
                    st.markdown("**Strengths:**")
                    for s in grade.strengths:
                        st.write(f"- {s}")
                if grade.improvements:
                    st.markdown("**Areas for Improvement:**")
                    for imp in grade.improvements:
                        st.write(f"- {imp}")
                st.markdown("---")
                st.markdown("**Student Response:**")
                st.text(g["response"])


# ── Student Exam Page ───────────────────────────────────────────────────────

def student_exam_page():
    """Student exam-taking interface with timer and auto-save."""
    exam_id = st.session_state.current_exam_id
    exam = get_exam_by_id(exam_id)

    if not exam:
        st.error("Exam not found.")
        return

    st.title(exam.title)
    st.markdown(exam.instructions)
    st.markdown("---")

    # Timer
    if exam.time_limit_minutes:
        start = datetime.fromisoformat(st.session_state.exam_start_time)
        elapsed = (datetime.utcnow() - start).total_seconds()
        remaining = exam.time_limit_minutes * 60 - elapsed

        if remaining <= 0:
            st.error("Time is up! Your exam has been auto-submitted.")
            submit_student_exam(exam_id, st.session_state.student_name)
            st.session_state.role = None
            st.session_state.authenticated = False
            st.rerun()
            return

        mins = int(remaining // 60)
        secs = int(remaining % 60)
        st.sidebar.markdown(f"### Time Remaining: {mins:02d}:{secs:02d}")
        st.sidebar.markdown("*Page refresh to update timer*")

    eq_list = get_exam_questions(exam_id)
    student = st.session_state.student_name
    student_id = st.session_state.student_id

    if exam.show_all_questions:
        # Show all questions on one page
        for i, eq_data in enumerate(eq_list):
            q = eq_data["question"]
            eq = eq_data["eq"]
            st.subheader(f"Question {i+1} ({eq.points} pts)")
            st.markdown(f"*{q.difficulty} — {q.bloom_level}*")
            st.write(q.question_text)

            response_key = f"resp_{exam_id}_{q.id}"
            response = st.text_area(
                f"Your response (aim for 400-600 words)",
                key=response_key,
                height=300,
            )
            word_count = len(response.split()) if response else 0
            st.caption(f"Word count: {word_count}")

            if st.button(f"Save Response", key=f"save_{q.id}"):
                save_student_response(exam_id, student, student_id, q.id, response)
                st.success("Response saved!")
            st.markdown("---")
    else:
        # One question at a time
        if "current_q_idx" not in st.session_state:
            st.session_state.current_q_idx = 0

        idx = st.session_state.current_q_idx
        if idx >= len(eq_list):
            idx = len(eq_list) - 1

        eq_data = eq_list[idx]
        q = eq_data["question"]
        eq = eq_data["eq"]

        st.progress((idx + 1) / len(eq_list))
        st.subheader(f"Question {idx + 1} of {len(eq_list)} ({eq.points} pts)")
        st.markdown(f"*{q.difficulty} — {q.bloom_level}*")
        st.write(q.question_text)

        response_key = f"resp_{exam_id}_{q.id}"
        response = st.text_area("Your response (aim for 400-600 words)", key=response_key, height=300)
        word_count = len(response.split()) if response else 0
        st.caption(f"Word count: {word_count}")

        col1, col2, col3 = st.columns(3)
        with col1:
            if idx > 0 and st.button("Previous"):
                save_student_response(exam_id, student, student_id, q.id, response)
                st.session_state.current_q_idx = idx - 1
                st.rerun()
        with col2:
            if st.button("Save"):
                save_student_response(exam_id, student, student_id, q.id, response)
                st.success("Saved!")
        with col3:
            if idx < len(eq_list) - 1 and st.button("Next"):
                save_student_response(exam_id, student, student_id, q.id, response)
                st.session_state.current_q_idx = idx + 1
                st.rerun()

    # Submit button
    st.markdown("---")
    st.markdown("### Submit Exam")
    st.warning("Once submitted, you cannot make changes.")
    if st.button("Submit Exam", type="primary"):
        # Save all current responses first
        for i, eq_data in enumerate(eq_list):
            q = eq_data["question"]
            resp_key = f"resp_{exam_id}_{q.id}"
            if resp_key in st.session_state:
                save_student_response(exam_id, student, student_id, q.id, st.session_state[resp_key])
        submit_student_exam(exam_id, student)
        st.success("Exam submitted successfully! You may close this window.")
        st.balloons()
        st.session_state.authenticated = False
        st.session_state.role = None


# ── Navigation ──────────────────────────────────────────────────────────────

def main():
    if not st.session_state.authenticated:
        login_page()
        return

    if st.session_state.role == "student":
        # Minimal sidebar for students
        st.sidebar.markdown(f"**Student:** {st.session_state.student_name}")
        if st.sidebar.button("Logout"):
            for k in defaults:
                st.session_state[k] = defaults[k]
            st.rerun()
        student_exam_page()
        return

    # Teacher navigation
    st.sidebar.title("Teacher Dashboard")
    if st.sidebar.button("Logout"):
        for k in defaults:
            st.session_state[k] = defaults[k]
        st.rerun()

    page = st.sidebar.radio(
        "Navigation",
        ["Content Library", "Generate Questions", "Question Bank",
         "Exam Builder", "Manage Exams", "Gradebook & Analytics"],
    )

    if page == "Content Library":
        content_library_page()
    elif page == "Generate Questions":
        question_generator_page()
    elif page == "Question Bank":
        question_bank_page()
    elif page == "Exam Builder":
        exam_builder_page()
    elif page == "Manage Exams":
        manage_exams_page()
    elif page == "Gradebook & Analytics":
        gradebook_page()


if __name__ == "__main__":
    main()
