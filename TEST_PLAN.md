# Essay Exam Generator & Grader -- Test Plan

**Status: DRAFT - PENDING APPROVAL**

**Application:** Essay Exam Generator & Grader (Streamlit)
**Date:** 2026-04-02
**Modules Under Test:** main.py, database.py, ai_engine.py, content_processor.py

---

## 1. System Tests (Infrastructure)

### SYS-01: App Startup
- **Description:** Verify the Streamlit app starts without errors and renders the login page.
- **Steps:**
  1. Run `streamlit run main.py`.
  2. Open the URL printed to the console.
- **Expected Result:** The browser loads the app with the title "Essay Exam Generator & Grader" and shows Teacher Login and Student Exam Portal columns.
- **Type:** Manual

### SYS-02: Database Initialization
- **Description:** Verify `init_db()` creates the SQLite database file and all required tables on first run.
- **Steps:**
  1. Delete `essay_exam.db` if it exists.
  2. Import `database` and call `init_db()`.
  3. Inspect the database for all expected tables.
- **Expected Result:** The file `essay_exam.db` is created. Tables present: `contents`, `questions`, `exams`, `exam_questions`, `student_responses`, `grades`, `exam_registrations`.
- **Type:** Automated

### SYS-03: Database Migration Columns
- **Description:** Verify `_migrate_db()` adds missing columns to existing tables without data loss.
- **Steps:**
  1. Create a database with an older schema that lacks `teacher_adjusted_score`, `teacher_adjusted_rubric`, `teacher_comments`, `is_approved`, `approved_at` on `grades` and `allow_registration` on `exams`.
  2. Call `init_db()`.
  3. Inspect the `grades` and `exams` tables for the new columns.
- **Expected Result:** All six migration columns exist on their respective tables. Pre-existing data is preserved.
- **Type:** Automated

### SYS-04: Schema Column Verification
- **Description:** Verify every model column maps to a database column with the correct type.
- **Steps:**
  1. Call `init_db()`.
  2. Use `sqlalchemy.inspect(engine)` to list columns for each table.
  3. Compare against the expected column names and types defined in the ORM models.
- **Expected Result:** All columns from the `Content`, `Question`, `Exam`, `ExamQuestion`, `StudentResponse`, `Grade`, and `ExamRegistration` models are present with matching types.
- **Type:** Automated

### SYS-05: Environment Variable Loading
- **Description:** Verify `.env` file values are loaded at startup via `dotenv`.
- **Steps:**
  1. Create a `.env` file with `TEACHER_PASSWORD=testpw123` and `ANTHROPIC_API_KEY=sk-test`.
  2. Start the app.
  3. Verify `os.environ.get("TEACHER_PASSWORD")` returns `testpw123`.
- **Expected Result:** Environment variables from `.env` are accessible via `os.environ`.
- **Type:** Automated

---

## 2. Functional Tests by Feature Area

### A. Authentication

#### AUTH-01: Teacher Login -- Correct Password
- **Description:** Teacher can log in with the correct password.
- **Steps:**
  1. Navigate to the app.
  2. Enter the password matching `TEACHER_PASSWORD` (default: `admin`).
  3. Click "Login as Teacher".
- **Expected Result:** Session state sets `authenticated=True` and `role="teacher"`. The sidebar shows "Teacher Dashboard" with navigation options.
- **Type:** Manual

#### AUTH-02: Teacher Login -- Incorrect Password
- **Description:** Teacher is rejected with an incorrect password.
- **Steps:**
  1. Navigate to the app.
  2. Enter an incorrect password.
  3. Click "Login as Teacher".
- **Expected Result:** An error message "Incorrect password." is displayed. Session state `authenticated` remains `False`.
- **Type:** Manual

#### AUTH-03: Student Registration -- Valid Code
- **Description:** Student can register for an exam with a valid access code.
- **Steps:**
  1. Create and publish an exam with access code `ABC123` (registration open).
  2. On the login page, go to the "Register for Exam" tab.
  3. Enter name, student ID, and access code `ABC123`.
  4. Click "Register".
