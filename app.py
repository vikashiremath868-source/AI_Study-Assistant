import os
import re
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# ==============================
# CONFIGURATION
# ==============================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
NOTES_FILE = Path("notes.txt")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Check your .env file."
    )

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.6-flash"


# ==============================
# STUDY NOTES
# ==============================

def study_notes():
    print("\n--- Study Notes ---")

    subject = input("Enter subject: ").strip()
    note = input("Enter your note: ").strip()

    if not subject or not note:
        print("Subject and note cannot be empty.")
        return

    with NOTES_FILE.open("a", encoding="utf-8") as file:
        file.write(f"\nSubject: {subject}\n")
        file.write(f"Note: {note}\n")
        file.write("-" * 40 + "\n")

    print("Notes saved successfully!")


def view_notes():
    print("\n--- Your Study Notes ---")

    if not NOTES_FILE.exists():
        print("No notes found.")
        return

    content = NOTES_FILE.read_text(encoding="utf-8")

    if not content.strip():
        print("No notes found.")
        return

    print(content)


# ==============================
# ASK AI
# ==============================

def ask_question():
    print("\n--- Ask AI ---")

    question = input("Enter your question: ").strip()

    if not question:
        print("Question cannot be empty.")
        return

    print("\nGenerating answer...")

    try:
        interaction = client.interactions.create(
            model=MODEL_NAME,
            input=question,
            generation_config={
                "thinking_level": "low"
            }
        )

        print("\nAI Response:")
        print(interaction.output_text)

    except Exception as error:
        print("\nUnable to get AI response.")
        print("Error:", error)


# ==============================
# GENERATE QUIZ
# ==============================

def generate_quiz():
    print("\n--- Generate Quiz ---")
    score=0
    correct_answers=[]

    topic = input("Enter the topic: ").strip()

    if not topic:
        print("Topic cannot be empty.")
        return

    prompt = f"""
Create a beginner-friendly quiz about {topic}.

give me exactly 5 multiple-choice questions.

For each question provide:
A. Option
B. Option
C. Option
D. Option

Then provide:
correct Answer:A/B/C/D
Explanation:

Keep the quiz suitable for a BTech CSE student.
"""

    print("\nGenerating quiz...")

    try:
        interaction = client.interactions.create(
            model=MODEL_NAME,
            input=prompt,
            generation_config={
                "thinking_level": "low"
            }
        )

        print("\n" + "=" * 50)
        print("                 AI QUIZ")
        print("=" * 50)

        quiz_text = interaction.output_text
        correct_answers = re.findall(r"Correct Answer:\s*([A-D])", quiz_text, re.IGNORECASE)
        quiz_for_user = re.sub(r"Correct Answer:.*(?:\n|$)", "", quiz_text)
        quiz_for_user = re.sub(r"Explanation:.*(?:\n|$)", "", quiz_for_user)

        print(quiz_for_user)
        user_answers = input("Enter your 5 answers (A/B/C/D), separated by spaces: ").upper().split()
        score = 0

        for i in range(min(len(user_answers), len(correct_answers))):
            if user_answers[i] == correct_answers[i].upper():
                score += 1

        print(f"\nYour Score: {score}/5")
        percentage=(score/5)*100
        print(f"Percentage: {percentage:.2f}%")
        if score >=3:
            print(" result: good job!")
        else:
            print("result keep practicing!")

        print(quiz_text)

        print("=" * 50)
        print("\nNow you can review your answers above.")

    except Exception as error:
       print("\nQuiz could not be generated.")
       print("Please try again in a few seconds.")
       print("Error:", error)

# ==============================
# MENU
# ==============================

def display_menu():
    print("\n" + "=" * 40)
    print("        AI STUDY ASSISTANT")
    print("=" * 40)
    print("1. Study Notes")
    print("2. View Notes")
    print("3. Ask AI")
    print("4. Generate Quiz")
    print("5. Exit")
    print("=" * 40)


# ==============================
# MAIN PROGRAM
# ==============================

def main():
    while True:
        display_menu()

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            study_notes()

        elif choice == "2":
            view_notes()

        elif choice == "3":
            ask_question()

        elif choice == "4":
            generate_quiz()

        elif choice == "5":
            print("\nThank you for using AI Study Assistant!")
            break

        else:
            print("\nInvalid choice. Please enter 1, 2, 3, 4, or 5.")


# ==============================
# START PROGRAM
# ==============================

if __name__ == "__main__":
    main()