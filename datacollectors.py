# data_collectors.py

def get_susceptible(model):
    """Returns the number of susceptible from the model"""
    return model.susceptible

def get_exposed(model):
    """Returns the number of exposed from the model"""
    return model.exposed

def get_infected(model):
    """Returns the number of infected from the model"""
    return model.infected

def get_removed(model):
    """Returns the number of removed from the model"""
    return model.removed