# 📚 GradeMirror

> Learn from your own mistakes.

GradeMirror is an AI-powered feedback memory tool for students. It remembers the feedback from your graded assignments, finds the mistakes you keep repeating across them, and warns you before you make them again.

## The Problem

Feedback gets scattered and forgotten. You fix what a grader marked on one homework, then make the same underlying mistake on the next one — because nothing connects your feedback over time. A great tutor who had seen all your past work might say "you keep leaving required pieces out" — but no tool does that. Your feedback lives in a dozen disconnected Canvas comments and never gets synthesized into actionable self-knowledge.

## What It Does

1. **Remember** — Paste feedback from a graded assignment (optionally upload the assignment PDF to sharpen the results). GradeMirror extracts each mistake as a structured record: which question, what concept, what went wrong, points lost.
2. **Analyze** — Ask it to find your recurring weaknesses. It reads your entire history and surfaces patterns that span multiple assignments — not just one-off mistakes.
3. **Prevent** — Before submitting your next assignment, describe it and get a personalized pre-submission checklist based on *your* past mistakes. Targeted at the specific weaknesses most likely to cost you points on *this* assignment.

## Why It's Not Just ChatGPT

ChatGPT is stateless — it forgets you the moment you close the tab. The value here is a persistent, growing record of your own work that accumulates across a whole semester. Cross-assignment pattern detection only works if someone is holding all your assignments at once. That's what GradeMirror does.

## Tech Stack

- **Python** — core logic
- **Anthropic Claude API** (claude-haiku-4-5) — structured mistake extraction and pattern reasoning
- **Streamlit** — web UI
- **pypdf** — PDF text extraction
- **JSON** — persistent per-user memory (download/restore)

## Architecture

The project separates concerns cleanly:
- `core.py` — pure logic (extraction, pattern finding, checklist generation). No UI, no storage.
- `app.py` — Streamlit UI. Manages per-session state, calls core functions, handles errors.

Each user's data is isolated in their browser session (no shared state). Users can download their data as JSON and restore it on their next visit.

## Running Locally

```bash
# Clone the repo
git clone https://github.com/rishabsati/GradeMirror.git
cd GradeMirror

# Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt

# Set your Anthropic API key
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Run the app
streamlit run app.py
```

## Live Demo

[Link coming soon]

---

Built by [Rishab Sati](https://github.com/rishabsati) · ASU Computer Science
