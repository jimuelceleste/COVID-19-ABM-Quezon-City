# agents.py

from mesa import Agent
from model import *
import random

# Random output generator
def coin_flip(ptrue):
    test = random.uniform(0.0,1.0)
    if ptrue == 0:
        out = False
    elif test < ptrue:
        out = True
    else:
        out = False
    return out

class PersonAgent(Agent):
    """An agent that represents a person."""

    def __init__(self, unique_id, model):
        """Initializes Person Agent"""
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.model = model
        self.susceptible = True
        self.exposed = False
        self.infected = False
        self.removed = False
        print("Agent %s created." % (str(self.unique_id)))

    def step(self):
        """Advances an agent by a step"""
        # Case: agent is exposed; gets infected or not
        if self.exposed:
            if coin_flip(self.model.infection_rate):
                self.get_infected()
                self.model.add_infected()
        # Case: agent is infected; gets removed or infect others
        elif self.infected:
            if coin_flip(self.model.removal_rate):
                self.get_removed()
                self.model.add_removed()
            else:
                neighbors = self.get_neighbors()
                for agent in neighbors:
                    if agent.susceptible and coin_flip(self.model.transmission_rate):
                        agent.get_exposed()
                        self.model.add_exposed()
        self.move()

    def move(self):
        """Moves an agent on the space"""
        possible_steps = self.model.grid.get_neighborhood(
            pos=self.pos,
            moore=True,
            include_center=False)
        random_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, random_position)

    def get_neighbors(self):
        """Returns agent's neighbors"""
        return self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=True
        )

    def get_exposed(self):
        """Makes agent exposed"""
        self.susceptible = False
        self.exposed = True
        self.infected = False
        self.removed = False

    def get_infected(self):
        """Makes agent infected"""
        self.susceptible = False
        self.exposed = False
        self.infected = True
        self.removed = False

    def get_removed(self):
        """Makes agent removed"""
        self.susceptible = False
        self.exposed = False
        self.infected = False
        self.removed = True
