from anthropic import Anthropic
import json

client = Anthropic()

# Load the whole memory pile.
with open("mistakes.json", "r") as f:
    all_mistakes = json.load(f)

# Turn the records into readable text to hand to the model.
mistakes_text = ""
for m in all_mistakes:
    mistakes_text += f"- [{m['assignment']}] {m['question']}: {m['concept']} — {m['mistake']} (-{m['points_lost']} pts)\n"

prompt = f"""Here is a list of a student's past mistakes across several assignments:

{mistakes_text}

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

print(response.content[0].text)