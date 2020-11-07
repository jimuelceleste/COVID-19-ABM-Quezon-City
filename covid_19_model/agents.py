# agents.py
from mesa import Agent
import random

class PersonAgent(Agent):
    """An agent that represents a person."""

    def __init__(self, unique_id, model, district):
        """Initializes a PersonAgent"""
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.district = district
        self.model = model
        self.state = "S"
        self.susceptible = True
        self.exposed = False
        self.infected = False
        self.removed = False

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
        if self.exposed and self.coin_toss(self.model.SEIR[self.district]["incubation_rate"]):
            self.infect()
            self.model.remove_exposed(self.district)
            self.model.add_infected(self.district)
            self.model.update_summary(self.district, SEIR_var = "I", summary_var = "max_infected")
        # Case: agent gets removed
        elif self.infected and self.coin_toss(self.model.SEIR[self.district]["removal_rate"]):
            self.remove()
            self.model.schedule.remove(self)
            self.model.remove_infected(self.district)
            self.model.add_removed(self.district)

    def interact(self):
        """Agent interacts with other agents within the district"""
        if self.infected:
            neighbors = self.get_neighbors()
            for agent in neighbors:
                # Case: agent exposes neighbor agent
                if agent.susceptible and self.coin_toss(self.model.SEIR[self.district]["transmission_rate"]):
                    agent.expose()
                    agent.model.remove_susceptible(agent.district)
                    agent.model.add_exposed(agent.district)
                    self.model.update_summary(agent.district, SEIR_var = "E", summary_var = "max_exposed")

    def move(self):
        """Moves agent on a random cell"""
        if not self.removed:
            # Agent moves on a random possible position
            possible_steps = self.get_neighborhood()
            random_position = self.random.choice(possible_steps)
            self.model.grid.move_agent(self, random_position)

            # Case: agent moved on other districts
            new_district = self.model.grid.get_district_of(random_position)
            if new_district != self.district:
                # Updates SEIR values of previous and new district of agent
                self.model.SEIR[self.district][self.state] -= 1
                self.model.SEIR[new_district][self.state] += 1
                # Updates agent's district to the new district
                self.district = new_district

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
        """Makes agent exposed"""
        self.state = "E"
        self.susceptible = False
        self.exposed = True
        self.infected = False
        self.removed = False

    def infect(self):
        """Makes agent infected"""
        self.state = "I"
        self.susceptible = False
        self.exposed = False
        self.infected = True
        self.removed = False

    def remove(self):
        """Makes agent removed"""
        self.state = "R"
        self.susceptible = False
        self.exposed = False
        self.infected = False
        self.removed = True


