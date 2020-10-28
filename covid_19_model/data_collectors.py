# data_collectors.py
"""
    Collection of functions that return configured data collector methods.
    Each of the data collectors return one of the four types of data: S, E, I, or R.
"""

def get_susceptible_function(district):
    def get_susceptible(model):
        """Returns the number of susceptible in a district."""
        return model.SEIR[district]["S"]
    return get_susceptible

def get_exposed_function(district):
    def get_exposed(model):
        """Returns the number of exposed in a district"""
        return model.SEIR[district]["E"]
    return get_exposed

def get_infected_function(district):
    def get_infected(model):
        """Returns the number of infected in a district"""
        return model.SEIR[district]["I"]
    return get_infected

def get_removed_function(district):
    def get_removed(model):
        """Returns the number of removed in a district"""
        return model.SEIR[district]["R"]
    return get_removed