from collections import deque

class Bot3:

    #Bot 3 plans a path to the button at the very beginning of the simulation
    #and recalculates it around the fire AND its neighbours every timestep.
    #if no neighbours exist, it will recalculate around the fire only.

    # Initializes the bot's planned path to empty.
    def __init__(self):
        self.path = []

    def chooseMove(self, ship, botPosition, buttonPosition, fireCells):

        #Bot3 needs a set of danger cells to avoid, we can start with the actual fire.
        dangerCells = set(fireCells)

        # Find every cell directly next to a fire cell.
        for firePosition in fireCells:

            row, col = firePosition

            # Check the four neighboring cells.
            neighbors = []

            if row > 0:
                neighbors.append((row - 1, col))

            if row < len(ship) - 1:
                neighbors.append((row + 1, col))

            if col > 0:
                neighbors.append((row, col - 1))

            if col < len(ship) - 1:
                neighbors.append((row, col + 1))

            # Add each neighboring cell to the dangerous cells.
            for neighbor in neighbors:
                dangerCells.add(neighbor)

        # First try to find a path that avoids both fire and cells
        # directly next to fire.
        self.path = self.findPath(ship, botPosition, buttonPosition, dangerCells)

        # If no safer path exists, try again while only avoiding
        # the actual fire cells.
        if self.path is None: self.path = self.findPath(ship, botPosition, buttonPosition, fireCells)
        # If no path was found, the bot cannot move.
        if self.path is None:
            return None

        # Move to the next cell in the newly calculated path.
        return self.path.pop(0)

    #same as bot1.
    def findPath(self, ship, botPosition, buttonPosition, dangerCells):

        queue = deque([botPosition])

        visited = {botPosition}

        previous = {}

        while len(queue) > 0:

            currentPosition = queue.popleft()

            if currentPosition == buttonPosition:

                path = []

                while currentPosition != botPosition:

                    path.append(currentPosition)

                    currentPosition = previous[currentPosition]

                path.reverse()
                return path

            row, col = currentPosition

            neighbors = []

            if row > 0:
                neighbors.append((row - 1, col))

            if row < len(ship) - 1:
                neighbors.append((row + 1, col))

            if col > 0:
                neighbors.append((row, col - 1))

            if col < len(ship) - 1:
                neighbors.append((row, col + 1))

            for neighbor in neighbors:

                row, col = neighbor

                if ship[row][col] == False:
                    continue

                if neighbor in dangerCells:
                    continue

                if neighbor in visited:
                    continue

                previous[neighbor] = currentPosition

                visited.add(neighbor)

                queue.append(neighbor)

        return None