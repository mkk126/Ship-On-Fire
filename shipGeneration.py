import random

#RULES FOR GENERATION
# - Start with a square grid of "Blocked" cells, and define orthognal cells as neighbours
# - Randomly choose a cell (excluding the border of the grid) and declare it an "open" cell
# - Iteratively, do the following
    # identify all currently blocked cells with open neighbours
    # of the cells with just one neighbour, pick one at random and open it
    # repeat until the conditions are impossible to satisfy
# identify all open cells with one open neighbour as "Dead Ends"
# Pick a random dead end, open one of its blocked neighbours and repeat until half or less remain.


def generateShip(dimension):

    #if the dimension is not an integer, raise an error
    if isinstance(dimension, int) == False:
        raise TypeError("Dimension must be an integer.")

    #If the dimension is less than 3 x 3, no "interior cells" exist, so we cannot generate a ship.
    if(dimension < 3):
        raise ValueError("Dimension must be at least 3.")
    

    # Start with every cell blocked.
    # False = blocked
    # True = open
    ship = [[False for col in range(dimension)] for row in range(dimension)]

    # Pick a random cell and open it.
    # -2 ensures that we don't pick a border cell.
    row = random.randint(1, dimension - 2)
    col = random.randint(1, dimension - 2)
    ship[row][col] = True

    # Grow the ship.
    while True:
        candidates = []
        # Find every blocked cell
        for row in range(dimension):
            for col in range(dimension):
                if ship[row][col] == False:
                    #Checks if its exactly 1 neighbour
                    if countOpenNeighbors(ship, row, col) == 1:
                        candidates.append((row, col))

        # If there are no candidates, ship growth is finished.
        if len(candidates) == 0:
            break

        # Randomly choose one candidate and open it.
        row, col = random.choice(candidates)
        ship[row][col] = True

    # Find all dead ends.
    deadEnds = []

    for row in range(dimension):
        for col in range(dimension):
            if ship[row][col]:
                #While previously this helped us discover cells with only one neighbour, now it helps us discover dead ends
                #Because dead ends are defined as cells with only one open neighbour, this is the same check as before.
                if countOpenNeighbors(ship, row, col) == 1:
                    deadEnds.append((row, col))

    # Set target number of dead ends at beginning to half the current number of dead ends.
    # Loop until target is met
    targetDeadEnds = len(deadEnds) // 2

    while len(deadEnds) > targetDeadEnds:

        # Pick a random dead end.
        row, col = random.choice(deadEnds)

        #Check each of the four neighbours and see if they are blocked. If they are, add them to the list of blocked neighbours.
        blockedNeighbors = []
        #Up
        if row > 0 and ship[row - 1][col] == False:
            blockedNeighbors.append((row - 1, col))
        #Down
        if row < dimension - 1 and ship[row + 1][col] == False:
            blockedNeighbors.append((row + 1, col))
        #Left
        if col > 0 and ship[row][col - 1] == False:
            blockedNeighbors.append((row, col - 1))
        #Right
        if col < dimension - 1 and ship[row][col + 1] == False:
            blockedNeighbors.append((row, col + 1))

        # Pick one blocked neighbor and open it.
        newRow, newCol = random.choice(blockedNeighbors)
        ship[newRow][newCol] = True

        # Recalculate the current dead ends.
        deadEnds = []

        for row in range(dimension):
            for col in range(dimension):
                if ship[row][col]:
                    if countOpenNeighbors(ship, row, col) == 1:
                        deadEnds.append((row, col))

    return ship

def countOpenNeighbors(ship, row, col):
    count = 0
    dimension = len(ship)

    # Up
    if row > 0 and ship[row - 1][col]:
        count += 1

    # Down
    if row < dimension - 1 and ship[row + 1][col]:
        count += 1

    # Left
    if col > 0 and ship[row][col - 1]:
        count += 1  

    # Right
    if col < dimension - 1 and ship[row][col + 1]:
        count += 1

    return count