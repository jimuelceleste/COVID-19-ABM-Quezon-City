# model.py

from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from covid_19_model.enum.immunity import Immunity
from covid_19_model.enum.state import State
from covid_19_model.agents import PersonAgent
from covid_19_model.space import QuezonCity
from covid_19_model.data_collectors import *
from covid_19_model.utils import coin_toss
from shapely.geometry import Point
import numpy as np
import random

class Covid19Model(Model):
    """
    Covid19 Agent-Based Model
    """

    def __init__(self, variable_params, fixed_params):
        """
        Initializes the model
        """
        # SEIR Values
        self.SEIR = self.initialize_SEIR_dictionary(variable_params)

        # Virus-Host Parameters
        self.transmission_rate = fixed_params["transmission_rate"]
        self.incubation_rate = fixed_params["incubation_rate"]
        self.removal_rate = fixed_params["removal_rate"]

        # Age-stratified infection expectation
        self.as_infection_expectation = fixed_params["as_infection_expectation"]

        # Income
        self.income = fixed_params["income"]

        # Behavioral- and disease-resistance factors
        self.wearing_mask_protection = fixed_params["wearing_mask_protection"]
        self.physical_distancing_protection = fixed_params["physical_distancing_protection"]

        # Quarantine age-restriction policy
        self.min_age_restriction = fixed_params["min_age_restriction"]
        self.max_age_restriction = fixed_params["max_age_restriction"]

        # Agent movement configuration
        self.agent_exposure_distance = fixed_params["agent_exposure_distance"]
        self.agent_mobility_range = fixed_params["agent_mobility_range"]

        # Instantiates scheduler and space for model
        self.schedule = RandomActivation(self)
        self.grid = QuezonCity(self)

        # Instantiates PersonAgents
        for compartment, state in (
            ("susceptible", State.SUSCEPTIBLE),
            ("exposed", State.EXPOSED),
            ("infected", State.INFECTED)
        ):
            self.instantiate_person_agents(
                variable_params[compartment],
                state,
                self.schedule,
                self.grid,
                fixed_params["wearing_mask_percentage"],
                fixed_params["physical_distancing_percentage"],
                fixed_params["with_low_immunity_percentage"],
                fixed_params["mobile_worker_percentage"])

        # Instantiates data collectors
        self.data_collector_1 = self.instantiate_data_collector("district1")
        self.data_collector_2 = self.instantiate_data_collector("district2")
        self.data_collector_3 = self.instantiate_data_collector("district3")
        self.data_collector_4 = self.instantiate_data_collector("district4")
        self.data_collector_5 = self.instantiate_data_collector("district5")
        self.data_collector_6 = self.instantiate_data_collector("district6")

        # Sets summary-related variables
        self.summary = self.initialize_summary_dictionary()
        self.steps = 0

        # Sets the running state of model to True
        self.running = True

    def initialize_SEIR_dictionary(self, model_params):
        """
        Initializes SEIR data holder
        """
        SEIR = {"total": {"S": 0, "E": 0, "I": 0, "R": 0}}

        for i in range(6):
            S = int(np.array(model_params['susceptible']).sum(axis=0)[i])
            E = int(np.array(model_params['exposed']).sum(axis=0)[i])
            I = int(np.array(model_params['infected']).sum(axis=0)[i])
            R = int(np.array(model_params['removed']).sum(axis=0)[i])

            SEIR["district" + str(i + 1)] = {"S": S, "E": E, "I": I, "R": R}

            SEIR["total"]["S"] += S
            SEIR["total"]["E"] += E
            SEIR["total"]["I"] += I
            SEIR["total"]["R"] += R

        return SEIR

    def initialize_summary_dictionary(self):
        """
        Initializes summary data holder
        """
        summary = {
            "total": {
                "max_infected": (self.SEIR["total"]["I"], 0),
                "max_exposed": (self.SEIR["total"]["E"], 0),
            }
        }

        for i in range(6):
            district = "district" + str(i + 1)
            summary[district] = {
                "max_infected": (self.SEIR[district]["I"], 0),
                "max_exposed": (self.SEIR[district]["E"], 0)
            }
        return summary

    def instantiate_data_collector(self, district):
        """
        Returns the datacollector for given district
        """
        return DataCollector(
            model_reporters = {
                "S": get_susceptible_function(district),
                "E": get_exposed_function(district),
                "I": get_infected_function(district),
                "R": get_removed_function(district)
            })

    def instantiate_person_agents(
        self,
        population,
        state,
        schedule,
        grid,
        wearing_mask_percentage,
        physical_distancing_percentage,
        with_low_immunity_percentage,
        mobile_worker_percentage,
    ):
        """
        Instantiates PersonAgents
        """
        # Nine age groups: 0-9, 10-19, ..., 80-89
        age_groups = [(i*10, i*10+9) for i in range(9)]

        for i, age_group_pop in enumerate(population):
            min_age, max_age = age_groups[i]

            for j, district_pop in enumerate(age_group_pop):
                district = "district" + str(j + 1)

                for k in range(district_pop):
                    # Agent's properties
                    id = str(i) + str(j) + str(k) + state
                    age = random.randint(min_age, max_age)
                    wearing_mask = coin_toss(wearing_mask_percentage)
                    physical_distancing = coin_toss(physical_distancing_percentage)
                    immunity = Immunity.LOW if coin_toss(with_low_immunity_percentage) else Immunity.HIGH
                    mobile_worker = coin_toss(mobile_worker_percentage) if 18 <= age <= 65 else False

                    # Generates a random point for agent's position
                    pos_x, pos_y = self.grid.random_position(district)
                    shape = Point(pos_x, pos_y)

                    # Instantiates Agent
                    agent = PersonAgent(
                        unique_id = id,
                        model = self,
                        shape = shape,
                        district = district,
                        state = state,
                        age = age,
                        wearing_mask = wearing_mask,
                        physical_distancing = physical_distancing,
                        immunity = immunity,
                        mobile_worker = mobile_worker)

                    # Adds agent to grid and scheduler
                    grid.add_agents(agent)
                    schedule.add(agent)

    def step(self):
        """
        Advances the model by one step
        """
        self.steps += 1
        self.data_collector_1.collect(self)
        self.data_collector_2.collect(self)
        self.data_collector_3.collect(self)
        self.data_collector_4.collect(self)
        self.data_collector_5.collect(self)
        self.data_collector_6.collect(self)
        self.schedule.step()
        self.grid._recreate_rtree()

    def get_compartment(self, district, compartment):
        return self.SEIR[district][compartment]

    def get_SEIR(self, district):
        """
        Returns the SEIR value of the given district
        """
        return [self.SEIR[district][compartment] for compartment in "SEIR"]

    def update_summary(self, district, max_state, state):
        """
        Updates summary variable
        """
        if self.SEIR[district][state] > self.summary[district][max_state][0]:
            self.summary[district][max_state] = (self.SEIR[district][state], self.steps)

    def as_infection_probability(self, district):
        """
        Age-stratified infection probability
        """
        return self.as_infection_expectation[district] * self.incubation_rate[district]

    def add_one(self, district, compartment):
        """
        Adds one to the compartment
        """
        self.SEIR[district][compartment] += 1
        self.SEIR["total"][compartment] += 1

    def remove_one(self, district, compartment):
        self.SEIR[district][compartment] -= 1
        self.SEIR["total"][compartment] -= 1

