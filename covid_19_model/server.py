# server.py
from mesa.visualization.ModularVisualization import ModularServer
from covid_19_model.visualization import *

abm_parameters = {
    "model_parameters": {
        "SEIR": {
            "district1": {
                "S": 100, "E": 0, "I": 10, "R": 0,
                "transmission_rate": 0.24,
                "infection_rate": 0.2,
                "removal_rate": 0.1
            },
            "district2": {
                "S": 70, "E": 0, "I": 10, "R": 0,
                "transmission_rate": 0.24,
                "infection_rate": 0.2,
                "removal_rate": 0.1
            },
            "district3": {
                "S": 100, "E": 0, "I": 10, "R": 0,
                "transmission_rate": 0.24,
                "infection_rate": 0.2,
                "removal_rate": 0.1
            },
            "district4": {
                "S": 70, "E": 0, "I": 10, "R": 0,
                "transmission_rate": 0.24,
                "infection_rate": 0.2,
                "removal_rate": 0.1
            },
            "district5": {
                "S": 100, "E": 0, "I": 10, "R": 0,
                "transmission_rate": 0.24,
                "infection_rate": 0.2,
                "removal_rate": 0.1
            },
            "district6": {
                "S": 70, "E": 0, "I": 10, "R": 0,
                "transmission_rate": 0.24,
                "infection_rate": 0.2,
                "removal_rate": 0.1
            }
        },
        "travel_rate": 1.0
    },
    "space_parameters": {
        "width": 20,
        "height": 30,
        "torus": True
    }
}

server = ModularServer(
        model_cls = Covid19Model,
        visualization_elements = [
            canvas_grid,
            chart_modules["district1"],
            chart_modules["district2"],
            chart_modules["district3"],
            chart_modules["district4"],
            chart_modules["district5"],
            chart_modules["district6"],
        ],
        name = "COVID19 Agent-Based Model",
        model_params = abm_parameters)

server.port = 8521
