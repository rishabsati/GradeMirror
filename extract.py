from anthropic import Anthropic
import json

client = Anthropic()

# Which assignment this feedback is from.
assignment = "CSE 355 - HW4"

# Your real Canvas feedback, pasted in.
feedback_text = """
Q2a) Missing few rules (-3)
"""

prompt = f"""You are analyzing a student's graded assignment feedback.
Extract each mistake where the student LOST points, as a JSON list.
For each mistake include:
- "question": which question (e.g. "Q3b")
- "concept": the topic the question tested, in a few words
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

raw = response.content[0].text.strip()
if raw.startswith("```"):
    raw = raw.split("```")[1].replace("json", "", 1).strip()

mistakes = json.loads(raw)

# Tag each mistake with which assignment it came from.
for m in mistakes:
    m["assignment"] = assignment

# ---- Save into our growing memory file ----
store_path = "mistakes.json"

# Load what we saved before; if the file doesn't exist yet, start empty.
try:
    with open(store_path, "r") as f:
        all_mistakes = json.load(f)
except FileNotFoundError:
    all_mistakes = []

# Remove any old records from this same assignment, so re-running just refreshes it.
all_mistakes = [m for m in all_mistakes if m["assignment"] != assignment]

# Add this assignment's mistakes to the pile.
all_mistakes.extend(mistakes)

# Write the updated pile back to the file (indent=2 makes it readable).
with open(store_path, "w") as f:
    json.dump(all_mistakes, f, indent=2)

# ---- Show what just happened ----
print(f"{assignment} — found {len(mistakes)} mistakes (saved):\n")
for m in mistakes:
    print(f"- {m['question']} | {m['concept']} | -{m['points_lost']} pts | {m['mistake']}")

print(f"\nMemory now holds {len(all_mistakes)} mistakes across all assignments.")