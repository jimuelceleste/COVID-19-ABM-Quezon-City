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
    district_number = i+1
    district = "District " + str(district_number)
    charts[district] = SEIRChartModule(CHART_WIDTH, CHART_HEIGHT, district_number)
    labels[district] = DistrictInformation(district_number)

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
    "model_params": {
        "susceptible": [[40]*6]*9,
        "exposed": [[1]*6]*9,
        "infected": [
            [1,   5,  3,  1,   4,  2],   # 0-9
            [9,  15, 13, 14,  17,  9],   # 10-19
            [21, 23, 32, 15,  34, 12],   # 20-29
            [35, 45, 73, 41,  59, 32],   # 30-39
            [49, 35, 83, 91, 106, 98],   # 40-49
            [57, 65, 74, 74,  83, 82],   # 50-59
            [31, 18, 53, 57,  50, 49],   # 60-69
            [21, 12, 42, 21,  34, 41],   # 70-79
            [14,  3, 17, 13,  11, 10],   # 80+
        ],
        "removed": [[10]*6]*9,
        "transmission_rate": [0.50]*6,
        "incubation_rate": [1/7]*6,
        "removal_rate": [0.3]*6
    },
    "space_params": {
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