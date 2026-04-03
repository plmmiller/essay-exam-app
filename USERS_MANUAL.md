# Essay Exam Generator & Grader -- User's Manual

## Table of Contents

1. [Introduction](#1-introduction)
2. [Getting Started](#2-getting-started)
3. [Teacher Guide](#3-teacher-guide)
4. [Student Guide](#4-student-guide)
5. [Exam Administration Workflow](#5-exam-administration-workflow)
6. [Grading & Review Workflow](#6-grading--review-workflow)
7. [Troubleshooting / FAQ](#7-troubleshooting--faq)

---

## 1. Introduction

The Essay Exam Generator & Grader is a Streamlit-based web application that helps teachers create, administer, and grade essay exams. It uses AI (Anthropic Claude) to generate essay questions from uploaded teaching content and to automatically grade student responses using a structured rubric.

### Key Capabilities

- **Content Management** -- Upload teaching materials (PDF, Word, Markdown, plain text) and store them in a searchable library.
- **AI Question Generation** -- Produce essay questions at multiple difficulty levels using Bloom's Taxonomy, grounded entirely in your uploaded content.
- **Exam Building** -- Assemble questions into exams with configurable time limits, point values, and access codes.
- **Student Registration & Exam Taking** -- Students register with an access code, then take the exam in-browser with auto-save and an optional countdown timer.
- **Automated Grading** -- AI grades student responses across four rubric dimensions (accuracy, depth, organization, clarity) and provides detailed feedback, strengths, and improvement areas.
- **Teacher Review** -- Review and adjust AI-assigned grades per student, add comments, and approve grades individually or in bulk before export.
- **Analytics & Export** -- View score distributions by difficulty and Bloom level, and export grades to CSV.

### Roles

| Role | Access |
|---------|--------------------------------------------------------------|
| Teacher | Full access to all pages via sidebar navigation after login. |
| Student | Access to exam registration and exam-taking interface only.  |

---

## 2. Getting Started

### 2.1 Prerequisites

- Python 3.9 or higher
- An Anthropic API key (required for AI question generation and grading)

### 2.2 Installation

1. Clone or download the project folder.

2. Open a terminal and navigate to the project directory:
   ```
   cd /path/to/essay-exam-app
   ```

3. Install the Python dependencies:
   ```
   pip install -r requirements.txt
   ```

   The required packages are: `streamlit`, `anthropic`, `sqlalchemy`, `python-dotenv`, `markdown2`, `PyMuPDF`, `python-docx`, `reportlab`, and `pandas`.

### 2.3 Configuration

1. Create a file named `.env` in the project root directory (same folder as `main.py`).

2. Add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

3. Optionally set a custom teacher login password (the default is `admin`):
   ```
   TEACHER_PASSWORD=your-secure-password
   ```

### 2.4 Running the Application

Start the app with:

```
streamlit run main.py
```

Alternatively, use the included launcher script which sets the working directory and port automatically:

```
python start.py
```

The application will open in your browser at `http://localhost:8501`.

### 2.5 Database

The app uses a SQLite database file named `essay_exam.db`, created automatically in the project directory on first run. No separate database setup is needed. The database schema is managed internally and will auto-migrate when new features are added.

---

## 3. Teacher Guide

After logging in with the teacher password, you will see a sidebar on the left with seven navigation pages. This section explains each one.

### 3.1 Content Library

The Content Library is where you upload and manage the teaching materials that will serve as the basis for generated exam questions.

**Uploading Content:**

1. Navigate to **Content Library** in the sidebar.
2. In the "Upload New Content" section, drag and drop files or click to select them. Supported formats: `.md` (Markdown), `.pdf`, `.txt` (plain text), `.docx` (Microsoft Word).
3. Optionally enter comma-separated tags in the "Tags" field (e.g., `biology, chapter3, ecology`).
4. Click **Process & Upload**.
5. Each file will be converted to clean Markdown internally. A confirmation message will show the filename and word count.

**Viewing Content:**

- Uploaded files are listed below the upload section, showing the filename, file type badge, word count, tags, and upload date.
- Click the **Preview** expander on any item to see the first 2,000 characters of the cleaned Markdown.

**Deleting Content:**

- Click the **Delete** button next to any content item.
- Note: Deleting content will mark all questions generated from that content as inactive. Those questions will no longer appear in the Question Bank.

### 3.2 Generate Questions

This page uses AI to create essay questions from your uploaded content.

1. Navigate to **Generate Questions** in the sidebar.
2. In the multiselect dropdown, choose one or more content sources to generate questions from. The content will be combined for the AI prompt.
3. Select a **Difficulty Level**:
   - **Basic** -- Questions targeting Remember and Understand levels of Bloom's Taxonomy (explain, summarize, define, describe, identify).
   - **Intermediate** -- Questions targeting Apply and Analyze levels (compare, apply, break down, examine, contrast).
   - **Advanced** -- Questions targeting Evaluate and Create levels (argue, critique, design, synthesize, propose, assess).
   - **All Levels** -- Generates a mix across all three levels, distributed evenly.
4. Use the slider to set the **Number of questions** (3 to 15).
5. Optionally provide **Custom instructions** (e.g., "Focus on Chapter 3 themes" or "Emphasize ethical implications").
6. Click **Generate Questions**.
7. The AI will process the request. For "All Levels," it runs three separate generation passes. Generated questions are displayed on screen and saved to the Question Bank automatically.

Each generated question includes:
- The question text
- Difficulty level (Basic, Intermediate, or Advanced)
- Bloom's Taxonomy level (e.g., Analyze, Evaluate)
- Source section references

### 3.3 Question Bank

The Question Bank displays all previously generated questions.

1. Navigate to **Question Bank** in the sidebar.
2. Use the **Filter by Difficulty** dropdown to show only Basic, Intermediate, or Advanced questions (or All).
3. Use the **Filter by Bloom Level** text input to search by Bloom level (e.g., typing "Analyze" will show only Analyze-level questions).
4. Each question card shows:
   - Question ID number
   - Difficulty and Bloom level tags
   - The full question text
   - Source section references
   - The source content filename
   - Creation date

There is no manual question editing in this view. To remove questions, delete the source content from the Content Library (which deactivates all related questions).

### 3.4 Exam Builder

The Exam Builder lets you assemble questions into a formal exam.

1. Navigate to **Exam Builder** in the sidebar.
2. Enter an **Exam Title** (e.g., "Midterm Essay Exam").
3. Write or edit the **Instructions for Students**. A default prompt about essay length and sourcing is pre-filled.
4. Set the following options:
   - **Time Limit** -- Enter minutes. Set to 0 for unlimited time.
   - **Points per Question** -- Default is 10. All questions on the exam will have this point value.
   - **Show all questions at once** -- When checked, students see every question on a single scrollable page. When unchecked, students navigate one question at a time with Previous/Next buttons.
5. In the **Select Questions** multiselect, choose the questions you want on the exam. Each option shows the difficulty, Bloom level, and a preview of the question text.
6. Review the summary line showing the number of selected questions and total points.
7. Optionally click **Preview Exam** to expand a formatted preview of how the exam will appear.
8. Click **Create Exam**.
9. The system will generate a random 6-character access code (letters and digits). Note this code -- you will give it to students so they can register and take the exam.
10. The exam is created in **Draft** status. You must publish it from the Manage Exams page before students can take it.

### 3.5 Manage Exams

This page lets you view all exams, publish them, and monitor student registrations and submissions.

1. Navigate to **Manage Exams** in the sidebar.
2. Each exam card displays:
   - Title and status (**Draft** or **LIVE**)
   - Access code
   - Total points and time limit
   - Number of questions
   - Count of registered and submitted students
3. For Draft exams, click **Publish** to make the exam live. Once published, registered students can enter and take the exam.
4. Expand the **Registered Students** section to see a list of all students who have registered, along with their submission status (Submitted or Not submitted).

Important: Students must register before the exam is published or while registration remains open. The access code is the same for both registration and exam entry.

### 3.6 Gradebook & Analytics

The Gradebook provides an overview of grading status, lets you trigger AI grading, and shows analytics.

**Viewing the Gradebook:**

1. Navigate to **Gradebook & Analytics** in the sidebar.
2. Select an exam from the dropdown.
3. The summary bar at the top shows four metrics: Total Responses, Graded, Ungraded, and Approved.

**Running Auto-Grading:**

1. If there are ungraded responses, a warning banner will appear showing the count.
2. Click **Auto-Grade Ungraded Responses**. The AI will grade each response one by one, showing a progress bar.
3. Grading uses a rubric with four dimensions:
   - Content Accuracy & Fidelity to Source (30% of points)
   - Depth & Analysis / Bloom's Level (30% of points)
   - Organization & Structure (20% of points)
   - Clarity, Grammar & Style (20% of points)
4. After grading completes, the page will refresh with results.

**Approving Grades in Bulk:**

- Click **Approve All AI Grades** to mark every graded-but-unapproved response as approved. Use this if you are satisfied with the AI grades and do not need to review each one individually.

**Results Table:**

- A table shows each response with: Student name, Question (truncated), Difficulty, Bloom Level, AI Score, Final Score, Letter Grade, Status (Approved or Pending Review), and Submission timestamp.
- Click **Export CSV** to download the full results table.

**Analytics Section:**

- Average, highest, and lowest scores across all graded responses.
- Average score broken down by difficulty level (Basic, Intermediate, Advanced).
- Average score broken down by Bloom's Taxonomy level.

**Detailed Feedback:**

- Below the analytics, each graded response has an expandable section showing the full AI score, rubric breakdown, written feedback, strengths, areas for improvement, and the student's original response text.

### 3.7 Review Grades

The Review Grades page provides a per-student, per-question interface for reviewing and adjusting AI grades before finalizing them.

1. Navigate to **Review Grades** in the sidebar.
2. Select an exam from the dropdown.
3. The summary bar shows Graded/Total, Approved/Graded, and Average Score.
4. If there are ungraded responses, a warning directs you to auto-grade them first from the Gradebook page.
5. Use the **Show** filter to display All responses, only Pending Review, or only Approved.

**Reviewing Individual Grades:**

1. Responses are grouped by student name.
2. Expand any response to see:
   - The question text with difficulty and Bloom level
   - The student's full response (read-only)
   - AI grading results: score, letter grade, rubric breakdown, feedback, strengths, and improvement areas
3. In the **Teacher Review** section:
   - Adjust the **Adjusted Score** using the number input (defaults to the AI score).
   - Modify individual rubric dimension scores if desired.
   - Add **Teacher Comments** in the text area.
4. Click **Approve As-Is** to approve the grade without changes (your comments will still be saved).
5. Click **Save Adjustments & Approve** to save your adjusted score, modified rubric scores, and comments, and mark the grade as approved.

**Bulk Approve:**

- At the top of the page, click **Approve All [N] AI Grades Without Changes** to approve all remaining unapproved grades at once.

**Exporting Approved Grades:**

- At the bottom of the page, an **Export Approved Grades (CSV)** button appears once approved grades exist. The export includes: Student, Student ID, Question, AI Score, Final Score, Grade, and Teacher Comments.

---

## 4. Student Guide

### 4.1 Registering for an Exam

1. Open the application URL in your browser (provided by your teacher).
2. On the landing page, look at the **Student Exam Portal** panel on the right side.
3. Click the **Register for Exam** tab.
4. Enter:
   - **Your Name** -- Use the name your teacher expects (this is how your submission will be identified).
   - **Student ID** -- Enter your student ID number.
   - **Email** -- Optional.
   - **Exam Access Code** -- The 6-character code provided by your teacher.
5. Click **Register**.
6. If successful, you will see a confirmation message with the exam title. You can now close the page and return when your teacher makes the exam live.

### 4.2 Taking an Exam

1. Return to the application URL.
2. On the landing page, click the **Take Exam** tab in the Student Exam Portal.
3. Enter:
   - **Your Name** -- Must match the name you registered with exactly.
   - **Student ID** -- Optional.
   - **Exam Access Code** -- The same 6-character code.
4. Click **Enter Exam**.
5. If the exam is live and you are registered, you will enter the exam interface.

**During the Exam:**

- If the exam has a time limit, a countdown timer appears in the sidebar. Refresh the page to update the displayed time. When time expires, your exam is auto-submitted.
- Each question shows its point value, difficulty, and Bloom level.
- Type your response in the text area below each question. A live word count is displayed beneath each response area. Aim for 400-600 words per question.

**If all questions are shown at once:**
- Scroll through the page to see and answer all questions.
- Click **Save Response** under each question to save your work as you go.

**If questions are shown one at a time:**
- Use the **Previous** and **Next** buttons to navigate between questions. Your current response is saved automatically when you navigate.
- Click **Save** to explicitly save your current response.

**Submitting:**

1. When you have answered all questions, scroll to the bottom.
2. Read the warning: "Once submitted, you cannot make changes."
3. Click **Submit Exam**.
4. All responses are saved and marked as final. You will see a success message.
5. After submission, you cannot re-enter the exam. If you try to log in again with the same name and access code, you will see a message saying you have already submitted.

---

## 5. Exam Administration Workflow

This section outlines the complete end-to-end process for creating and administering an exam.

### Step 1: Upload Content

1. Go to **Content Library**.
2. Upload all relevant teaching materials (lecture notes, readings, textbook chapters) as PDF, DOCX, MD, or TXT files.
3. Add tags to organize content for easy selection later.

### Step 2: Generate Questions

1. Go to **Generate Questions**.
2. Select the content source(s) for this exam.
3. Choose the difficulty level and number of questions.
4. Optionally add custom instructions to focus the AI on specific topics.
5. Click **Generate Questions** and wait for the AI to finish.
6. Review the generated questions on screen.

### Step 3: Review the Question Bank

1. Go to **Question Bank**.
2. Browse and filter the generated questions.
3. If you need more questions, return to Generate Questions and run another batch. You can generate from different content sources or at different difficulty levels.

### Step 4: Build the Exam

1. Go to **Exam Builder**.
2. Enter the exam title and instructions.
3. Set the time limit, points per question, and question display mode.
4. Select questions from the bank.
5. Preview the exam layout.
6. Click **Create Exam** and record the 6-character access code.

### Step 5: Share the Access Code

- Distribute the access code to your students through your usual communication channel (email, LMS, in class). Students need this code to register.

### Step 6: Let Students Register

- Students go to the app URL and register using the access code, their name, student ID, and optionally their email.
- You can monitor registrations from the **Manage Exams** page by expanding the "Registered Students" section.

### Step 7: Publish the Exam

1. Go to **Manage Exams**.
2. Find your exam (it will show as "Draft").
3. Click **Publish**. The status changes to "LIVE."
4. Students who have registered can now enter and take the exam.

### Step 8: Monitor Submissions

- On the **Manage Exams** page, watch the submitted count increase as students finish.
- Each student's registration entry will show "Submitted" or "Not submitted."

### Step 9: Grade and Review

- Once students have submitted, proceed to the grading workflow described in the next section.

---

## 6. Grading & Review Workflow

### Step 1: Auto-Grade Responses

1. Go to **Gradebook & Analytics**.
2. Select the exam from the dropdown.
3. Review the summary metrics. The "Ungraded" count tells you how many responses need grading.
4. Click **Auto-Grade Ungraded Responses**.
5. Wait for the AI to grade each response. A progress bar tracks completion. This may take several minutes depending on the number of responses.

### Step 2: Review the Results

1. Examine the results table for any scores that seem unusually high or low.
2. Scroll down to the **Detailed Feedback** section to read the AI's rubric breakdown, strengths, and improvement notes for each response.

### Step 3: Decide on Your Review Approach

You have two options:

**Option A -- Approve all AI grades as-is:**
- If you are satisfied with the AI grading, click **Approve All AI Grades** on the Gradebook page. This marks all grades as final.

**Option B -- Review and adjust individually:**
1. Go to **Review Grades**.
2. Select the exam.
3. Set the filter to "Pending Review" to focus on unapproved grades.
4. Work through each student's responses:
   - Read the question and the student's response.
   - Review the AI score, rubric breakdown, and feedback.
   - If the AI score is appropriate, click **Approve As-Is**.
   - If you want to change the score, adjust the score and/or rubric dimension values, add teacher comments, then click **Save Adjustments & Approve**.
5. Once all grades are reviewed, the Approved count should match the Graded count.

### Step 4: Export Grades

1. On the **Gradebook & Analytics** page, click **Export CSV** to download the full results table with all grading data.
2. On the **Review Grades** page, click **Export Approved Grades (CSV)** at the bottom to download only the finalized, approved grades. This export includes the final score (teacher-adjusted if applicable) and teacher comments.

---

## 7. Troubleshooting / FAQ

**Q: I see "ANTHROPIC_API_KEY not set" when generating questions or grading.**
A: Make sure you have created a `.env` file in the project root directory containing `ANTHROPIC_API_KEY=your-key-here`. Restart the Streamlit app after adding the key.

**Q: The teacher password "admin" does not work.**
A: Check if someone has set a custom password via the `TEACHER_PASSWORD` environment variable in the `.env` file. The default is `admin` only when that variable is not set.

**Q: A student says they cannot enter the exam.**
A: Verify all of the following:
1. The student has registered using the correct access code.
2. The exam has been published (status is "LIVE" on the Manage Exams page).
3. The student is entering their name exactly as they registered it (names are case-sensitive).
4. The student has not already submitted the exam (re-entry after submission is not allowed).

**Q: A student's name at registration does not match what they use to take the exam.**
A: The system matches students by exact name string. If a student registers as "John Smith" but tries to enter as "john smith," it will not match. The student will need to register again with the exact name they plan to use, or you can have them re-register.

**Q: Can I edit a question after it has been generated?**
A: There is no question editing interface in the current version. If a question is unsuitable, generate a new batch and select different questions for your exam. You can delete source content from the Content Library to deactivate all questions generated from it.

**Q: Can I edit an exam after creating it?**
A: The current version does not support editing exams after creation. Create a new exam if you need to make changes to the question selection or settings.

**Q: Can students see their grades?**
A: No. In the current version, grades are only visible to the teacher through the Gradebook and Review Grades pages.

**Q: How does the timer work?**
A: The timer starts when the student enters the exam. It counts down based on the time limit set in the Exam Builder. The timer display in the sidebar updates when the student refreshes the page. When time expires, the exam is auto-submitted with whatever responses have been saved.

**Q: What happens if a student loses their connection during the exam?**
A: Responses are saved each time a student clicks "Save Response" (or "Save" / "Previous" / "Next" in single-question mode). The student can close and re-enter the exam using the same name and access code, and their saved responses will be restored -- as long as they have not clicked "Submit Exam."

**Q: How is the AI grading rubric structured?**
A: Each response is graded on four dimensions, scaled proportionally to the points per question:
- Content Accuracy & Fidelity to Source -- 30% of total points
- Depth & Analysis (Bloom's level alignment) -- 30% of total points
- Organization & Structure -- 20% of total points
- Clarity, Grammar & Style -- 20% of total points

The AI also provides a letter grade, written feedback, a list of strengths, and a list of areas for improvement.

**Q: What does "Approve" mean for a grade?**
A: Approving a grade marks it as teacher-reviewed and finalized. Until a grade is approved, it is considered "Pending Review." Only approved grades appear in the approved grades CSV export from the Review Grades page. Approving does not change the score unless you explicitly adjust it.

**Q: Can I re-grade a response after it has already been graded?**
A: Running auto-grade again from the Gradebook will only grade responses that have not been graded yet. To change an existing grade, use the Review Grades page to adjust the score manually.

**Q: What file formats are supported for content upload?**
A: The app supports four formats:
- `.md` -- Markdown files (used as-is)
- `.pdf` -- PDF documents (text extracted via PyMuPDF)
- `.txt` -- Plain text files
- `.docx` -- Microsoft Word documents (text and tables extracted, headings preserved)

**Q: Is there a limit on content size?**
A: For question generation, content is truncated to approximately 80,000 characters (roughly 20,000 tokens) per AI request. For grading, source content is truncated to 60,000 characters. Very large documents will work but content beyond these limits will not be seen by the AI.

**Q: How do I reset the database and start fresh?**
A: Stop the application, delete the `essay_exam.db` file from the project directory, and restart the app. A new empty database will be created automatically.
