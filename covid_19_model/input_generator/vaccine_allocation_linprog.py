import numpy as np
import pandas as pd
import json

from scipy.optimize import linprog
from numpyencoder import NumpyEncoder

def vaccine_allocation_linprog(locations, doses, cases, age_population, mean_r0, available_vaccines):

    vaccine = np.empty(locations, dtype=int)
    obj_vaccine = np.empty(locations, dtype=int)

    vaccine.fill(doses)
    obj_vaccine.fill(1)

    vaccine = np.array([vaccine])

    susceptible = (age_population - cases)
    susceptible_population = susceptible.sum(axis=0)
    susceptible_percentage = susceptible/susceptible_population
    max_allowed_susceptible = susceptible.sum(axis=1)*(1-(mean_r0-1))
    available_vaccines = np.array([available_vaccines])

    lower_bound = np.empty(locations, dtype=int)
    lower_bound.fill(0)
    lower_bound

    vaccine_limit = list(map(lambda x, y:(x,y), lower_bound.tolist(),susceptible_population.tolist()[0]))

    opt = linprog(c=obj_vaccine,
              A_ub=susceptible_percentage,
              b_ub=max_allowed_susceptible,
              A_eq=vaccine,
              b_eq=available_vaccines,
              bounds=vaccine_limit)

    return json.dumps({
        'age_population': age_population,
        'susceptible_percentage': susceptible_percentage,
        'max_allowed_susceptible': max_allowed_susceptible,
        'available_vaccines': available_vaccines,
        'vaccine_limit': vaccine_limit,
        'optimal_allocation': opt.x,
        'optimal_allocation_per_age': susceptible_percentage * opt.x[0],
        'susceptible': susceptible
    },cls=NumpyEncoder)


def generate_vaccinated():
    # 6 Districts of Quezon City
    locations = 6

    # Vaccine Doses
    doses = 2

    # Age Distribution for each District
    age_population = np.matrix([
        [ 72429., 121926.,  57472.,  78972.,  94846.,  94102.],
        [ 77266., 130067.,  61310.,  84245., 101180., 100385.],
        [ 83279., 140189.,  66081.,  90801., 109054., 108197.],
        [ 64710., 108931.,  51347.,  70555.,  84738.,  84073.],
        [ 49312.,  83012.,  39129.,  53767.,  64575.,  64068.],
        [ 34796.,  58574.,  27610.,  37939.,  45565.,  45207.],
        [ 18025.,  30343.,  14303.,  19653.,  23604.,  23419.],
        [  6581.,  11079.,   5222.,   7176.,   8618.,   8551.],
        [  2760.,   4646.,   2190.,   3009.,   3614.,   3586.]])

    # COVID19 Cases - Age Distribution for each District
    cases = np.matrix([
        [ 51.,  48.,  56.,  80.,  80.,  51.],
        [114., 117.,  83., 150., 150.,  79.],
        [563., 477., 435., 504., 504., 476.],
        [451., 368., 391., 482., 482., 397.],
        [287., 249., 295., 283., 283., 275.],
        [251., 178., 192., 254., 254., 202.],
        [178., 121., 140., 160., 160., 136.],
        [ 70.,  59.,  55.,  78.,  78.,  48.],
        [ 40.,  19.,  35.,  24.,  24.,  26.]
    ])

    # Mean reproduction number for Quezon City
    mean_r0 = 1.0768713819839701

    # Available Vaccines to be distributed
    available_vaccines = 100000

    result = vaccine_allocation_linprog(locations, doses, cases, age_population, mean_r0, available_vaccines)
    result_json = json.loads(result)

    return result_json["optimal_allocation"]