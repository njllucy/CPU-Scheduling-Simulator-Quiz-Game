import sys, random

algo_choice = sys.argv[1]
player = sys.argv[2]

algorithms = {
    "1": "First Come First Serve",
    "2": "Shortest Job First",
    "3": "Longest Job First",
    "4": "Round Robin",
    "5": "Longest Remaining Time First",
    "6": "Earliest Deadline First"
}

algo_name = algorithms.get(algo_choice, "Unknown")
print(f"\n{player}, Algorithm: {algo_name}")

# Generate processes
n = 4
processes = [f"P{i+1}" for i in range(n)]
arrival = sorted([random.randint(0, 3) for _ in range(n)])
burst = [random.randint(1, 5) for _ in range(n)]
deadline = [arrival[i] + random.randint(4, 8) for i in range(n)]  # EDF only

print("Process\tArrival\tBurst" + ("\tDeadline" if algo_choice == "6" else ""))
for i in range(n):
    if algo_choice == "6":
        print(f"{processes[i]}\t{arrival[i]}\t{burst[i]}\t{deadline[i]}")
    else:
        print(f"{processes[i]}\t{arrival[i]}\t{burst[i]}")

# Data for simulation
time = 0
completed = [False]*n
remaining = burst[:]
completion_time = [0]*n
gantt_processes = []
gantt_times = []

if algo_choice == "1":  # FCFS
    order = sorted(range(n), key=lambda i: arrival[i])
    for i in order:
        time = max(time, arrival[i])
        gantt_processes.append(processes[i])
        time += burst[i]
        gantt_times.append(time)
        completion_time[i] = time

elif algo_choice == "2":  # SJF Non-preemptive
    completed_count = 0
    while completed_count < n:
        ready = [i for i in range(n) if arrival[i] <= time and not completed[i]]
        if not ready:
            time += 1
            continue
        idx = min(ready, key=lambda x: burst[x])
        time = max(time, arrival[idx])
        gantt_processes.append(processes[idx])
        time += burst[idx]
        gantt_times.append(time)
        completion_time[idx] = time
        completed[idx] = True
        completed_count += 1

elif algo_choice == "3":  # LJF Non-preemptive
    completed_count = 0
    while completed_count < n:
        ready = [i for i in range(n) if arrival[i] <= time and not completed[i]]
        if not ready:
            time += 1
            continue
        idx = max(ready, key=lambda x: burst[x])
        time = max(time, arrival[idx])
        gantt_processes.append(processes[idx])
        time += burst[idx]
        gantt_times.append(time)
        completion_time[idx] = time
        completed[idx] = True
        completed_count += 1

elif algo_choice == "4":  # Round Robin
    tq = 2
    print(f"Time Quantum: {tq}")
    queue = []
    time = 0
    completed_count = 0
    in_queue = [False]*n
    while completed_count < n:
        for i in range(n):
            if arrival[i] <= time and not completed[i] and not in_queue[i]:
                queue.append(i)
                in_queue[i] = True
        if not queue:
            time += 1
            continue
        idx = queue.pop(0)
        in_queue[idx] = False
        exec_time = min(tq, remaining[idx])
        time += exec_time
        remaining[idx] -= exec_time
        gantt_processes.append(processes[idx])
        gantt_times.append(time)
        if remaining[idx] == 0:
            completed[idx] = True
            completed_count += 1
            completion_time[idx] = time
        else:
            for i in range(n):
                if arrival[i] <= time and not completed[i] and not in_queue[i] and i != idx:
                    queue.append(i)
                    in_queue[i] = True
            queue.append(idx)
            in_queue[idx] = True

elif algo_choice == "5":  # LRTF Preemptive
    completed_count = 0
    while completed_count < n:
        ready = [i for i in range(n) if arrival[i] <= time and not completed[i]]
        if not ready:
            time += 1
            continue
        idx = max(ready, key=lambda x: remaining[x])
        remaining[idx] -= 1
        time += 1
        gantt_processes.append(processes[idx])
        gantt_times.append(time)
        if remaining[idx] == 0:
            completed[idx] = True
            completed_count += 1
            completion_time[idx] = time

elif algo_choice == "6":  # EDF Non-preemptive
    completed_count = 0
    while completed_count < n:
        ready = [i for i in range(n) if arrival[i] <= time and not completed[i]]
        if not ready:
            time += 1
            continue
        idx = min(ready, key=lambda x: deadline[x])
        time = max(time, arrival[idx])
        gantt_processes.append(processes[idx])
        time += burst[idx]
        gantt_times.append(time)
        completion_time[idx] = time
        completed[idx] = True
        completed_count += 1

# --- Prepare Puzzle ---
# choose some blank indices randomly for quiz
blank_indices = random.sample(range(len(gantt_times)), min(2, len(gantt_times)))

print("\nGantt Chart Timeline (fill the blanks):")
print("Process:", "  ".join(gantt_processes))
print("CT     :", end=" ")
for i, t in enumerate(gantt_times):
    if i in blank_indices:
        print("__", end="  ")
    else:
        print(t, end="  ")
print("\n")

score = 0
for idx in blank_indices:
    ans = input(f"Enter completion time for {gantt_processes[idx]}: ")
    if ans.isdigit() and int(ans) == gantt_times[idx]:
        print("Correct! +5 points")
        score += 5
    else:
        print(f"Wrong! Correct answer: {gantt_times[idx]}")

with open("puzzle_score.txt", "w") as f:
    f.write(str(score))