- **Expected Result:** A success message appears confirming registration. An `ExamRegistration` row is created in the database.
- **Type:** Manual

#### AUTH-04: Student Registration -- Invalid Code
- **Description:** Student receives an error when registering with a nonexistent access code.
- **Steps:**
  1. On the login page, go to the "Register for Exam" tab.
  2. Enter name, student ID, and access code `ZZZZZ`.
  3. Click "Register".
- **Expected Result:** An error message "Invalid access code." is displayed. No registration row is created.
- **Type:** Manual

#### AUTH-05: Student Registration -- Closed Registration
- **Description:** Student is blocked when registration is closed for the exam.
- **Steps:**
  1. Create an exam and set `allow_registration=False` in the database.
  2. Attempt to register using that exam's access code.
- **Expected Result:** An error message "Registration is closed for this exam." is displayed.
- **Type:** Manual

#### AUTH-06: Student Registration -- Duplicate
- **Description:** Registering the same student name for the same exam again does not create a duplicate.
- **Steps:**
  1. Register student "Alice" for exam with code `ABC123`.
  2. Register student "Alice" for the same exam code again.
- **Expected Result:** The second registration returns the existing record. Only one `ExamRegistration` row exists for that student/exam pair.
- **Type:** Automated

#### AUTH-07: Student Exam Entry -- Registered and Live
- **Description:** A registered student can enter a live exam.
- **Steps:**
  1. Register student "Alice" for an exam. Publish the exam.
  2. On the "Take Exam" tab, enter name "Alice" and the exam access code.
  3. Click "Enter Exam".
- **Expected Result:** Session state sets `authenticated=True`, `role="student"`, `current_exam_id` to the exam ID. The student exam page renders.
- **Type:** Manual

#### AUTH-08: Student Exam Entry -- Not Registered
- **Description:** An unregistered student cannot enter an exam.
- **Steps:**
  1. Publish an exam.
  2. On the "Take Exam" tab, enter a name that is not registered and the exam access code.
  3. Click "Enter Exam".
- **Expected Result:** An error message "You are not registered for this exam. Please register first." is displayed.
- **Type:** Manual

#### AUTH-09: Student Exam Entry -- Already Submitted
- **Description:** A student who already submitted cannot re-enter the exam.
- **Steps:**
  1. Register and submit an exam as student "Alice".
  2. Attempt to enter the same exam again as "Alice".
- **Expected Result:** An error message "You have already submitted this exam." is displayed.
- **Type:** Manual

#### AUTH-10: Student Exam Entry -- Exam Not Live
- **Description:** A student cannot enter a draft (unpublished) exam.
- **Steps:**
  1. Create an exam but do not publish it. Register a student.
  2. Attempt to enter the exam using the access code.
- **Expected Result:** An error message "This exam is not yet live. Please contact your teacher." is displayed.
- **Type:** Manual

---

### B. Content Library

#### CL-01: Upload Markdown File
- **Description:** Upload a `.md` file and verify it is stored correctly.
- **Steps:**
  1. Log in as teacher. Navigate to Content Library.
  2. Upload a valid `.md` file with tags "test, markdown".
  3. Click "Process & Upload".
- **Expected Result:** A success message shows the filename and word count. The file appears in the library list with file type badge "Markdown" and the entered tags.
- **Type:** Manual

#### CL-02: Upload PDF File
- **Description:** Upload a `.pdf` file and verify text extraction.
- **Steps:**
  1. Upload a multi-page PDF file.
  2. Click "Process & Upload".
  3. Expand the "Preview" section.
- **Expected Result:** The file is stored. Preview shows extracted text with `## Page N` headings. Word count is greater than zero.
- **Type:** Manual

#### CL-03: Upload TXT File
- **Description:** Upload a `.txt` file.
- **Steps:**
  1. Upload a valid `.txt` file.
  2. Click "Process & Upload".
- **Expected Result:** The file is stored with file type badge "Text" and correct word count.
- **Type:** Manual

