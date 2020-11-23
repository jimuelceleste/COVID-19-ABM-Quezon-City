# server.py
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from covid_19_model.visualization import *
from .input_generator.input_generator import generate_input_to_model

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
visualization_elements = [canvas_grid]
for i in range(1, 7):
    visualization_elements.append(labels["District " + str(i)])
    visualization_elements.append(charts["District " + str(i)])

# Model Parameters
model_params = {
    "model_params": generate_input_to_model(agent_person_ratio = 1000),
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