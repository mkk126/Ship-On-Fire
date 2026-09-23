import random


#Function randomly spreads fire to neighboring cells based on the probability.
def spreadFire(ship, fireCells, q):

    # Create a copy of the fireCells set to avoid modifying it while iterating.
    # modifying it is bad because it might cause the fire to spread to a cell that was just added in this iteration.
    newFireCells = set(fireCells)

    # Iterate through all cells in the ship.
    for row in range(len(ship)):
        for col in range(len(ship)):

            #trying out ignore if statements to see if it works better than nesting

            # Ignore blocked cells.
            if not ship[row][col]:
                continue

            # Ignore cells that are already burning.
            if (row, col) in fireCells:
                continue

            # Count the number of burning neighbors for the current cell.
            burningNeighbors = countBurningNeighbors(row,col,fireCells,len(ship))

            # If there are burning neighbors, calculate the probability of this cell catching fire.
            if burningNeighbors > 0:

                #q is the tweakable parameter that controls the probability of fire spreading. The more burning neighbors, the higher the probability.
                probability = 1 - (1 - q) ** burningNeighbors

                # Randomly determine if the cell catches fire based on the calculated probability.
                if random.random() < probability:
                    newFireCells.add((row, col))

    return newFireCells

    #counts the number of burning neighbors for a given cell.
def countBurningNeighbors(row, col, fireCells, dimension):

    count = 0
    #up
    if row > 0 and (row - 1, col) in fireCells:
        count += 1
    #down
    if row < dimension - 1 and (row + 1, col) in fireCells:
        count += 1
    #left
    if col > 0 and (row, col - 1) in fireCells:
        count += 1
    #right
    if col < dimension - 1 and (row, col + 1) in fireCells:
        count += 1

    return count