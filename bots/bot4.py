import random
from collections import deque


class Bot4:

    #Bot 4 plans a path to the button at the very beginning of the simulation
    #and recalculates it around the fire every timestep
    #if the fire is nearby, it will move away from the fire while making as much
    #progress toward the button as possible. If no such move exists, it will follow the normal shortest path.

    # Initializes the bot's planned path to empty.
    def __init__(self):
        self.path = []

    # Chooses the bot's next move based on its current position,
    def chooseMove(self, ship, botPosition, buttonPosition, fireCells):

        # Find the normal shortest path to the button while avoiding
        # the current fire cells.
        self.path = self.findPath(ship, botPosition, buttonPosition, fireCells)

        # If no path was found, the bot cannot move.
        if self.path is None:
            return None

        # If the fire is nearby, look for a safer move that still
        # makes progress toward the button.
        if self.isFireNearby(botPosition, fireCells):

            panicMove = self.findPanicMove(ship, botPosition, buttonPosition, fireCells)

            # If a safer forward move exists, take it.
            if panicMove is not None:
                self.path = []
                return panicMove

        # Otherwise, follow the normal shortest path.
        return self.path.pop(0)


    # Checks whether any fire cell is within a Manhattan distance of 2.
    def isFireNearby(self, botPosition, fireCells):

        botRow, botCol = botPosition

        # Check the distance from the bot to every fire cell.
        for firePosition in fireCells:

            fireRow, fireCol = firePosition

            distance = abs(botRow - fireRow) + abs(botCol - fireCol)

            # Panic if any fire is within a distance of 2.
            if distance <= 2:
                return True

        return False


    # Finds a neighboring cell that moves the bot farther from the fire
    # while still making progress toward the button.
    def findPanicMove(self, ship, botPosition, buttonPosition, fireCells):

        row, col = botPosition

        # Find the bot's current shortest distance to the button.
        currentPath = self.findPath(ship, botPosition, buttonPosition, fireCells)

        # If there is no path to the button, there is no panic move.
        if currentPath is None:
            return None

        currentDistance = len(currentPath)

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

        # Store moves that still make progress toward the button.
        validMoves = []

        for neighbor in neighbors:

            neighborRow, neighborCol = neighbor

            # Ignore blocked cells.
            if ship[neighborRow][neighborCol] == False:
                continue

            # Ignore cells that are currently on fire.
            if neighbor in fireCells:
                continue

            # Find the shortest path from this neighboring cell
            # to the button.
            neighborPath = self.findPath(ship, neighbor, buttonPosition, fireCells)
            # Ignore moves that cannot still reach the button.
            if neighborPath is None:
                continue

            # Only consider moves that reduce the remaining distance
            # to the button.
            if len(neighborPath) >= currentDistance:
                continue

            validMoves.append(neighbor)

        # If there are no forward-moving panic choices,
        # use the normal shortest path instead.
        if len(validMoves) == 0:
            return None

        bestMoves = []
        bestDistance = -1

        # Of the forward-moving choices, find the moves that put
        # the bot farthest from the closest fire.
        for move in validMoves:

            moveRow, moveCol = move

            # Start the closest fire distance at a value larger than
            # any possible Manhattan distance in the ship.
            closestFireDistance = len(ship) * 2

            # Find the distance from this move to the closest fire.
            for firePosition in fireCells:

                fireRow, fireCol = firePosition

                distance = abs(moveRow - fireRow) + abs(moveCol - fireCol)

                if distance < closestFireDistance:
                    closestFireDistance = distance

            # If this move is safer than all previous moves,
            # make it the new best move.
            if closestFireDistance > bestDistance:
                bestDistance = closestFireDistance
                bestMoves = [move]

            # If this move is equally safe, also consider it.
            elif closestFireDistance == bestDistance:
                bestMoves.append(move)

        # Randomly choose between equally safe forward moves.
        return random.choice(bestMoves)


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