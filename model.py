# model.py

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from agents import PersonAgent
from datacollectors import *

class Covid19Model(Model):
    """Covid19 Agent-Based Model"""

    def __init__(self, model_parameters, space_parameters):
        """Initializes the model"""
        # Gets model parameters from model_parameters
        self.susceptible = model_parameters["susceptible"]
        self.exposed = model_parameters["exposed"]
        self.infected = model_parameters["infected"]
        self.removed = model_parameters["removed"]
        self.transmission_rate = model_parameters["transmission_rate"]
        self.infection_rate = model_parameters["infection_rate"]
        self.removal_rate = model_parameters["removal_rate"]

        # Total population
        self.N = self.susceptible + self.exposed + self.infected + self.removed

        # Instantiates a MultiGrid space
        self.grid = MultiGrid(
            width = space_parameters["width"],
            height = space_parameters["height"],
            torus = space_parameters["torus"])

        # Instantiates a RandomActivation scheduler
        self.schedule = RandomActivation(self)

        # Sets the stopping condition of the model
        self.running = True

        # Instantiates PersonAgents
        for id in range(self.N):
            agent = PersonAgent(id, self)
            if id < self.susceptible: pass
            elif id < self.susceptible + self.exposed: agent.get_exposed()
            elif id < self.susceptible + self.exposed + self.infected: agent.get_infected()
            elif id < self.susceptible + self.exposed + self.infected + self.removed: agent.get_removed()

            # Adds agent to the space
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

            # Adds agent to the scheduler
            self.schedule.add(agent)

        # Instantiates data collector
        self.datacollector = DataCollector(
            model_reporters = {
                "S": get_susceptible,
                "E": get_exposed,
                "I": get_infected,
                "R": get_removed
            })

    def step(self):
        """Advances the model by one step"""
        self.datacollector.collect(self)
        self.schedule.step()

    def add_exposed(self):
        """Adds 1 to exposed and subtracts 1 from susceptible"""
        self.susceptible -= 1
        self.exposed += 1

    def add_infected(self):
        """Adds 1 to infected and subtracts 1 from exposed"""
        self.exposed -= 1
        self.infected += 1

    def add_removed(self):
        """Adds 1 to removed and subtracts 1 from infected"""
        self.infected -= 1
        self.removed += 1