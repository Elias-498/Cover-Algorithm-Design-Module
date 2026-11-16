# Aim:  Stop exploring combinations that cannot produce a better result

import time
import tracemalloc
# Check whether a position receives water
def is_watered(pos, selected, S, R):

    for i in range(len(selected)):
        j = selected[i]

        left = S[j] - R[j]
        right = S[j] + R[j]

        if left <= pos <= right:
            return True

    return False

def cover_faster(O, C, S, R):

    # sprinklers currently turned on
    selected = []

    def backtrack(i, best_selection, best_count):
        # cacti count
        cactus_count = 0
        for j in range(len(C)):
            if is_watered(C[j], selected, S, R):
                cactus_count += 1

        # If the current selection already waters more cacti than the best result, then adding sprinklers won't improve it
        if cactus_count >= best_count:
            return best_selection, best_count

        # check for if all oranges are watered
        all_watered = True
        for j in range(len(O)):
            if not is_watered(O[j], selected, S, R):
                all_watered = False
                break

        # all oranges are watered and current selection has smaller cacti count. no need to add more sprinklers
        if all_watered:
            new_selection = []
            for j in range(len(selected)):
                new_selection.append(selected[j])

            return new_selection, cactus_count

        # no sprinklers remaining
        if i == len(S):
            return best_selection, best_count

        # check the remaining sprinkler without selecting current sprinkler
        best_selection, best_count = backtrack(
            i + 1, best_selection, best_count)

        selected.append(i) # adding current sprinkler

        # check the remaining sprinkler while keeping current sprinkler on
        best_selection, best_count = backtrack(
            i + 1, best_selection, best_count)

        selected.pop()
        # best solution found so far
        return best_selection, best_count

    return backtrack(0, None, len(C) + 1)

def run_experiments(alg):
    # Experiment 1: Increase the number of sprinklers when every sprinkler is necessary (scalability and memory)
    print("Experiment 1")
    largest = 0  # largest number of sprinklers handled within limit
    for s in [4, 8, 12, 16, 18, 20, 22, 24]:
        O = []
        C = [3, 13]
        S = []
        R = []

        for i in range(s):
            O.append(i * 10)
            S.append(i * 10)
            R.append(0)

        # measuring execution time
        total_time = 0
        for i in range(5):  # 5 times to get an avg
            start = time.perf_counter()
            solution, count = alg(O, C, S, R)
            end = time.perf_counter()
            total_time += end - start

        # average execution time in ms
        average = (total_time / 5) * 1000

        # Measuring memory space
        tracemalloc.start()
        solution, count = alg(O, C, S, R)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        memory = peak / 1024  # KIb

        print("Sprinklers:", s, "| Average time:", round(average, 3), "ms", "| Memory:", round(memory, 3), "Kib")

        # Time limit for test = 1s/1000ms
        # Memory limit = 64Mib
        # Stop testing for larger inputs if either limits exceed
        if average > 1000 or memory > 64 * 1024:
            break

        largest = s
        print("Largest tested within limits:", largest)

    # Experiment 2: Adding unnecessary sprinklers (Performance for early stops)
    print("\nExperiment 2")
    for s in [4, 6, 8, 10, 12, 14]:
        O = [2, 8]
        C = [4, 6]
        S = [2, 4, 6, 8]
        R = [0, 2, 2, 0]

        # adding more sprinklers
        for i in range(4, s):
            if i % 2 == 0:
                S.append(4)
            else:
                S.append(6)
            R.append(2)

        total_time = 0
        for i in range(5):
            start = time.perf_counter()
            solution, count = alg(O, C, S, R)
            end = time.perf_counter()
            total_time += end - start

        average = (total_time / 5) * 1000
        print("Sprinklers:", s, "| Cacti watered:", count, "| Average time:", round(average, 3), "ms")

    # Experiment 3: increasing number of cacti (Comparing baseline and faster execution times)
    print("\nExperiment 3")

    for c in [2, 5, 10, 15, 20]:
        O = [2, 8]
        C = [4, 6]
        S = [2, 4, 6, 8]
        R = [0, 2, 2, 0]

        # adding more cacti
        for i in range(2, c):
            C.append(20 + i)

        total_time = 0
        for i in range(5):
            start = time.perf_counter()
            solution, count = alg(O, C, S, R)
            end = time.perf_counter()
            total_time += end - start

        average = (total_time / 5) * 1000
        print("Cacti:", c, "| Cacti watered:", count, "| Average time:", round(average, 3), "ms")


run_experiments(cover_faster)