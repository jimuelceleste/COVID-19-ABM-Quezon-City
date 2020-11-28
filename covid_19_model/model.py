# model.py
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from covid_19_model.agents import PersonAgent
from covid_19_model.space import QuezonCity
from covid_19_model.data_collectors import *
from shapely.geometry import Point
# from mesa_geo import AgentCreator
import random

class Covid19Model(Model):
    """Covid19 Agent-Based Model"""

    def __init__(
        self,
        model_params,
        transmission_rate = 0,
        incubation_rate = 0,
        removal_rate = 0,
        exposure_distance = 200,
        mobility_range = 100,
        age_strat = False,
    ):
        """Initializes the model"""
        # Sets parameters and initial SEIR values of the model
        self.SEIR = self.initialize_SEIR_values(model_params)
        self.transmission_rate = transmission_rate
        self.incubation_rate = incubation_rate
        self.removal_rate = removal_rate
        self.exposure_distance = exposure_distance
        self.mobility_range = mobility_range

        # Sets age stratification feature of the model
        self.age_strat = age_strat

        # Sets summary-related variables
        self.summary = self.initialize_summary()
        self.steps = 0

        # Instantiates a scheduler and a space for model
        self.schedule = RandomActivation(self)
        self.grid = QuezonCity(self)

        # Instantiates PersonAgents
        self.instantiate_person_agents(model_params["susceptible"], "S")
        self.instantiate_person_agents(model_params["exposed"], "E")
        self.instantiate_person_agents(model_params["infected"], "I")

        # Instantiates data collectors
        self.data_collector_1 = self.instantiate_data_collector(district = "district1")
        self.data_collector_2 = self.instantiate_data_collector(district = "district2")
        self.data_collector_3 = self.instantiate_data_collector(district = "district3")
        self.data_collector_4 = self.instantiate_data_collector(district = "district4")
        self.data_collector_5 = self.instantiate_data_collector(district = "district5")
        self.data_collector_6 = self.instantiate_data_collector(district = "district6")

        # Sets the running state of model to True
        self.running = True

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

    def instantiate_person_agents(self, population, state):
        """Instantiates PersonAgents"""
        for i, district_pop in enumerate(population):
            district = "district" + str(i + 1)

            for j in range(int(district_pop)):
                # Sets the unique_id for agent
                id = str(i) + str(j) + str(random.random())

                # Gets a random point for agent
                pos_x, pos_y = random_pos = self.grid.random_position(district)

                # Instantiates Agent
                agent = PersonAgent(
                    unique_id = id,
                    model = self,
                    shape = Point(pos_x, pos_y),
                    district = district,
                    state = state)

                # Adds agent to grid and scheduler
                self.grid.add_agents(agent)
                self.schedule.add(agent)

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
        self.grid._recreate_rtree()

    def get_SEIR(self, district):
        """Returns the SEIR value of the given district."""
        return [self.SEIR[district][state] for state in "SEIR"]

    def expose_one_agent(self, district):
        """Exposes one agent from model."""
        # Updates S, E values of given district
        self.SEIR[district]["S"] -= 1
        self.SEIR[district]["E"] += 1

        # Updates exposed summary
        if self.SEIR[district]["E"] > self.summary[district]["max_exposed"][0]:
            self.summary[district]["max_exposed"] = (self.SEIR[district]["E"], self.steps)

    def infect_one_agent(self, district):
        """Infects one agent from model."""
        # Updates E, I values of given district
        self.SEIR[district]["E"] -= 1
        self.SEIR[district]["I"] += 1

        # Updates infected summary
        if self.SEIR[district]["I"] > self.summary[district]["max_infected"][0]:
            self.summary[district]["max_infected"] = (self.SEIR[district]["I"], self.steps)

    def remove_one_agent(self, agent):
        """Removes one agent from model."""
        # Updates I, R values of given district
        self.SEIR[agent.district]["I"] -= 1
        self.SEIR[agent.district]["R"] += 1

        # Removes agent from grid and scheduler
        self.schedule.remove(agent)
        self.grid.remove_agent(agent)



