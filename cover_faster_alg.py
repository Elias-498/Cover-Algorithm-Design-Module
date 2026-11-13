# Aim:  Stop exploring combinations that cannot produce a better result

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

O = [2, 6, 11]
C = [4, 8, 14]
S = [3, 7, 12]
R = [2, 2, 1]

solution, count = cover_faster(O, C, S, R)


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