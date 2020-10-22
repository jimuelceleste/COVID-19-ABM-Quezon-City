# visualization.py

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule

def agent_portrayal(agent):
    """Defines the portayal of an agent"""
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": 0.6
    }

    if agent.susceptible:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
    elif agent.exposed:
        portrayal["Color"] = "orange"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.5
    elif agent.infected:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.4
    elif agent.removed:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 3
        portrayal["r"] = 0.3

    return portrayal

canvas_grid = CanvasGrid(
    portrayal_method = agent_portrayal,
    grid_width = 20,
    grid_height = 20,
    canvas_width = 300,
    canvas_height = 300
    )

chart_module = ChartModule(
    series = [
        {"Label": "S", "Color": "Green"},
        {"Label": "E", "Color": "Yellow"},
        {"Label": "I", "Color": "Red"},
        {"Label": "R", "Color": "Grey"}
    ],
    canvas_width = 300,
    canvas_height = 100,
    data_collector_name = 'datacollector'
    )