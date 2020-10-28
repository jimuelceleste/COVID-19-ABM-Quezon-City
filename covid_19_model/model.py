# model.py
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from covid_19_model.agents import PersonAgent
from covid_19_model.space import QuezonCity
from covid_19_model.data_collectors import *

class Covid19Model(Model):
    """Covid19 Agent-Based Model"""

    def __init__(self, model_parameters, space_parameters):
        """Initializes the model"""
        # Gets model parameters from model_parameters
        self.SEIR = model_parameters["SEIR"]

        # Instantiates the space/grid
        self.grid = QuezonCity(
            width = space_parameters["width"],
            height = space_parameters["height"],
            torus = space_parameters["torus"])

        # Instantiates a RandomActivation scheduler
        self.schedule = RandomActivation(self)

        # Sets the stopping condition for the model run
        self.running = True

        # Instantiates PersonAgents
        self.instantiate_agents()

        # Instantiates data collectors
        self.data_collector_1 = self.instantiate_data_collector(district = "district1")
        self.data_collector_2 = self.instantiate_data_collector(district = "district2")
        self.data_collector_3 = self.instantiate_data_collector(district = "district3")
        self.data_collector_4 = self.instantiate_data_collector(district = "district4")
        self.data_collector_5 = self.instantiate_data_collector(district = "district5")
        self.data_collector_6 = self.instantiate_data_collector(district = "district6")

    def instantiate_data_collector(self, district):
        """
        Returns six instances of the DataCollector class
        for the six districts of Quezon City.
        """
        return DataCollector(
            model_reporters = {
                "S": get_susceptible_function(district),
                "E": get_exposed_function(district),
                "I": get_infected_function(district),
                "R": get_removed_function(district)
            })

    def instantiate_agents(self):
        """Instantiate agents"""
        # Sets the starting agent id number
        id_start = 0

        for district in self.SEIR:
            # Gets the S, E, I, R counts to be instantiated
            SEIR = S, E, I, R = self.get_SEIR(district)
            id_end = id_start + sum(SEIR)

            for id in range(id_start, id_end):
                # Instantiates a PersonAgent
                agent = PersonAgent(
                    unique_id = id,
                    district = district,
                    model = self)

                # Sets agent type
                if id < S + id_start: pass
                elif id < S + E + id_start: agent.expose()
                elif id < S + E + I + id_start: agent.infect()
                elif id < S + E + I + R + id_start: agent.remove()

                # Adds agent to the space
                pos = self.grid.random_pos(district = district)
                self.grid.place_agent(agent, pos)

                # Adds agent to the scheduler
                self.schedule.add(agent)

            # Computes the next id_start
            id_start = id_end

    def step(self):
        """Advances the model by one step"""
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

    def get_SEIR(self, district):
        """Returns the SEIR value of the given district."""
        return [
            self.SEIR[district]["S"],
            self.SEIR[district]["E"],
            self.SEIR[district]["I"],
            self.SEIR[district]["R"]]