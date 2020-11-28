# visualization.py
from mesa.visualization.modules import ChartModule, TextElement
from covid_19_model.model import Covid19Model
from covid_19_model.agents import PersonAgent
from covid_19_model.space import DistrictAgent

def agent_portrayal(agent):
    """Portrayal method of agents"""
    portrayal = dict()

    if isinstance(agent, PersonAgent):
        portrayal["radius"] = "1"

        if agent.state == "S":
            portrayal["color"] = "Green"
        elif agent.state == "E":
            portrayal["color"] = "Orange"
        elif agent.state == "I":
            portrayal["color"] = "Red"
        elif agent.state == "R":
            portrayal["color"] = "Grey"

    elif isinstance(agent, DistrictAgent):
        portrayal["color"] = "Blue"

    return portrayal

class SEIRChartModule(ChartModule):
    """SEIR Chart"""
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
    """District Information"""
    def __init__(self, district_number):
        super().__init__()
        self.district_number = district_number
        self.district = "district" + str(district_number)

    def render(self, model):
        max_exposed, max_exposed_time = model.summary[self.district]["max_exposed"]
        max_infected, max_infected_time = model.summary[self.district]["max_infected"]
        params = (
            self.district_number,
            max_exposed,
            max_exposed_time,
            max_infected,
            max_infected_time,
        )
        return "District %i | max(E) = %i, t = %i | max(I) = %i, t = %i" % params