#### CL-04: Upload DOCX File
- **Description:** Upload a `.docx` file and verify heading/table extraction.
- **Steps:**
  1. Upload a `.docx` file containing headings, body text, and a table.
  2. Click "Process & Upload".
  3. Expand the "Preview" section.
- **Expected Result:** Preview shows headings as markdown headings (`#`, `##`), paragraphs as text, and tables in markdown table format.
- **Type:** Manual

#### CL-05: Content Preview Rendering
- **Description:** Verify the preview is truncated at 2000 characters with a truncation notice.
- **Steps:**
  1. Upload a file with more than 2000 characters of cleaned markdown.
  2. Expand the "Preview" section.
- **Expected Result:** Preview ends with "*[Preview truncated...]*" and shows at most 2000 characters of content.
- **Type:** Manual

#### CL-06: Content Deletion and Question Deactivation
- **Description:** Deleting content marks all linked questions as inactive.
- **Steps:**
  1. Upload content and generate questions from it.
  2. Confirm questions appear in the Question Bank.
  3. Delete the content from the Content Library.
- **Expected Result:** The content row is removed. All questions with that `content_id` have `is_active=False` and no longer appear in the Question Bank (active-only view).
- **Type:** Automated

#### CL-07: Tag Storage and Display
- **Description:** Tags entered during upload are stored and displayed.
- **Steps:**
  1. Upload a file with tags "biology, chapter3, ecology".
  2. View the Content Library list.
- **Expected Result:** The content entry displays "Tags: biology, chapter3, ecology" below the filename.
- **Type:** Manual

---

### C. Question Generation

#### QG-01: Single Difficulty Level Generation
- **Description:** Generate questions at a single specified difficulty.
- **Steps:**
  1. Upload content. Navigate to Generate Questions.
  2. Select the content, choose "Intermediate" difficulty, set count to 5.
  3. Click "Generate Questions".
- **Expected Result:** Exactly 5 questions are returned. All have `difficulty="Intermediate"`. Each has a `bloom_level` consistent with Intermediate (Apply or Analyze). Questions are saved to the database.
- **Type:** Manual

#### QG-02: All Levels Generation
- **Description:** Generate questions across all difficulty levels.
- **Steps:**
  1. Select content, choose "All Levels" difficulty, set count to 9.
  2. Click "Generate Questions".
- **Expected Result:** 9 questions total: 3 Basic, 3 Intermediate, 3 Advanced (distribution: `per_level = max(1, 9//3) = 3`). Each level's Bloom verbs match the expected mapping.
- **Type:** Manual

#### QG-03: Custom Instructions
- **Description:** Custom instructions are included in the AI prompt.
- **Steps:**
  1. Select content, enter custom instructions "Focus only on Chapter 2 themes".
  2. Generate questions.
- **Expected Result:** Generated questions are thematically related to the custom instruction topic. The prompt sent to the API includes the custom instructions string.
- **Type:** Manual

#### QG-04: Multiple Content Sources
- **Description:** Generate questions from multiple selected content items.
- **Steps:**
  1. Upload two separate content files.
  2. Select both in the content multiselect.
  3. Generate questions.
- **Expected Result:** Questions are generated from the combined content. The `content_id` on all saved questions is set to the first selected content ID (`selected_ids[0]`).
- **Type:** Manual

#### QG-05: Error Handling -- No API Key
- **Description:** A clear error is shown when `ANTHROPIC_API_KEY` is not set.
- **Steps:**
  1. Unset or remove `ANTHROPIC_API_KEY` from `.env`.
  2. Restart the app and attempt to generate questions.
- **Expected Result:** An error message appears: "ANTHROPIC_API_KEY not set. Add it to your .env file."
- **Type:** Manual

#### QG-06: Error Handling -- API Failure
- **Description:** An API error is caught and displayed to the teacher.
- **Steps:**
  1. Set `ANTHROPIC_API_KEY` to an invalid key.
  2. Attempt to generate questions.
- **Expected Result:** An error message is displayed (e.g., "Error: ...authentication..."). No questions are saved to the database. The app does not crash.
- **Type:** Manual

---

### D. Question Bank

