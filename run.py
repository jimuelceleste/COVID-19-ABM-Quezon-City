# run.py

from mesa.visualization.ModularVisualization import ModularServer
from model import Covid19Model
from visualization import canvas_grid, chart_module

covid_19_model_parameters = {
    "model_parameters": {
        "susceptible": 100,
        "exposed": 0,
        "infected": 21,
        "removed": 0,
        "transmission_rate": 0.24,
        "infection_rate": 0.24,
        "removal_rate": 0.1
    },
    "space_parameters": {
        "width": 20,
        "height": 20,
        "torus": True
    }
}

server = ModularServer(
        model_cls = Covid19Model,
        visualization_elements = [canvas_grid, chart_module],
        name = "COVID19 Agent-Based Model",
        model_params = covid_19_model_parameters)

server.port = 8521
server.launch()
