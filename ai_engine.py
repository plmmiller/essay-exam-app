"""
AI Engine for essay question generation and automated grading.

Uses the Anthropic Claude API with carefully structured prompts based on
Bloom's Taxonomy. All questions are grounded in uploaded content only.
Grading uses a 10-point rubric across four dimensions.
"""

import json
import os
from anthropic import Anthropic

client = None


def _get_client():
    global client
    if client is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set. Add it to your .env file.")
        client = Anthropic(api_key=api_key)
    return client


def generate_questions(content_markdown, num_questions, difficulty,
                       custom_instructions=""):
    """
    Generate essay questions from content using Bloom's Taxonomy.

    Returns a list of dicts with keys: id, question, difficulty, bloom_level, source_sections.
    Content is chunked if too long to fit in a single prompt.
    """
    # Chunk content if very long (>80k chars ~ 20k tokens)
    max_content_len = 80000
    content_to_use = content_markdown[:max_content_len]
    if len(content_markdown) > max_content_len:
        content_to_use += "\n\n[Content truncated for length]"

    custom_line = ""
    if custom_instructions.strip():
        custom_line = f"\nAdditional instructions from the teacher: {custom_instructions.strip()}"

    prompt = f"""You are an expert educator using Bloom's Taxonomy.

Content:
{content_to_use}

Generate EXACTLY {num_questions} essay questions at {difficulty} level.{custom_line}

Rules:
- Every question must be answerable ONLY from the provided content.
- Questions must be open-ended, requiring 400-600 word essays.
- Include the exact Bloom's verb in parentheses at the end of each question.
- Number them clearly.
- For each question, provide a model_answer: a comprehensive 400-600 word ideal response that demonstrates the depth, accuracy, and structure expected for full marks. The model answer should reference specific content from the source material.
- Return ONLY a JSON array: [{{"id":1, "question":"...", "difficulty":"{difficulty}", "bloom_level":"Analyze", "source_sections":"pages/sections referenced", "model_answer":"A comprehensive ideal response..."}}]

Bloom's level mapping:
- Basic: Remember, Understand (verbs: explain, summarize, define, describe, identify)
- Intermediate: Apply, Analyze (verbs: compare, apply, break down, examine, contrast)
- Advanced: Evaluate, Create (verbs: argue, critique, design, synthesize, propose, assess)"""

    c = _get_client()
    response = c.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=16384,
        temperature=0.2,
        top_p=0.95,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text.strip()
    # Extract JSON from response (handle markdown code blocks)
    if "```" in text:
        start = text.find("[")
        end = text.rfind("]") + 1
        text = text[start:end]

    questions = json.loads(text)
    return questions


def grade_response(question_text, response_text, source_content, max_points=10.0,
                    model_answer=""):
    """
    Grade a student's essay response using a rubric scaled to max_points.

    If a model_answer is provided, it is used as the benchmark for grading.
    Returns a dict with: score, rubric_scores, detailed_feedback,
    strengths, improvements, overall_grade, excerpts_from_source.
    """
    max_source_len = 60000
    source_to_use = source_content[:max_source_len]

    # Scale rubric dimensions proportionally
    accuracy_max = round(max_points * 0.3, 1)
    depth_max = round(max_points * 0.3, 1)
    org_max = round(max_points * 0.2, 1)
    clarity_max = round(max_points - accuracy_max - depth_max - org_max, 1)

    model_answer_section = ""
    if model_answer.strip():
        model_answer_section = f"""
Model Answer (use as the benchmark for a perfect response — compare the student's essay against this):
{model_answer.strip()}

"""

    prompt = f"""You are an expert, fair, and consistent essay grader using the following rubric ({max_points}-point scale):

Content Accuracy & Fidelity to Source (0-{accuracy_max})
Depth & Analysis (Bloom's level) (0-{depth_max})
Organization & Structure (0-{org_max})
Clarity, Grammar & Style (0-{clarity_max})

Original Question: {question_text}
{model_answer_section}
Student Essay: {response_text}

Source Content: {source_to_use}

{"Compare the student's response against the model answer above. " if model_answer.strip() else ""}Grade based on how well the student addresses the question using evidence from the source content.

Return ONLY valid JSON:
{{
  "score": {max_points * 0.85},
  "rubric_scores": {{"accuracy": {accuracy_max}, "depth": {depth_max * 0.8}, "organization": {org_max * 0.75}, "clarity": {clarity_max * 0.75}}},
  "detailed_feedback": "Excellent synthesis of...",
  "strengths": ["..."],
  "improvements": ["..."],
  "overall_grade": "A-",
  "excerpts_from_source": ["quoted evidence student should have used"]
}}"""

    c = _get_client()
    response = c.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        temperature=0.2,
        top_p=0.95,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text.strip()
    if "```" in text:
        start = text.find("{")
        end = text.rfind("}") + 1
        text = text[start:end]

    return json.loads(text)