#### QB-01: Filter by Difficulty
- **Description:** The difficulty filter correctly narrows the question list.
- **Steps:**
  1. Generate questions at Basic, Intermediate, and Advanced levels.
  2. Navigate to Question Bank.
  3. Select "Basic" from the difficulty filter.
- **Expected Result:** Only Basic-level questions are shown. The count line reads "Showing N of M questions" where N < M.
- **Type:** Manual

#### QB-02: Filter by Bloom Level
- **Description:** The Bloom level text filter works.
- **Steps:**
  1. Navigate to Question Bank.
  2. Enter "Analyze" in the Bloom Level filter.
- **Expected Result:** Only questions whose `bloom_level` contains "Analyze" (case-insensitive) are displayed.
- **Type:** Manual

#### QB-03: Display of Question Metadata
- **Description:** Each question displays all expected metadata fields.
- **Steps:**
  1. Navigate to Question Bank with questions present.
  2. Inspect any question entry.
- **Expected Result:** Each entry shows: question ID (`Q#N`), difficulty badge, Bloom level badge, question text, source sections (if present), source filename, and created date.
- **Type:** Manual

---

### E. Exam Builder

#### EB-01: Create Exam with All Options
- **Description:** Create an exam specifying all configuration options.
- **Steps:**
  1. Navigate to Exam Builder.
  2. Enter title "Midterm Essay", custom instructions, time limit 60, points per question 15, uncheck "Show all questions at once".
  3. Select 3 questions.
  4. Click "Create Exam".
- **Expected Result:** Success message shows a 6-character access code. The exam is saved with `title="Midterm Essay"`, `time_limit_minutes=60`, `total_points=45` (3 x 15), `show_all_questions=False`, `is_live=False`. Three `ExamQuestion` rows with `points=15.0` and `order` 1, 2, 3.
- **Type:** Manual

#### EB-02: Access Code Uniqueness
- **Description:** Each exam receives a unique randomly generated access code.
- **Steps:**
  1. Create 10 exams in rapid succession.
  2. Query all access codes from the database.
- **Expected Result:** All 10 access codes are distinct 6-character strings composed of uppercase letters and digits.
- **Type:** Automated

#### EB-03: Question Selection and Ordering
- **Description:** Questions are stored in the order they were selected.
- **Steps:**
  1. Select questions Q3, Q1, Q5 (in that order) in the multiselect.
  2. Create the exam.
  3. Query `exam_questions` for that exam, ordered by `order`.
- **Expected Result:** `ExamQuestion` rows have `order=1` for Q3, `order=2` for Q1, `order=3` for Q5.
- **Type:** Automated

#### EB-04: Exam Preview
- **Description:** The preview expander shows exam title, instructions, and selected questions.
- **Steps:**
  1. Fill in exam title and instructions, select questions.
  2. Expand "Preview Exam".
- **Expected Result:** Preview displays the title as an H2, the instructions, and each selected question numbered with points and difficulty.
- **Type:** Manual

---

### F. Manage Exams

#### ME-01: Publish Exam (Draft to Live)
- **Description:** Publishing changes an exam's status from Draft to Live.
- **Steps:**
  1. Create an exam (defaults to draft).
  2. Navigate to Manage Exams.
  3. Click the "Publish" button on the draft exam.
- **Expected Result:** The exam's status changes to "LIVE". The Publish button is replaced by a "Live" success badge. Database `is_live=True`.
- **Type:** Manual

#### ME-02: Registration Count Display
- **Description:** The registration and submission counts are accurate.
- **Steps:**
  1. Create and publish an exam.
  2. Register 3 students. Have 1 student submit.
  3. Navigate to Manage Exams.
- **Expected Result:** The exam entry shows "Registered: 3 | Submitted: 1".
- **Type:** Manual

#### ME-03: Registered Student List with Status
- **Description:** The registered students expander shows each student with their submission status.
- **Steps:**
  1. Register students "Alice" and "Bob". Have "Alice" submit.
  2. Expand the "Registered Students" section.
- **Expected Result:** Alice is listed with "Submitted" status. Bob is listed with "Not submitted" status. Both show student ID and email if provided.
- **Type:** Manual

