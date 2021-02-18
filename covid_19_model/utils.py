import random
import json

def coin_toss(ptrue):
    """
    Generates a pseudo-random choice
    """
    if ptrue == 0: return False
    return random.uniform(0.0, 1.0) <= ptrue

def parse_json(filename):
    content = None

    with open(filename) as file:
        content = json.load(file)

    return content

    # Use for virus-host parameter formatting
    # with open("virus_host_parameters.json") as infile:
    #     virus_host_parameters = json.load(infile)
    #     entries = ["transmission_rate", "incubation_rate", "removal_rate"]
    #     for entry in entries:
    #         for i, data in enumerate(virus_host_parameters[entry]):
    #             district = "district" + str(i+1)
    #             virus_host_parameters_temp[entry][district] = data