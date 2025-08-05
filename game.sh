#!/bin/bash

# Initialize scores with player names
echo "==============================="
echo " CPU Scheduling Simulator Quiz Game "
echo "==============================="

read -p "Enter Player 1 Name: " player1
read -p "Enter Player 2 Name: " player2

declare -A scores
scores["$player1"]=0
scores["$player2"]=0

while true; do
    echo
    echo "==== Main Menu ===="
    echo "1. First Come First Serve"
    echo "2. Shortest Job First"
    echo "3. Longest Job First"
    echo "4. Round Robin"
    echo "5. Longest Remaining Time First"
    echo "6. Earliest Deadline First"
    echo "7. Exit"
    echo "===================="
    read -p "Choose an option (1-7): " choice

    if [[ "$choice" == "7" ]]; then
        echo "Game Over!"
        echo "Final Scores:"
        echo "$player1: ${scores["$player1"]}"
        echo "$player2: ${scores["$player2"]}"

        if (( ${scores["$player1"]} > ${scores["$player2"]} )); then
            echo "Winner: $player1 🎉"
        elif (( ${scores["$player1"]} < ${scores["$player2"]} )); then
            echo "Winner: $player2 🎉"
        else
            echo "It's a tie!"
        fi
        exit 0
    fi

    echo "=== Toss Time ==="
    toss_result=$((RANDOM % 2)) # 0 = head, 1 = tail

    # Player 1 choose
    while true; do
        read -p "$player1, choose head or tail: " p1_choice
        [[ "$p1_choice" == "head" || "$p1_choice" == "tail" ]] && break
        echo "Invalid input. Type 'head' or 'tail'."
    done

    # Player 2 choose
    while true; do
        read -p "$player2, choose head or tail: " p2_choice
        if [[ "$p2_choice" == "head" || "$p2_choice" == "tail" ]]; then
            [[ "$p2_choice" == "$p1_choice" ]] && echo "Both players chose same side. Choose different." || break
        else
            echo "Invalid input. Type 'head' or 'tail'."
        fi
    done

    toss_str=$([[ $toss_result -eq 0 ]] && echo "head" || echo "tail")
    echo "Toss Result: $toss_str"

    if [[ "$p1_choice" == "$toss_str" ]]; then
        toss_winner="$player1"
        toss_loser="$player2"
    else
        toss_winner="$player2"
        toss_loser="$player1"
    fi

    echo "$toss_winner wins the toss!"
    echo "Starting quiz for the chosen algorithm..."
    echo

    # 1️⃣ Quiz
    python3 quiz_game.py "$choice" "$toss_winner"
    quiz_score=0
    [[ -f quiz_score.txt ]] && quiz_score=$(cat quiz_score.txt)

    echo "Now Gantt Chart Puzzle..."
    # 2️⃣ Gantt Puzzle
    python3 gantt_puzzle.py "$choice" "$toss_winner"
    gantt_score=0
    [[ -f puzzle_score.txt ]] && gantt_score=$(cat puzzle_score.txt)

    total_score=$((quiz_score + gantt_score))
    echo "Round Finished! $toss_winner scored $total_score points this round."

    # ✅ Update score using player name
    scores["$toss_winner"]=$(( ${scores["$toss_winner"]} + total_score ))

    echo
    echo "Current Scores:"
    echo "$player1: ${scores["$player1"]} | $player2: ${scores["$player2"]}"
done
