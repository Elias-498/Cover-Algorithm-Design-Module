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
