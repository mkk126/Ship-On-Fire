from shipGeneration import generateShip
from simulation import placeEntities
from visualizer import visualizeShip
from bots import bot1, bot2, bot3, bot4


#test settings
dimension = 100
q = 0.5
bottype = 4

# Generate a new environment for the simulation.
ship = generateShip(dimension)

# Place the bot, button, and fire cells in the ship.
botPosition, buttonPosition, fireCells = placeEntities(ship)

#Determine which bot to use based on the bottype variable.
if bottype == 1:
    bot = bot1.Bot1()
elif bottype == 2:
    bot = bot2.Bot2()
elif bottype == 3:
    bot = bot3.Bot3()
elif bottype == 4:
    bot = bot4.Bot4()

# Visualize the ship and the entities within it.
visualizeShip(ship,bot,botPosition,buttonPosition,fireCells,q)