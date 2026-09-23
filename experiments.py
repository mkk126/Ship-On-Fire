import time

from shipGeneration import generateShip
from simulation import placeEntities, runSimulation
from bots import bot1, bot2, bot3, bot4


# Experiment settings.
dimension = 100

qValues = [
    0.3,
    0.4,
    0.5,
    0.6,
    0.7,
    0.8,
]

numberOfTrials = 50


# Runs the experiment for all four bots over a range of q values.
def runExperiments(
    dimension,
    qValues,
    numberOfTrials
):

    #final list of summarized results
    results = []

    # Store each bot class so they can all be tested on the same environments.
    botClasses = [
        ("Bot 1", bot1.Bot1),
        ("Bot 2", bot2.Bot2),
        ("Bot 3", bot3.Bot3),
        ("Bot 4", bot4.Bot4)
    ]

    # Test each value of q.
    for q in qValues:

        #temp counter for each bot's results at this value of q
        botResults = {}

        for botName, botClass in botClasses:
            botResults[botName] = {
                "successes": 0,
                "burned": 0,
                "noValidPath": 0,
                "totalTimeSteps": 0
            }

        # Generate and test the requested number of environments.
        for trial in range(numberOfTrials):

            # Generate one environment shared by all four bots.
            print("Generating trial", trial + 1, "of", numberOfTrials, "for q =", q)

            ship = generateShip(dimension)

            print("Running trial", trial + 1, "of", numberOfTrials, "for q =", q)

            #place all entities in the ship, including the bot, button, and fire. this is the same for all bots in this trial.
            botPosition, buttonPosition, fireCells = placeEntities(ship)

            # Run all four bots
            for botName, botClass in botClasses:

                print("    Running", botName)
                # Create a new bot for this simulation.
                bot = botClass()

                # Give this bot its own copy of the initial fire cells.
                # so the randomized fire spread cannot modify the fire cells for the other bots.
                startingFireCells = set(fireCells)

                success, timeSteps, status = runSimulation(ship, bot, botPosition, buttonPosition, startingFireCells, q)

                # Record the result for the temporary counter.
                if success:
                    botResults[botName]["successes"] += 1

                elif status == "BURNED":
                    botResults[botName]["burned"] += 1

                elif status == "NO_VALID_PATH":
                    botResults[botName]["noValidPath"] += 1

                botResults[botName]["totalTimeSteps"] += timeSteps

        #All trials for this q are now finishd
        #Convert the counters into summary statistics
        for botName, botClass in botClasses:

            successes = botResults[botName]["successes"]
            burned = botResults[botName]["burned"]
            noValidPath = botResults[botName]["noValidPath"]

            # Calculate the rate of each possible result.
            successRate = successes / numberOfTrials
            burnRate = burned / numberOfTrials
            noValidPathRate = noValidPath / numberOfTrials

            averageTimeSteps = (
                botResults[botName]["totalTimeSteps"]
                / numberOfTrials
            )

            #Add the summary statistics for this bot and q value to the final results list.
            results.append({
                "bot": botName,
                "dimension": dimension,
                "q": q,
                "trials": numberOfTrials,

                "successes": successes,
                "successRate": successRate,

                "burned": burned,
                "burnRate": burnRate,

                "noValidPath": noValidPath,
                "noValidPathRate": noValidPathRate,

                "averageTimeSteps": averageTimeSteps
            })

    return results

# Saves the results of the experiments to a CSV file.
def saveResults(results):

    file = open("experimentResults.csv", "w")

    # Create the column headers.
    file.write(
        "q,"
        "Bot,"
        "Trials,"
        "Successes,"
        "Success Rate,"
        "Burned,"
        "Burn Rate,"
        "No Valid Path,"
        "No Valid Path Rate,"
        "Average Steps\n"
    )

    # Write each result as a new row.
    for result in results:

        file.write(
            f"{result['q']},"
            f"{result['bot']},"
            f"{result['trials']},"
            f"{result['successes']},"
            f"{result['successRate'] * 100:.1f}%,"
            f"{result['burned']},"
            f"{result['burnRate'] * 100:.1f}%,"
            f"{result['noValidPath']},"
            f"{result['noValidPathRate'] * 100:.1f}%,"
            f"{result['averageTimeSteps']:.2f}\n"
        )

    file.close()


# Record how long the entire experiment takes.
startTime = time.time()


#run the experiments
results = runExperiments(
    dimension,
    qValues,
    numberOfTrials
)

#save the results to a CSV file
saveResults(results)

#Record the end time of the experiments.
endTime = time.time()


# Print the results.
print()
print("EXPERIMENT RESULTS")
print("------------------")

for result in results:

    print(
        result["bot"],
        "| q =", result["q"],
        "| Success =",
        f"{result['successes']}/{result['trials']}",
        f"({result['successRate'] * 100:.1f}%)",
        "| Burned =",
        f"{result['burned']}/{result['trials']}",
        f"({result['burnRate'] * 100:.1f}%)",
        "| No Valid Path =",
        f"{result['noValidPath']}/{result['trials']}",
        f"({result['noValidPathRate'] * 100:.1f}%)",
        "| Average Steps =",
        round(result["averageTimeSteps"], 2)
    )


# Print the total runtime.
print()
print("Total Simulations:", len(qValues) * numberOfTrials * 4)
print("Total Runtime:", round(endTime - startTime, 2), "seconds")