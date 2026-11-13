# Attempt to solve with backtracking
#O - orange tree positions
#C -  cacuts positions
#S - sprinkler positions
#R  - Sprinkler watering radii
# Goal: Water every orange tree and water the minimum possible number of cacti

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

# Testing with given example
O = [2, 8]
C = [4, 6]
S = [2, 4, 6, 8]
R = [0, 2, 2, 0]

solution, count = cover_basline(O, C, S, R)

if solution is None:
    print("No valid sprinkler selection.")
else:

    positions = []
    watered_oranges = []
    watered_cacti = []
    dry_cacti = []

    # selected sprinkler's positions
    for i in range(len(solution)):
        positions.append(S[solution[i]])

    # which orange trees are watered
    for i in range(len(O)):
        if is_watered(O[i], solution, S, R):
            watered_oranges.append(O[i])

    # which cacti are watered
    for i in range(len(C)):
        if is_watered(C[i], solution, S, R):
            watered_cacti.append(C[i])
        else:
            dry_cacti.append(C[i])

    print("The selected sprinklers are those at positions", positions)

    print("Number of orange trees watered=",len(watered_oranges), ".Orange trees watered positions", watered_oranges)
    print("Number of cacti watered =", count, ".Cacti watered positions", watered_cacti )
    print("Cacti not watered:", dry_cacti)