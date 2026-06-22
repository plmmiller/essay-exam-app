# Project Status — essay-exam-app

> **What this file is:** the single living source of truth for what is done and what
> is not. It is a burndown, not a planning snapshot. Every status here has been
> **verified against the actual code/repo at the date shown — never assumed.**
> When work lands, this file is updated in the same change.

- **Last updated:** 2026-06-22
- **Updated by:** reconciled by agent (verified against code)
- **Verified against:** `main @ 3f45889`
- **Phase / milestone:** Feature-complete v1 (Streamlit MVP), deployment-ready
- **Source plan(s):** `docs/PRD.docx` (binary, not parsed), `TEST_PLAN.md`, `USERS_MANUAL.md`, `Essay exams.docx`. No `F-NN` work-item list existed in the repo; IDs below are derived from the actual modules/features.

## At a glance

| Metric | Count |
|---|---|
| ✅ Done | 14 |
| 🟡 Partial / in progress | 3 |
| ⬜ Not started | 1 |
| 🚫 Blocked | 0 |
| **Total items** | **18** |

**Current focus:** Deployment configuration. The three most recent commits added Render (`render.yaml`) and Streamlit Cloud (`.streamlit/config.toml`) deploy config on top of the feature-complete app. No deploy has been verified live.

---

## Task list

> Legend: ✅ done · 🟡 partial / in progress · ⬜ not started · 🚫 blocked
> "Evidence" must point to something real — a file, function, PR, test, or migration.

