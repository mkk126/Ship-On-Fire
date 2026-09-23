import random

from fire import spreadFire


# Function that randomly places the bot, button, and initial fire in the ship.
def placeEntities(ship):
    openCells = []

    # Iterate through the ship to find all open cells.
    for row in range(len(ship)):
        for col in range(len(ship)):
            if ship[row][col]:
                openCells.append((row, col))

    # Bot, button, and initial fire must occupy different open cells.
    botPosition, buttonPosition, firePosition = random.sample(openCells, 3)

    #Fire cells are stored in a set 
    fireCells = {firePosition}

    return botPosition, buttonPosition, fireCells


# Function that runs a single time step of the simulation.
def runTimeStep(ship, bot, botPosition, buttonPosition, fireCells, q):
    # Step 1: Ask the bot where it wants to move.
    newBotPosition = bot.chooseMove(ship, botPosition, buttonPosition, fireCells)

    # If the bot cannot find a valid move/path, it fails.
    if newBotPosition is None:
        return botPosition, fireCells, "NO_VALID_PATH"

    # Step 2: Move the bot.
    botPosition = newBotPosition

    # Step 3: Check whether the bot reached the button.
    if botPosition == buttonPosition:
        return botPosition, fireCells, "SUCCESS"

    # Step 4: Advance the fire.
    fireCells = spreadFire(ship,fireCells,q)

    # Step 5: Check whether the bot is now on fire.
    if botPosition in fireCells:
        return botPosition, fireCells, "BURNED"

    return botPosition, fireCells, "CONTINUE"

# Function that runs the entire simulation until the bot either succeeds or fails.
def runSimulation(ship, bot, botPosition, buttonPosition, fireCells, q):
    timeSteps = 0
    # Run the simulation until the bot either succeeds or fails.
    while True:
        # Run a single time step of the simulation.
        botPosition, fireCells, status = runTimeStep(ship, bot, botPosition, buttonPosition, fireCells, q)

        # Increment the time step counter.
        timeSteps += 1

        # Check the status of the simulation after each time step.
        if status == "SUCCESS":
            return True, timeSteps, status

        if status == "NO_VALID_PATH" or status == "BURNED":
            return False, timeSteps, status