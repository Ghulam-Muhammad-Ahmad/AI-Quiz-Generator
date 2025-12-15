import sys
import os
from extractor import extract_text_from_file
from prompt_builder import build_prompt
from ai_adapter import generate_from_llm
from utils import ensure_folder
import uuid
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import markdown


OUTPUT_FOLDER = "outputs"
ensure_folder(OUTPUT_FOLDER)


def read_text_input():
    print("\nEnter/Paste Topics (finish with an empty line):")
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines)


def read_instructions():
    print("\nEnter instructions (Provide type of quiz, questions numbers, and difficuly level):")
    instr = input("> ")
    return instr.strip()


def convert_markdown_to_pdf(md_text, output_path):
    """Convert markdown text to a PDF using python (reportlab)."""

    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]

    # Convert markdown → simple HTML
    html_text = markdown.markdown(md_text)

    # ReportLab only supports limited HTML tags (<b>, <i>, <u>, <br>, <strong>, <em>, <para>)
    # We can split on <br> to avoid layout issues
    html_lines = html_text.replace("<br>", "\n").split("\n")

    story = []
    for line in html_lines:
        if line.strip():
            story.append(Paragraph(line, normal_style))
            story.append(Spacer(1, 12))

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    doc.build(story)


def main():
    print("=== AI Quiz Generator (Pure Python MVP) ===")

    print("\nChoose input mode:")
    print("1. Upload File (txt / pdf / docx)")
    print("2. Enter Topics")

    choice = input("\nSelect 1 or 2: ").strip()

    if choice == "1":
        filepath = input("\nEnter file path: ").strip()
        if not os.path.exists(filepath):
            print("❌ File not found.")
            sys.exit(1)
        print("Extracting text...")
        source_text = extract_text_from_file(filepath)

    elif choice == "2":
        source_text = "Topics are " + read_text_input()
    else:
        print("Invalid option.")
        sys.exit(1)

    instructions = read_instructions()

    # Build prompt
    print("\nBuilding prompt...")
    prompt = build_prompt(source_text, instructions)

    # Generate quiz using LLM adapter
    print("Calling AI model...")
    raw_quiz = generate_from_llm(prompt=prompt, instructions=instructions)

    # Save output as PDF
    fname = f"quiz_{uuid.uuid4().hex}.pdf"
    out_path = os.path.join(OUTPUT_FOLDER, fname)

    try:
        print("Generating PDF using ReportLab...")
        convert_markdown_to_pdf(raw_quiz, out_path)

    except Exception as e:
        print(f"❌ PDF generation failed: {e}")

        # fallback
        md_path = out_path.replace(".pdf", ".md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(raw_quiz)
        print(f"⚠️ Saved Markdown instead: {md_path}")
        sys.exit(1)

    print(f"\n✅ Quiz generated and saved to: {out_path}")
    print("Done!")


if __name__ == "__main__":
    main()