| ID | Item | Status | Owner | Evidence (file / PR / test) | Notes |
|---|---|---|---|---|---|
| F-01 | Data model & SQLite persistence (7 tables) | ✅ | — | `database.py` ORM models; `test_automated.py::TestSYS02/SYS04` | contents, questions, exams, exam_questions, student_responses, grades, exam_registrations |
| F-02 | Schema migration (additive ALTER TABLE) | ✅ | — | `database.py::_migrate_db`; `test_automated.py::TestSYS03` | Adds teacher-review + model_answer + allow_registration columns |
| F-03 | Content upload & processing (MD/PDF/TXT/DOCX → markdown) | ✅ | — | `content_processor.py::process_file`; `main.py::content_library_page` | PDF via PyMuPDF, DOCX via python-docx (incl. tables) |
| F-04 | Content Library UI (upload, preview, delete, tags) | ✅ | — | `main.py::content_library_page`; `database.py::delete_content` | — |
| F-05 | Content deletion deactivates linked questions | ✅ | — | `database.py::delete_content`; `test_automated.py::TestCL06` | — |
| F-06 | AI question generation (Bloom's Taxonomy) | ✅ | — | `ai_engine.py::generate_questions`; `main.py::question_generator_page` | Anthropic claude-sonnet-4; difficulty levels + "All Levels" mix |
| F-07 | Model answer keys (generate, view, edit) | ✅ | — | `ai_engine.py` prompt `model_answer`; `database.py::update_model_answer`; `main.py::question_bank_page` | Editable in Question Bank |
| F-08 | Question Bank (view, filter by difficulty/Bloom) | ✅ | — | `main.py::question_bank_page`; `database.py::get_all_questions` | — |
| F-09 | Exam Builder (compose, order, points, preview, access code) | ✅ | — | `main.py::exam_builder_page`; `database.py::create_exam`; `test_automated.py::TestEB02/EB03` | 6-char alphanumeric code; order preserved |
| F-10 | Exam management & publishing (draft → live) | ✅ | — | `main.py::manage_exams_page`; `database.py::publish_exam` | — |
| F-11 | Student registration (with duplicate guard) | ✅ | — | `main.py` login_page register tab; `database.py::register_student`; `test_automated.py::TestAUTH06/EDGE07` | — |
| F-12 | Student exam-taking (auto-save drafts, word count, timer, submit) | 🟡 | — | `main.py::student_exam_page` | Timer requires manual page refresh to update (no live countdown); auto-submit only fires on refresh |
| F-13 | AI auto-grading (4-dimension rubric, scaled to points) | ✅ | — | `ai_engine.py::grade_response`; `main.py::gradebook_page`; `test_automated.py::TestAG02` | Compares against model answer when present |
| F-14 | Re-grade upsert (no duplicate grade rows) | ✅ | — | `database.py::save_grade`; `test_automated.py::TestEDGE04` | — |
| F-15 | Gradebook & analytics (summary, CSV export, by difficulty/Bloom) | ✅ | — | `main.py::gradebook_page`; `database.py::get_grading_summary`; `test_automated.py::TestAG04` | — |
| F-16 | Teacher grade review (adjust score/rubric, comments, approve, bulk-approve) | ✅ | — | `main.py::review_grades_page`; `database.py::adjust_grade/approve_grade/bulk_approve_grades`; `test_automated.py::TestEDGE05/EDGE08` | — |
| F-17 | Authentication (teacher password, student portal) | 🟡 | — | `main.py::login_page` (`TEACHER_PASSWORD`, default `"admin"`) | Single shared teacher password from env; defaults to `admin` if unset. No per-user accounts/roles beyond teacher/student |
| F-18 | Deployment configuration (Render + Streamlit Cloud) | 🟡 | — | `render.yaml`; `.streamlit/config.toml`; `start.py`; commits 9e0225a, 3f45889 | Config files present but no verified live deploy; SQLite file storage is ephemeral on these hosts |

### Partial items — what's left

- **F-12 (Student exam timer):** The countdown is computed server-side but only re-renders on page refresh (`main.py` notes "*Page refresh to update timer*"). Auto-submit on timeout fires only when the student refreshes; there is no background/JS live timer. Functional but UX-limited.
- **F-17 (Auth):** Only a single shared teacher password (env `TEACHER_PASSWORD`, falling back to the literal `"admin"` when unset). No multi-teacher accounts, no password hashing, no student authentication beyond name + access-code matching.
- **F-18 (Deployment):** `render.yaml` and `.streamlit/config.toml` exist and define env vars (`ANTHROPIC_API_KEY`, `TEACHER_PASSWORD`), but there is no evidence in-repo of a successful live deployment. SQLite (`essay_exam.db`) is local/ephemeral — data will not persist across restarts on Render/Streamlit Cloud's default filesystem.

---

## Next up (in priority order)

1. Verify a live deployment (Render or Streamlit Cloud) and confirm env vars are set (F-18).
2. Address ephemeral SQLite storage for any real deployment (managed Postgres or persistent disk) (F-18/F-01).
3. Improve the student exam timer to update without a manual refresh; harden auto-submit (F-12).
4. Strengthen auth: remove the `"admin"` default, consider per-teacher accounts / hashing (F-17).
5. Add an automated test runner / CI to execute `test_automated.py` on each change (F-19, not yet started).

## Blocked

| ID | Blocked on | Since | What would unblock it |
|---|---|---|---|
| — | — | — | — |

## Decisions & pivots

- **2026-06-22** — STATUS.md reconciled against the codebase by agent.
- **Observed** — App is a single-file Streamlit MVP (`main.py`) backed by SQLite via SQLAlchemy; grading/generation use the Anthropic API (`claude-sonnet-4-20250514`). No web framework, no separate frontend.

## Changelog

- **2026-06-22** — reconciled seed → verified statuses (✅ 14 / 🟡 3 / ⬜ 1 / 🚫 0). Derived F-01..F-18 from actual modules/features; cited `test_automated.py` cases and source functions as evidence. (F-19 "CI test runner" tracked as ⬜ in Next up — no in-repo evidence.)

---

### Maintenance rules (do not delete)

1. **Verify, don't guess.** Before marking anything ✅ or 🟡, confirm it against the
   code/tests/repo. Cite the evidence. If you can't verify, mark it ⬜ and say so.
2. **Update in the same change as the work.** A landed feature and its status entry
   move together. This file should never lag the repo by more than the current change.
3. **One source of truth.** Planning docs describe intent and sequence; this file is the
   only place that tracks completion state.
4. **Refresh the header every update** — date, updater, and the git SHA verified against.
5. **Don't silently drop items.** Move descoped items to a `## Dropped` section with a
   dated reason rather than deleting them.
