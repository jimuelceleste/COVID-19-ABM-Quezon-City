# server.py
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from covid_19_model.visualization import *

# Constants
SPACE_WIDTH = 120
SPACE_HEIGHT = 120
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
CHART_WIDTH = 200
CHART_HEIGHT = 50

# Instantiates space + agent representation
canvas_grid = CanvasGrid(
    portrayal_method = agent_portrayal,
    grid_width = SPACE_WIDTH,
    grid_height = SPACE_HEIGHT,
    canvas_width = CANVAS_WIDTH,
    canvas_height = CANVAS_HEIGHT)

# Instantiates charts and labels per district
charts = {}
labels = {}
for i in range(6):
    district_number = str(i+1)
    district = "District " + district_number
    charts[district] = SEIRChartModule(CHART_WIDTH, CHART_HEIGHT, district_number)
    labels[district] = Text(district)

# Visualization Elements
visualization_elements = [
    canvas_grid,
    labels["District 1"],
    charts["District 1"],
    labels["District 2"],
    charts["District 2"],
    labels["District 3"],
    charts["District 3"],
    labels["District 4"],
    charts["District 4"],
    labels["District 5"],
    charts["District 5"],
    labels["District 6"],
    charts["District 6"],
]

# Model Parameters
model_params = {
    "model_parameters": {
        "SEIR": {
            "district1": {
                "S": 500, "E": 1, "I": 12, "R": 0,
                "transmission_rate": 3.2,
                "incubation_rate": 1/7,
                "removal_rate": 0.3
            },
            "district2": {
                "S": 500, "E": 1, "I": 1, "R": 0,
                "transmission_rate": 3.2,
                "incubation_rate": 1/7,
                "removal_rate": 0.3
            },
            "district3": {
                "S": 500, "E": 1, "I": 12, "R": 0,
                "transmission_rate": 3.2,
                "incubation_rate": 1/7,
                "removal_rate": 0.3
            },
            "district4": {
                "S": 500, "E": 1, "I": 12, "R": 0,
                "transmission_rate": 3.2,
                "incubation_rate": 1/7,
                "removal_rate": 0.3
            },
            "district5": {
                "S": 500, "E": 1, "I": 12, "R": 0,
                "transmission_rate": 3.2,
                "incubation_rate": 1/7,
                "removal_rate": 0.3
            },
            "district6": {
                "S": 500, "E": 1, "I": 12, "R": 0,
                "transmission_rate": 3.2,
                "incubation_rate": 1/7,
                "removal_rate": 0.3
            }
        }
    },
    "space_parameters": {
        "width": SPACE_WIDTH,
        "height": SPACE_HEIGHT,
        "torus": True
    }
}

# Modular Server
server = ModularServer(
        model_cls = Covid19Model,
        visualization_elements = visualization_elements,
        name = "COVID19 Agent-Based Model",
        model_params = model_params)

# Sets the server port
server.port = 8521