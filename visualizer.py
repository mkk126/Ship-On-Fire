import tkinter as tk

from simulation import runTimeStep


def visualizeShip(ship, bot, botPosition, buttonPosition, fireCells, q):
    dimension = len(ship)

    # Create the application window.
    window = tk.Tk()
    window.title("Ship Visualizer")

    # Get the screen dimensions.
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()

    # Keep the visualizer at a good size.
    maxWindowSize = min(750, int(screenWidth * 0.8), int(screenHeight * 0.8))

    # Automatically scale cells to the ship dimension.
    cellSize = max(1, maxWindowSize // dimension)
    canvasSize = dimension * cellSize

    # Create the drawing area.
    canvas = tk.Canvas(window, width=canvasSize, height=canvasSize, background="black", highlightthickness=0)
    canvas.pack()

    # Store the parts of the simulation that change over time.
    simulationState = {"botPosition": botPosition, "fireCells": fireCells, "timeStep": 0, "status": "RUNNING"}

    # Display the current timestep.
    timeStepLabel = tk.Label(window,text="Time Step: 0")
    timeStepLabel.pack()

    # Display the current simulation status.
    statusLabel = tk.Label(window,text="Status: RUNNING")
    statusLabel.pack()

    # Advance the simulation by one complete timestep.
    def nextStep():

        # Do nothing if the simulation has already ended.
        if simulationState["status"] != "RUNNING":
            return

        # Ask the simulation to run one timestep and return the new state.
        newBotPosition, newFireCells, status = runTimeStep(ship, bot, simulationState["botPosition"], buttonPosition, simulationState["fireCells"], q)
        # Save the new simulation state.
        simulationState["botPosition"] = newBotPosition
        simulationState["fireCells"] = newFireCells
        simulationState["timeStep"] += 1

        # Convert CONTINUE into RUNNING for the display.
        if status == "CONTINUE":
            simulationState["status"] = "RUNNING"
        else:
            simulationState["status"] = status

        # Update the labels.
        timeStepLabel.config(
            text=f"Time Step: {simulationState['timeStep']}"
        )

        # Display a message based on the simulation status.
        if status == "CONTINUE":
            statusLabel.config(text="Status: RUNNING")

        elif status == "SUCCESS":
            statusLabel.config(text="Day is Saved, The Fire is Extinguished, and the Bot is a Hero")

        elif status == "NO_VALID_PATH":
            statusLabel.config(text="No Valid Move Found, The Fire Has Consumed All Hope Of Victory")

        elif status == "BURNED":
            statusLabel.config(text="Burnt Chicken Nugget")

        # Redraw the ship using the new state.
        drawShip(canvas, ship, simulationState["botPosition"], buttonPosition, simulationState["fireCells"], bot.path, cellSize)
        # Disable the button once the simulation is finished.
        if simulationState["status"] != "RUNNING":
            nextStepButton.config(state="disabled")

    # Create the Next Step button.
    nextStepButton = tk.Button(window, text="Next Step", command=nextStep)
    nextStepButton.pack(pady=5)

    # Draw the initial ship.
    drawShip(canvas, ship, simulationState["botPosition"], buttonPosition, simulationState["fireCells"], bot.path, cellSize)
    # Finish calculating the window size.
    window.update_idletasks()

    windowWidth = window.winfo_width()
    windowHeight = window.winfo_height()

    # Center the window.
    xPosition = (screenWidth - windowWidth) // 2
    yPosition = (screenHeight - windowHeight) // 2

    window.geometry(
        f"{windowWidth}x{windowHeight}+{xPosition}+{yPosition}"
    )

    # Keep the visualizer open.
    window.mainloop()


def drawShip(canvas, ship, botPosition, buttonPosition, fireCells, plannedPath, cellSize):
    dimension = len(ship)

    # Clear the previous drawing.
    canvas.delete("all")

    # Draw every cell.
    for row in range(dimension):
        for col in range(dimension):

            # Bot
            if (row, col) == botPosition:
                cellColor = "blue"
            # Fire
            elif (row, col) in fireCells:
                cellColor = "red"
            # Button
            elif (row, col) == buttonPosition:
                cellColor = "limegreen"

            # Bot's currently planned path
            elif plannedPath is not None and (row, col) in plannedPath:
                cellColor = "yellow"

            # Open cell
            elif ship[row][col]:
                cellColor = "lightblue"

            # Blocked cell
            else:
                cellColor = "gray"

            # Convert grid coordinates into canvas coordinates.
            x1 = col * cellSize
            y1 = row * cellSize
            x2 = x1 + cellSize
            y2 = y1 + cellSize

            # Draw the cell.
            canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=cellColor,
                outline="black",
                width=1
            )