# Attempt to solve with backtracking
#O - orange tree positions
#C -  cacuts positions
#S - sprinkler positions
#R  - Sprinkler watering radii
# Goal: Water every orange tree and water the minimum possible number of cacti

import time
import tracemalloc

# Checking to see whether a position is watered
def is_watered(pos, selected, S, R):
    for i in selected:
        left = S[i] - R[i]
        right = S[i] + R[i]
        # has received water
        if left <= pos <= right:
            return True

    return False

# Finding the optimal sprinkler's to select
def cover_basline(O, C, S, R):

    b_count = len(C) + 1
    b_selection = None # will store the  best selection of sprinkler's
    selected = []


    def backtrack(i):
        # base case: considering all sprinklers
        if i == len(S):
            # checking if all oranges have been watered
            for j in range(len(O)):
                # Not valid if all orange tree are not watered
                if not is_watered(O[j], selected, S, R):
                    return None, len(C) + 1

            # count for number of cactus watered
            cactus_count = 0
            for j in range(len(C)):
                if is_watered(C[j], selected, S, R):
                    cactus_count += 1

            best_selection = []
            for j in range(len(selected)):
                best_selection.append(selected[j])

            return best_selection, cactus_count

        # leaving current sprinkler off
        off_selection, off_count = backtrack(i + 1)


        # turn current sprinkler on
        selected.append(i)
        on_selection, on_count = backtrack(i + 1)
        selected.pop()

        # return the choice watering fewer cacti
        if on_count < off_count:
            return on_selection, on_count
        return off_selection, off_count

    return backtrack(0) # begin from the  first sprinkler

def run_experiments(alg):
    # Experiment 1: Increase the number of sprinklers when every sprinkler is necessary (scalability and memory)
    print("Experiment 1")
    largest = 0 # largest number of sprinklers handled within limit
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
        for i in range(5): # 5 times to get an avg
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

        memory = peak / 1024  # bytes to Kib

        print("Sprinklers:", s, "| Average time:", round(average, 3), "ms", "| Memory:", round(memory, 3), "KiB")

        # Time limit for test = 1s/1000ms
        # Memory limit = 64Mib
        # Stop testing for larger inputs if either limits exceeds
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


run_experiments(cover_basline)

