import json

def normalize_instructions(instr):
    if not instr:
        return {}

    try:
        return json.loads(instr)
    except (json.JSONDecodeError, TypeError):
        return {"raw_instruction_text": instr}


def build_prompt(source_text, instructions):
    instr = normalize_instructions(instructions)

    prompt = f"""
You are an expert exam generator.

SOURCE MATERIAL:
{source_text[:15000]}

INSTRUCTIONS:
{json.dumps(instr, indent=2)}

Generate a quiz in a clean, well-formatted MARKDOWN format.
Use headings for the title and questions.
Use lists for multiple-choice options (if asked for mcqs format).
"""
    print(prompt)
    return prompt.strip()
