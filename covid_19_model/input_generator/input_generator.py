# pipeline.py

"""
    IMPORTANT:
    Modify values of exposed, transmission_rate, incubation_rate, and removal_rate later.
"""

from .covid_data_extractor import generate_SEIR
from .vaccine_allocation_linprog import generate_vaccinated
import numpy as np

def generate_input_to_model(agent_person_ratio=1000):
    # Gets SEIR from COVID Data
    # By default, exposed = 0;
    SEIR = generate_SEIR()

    # Gets number of vaccinated according to Joma's work
    vaccinated = generate_vaccinated()

    # Recomputes removed and susceptible
    SEIR["removed"] = np.add(SEIR["removed"], vaccinated)
    SEIR["susceptible"] = np.subtract(SEIR["susceptible"], vaccinated)

    # Formats data to desired input format
    for key in SEIR:
        SEIR[key] = list(np.round(np.divide(SEIR[key], agent_person_ratio)))

    # Adds virus-host properties to the input
    SEIR["transmission_rate"] = 2.8
    SEIR["incubation_rate"] = 0.142857
    SEIR["removal_rate"] = 0.33

    return SEIR