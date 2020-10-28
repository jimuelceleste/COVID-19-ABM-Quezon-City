# visualization.py

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from covid_19_model.model import Covid19Model

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

def instantiate_chart_module(number):
    data_collector = "data_collector_" + str(number)
    return ChartModule(
        series = [
            {"Label": "S", "Color": "Green"},
            {"Label": "E", "Color": "Yellow"},
            {"Label": "I", "Color": "Red"},
            {"Label": "R", "Color": "Grey"}
        ],
        canvas_width = 200,
        canvas_height = 50,
        data_collector_name = data_collector)

canvas_grid = CanvasGrid(
    portrayal_method = agent_portrayal,
    grid_width = 20,
    grid_height = 30,
    canvas_width = 400,
    canvas_height = 400)

chart_modules = {}
for i in range(6):
    chart_modules["district" + str(i+1)] = instantiate_chart_module(i+1)