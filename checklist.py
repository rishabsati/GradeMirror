from anthropic import Anthropic
import json

client = Anthropic()

# Load your past mistakes (your recurring weaknesses).
with open("mistakes.json", "r") as f:
    all_mistakes = json.load(f)

# Describe the assignment you're about to submit (edit this to a real one).
upcoming_assignment = "CSE 355 HW5: prove languages are not context-free using the pumping lemma for CFLs, and convert between PDAs and CFGs."

# Format your past mistakes into readable text.
mistakes_text = ""
for m in all_mistakes:
    mistakes_text += f"- [{m['assignment']}] {m['question']}: {m['concept']} — {m['mistake']}\n"

prompt = f"""A student is about to submit this assignment:
{upcoming_assignment}

Here are mistakes the student made on PAST assignments:
{mistakes_text}

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

print("Pre-submission checklist:\n")
print(response.content[0].text)