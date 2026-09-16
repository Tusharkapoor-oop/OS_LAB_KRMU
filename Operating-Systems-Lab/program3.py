processes = [
    {"pid": "P1", "arrival": 0, "burst": 7, "priority": 3},
    {"pid": "P2", "arrival": 2, "burst": 4, "priority": 1},
    {"pid": "P3", "arrival": 4, "burst": 1, "priority": 4},
    {"pid": "P4", "arrival": 5, "burst": 4, "priority": 2},
]

def priority_scheduling(process_list):
    remaining = process_list.copy()
    current_time = 0
    intervals = []
    while remaining:
        ready = [p for p in remaining if p["arrival"] <= current_time]
        if not ready:
            next_arrival = min(p["arrival"] for p in remaining)
            intervals.append(("IDLE", current_time, next_arrival))
            current_time = next_arrival
            continue
        process = min(
            ready,
            key=lambda p: (p["priority"], p["arrival"], p["pid"])
        )
        start = current_time
        end = start + process["burst"]
        intervals.append((process["pid"], start, end))
        current_time = end
        remaining.remove(process)
    return intervals

def round_robin(process_list, quantum=3):
    remaining = [dict(p) for p in process_list]
    for p in remaining:
        p["remaining"] = p["burst"]
    current_time = 0
    intervals = []
    queue = []
    arrived = []
    while remaining or queue:
        for p in remaining:
            if p["arrival"] <= current_time and p not in arrived and p not in queue:
                queue.append(p)
        if not queue:
            next_arrival = min(p["arrival"] for p in remaining if p not in arrived)
            intervals.append(("IDLE", current_time, next_arrival))
            current_time = next_arrival
            continue
        process = queue.pop(0)
        if process not in arrived:
            arrived.append(process)
        start = current_time
        run_time = min(quantum, process["remaining"])
        end = start + run_time
        intervals.append((process["pid"], start, end))
        current_time = end
        process["remaining"] -= run_time
        for p in remaining:
            if p["arrival"] <= current_time and p not in arrived and p not in queue and p is not process:
                queue.append(p)
        if process["remaining"] > 0:
            queue.append(process)
        else:
            remaining.remove(process)
    return intervals

def show_result(title, intervals):
    print("\n" + title)
    print("Process   Start   End")
    sequence = []
    for pid, start, end in intervals:
        print(f"{pid:<9} {start:<7} {end}")
        if pid != "IDLE":
            sequence.append(pid)
    print("Sequence:", " -> ".join(sequence))

print("INPUT PROCESSES")
print("PID   AT   BT   PRIORITY")
for p in processes:
    print(f'{p["pid"]:<5} {p["arrival"]:<4} {p["burst"]:<4} {p["priority"]}')

show_result("PRIORITY SCHEDULING (non-preemptive)", priority_scheduling(processes))
show_result("ROUND ROBIN (quantum=3)", round_robin(processes, quantum=3))
