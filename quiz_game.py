import sys
import requests
import html
import random

algo_choice = sys.argv[1]
player = sys.argv[2]

# Map algorithm for display
algo_name = {
    "1": "FCFS",
    "2": "SJF",
    "3": "LJF",
    "4": "RR",
    "5": "LRTF",
    "6": "EDF"
}.get(algo_choice, "Unknown")

print(f"Fetching random quiz for {player} on {algo_name}...")

# Fetch 1 multiple choice question from Open Trivia DB
url = "https://opentdb.com/api.php?amount=1&type=multiple"
try:
    res = requests.get(url, timeout=5)
    data = res.json()
except:
    print("Failed to fetch quiz from API. Scoring 0 this round.")
    with open("quiz_score.txt", "w") as f:
        f.write("0\n")
    exit(0)

if data.get("response_code") != 0 or not data.get("results"):
    print("No quiz received from API. Scoring 0 this round.")
    with open("quiz_score.txt", "w") as f:
        f.write("0\n")
    exit(0)

question_data = data["results"][0]
question = html.unescape(question_data["question"])
correct_answer = html.unescape(question_data["correct_answer"])
incorrect_answers = [html.unescape(ans) for ans in question_data["incorrect_answers"]]

# Shuffle options
options = incorrect_answers + [correct_answer]
random.shuffle(options)

print(f"\nQuiz for {player} on {algo_name}:")
print(question)
for idx, option in enumerate(options, start=1):
    print(f"{idx}. {option}")

try:
    ans = int(input("Enter option number: ").strip())
except:
    ans = 0

chosen_answer = options[ans-1] if 1 <= ans <= len(options) else ""

if chosen_answer == correct_answer:
    print("Correct!")
    score = 5
else:
    print(f"Wrong! Correct was: {correct_answer}")
    score = 0

# Save score to file for main game to read
with open("quiz_score.txt", "w") as f:
    f.write(f"{score}\n")
