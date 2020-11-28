# agents.py
from mesa_geo.geoagent import GeoAgent
from shapely.geometry import Point
import random

class PersonAgent(GeoAgent):
    """An agent that represents a person.

    Properties:
        unique_id: Agent's unique identification.
        model: Model which the agent belongs to.
        shape: Agent's shapely.geometry shape.
        district: Agent's home district.
        state: Agents current state; one of S, E, I, or R.
    """

    def __init__(self, unique_id, model, shape, district, state):
        """Initializes a PersonAgent"""
        super().__init__(unique_id, model, shape)
        self.district = district
        self.state = state

    def step(self):
        """Advances an agent by a step"""
        self.status()
        self.interact()
        self.move()

    def coin_toss(self, ptrue):
        """Generates a random choice"""
        if ptrue == 0:
            return False
        return random.uniform(0.0, 1.0) <= ptrue

    def status(self):
        """Checks agent's status"""
        # Case: agent gets infected
        if self.state == "E" and self.coin_toss(self.model.incubation_rate):
            self.infect()

        # Case: agent gets removed
        elif self.state == "I" and self.coin_toss(self.model.removal_rate):
            self.remove()

    def interact(self):
        """Agent interacts with other agents"""
        if self.state == "I":
            neighbors = self.model.grid.get_neighbors_within_distance(self, self.model.exposure_distance)
            for neighbor in neighbors:
                # Case: neighbor gets exposed
                if (
                    isinstance(neighbor, PersonAgent)
                    and neighbor.state == "S"
                    and self.coin_toss(self.model.transmission_rate)
                ):
                    neighbor.expose()

    def move(self):
        """ Makes agent move to a random position.

        IMPORTANT: Update this method to limit only the movement
        of agents inside Quezon City.
        """
        if self.state != "R":
            new_x = self.shape.x + self.random.randint(-self.model.mobility_range, self.model.mobility_range)
            new_y = self.shape.y + self.random.randint(-self.model.mobility_range, self.model.mobility_range)
            self.shape = Point(new_x, new_y)

    def expose(self):
        """Exposes agent"""
        self.state = "E"
        self.model.expose_one_agent(self.district)

    def infect(self):
        """Infects agent"""
        self.state = "I"
        self.model.infect_one_agent(self.district)

    def remove(self):
        """Removes agent"""
        self.state = "R"
        self.model.remove_one_agent(self)