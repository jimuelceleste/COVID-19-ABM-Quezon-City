# visualization.py
from mesa.visualization.modules import ChartModule, TextElement
from covid_19_model.model import Covid19Model

def agent_portrayal(agent):
    """Defines the portayal of an agent"""
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": 0.6
        }

    if agent.state == "S":
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
    elif agent.state == "E":
        portrayal["Color"] = "orange"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.5
    elif agent.state == "I":
        portrayal["Color"] = "red"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.4
    elif agent.state == "R":
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 3
        portrayal["r"] = 0.3

    return portrayal

class SEIRChartModule(ChartModule):
    def __init__(self, canvas_width, canvas_height, district_number):
        data_collector = "data_collector_" + str(district_number)
        super().__init__(
            series = [
                {"Label": "S", "Color": "Green"},
                {"Label": "E", "Color": "Yellow"},
                {"Label": "I", "Color": "Red"},
                {"Label": "R", "Color": "Grey"}
            ],
            canvas_width = canvas_width,
            canvas_height = canvas_height,
            data_collector_name = "data_collector_" + str(district_number))

class DistrictInformation(TextElement):
    def __init__(self, district_number):
        super().__init__()
        self.district_number = district_number
        self.district = "district" + str(district_number)

    def render(self, model):
        max_exposed = model.summary[self.district]["max_exposed"]
        max_infected = model.summary[self.district]["max_infected"]
        return "District %i / Max Exposed: %i at t = %i / Max Infected: %i at t = %i" % (self.district_number, max_exposed[0], max_exposed[1], max_infected[0], max_infected[1])