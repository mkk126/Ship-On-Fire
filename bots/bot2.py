from collections import deque

class Bot2:

    #Bot 2 plans a path to the button at the very beginning of the simulation
    #and recalculates it around the fire every timestep.

    # Initializes the bot's planned path to empty.
    def __init__(self):
        self.path = []

    # Chooses the bot's next move based on its current position,
    def chooseMove(self, ship, botPosition, buttonPosition, fireCells):

        #recalculates its path every timestep
        self.path = self.findPath(ship, botPosition, buttonPosition, fireCells)

        # If no path was found, the bot cannot move.
        if self.path is None:
            return None

        # Move to the next cell in the newly calculated path.
        return self.path.pop(0)

    #the exact same as bot1 but its actually allowed to use the new path.
    #finds a path from the bot's current position to the button's position, avoiding fire and blocked cells.
    def findPath(self, ship, botPosition, buttonPosition, fireCells):

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

                if neighbor in fireCells:
                    continue

                if neighbor in visited:
                    continue

                previous[neighbor] = currentPosition

                visited.add(neighbor)

                queue.append(neighbor)

        return None