# agents.py

from covid_19_model.enum.immunity import Immunity
from covid_19_model.enum.state import State
from covid_19_model.utils import coin_toss
from mesa_geo.geoagent import GeoAgent
from shapely.geometry import Point

class PersonAgent(GeoAgent):
    """
    PersonAgent represents a person.

    Properties:
        unique_id: Agent's unique identification string
        model: Model which the agent belongs to
        shape: Agent's shapely.geometry shape
        district: Agent's home district
        state: Agents current state: S, E, I, or R
        age: Agent's age
        wearing_mask: True if agent is wearing a mask; else, False
        physical_distancing: True if agent is observing physical distance; else, False
        immunity: Agent's immunity level
        mobile_worker: True if agent is a mobile worker; else, False
    """

    def __init__(
        self,
        unique_id,
        model,
        shape,
        district,
        state,
        age,
        wearing_mask,
        physical_distancing,
        immunity,
        mobile_worker,
    ):
        """
        Initializes PersonAgent
        """
        super().__init__(unique_id, model, shape)
        self.district = district
        self.state = state
        self.age = age
        self.wearing_mask = wearing_mask
        self.physical_distancing = physical_distancing
        self.immunity = immunity
        self.mobile_worker = mobile_worker
        self.days_infected = 0
        self.days_incubating = 0

    def step(self):
        """
        Advances agent by a step
        """
        self.status()
        self.interact()
        self.move()

    def status(self):
        """
        Checks agent's status
        """
        if self.state == State.EXPOSED:
            if coin_toss(self.model.as_infection_probability(self.district)):
                self.transition(
                    district = self.district,
                    prev_state = self.state,
                    next_state = State.INFECTED,
                    update_summary = True,
                    summary_key = "max_infected")

        elif self.state == State.INFECTED:
            # Case: Agent is removed
            if coin_toss(self.model.removal_rate[self.district]):
                self.transition(
                    district = self.district,
                    prev_state = self.state,
                    next_state = State.REMOVED)
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
                del self

    def interact(self):
        """
        Agent interacts with other agents
        """
        if self.state == State.INFECTED:
            neighbors = self.get_neighbors()
            for neighbor in neighbors:
                if (
                    isinstance(neighbor, PersonAgent)
                    and neighbor.state == State.SUSCEPTIBLE
                    and coin_toss(self.model.transmission_rate[self.district])
                ):
                    if (
                        neighbor.with_low_immunity()
                        and not (
                            neighbor.protected_by_wearing_mask()
                            or neighbor.protected_by_physical_distancing()
                        )
                    ):
                        neighbor.transition(
                            district = neighbor.district,
                            prev_state = neighbor.state,
                            next_state = State.EXPOSED,
                            update_summary = True,
                            summary_key = "max_exposed")

    def move(self):
        """
        Agent moves in a random position
        """
        if self.state != "R" and self.allowed_to_move():
            new_x = self.shape.x + self.random.randint(
                -self.mobility_range(),
                self.mobility_range())
            new_y = self.shape.y + self.random.randint(
                -self.mobility_range(),
                self.mobility_range())
            self.shape = Point(new_x, new_y)

    def allowed_to_move(self):
        """
        Checks if agent is allowed to go outside of residence
        """
        return self.model.min_age_restriction <= self.age <= self.model.max_age_restriction

    def get_neighbors(self):
        """
        Returns agents nearby (distance = self.model.agent_exposure_distance)
        """
        return self.model.grid.get_neighbors_within_distance(
            self,
            self.model.agent_exposure_distance)

    def mobility_range(self):
        if self.mobile_worker:
            return self.model.agent_mobility_range * 2
        return self.model.agent_mobility_range

    def protected_by_physical_distancing(self):
        """
        Checks if agent is protected by social distancing
        """
        if self.physical_distancing:
            return coin_toss(self.model.physical_distancing_protection)
        return False

    def protected_by_wearing_mask(self):
        if self.wearing_mask:
            return coin_toss(self.model.wearing_mask_protection)
        return False

    def set_state(self, state):
        """
        Set agent's state
        """
        self.state = state

    def transition(self, district, prev_state, next_state, update_summary = False, summary_key = ""):
        """
        Change's agent's state
        """
        self.set_state(next_state)
        self.model.add_one(district, next_state)
        self.model.remove_one(district, prev_state)

        if update_summary:
            self.model.update_summary(district, summary_key, next_state)
            self.model.update_summary("total", summary_key, next_state)

    def with_low_immunity(self):
        return self.immunity == Immunity.LOW and self.is_senior_citizen()

    def is_senior_citizen(self):
        return self.age >= 60