---

### G. Student Exam Taking

#### SE-01: Draft Response Pre-Loading
- **Description:** Previously saved but unsubmitted responses are restored on page refresh.
- **Steps:**
  1. Enter an exam as a student.
  2. Type a response and click "Save Response".
  3. Refresh the browser page and re-enter the exam.
- **Expected Result:** The previously saved response text appears pre-filled in the text area.
- **Type:** Manual

#### SE-02: Save Individual Responses
- **Description:** Clicking "Save Response" persists the text to the database.
- **Steps:**
  1. Enter an exam, type a response.
  2. Click "Save Response" (or "Save" in one-at-a-time mode).
- **Expected Result:** A `StudentResponse` row is created/updated with `is_submitted=False` and the entered text.
- **Type:** Manual

#### SE-03: Word Count Display
- **Description:** The word count updates as the student types.
- **Steps:**
  1. Enter an exam.
  2. Type a response with a known number of words.
- **Expected Result:** The caption below the text area shows "Word count: N" matching the actual word count (split by whitespace).
- **Type:** Manual

#### SE-04: Timer Functionality (Time-Limited Exam)
- **Description:** The countdown timer displays and auto-submits when time expires.
- **Steps:**
  1. Create an exam with a 2-minute time limit and publish it.
  2. Enter the exam as a student.
  3. Observe the sidebar timer.
  4. Wait for the timer to reach zero.
- **Expected Result:** Sidebar shows "Time Remaining: MM:SS" decrementing on page refresh. When time expires, the message "Time is up! Your exam has been auto-submitted." appears and all responses are marked as submitted.
- **Type:** Manual

#### SE-05: One-at-a-Time Navigation
- **Description:** When `show_all_questions=False`, Previous/Next buttons navigate between questions.
- **Steps:**
  1. Create an exam with 3 questions and `show_all_questions` unchecked. Publish it.
  2. Enter the exam. Verify only question 1 is shown.
  3. Click "Next". Verify question 2 is shown.
  4. Click "Previous". Verify question 1 is shown.
- **Expected Result:** Only one question is visible at a time. The progress bar updates. Navigation saves the current response before moving. "Previous" is hidden on question 1. "Next" is hidden on the last question.
- **Type:** Manual

#### SE-06: Show All Questions Mode
- **Description:** When `show_all_questions=True`, all questions render on a single page.
- **Steps:**
  1. Create an exam with `show_all_questions=True` and 3 questions. Publish and enter it.
- **Expected Result:** All 3 questions are visible on the page simultaneously, each with its own text area and "Save Response" button.
- **Type:** Manual

#### SE-07: Exam Submission
- **Description:** Submitting the exam marks all responses as submitted and logs the student out.
- **Steps:**
  1. Enter an exam, type responses, click "Submit Exam".
- **Expected Result:** A success message appears. All `StudentResponse` rows for this student/exam have `is_submitted=True` and `submitted_at` set. Session state resets (`authenticated=False`).
- **Type:** Manual

#### SE-08: Re-Entry Prevention After Submission
- **Description:** A student who already submitted sees a completion message instead of the exam.
- **Steps:**
  1. Submit an exam as student "Alice".
  2. Re-enter the exam as "Alice" (this is blocked at AUTH-09, but also test the exam page guard).
  3. Directly set session state to simulate entry and load the student exam page.
- **Expected Result:** The message "You have already submitted this exam. Thank you!" is displayed with a Logout button. No question text areas are shown.
- **Type:** Manual

---

### H. Auto-Grading

#### AG-01: Grade Ungraded Responses
- **Description:** The "Auto-Grade Ungraded Responses" button grades all ungraded submissions.
- **Steps:**
  1. Have 3 submitted responses for an exam, none graded.
  2. Navigate to Gradebook & Analytics, select the exam.
  3. Click "Auto-Grade Ungraded Responses".
