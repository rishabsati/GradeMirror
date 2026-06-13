# core.py — pure logic for GradeMirror. No storage here; the app decides where data lives.
from anthropic import Anthropic
import json
from pypdf import PdfReader

client = Anthropic()


def _clean_json(raw):
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1].replace("json", "", 1).strip()
    return raw


def _mistakes_to_text(all_mistakes):
    text = ""
    for m in all_mistakes:
        text += f"- [{m['assignment']}] {m['question']}: {m['concept']} — {m['mistake']}\n"
    return text


def read_pdf_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"
    return text


def extract_mistakes(feedback_text, assignment, assignment_context=""):
    """Extract structured mistakes from feedback. Returns a list of new mistake dicts."""
    context_block = ""
    if assignment_context:
        context_block = f"""For reference, here is the assignment itself. Use it to identify what each question was actually about:
{assignment_context}
"""
    prompt = f"""You are analyzing a student's graded assignment feedback.
{context_block}
Extract each mistake where the student LOST points, as a JSON list.
For each mistake include:
- "question": which question (e.g. "Q3b")
- "concept": the topic the question tested, in a few words (use the assignment above to be specific)
- "mistake": a short description of what went wrong
- "points_lost": the number of points lost (a number)

Respond with ONLY the JSON list. No other text, no markdown.

Feedback:
{feedback_text}
"""
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    try:
        mistakes = json.loads(_clean_json(response.content[0].text))
    except json.JSONDecodeError:
        raise ValueError("Couldn't read structured mistakes from that feedback. Try adding more detail or rephrasing it.")

    for m in mistakes:
        m["assignment"] = assignment
    return mistakes


def merge_mistakes(all_mistakes, new_mistakes, assignment):
    """Add new mistakes for an assignment, replacing any old records for that same assignment."""
    all_mistakes = [m for m in all_mistakes if m["assignment"] != assignment]
    all_mistakes.extend(new_mistakes)
    return all_mistakes


def find_patterns(all_mistakes):
    prompt = f"""Here is a list of a student's past mistakes across several assignments:

{_mistakes_to_text(all_mistakes)}

Identify the student's RECURRING weaknesses — patterns that appear across more than one assignment or question. For each pattern:
- Give it a short name.
- Explain it in one sentence.
- List which assignments/questions it shows up in.

Be specific, and only call something a pattern if the evidence actually supports it. If something happened only once, do not call it a pattern.
"""
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def make_checklist(upcoming_assignment, all_mistakes):
    prompt = f"""A student is about to submit this assignment:
{upcoming_assignment}

Here are mistakes the student made on PAST assignments:
{_mistakes_to_text(all_mistakes)}

Based on the student's past mistakes, write a short pre-submission checklist for THIS assignment.
- Focus on the recurring weaknesses most likely to bite them again on this particular assignment.
- Make each item a concrete thing to check, phrased as a question or an action.
- Only include items that are actually relevant to this assignment's topics.
- Keep it to 3-6 items.
"""
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text