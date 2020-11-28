# server.py
from covid_19_model.visualization import *
from mesa_geo.visualization.ModularVisualization import ModularServer
from mesa_geo.visualization.MapModule import MapModule
from covid_19_model.space import QuezonCity
from mesa.visualization.UserParam import UserSettableParameter
import json

# Adds MapModule to visualization_elements
visualization_elements = [
    MapModule(
        portrayal_method = agent_portrayal,
        view = QuezonCity.MAP_COORDS,
        zoom = 12,
        map_height = 600,
        map_width = 600
    )
]

# Adds charts and summary to visualization_elements
for i in range(6):
    district = "District " + str(i + 1)
    district_number = i + 1
    visualization_elements.append(DistrictInformation(
        district_number = district_number))
    visualization_elements.append(SEIRChartModule(
        canvas_width = 300,
        canvas_height = 100,
        district_number = district_number))

# Model Description
model_desc = """An agent-based model that simulates COVID-19 transmission
in the six districts of Quezon City, Metro Manila, Philippines."""

# Model Parameters
model_params = {
    "model_params": json.load(open("input.json")),
    "model_desc": UserSettableParameter('static_text', value = model_desc),
    "transmission_rate": UserSettableParameter('slider', "Transmission Rate", 1, 0, 1, .0001),
    "incubation_rate": UserSettableParameter('slider', "Incubation Rate", 0.142857, 0, 1, .0001),
    "removal_rate": UserSettableParameter('slider', "Removal Rate", 0.33, 0, 1, .0001),
    # "age_strat": UserSettableParameter('checkbox', "Age-Stratification", False),
}

# Modular Server
server = ModularServer(
    model_cls = Covid19Model,
    visualization_elements = visualization_elements,
    name = "COVID-19 Agent-Based Model",
    model_params = model_params)

# Sets the server port
server.port = 8521