- **Expected Result:** A progress bar advances through each response. After completion, all 3 responses have associated `Grade` records with `total_score`, `score_json`, `feedback_text`, `strengths`, `improvements`, and `overall_grade` populated. The summary metrics update (Graded: 3, Ungraded: 0).
- **Type:** Manual

#### AG-02: Rubric Scaling with Custom max_points
- **Description:** The grading rubric scales proportionally to the exam's points per question.
- **Steps:**
  1. Create an exam with `points_per_question=20`.
  2. Submit a response and auto-grade it.
  3. Inspect the `score_json` rubric dimensions.
- **Expected Result:** Rubric dimensions sum to approximately 20. Specifically: accuracy max = `round(20 * 0.3, 1) = 6.0`, depth max = 6.0, organization max = 4.0, clarity max = 4.0.
- **Type:** Automated

#### AG-03: Error Handling During Grading
- **Description:** An API error during grading shows an error message but does not halt grading of other responses.
- **Steps:**
  1. Have 3 ungraded responses.
  2. Mock or force the AI engine to fail on the second response.
  3. Click "Auto-Grade Ungraded Responses".
- **Expected Result:** An error message is displayed for the second response (e.g., "Error grading response N: ..."). Responses 1 and 3 are graded successfully.
- **Type:** Manual

#### AG-04: Grading Summary Metrics Accuracy
- **Description:** The `get_grading_summary()` function returns correct counts and averages.
- **Steps:**
  1. Create an exam with 4 submitted responses.
  2. Grade 3 of them with scores 8, 6, and 10. Approve 2 of those.
  3. Call `get_grading_summary(exam_id)`.
- **Expected Result:** Returns `total_responses=4`, `graded_count=3`, `ungraded_count=1`, `approved_count=2`, `average_score=8.0`.
- **Type:** Automated

---

### I. Grade Review

#### GR-01: View AI Grades Per Student
- **Description:** The Review Grades page shows graded responses grouped by student.
- **Steps:**
  1. Auto-grade responses for an exam with two students.
  2. Navigate to Review Grades and select the exam.
- **Expected Result:** Responses are grouped under student name subheaders. Each response shows the question text, student response (read-only), AI score, rubric breakdown, feedback, strengths, and areas for improvement.
- **Type:** Manual

#### GR-02: Adjust Individual Score
- **Description:** Teacher can change the adjusted score for a graded response.
- **Steps:**
  1. Navigate to Review Grades, expand a graded response.
  2. Change the "Adjusted Score" number input from the AI score to a new value (e.g., 7.5).
  3. Click "Save Adjustments & Approve".
- **Expected Result:** The `Grade` record has `teacher_adjusted_score=7.5` and `is_approved=True`. The `final_score` property returns 7.5.
- **Type:** Manual

#### GR-03: Adjust Rubric Dimension Scores
- **Description:** Teacher can individually adjust each rubric dimension score.
- **Steps:**
  1. Expand a graded response in Review Grades.
  2. Change the "Accuracy" rubric score from the AI value to a new value.
  3. Click "Save Adjustments & Approve".
- **Expected Result:** The `Grade` record has `teacher_adjusted_rubric` as a JSON dict with the modified "accuracy" value. Other rubric dimensions retain their values.
- **Type:** Manual

#### GR-04: Add Teacher Comments
- **Description:** Teacher can add free-text comments to a grade.
- **Steps:**
  1. Expand a graded response.
  2. Enter text in the "Teacher Comments" field.
  3. Click "Approve As-Is" or "Save Adjustments & Approve".
- **Expected Result:** The `Grade` record has `teacher_comments` set to the entered text.
- **Type:** Manual

#### GR-05: Approve Individual Grade (As-Is)
- **Description:** The "Approve As-Is" button approves without changing the score.
- **Steps:**
  1. Expand a graded, unapproved response.
  2. Click "Approve As-Is".
- **Expected Result:** The `Grade` record has `is_approved=True` and `approved_at` set. `teacher_adjusted_score` remains `None`.
- **Type:** Manual

#### GR-06: Save Adjustments and Approve
- **Description:** The "Save Adjustments & Approve" button saves score changes and approves in one action.
- **Steps:**
  1. Adjust the score and rubric values for a response.
  2. Click "Save Adjustments & Approve".
