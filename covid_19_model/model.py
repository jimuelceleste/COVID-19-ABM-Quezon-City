# model.py
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from covid_19_model.agents import PersonAgent
from covid_19_model.space import QuezonCity
from covid_19_model.data_collectors import *
import random

class Covid19Model(Model):
    """Covid19 Agent-Based Model"""

    def __init__(self, model_params, space_params):
        """Initializes the model"""
        # Sets initial values for SEIR
        self.SEIR = self.initialize_SEIR_values(model_params)

        # Instantiate summary data holder
        self.summary = self.initialize_summary()
        self.steps = 0

        # Instantiates the space/grid
        self.grid = QuezonCity(
            width = space_params["width"],
            height = space_params["height"],
            torus = space_params["torus"])

        # Instantiates a RandomActivation scheduler
        self.schedule = RandomActivation(self)

        # Sets the stopping condition for the model run
        self.running = True

        # Instantiates PersonAgents
        self.instantiate_agents(model_params["susceptible"], "S")
        self.instantiate_agents(model_params["exposed"], "E")
        self.instantiate_agents(model_params["infected"], "I")

        # Instantiates data collectors
        self.data_collector_1 = self.instantiate_data_collector(district = "district1")
        self.data_collector_2 = self.instantiate_data_collector(district = "district2")
        self.data_collector_3 = self.instantiate_data_collector(district = "district3")
        self.data_collector_4 = self.instantiate_data_collector(district = "district4")
        self.data_collector_5 = self.instantiate_data_collector(district = "district5")
        self.data_collector_6 = self.instantiate_data_collector(district = "district6")

    def initialize_SEIR_values(self, model_params):
        """Sets initial values for SEIR"""
        SEIR = {}
        for i in range(6):
            district_num = i + 1
            district = "district" + str(district_num)
            SEIR[district] = {
                "S": model_params['susceptible'][i],
                "E": model_params['exposed'][i],
                "I": model_params['infected'][i],
                "R": model_params['removed'][i],
                "transmission_rate": model_params["transmission_rate"],
                "incubation_rate": model_params["incubation_rate"],
                "removal_rate": model_params["removal_rate"],
            }
        return SEIR

    def initialize_summary(self):
        """Initializes data for summary."""
        summary = {}
        for i in range(6):
            district = "district" + str(i + 1)
            summary[district] = {
                "max_infected": (self.SEIR[district]["I"], 0),
                "max_exposed": (self.SEIR[district]["E"], 0)
            }
        return summary

    def instantiate_data_collector(self, district):
        """Returns the datacollector for given district"""
        return DataCollector(
            model_reporters = {
                "S": get_susceptible_function(district),
                "E": get_exposed_function(district),
                "I": get_infected_function(district),
                "R": get_removed_function(district)
            })

    def instantiate_agents(self, population, state):
        """Instantiates PersonAgents"""
        for i, district_pop in enumerate(population):
            district = "district" + str(i + 1)

            for j in range(int(district_pop)):
                # Sets the unique_id for agent
                id = str(i) + str(j) + str(random.random())

                # Instantiates agent
                agent = PersonAgent(
                    unique_id = id,
                    district = district,
                    model = self,
                    state = state,
                    age = 0)

                # Adds agent to a random position in its district
                pos = self.grid.random_pos(district)
                self.grid.place_agent(agent, pos)

                # Adds agent to the scheduler
                self.schedule.add(agent)

    def update_summary(self, district, SEIR_var, summary_var):
        """Updates summary of values for a given district"""
        if self.SEIR[district][SEIR_var] > self.summary[district][summary_var][0]:
            self.summary[district][summary_var] = (self.SEIR[district][SEIR_var], self.steps)

    def step(self):
        """Advances the model by one step"""
        self.steps += 1
        self.data_collector_1.collect(self)
        self.data_collector_2.collect(self)
        self.data_collector_3.collect(self)
        self.data_collector_4.collect(self)
        self.data_collector_5.collect(self)
        self.data_collector_6.collect(self)
        self.schedule.step()

    def add_susceptible(self, district):
        """Adds 1 to the susceptible of the given district."""
        self.SEIR[district]["S"] += 1

    def add_exposed(self, district):
        """Adds 1 to the exposed of the given district."""
        self.SEIR[district]["E"] += 1

    def add_infected(self, district):
        """Adds 1 to the infected of the given district."""
        self.SEIR[district]["I"] += 1

    def add_removed(self, district):
        """Adds 1 to the removed of the given district."""
        self.SEIR[district]["R"] += 1

    def remove_susceptible(self, district):
        """Subtracts 1 to the susceptible of the given district."""
        self.SEIR[district]["S"] -= 1

    def remove_exposed(self, district):
        """Subtracts 1 to the exposed of the given district."""
        self.SEIR[district]["E"] -= 1

    def remove_infected(self, district):
        """Subtracts 1 to the infected of the given district."""
        self.SEIR[district]["I"] -= 1

    def remove_removed(self, district):
        """Subtracts 1 to the removed of the given district."""
        self.SEIR[district]["R"] -= 1

    def get_susceptible(self, district):
        """Returns the number of susceptible."""
        return self.SEIR[district]["S"]

    def get_exposed(self, district):
        """Returns the number of exposed."""
        return self.SEIR[district]["E"]

    def get_infected(self, district):
        """Returns the number of infected."""
        return self.SEIR[district]["I"]

    def get_removed(self, district):
        """Returns the number of removed."""
        return self.SEIR[district]["R"]

    def get_SEIR(self, district):
        """Returns the SEIR value of the given district."""
        return [
            self.SEIR[district]["S"],
            self.SEIR[district]["E"],
            self.SEIR[district]["I"],
            self.SEIR[district]["R"]]