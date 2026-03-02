import os
import re


def sanitize_json_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    # Remove markdown code block markers like ```json or ```
    # Also handle multiple blocks in one file by extracting just the JSON part

    # Pattern for JSON arrays or objects
    # We look for the first [ or { and the last ] or }

    # First, strip trailing backticks or garbage
    content = content.strip()
    if content.endswith('```'):
        content = content[:-3].strip()
    if content.startswith('```json'):
        content = content[7:].strip()
    elif content.startswith('```'):
        content = content[3:].strip()

    # More robust: find the first and last significant JSON character
    start_idx = -1
    for i, char in enumerate(content):
        if char in ('[', '{'):
            start_idx = i
            break

    end_idx = -1
    for i, char in enumerate(reversed(content)):
        if char in (']', '}'):
            end_idx = len(content) - i
            break

    if start_idx != -1 and end_idx != -1:
        sanitized = content[start_idx:end_idx]

        # If there are multiple blocks (like in investment_thesis.json),
        # we might have ```json in the middle. Let's clean that too.
        sanitized = re.sub(r'```json\s*', '', sanitized)
        sanitized = re.sub(r'```\s*', '', sanitized)
        # Attempt to fix concatenated arrays like ][ or ],[
        sanitized = re.sub(r'\]\s*\[', ',\n', sanitized)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(sanitized)
        print(f"Sanitized: {filepath}")
    else:
        print(f"Could not find JSON markers in: {filepath}")

# Sanitize both outputs and frontend data
paths = [
    'outputs/investment_thesis.json',
    'outputs/thesis_json.json',
    'frontend/public/data/investment_thesis.json',
    'frontend/public/data/thesis_json.json'
]

for p in paths:
    sanitize_json_file(os.path.join(os.getcwd(), p))
