# space.py
from mesa.space import MultiGrid
import random

class District:
    """A class that represents a district."""
    
    def __init__(self, name, x_min, x_max, y_min, y_max):
        """Initializes a District class."""
        self.name = name
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def __str__(self):
        """Returns the string representation of the district."""
        return self.name

    def get_bounds(self):
        """Returns the bounds of the district."""
        return (self.x_min, self.x_max, self.y_min, self.y_max)

    def inside_bounds(self, pos):
        """Checks if pos is inside the bounds of the district."""
        x, y = pos
        return (self.x_min <= x <= self.x_max) and (self.y_min <= y <= self.y_max)


class QuezonCity(MultiGrid):
    """A class that represents the space of Quezon City."""

    def __init__(self, width, height, torus):
        """Initializes QuezonCity class"""
        super().__init__(width, height, torus)
        self.districts = self.instantiate_districts()

    def get_district_of(self, pos):
        """Returns the district where the given position is located at."""
        if self.out_of_bounds(pos): return ""

        x, y = pos
        for district in self.districts:
            district = self.districts[district]
            if (district.x_min <= x <= district.x_max) and (district.y_min <= y <= district.y_max):
                return district.name

    def get_neighbors(self, district, pos, moore = False, include_center = False):
        """Returns the list of agent's neighbors in the district"""
        return [neighbor
            for neighbor in super().get_neighbors(
                pos = pos,
                moore = True,
                include_center = True)
            if neighbor.district == district]

    def inside_bounds(self, pos, district):
        """Checks if pos is inside the bounds of the given district."""
        return self.districts[district].inside_bounds(pos)

    def instantiate_districts(self):
        """Instantiates the six districts of Quezon City"""
        # Sets the locations on a 3 x 2 grid
        TOP = 0; MIDDLE = 1; BOTTOM = 2
        LEFT = 0; RIGHT = 1

        # Sets the position of the districts on the grid
        locations = {
            "district1": (BOTTOM, LEFT),
            "district2": (TOP, RIGHT),
            "district3": (MIDDLE, RIGHT),
            "district4": (BOTTOM, RIGHT),
            "district5": (TOP, LEFT),
            "district6": (MIDDLE, LEFT)
        }

        # Creates the districts dictionary
        districts = {}

        # Computes the width and height of one district
        w = self.width // 2
        h = self.height // 3

        # Instantiates District objects
        for district in locations:
            row, col = locations[district]
            x_min = w * col
            x_max = x_min + w - 1
            y_min = self.height - (h * (row + 1))
            y_max = y_min + h - 1
            districts[district] = District(district, x_min, x_max, y_min, y_max)
            print("Created District: %s; x = (%i, %i); y = (%i, %i)" % (district, x_min, x_max, y_min, y_max))

        return districts

    def random_pos(self, district):
        """Returns a random position inside the bounds of the given district."""
        x_min, x_max, y_min, y_max = self.districts[district].get_bounds()
        x = random.randint(x_min, x_max)
        y = random.randint(y_min, y_max)
        return (x, y)