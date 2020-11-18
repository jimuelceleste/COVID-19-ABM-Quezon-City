# agents.py
from mesa import Agent
import random

class PersonAgent(Agent):
    """An agent that represents a person."""
    def __init__(self, unique_id, model, district, state, age):
        """Initializes a PersonAgent"""
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.model = model
        self.district = district
        self.state = state
        self.age = age

    def coin_toss(self, ptrue):
        """Generates a random choice"""
        return random.uniform(0.0, 1.0) < ptrue

    def step(self):
        """Advances an agent by a step"""
        self.status()
        self.interact()
        self.move()

    def status(self):
        """Checks agent's status"""
        # Case: agent gets infected
        if self.state == "E" and self.coin_toss(self.model.SEIR[self.district]["incubation_rate"]):
            self.infect()
            self.model.remove_exposed(self.district)
            self.model.add_infected(self.district)
            self.model.update_summary(self.district, SEIR_var = "I", summary_var = "max_infected")
        # Case: agent gets removed
        elif self.state == "I" and self.coin_toss(self.model.SEIR[self.district]["removal_rate"]):
            self.remove()
            self.model.remove_infected(self.district)
            self.model.add_removed(self.district)
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)

    def interact(self):
        """Agent interacts with other agents within the district"""
        if self.state == "I":
            neighbors = self.get_neighbors()
            for agent in neighbors:
                # Case: agent exposes neighbor agent
                if agent.state == "S" and self.coin_toss(self.model.SEIR[self.district]["transmission_rate"]):
                    agent.expose()
                    agent.model.remove_susceptible(agent.district)
                    agent.model.add_exposed(agent.district)
                    self.model.update_summary(agent.district, SEIR_var = "E", summary_var = "max_exposed")

    def move(self):
        """Moves agent on a random cell"""
        if self.state != "R":
            possible_steps = self.get_neighborhood()
            random_position = self.random.choice(possible_steps)
            self.model.grid.move_agent(self, random_position)

    def get_neighborhood(self):
        """Returns agent's neighborhood"""
        return self.model.grid.get_neighborhood(
            pos = self.pos,
            moore = True,
            include_center = True)

    def get_neighbors(self):
        """Returns neighbors of agent within the district only"""
        return self.model.grid.get_neighbors(
            district = self.district,
            pos = self.pos,
            moore = True,
            include_center = True)

    def expose(self):
        """Exposes agent."""
        self.state = "E"

    def infect(self):
        """Infects agent."""
        self.state = "I"

    def remove(self):
        """Removes agent."""
        self.state = "R"