- **Expected Result:** The `Grade` record has `teacher_adjusted_score` set to the new value, `teacher_adjusted_rubric` updated, `is_approved=True`, and `approved_at` set.
- **Type:** Manual

#### GR-07: Bulk Approve All
- **Description:** The "Approve All" button approves all graded but unapproved grades for the exam.
- **Steps:**
  1. Auto-grade 5 responses, leave all unapproved.
  2. Click the "Approve All N AI Grades Without Changes" button.
- **Expected Result:** All 5 grades have `is_approved=True` and `approved_at` set. The button disappears after rerun since no unapproved grades remain.
- **Type:** Manual

#### GR-08: Filter by Approval Status
- **Description:** The radio filter correctly narrows the displayed grades.
- **Steps:**
  1. Have a mix of approved and pending grades.
  2. Select "Pending Review" filter.
  3. Select "Approved" filter.
  4. Select "All" filter.
- **Expected Result:** "Pending Review" shows only unapproved grades. "Approved" shows only approved grades. "All" shows both.
- **Type:** Manual

#### GR-09: CSV Export of Approved Grades
- **Description:** The export button downloads a CSV containing only approved grade data.
- **Steps:**
  1. Approve some grades. Leave others unapproved.
  2. Click "Export Approved Grades (CSV)".
  3. Open the downloaded file.
- **Expected Result:** CSV contains columns: Student, Student ID, Question, AI Score, Final Score, Grade, Teacher Comments. Only approved grades are included. Final Score reflects teacher adjustments where present.
- **Type:** Manual

---

### J. Gradebook & Analytics

#### GA-01: Results Table Accuracy
- **Description:** The results table displays correct values for AI Score, Final Score, and Status.
- **Steps:**
  1. Auto-grade and partially approve responses for an exam.
  2. Navigate to Gradebook & Analytics.
  3. Inspect the dataframe.
- **Expected Result:** AI Score shows `grade.total_score`. Final Score shows `teacher_adjusted_score` if set, otherwise `total_score`. Status shows "Approved" or "Pending Review". Ungraded responses show "Ungraded" and "--".
- **Type:** Manual

#### GA-02: Analytics Calculations
- **Description:** Average score, average by difficulty, and average by Bloom level are correct.
- **Steps:**
  1. Grade responses across multiple difficulties and Bloom levels with known scores.
  2. View the Analytics section.
- **Expected Result:** Overall average matches manual calculation. Per-difficulty averages match. Per-Bloom-level averages match. Response counts per group are correct.
- **Type:** Automated

#### GA-03: Gradebook CSV Export
- **Description:** The gradebook CSV export contains all displayed rows.
- **Steps:**
  1. Navigate to Gradebook & Analytics with graded responses.
  2. Click "Export CSV".
  3. Open the file.
- **Expected Result:** CSV contains all rows shown in the results table with columns: Student, Question, Difficulty, Bloom Level, AI Score, Final Score, Grade, Status, Submitted.
- **Type:** Manual

---

## 3. Integration Tests

#### INT-01: Full End-to-End Workflow
- **Description:** Complete lifecycle from content upload through grade export.
- **Steps:**
  1. Log in as teacher.
  2. Upload a markdown file with tags "test".
  3. Generate 3 Intermediate questions from the uploaded content.
  4. Verify questions appear in the Question Bank.
  5. Build an exam with all 3 questions, title "E2E Test", 10 pts each, show all questions.
  6. Note the access code.
  7. Publish the exam in Manage Exams.
  8. Log out.
  9. Register student "Alice" with the access code.
  10. Enter the exam as "Alice".
  11. Write responses to all 3 questions (at least 50 words each).
  12. Save each response individually.
  13. Submit the exam.
  14. Log in as teacher.
  15. Navigate to Gradebook & Analytics, select the exam.
  16. Click "Auto-Grade Ungraded Responses".
  17. Verify 3 grades appear with scores and feedback.
  18. Navigate to Review Grades.
  19. Adjust one score, add a comment, click "Save Adjustments & Approve".
  20. Approve the remaining two grades as-is.
  21. Export the approved grades CSV.
  22. Open the CSV and verify all 3 rows are present with correct data.
