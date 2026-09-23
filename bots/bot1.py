from collections import deque

class Bot1:

    #Bot 1 plans a path to the button at the very beginning of the simulation
    #and follows it without any further alteration.

    #Initializes the bot's planned path to empty.
    def __init__(self):
        self.path = []

    #chooses the bot's next move
    def chooseMove(self,ship,botPosition,buttonPosition,fireCells):

        #Apparently necessary to avoid an error at the start when the bot has no planned path.
        if self.path is None:
            return None

        #if the bot has no planned path, it finds a new path to the button.
        #not strictly necessary to run each step, as this bot only chooses a path once
        #but this is decent structuring for future bots that need to replan their path each step.
        if len(self.path) == 0:
            self.path = self.findPath(ship,botPosition,buttonPosition,fireCells)

        # If no path was found, the bot cannot move.
        if self.path is None:
            return None

        # Move to the next cell in the path.
        return self.path.pop(0)

    #finds a path from the bot's current position to the button's position, avoiding fire and blocked cells.
    def findPath(self, ship, botPosition, buttonPosition, fireCells):
        # Start searching from the bot's position.
        # Originally this was a list.
        # A deque is faster for BFS since removing the first item does not shift every remaining item.
        queue = deque([botPosition])

        # Keep track of cells we have already found.
        # Originally this was a list.
        # A set is faster because it uses hash lookups i think
        visited = {botPosition}

        # Keep track of how we reached each cell.
        previous = {}

        #Keep running bfs until we find the button or run out of cells to search.
        while len(queue) > 0:
            #Take the first cell from the queue.
            #popleft is better than pop because it doesnt shift everything else
            currentPosition = queue.popleft()
            #Check if we have reached the button.
            if currentPosition == buttonPosition:
                #We found the button, so we create an empty list to start building the path from the bot to the button.
                path = []
                # Follow the previous cells back to the bot's position.
                while currentPosition != botPosition:
                    # Add the current cell to the path.
                    path.append(currentPosition)
                    # Move to the previous cell.
                    currentPosition = previous[currentPosition]
                # Reverse the path because we built it backwards from the button to the bot.
                path.reverse()
                return path

            row, col = currentPosition
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

            for neighbor in neighbors:

                row, col = neighbor

                # Ignore blocked cells.
                if ship[row][col] == False:
                    continue

                # Ignore fire.
                if neighbor in fireCells:
                    continue

                # Ignore cells we already found.
                if neighbor in visited:
                    continue

                # Remember how we reached this cell.
                previous[neighbor] = currentPosition

                # Mark the cell as visited.
                # Originally this used visited.append(neighbor). Sets use add() instead and make lookup faster.
                visited.add(neighbor)
                queue.append(neighbor)

        # No path to the button exists. Its joever.
        return None