- **Expected Result:** Each step succeeds. The exported CSV contains 3 rows with student name "Alice", correct AI scores, the adjusted final score for the modified grade, and the teacher comment.
- **Type:** Manual

---

## 4. Edge Cases

#### EDGE-01: Empty Content Upload
- **Description:** Uploading a file with no text content is handled gracefully.
- **Steps:**
  1. Upload an empty `.txt` file (0 bytes).
  2. Click "Process & Upload".
- **Expected Result:** The content is either rejected with an error message, or stored with `word_count=0` and empty `cleaned_markdown`. No crash occurs.
- **Type:** Manual

#### EDGE-02: Very Long Content Truncation
- **Description:** Content exceeding 80,000 characters is truncated for question generation.
- **Steps:**
  1. Upload a file with more than 80,000 characters of text.
  2. Generate questions from it.
- **Expected Result:** The AI prompt receives only the first 80,000 characters plus the note "[Content truncated for length]". Questions are generated successfully from the truncated content.
- **Type:** Automated

#### EDGE-03: Student Submitting with Empty Responses
- **Description:** A student can submit an exam even if some or all response text areas are empty.
- **Steps:**
  1. Enter an exam as a student.
  2. Leave all response text areas blank.
  3. Click "Submit Exam".
- **Expected Result:** The exam is submitted. `StudentResponse` rows are created with empty `response_text`. Auto-grading these empty responses does not crash (the AI engine receives an empty student essay string).
- **Type:** Manual

#### EDGE-04: Re-Grading Previously Graded Responses
- **Description:** Running auto-grade again on already-graded responses updates the existing grade.
- **Steps:**
  1. Auto-grade all responses for an exam.
  2. Manually delete one grade from the database (or simulate by setting the grade to NULL via a direct query).
  3. Click "Auto-Grade Ungraded Responses" again.
- **Expected Result:** Only the response without a grade is sent for grading. Previously graded responses are not re-graded. The `save_grade` function's update path handles pre-existing `Grade` rows by updating rather than inserting.
- **Type:** Automated

#### EDGE-05: Teacher Adjusts Score Then Bulk Approves
- **Description:** A teacher adjusts one grade manually, then bulk approves the rest.
- **Steps:**
  1. Auto-grade 3 responses.
  2. Adjust and approve one grade (changing the score to 5.0).
  3. Click "Approve All" in the Review Grades page.
- **Expected Result:** The manually adjusted grade retains `teacher_adjusted_score=5.0` and remains approved. The other 2 grades are approved as-is with no teacher adjustment. `bulk_approve_grades` skips already-approved grades (the count returned is 2, not 3).
- **Type:** Automated

#### EDGE-06: Unsupported File Type Upload
- **Description:** Uploading a file with an unsupported extension is rejected.
- **Steps:**
  1. Attempt to upload a `.xlsx` file via the Content Library uploader.
- **Expected Result:** Streamlit's file uploader rejects the file (only `md`, `pdf`, `txt`, `docx` are accepted). If somehow bypassed, `process_file` raises `ValueError("Unsupported file type: .xlsx")`.
- **Type:** Manual

#### EDGE-07: Concurrent Student Registrations
- **Description:** Two students registering simultaneously for the same exam do not cause database errors.
- **Steps:**
  1. Simulate two concurrent calls to `register_student()` with different student names for the same exam.
- **Expected Result:** Both registrations succeed. Two distinct `ExamRegistration` rows are created.
- **Type:** Automated

#### EDGE-08: Grade final_score Property
- **Description:** The `Grade.final_score` property returns the correct value in all states.
- **Steps:**
  1. Create a `Grade` with `total_score=8.0` and `teacher_adjusted_score=None`.
  2. Check `final_score`. Then set `teacher_adjusted_score=6.5` and check again.
- **Expected Result:** First check returns `8.0`. Second check returns `6.5`.
- **Type:** Automated
