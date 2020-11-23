# covid_data_extractor_qc.py

"""
    Credits to Jose Marie Minoza for providing the basis for these useful functions.
    We refactored Joma's code to fit with our needs but their core functionalities remain.
    Thank you, Joma!
"""

import pandas as pd

# Quezon City Districts
quezon_city_districts = ['District %i'%(i+1) for i in range(6)]

# PSGC codes of barangays per district
district_1_psgc = ['PH%i'%(psgc_code) for psgc_code in [
        137404001, 137404009, 137404012, 137404013, 137404018, 137404026, 137404027,
        137404029, 137404042, 137404049, 137404054, 137404056, 137404058, 137404061,
        137404064, 137404065, 137404069, 137404073, 137404076, 137404078, 137404081,
        137404084, 137404089, 137404093, 137404094, 137404096, 137404099, 137404100,
        137404104, 137404107, 137404118, 137404129, 137404130, 137404133
        ]
    ]
district_2_psgc = ['PH%i'%(psgc_code) for psgc_code in [
        137404010, 137404022, 137404138, 137404139, 137404140
        ]
    ]
district_3_psgc = ['PH%i'%(psgc_code) for psgc_code in [
        137404002, 137404007, 137404011, 137404014, 137404015, 137404016, 137404019,
        137404021, 137404030, 137404034, 137404035, 137404036, 137404037, 137404038,
        137404039, 137404040, 137404053, 137404055, 137404059, 137404062, 137404063,
        137404066, 137404067, 137404077, 137404085, 137404086, 137404087, 137404088,
        137404102, 137404114, 137404115, 137404117, 137404126, 137404131, 137404132,
        137404134
        ]
    ]
district_4_psgc = ['PH%i'%(psgc_code) for psgc_code in [
        137404006, 137404041, 137404043, 137404046, 137404068, 137404070, 137404079,
        137404095, 137404097, 137404136, 137404141, 137404142
        ]
    ]
district_5_psgc = ['PH%i'%(psgc_code) for psgc_code in [
        137404006, 137404041, 137404043, 137404046, 137404068, 137404070, 137404079,
        137404095, 137404097, 137404136, 137404141, 137404142
        ]
    ]
district_6_psgc = ['PH%i'%(psgc_code) for psgc_code in [
        137404003, 137404005, 137404023, 137404025, 137404080, 137404111, 137404119,
        137404120, 137404127, 137404135, 137404137
        ]
    ]
quezon_city_psgc_codes = [
    district_1_psgc,
    district_2_psgc,
    district_3_psgc,
    district_4_psgc,
    district_5_psgc,
    district_6_psgc,
    ]

# Quezon City Population
quezon_city_population = [
    404571,     # District 1
    743136,     # District 2
    341765,     # District 3
    463522,     # District 4
    585469,     # District 5
    577457,     # District 6
    ]

def data_extract_per_bgry(data, psgc_codes):
    # Filtering by CityMunRes column
    df = data[data["BarangayPSGC"].isin(psgc_codes)]

    # Checking if the df exists
    if not df.empty:
        # Case Incidence Data
        I_df = df['DateResultRelease'].dt.floor('d').value_counts().rename_axis('Date').reset_index(name='Case Incidence')
        I_df.sort_values(by='Date', inplace=True)
        I_df.set_index('Date', inplace=True)

        # Recovered Data
        R_df = df['DateRecover'].dt.floor('d').value_counts().rename_axis('Date').reset_index(name='Reported Recovered')
        R_df.sort_values(by='Date', inplace=True)
        R_df.set_index('Date', inplace=True)

        # Deaths Data
        D_df = df['DateDied'].dt.floor('d').value_counts().rename_axis('Date').reset_index(name='Reported Died')
        D_df.sort_values(by='Date', inplace= True)
        D_df.set_index('Date', inplace=True)

        # Merging of Data
        IRD_df = pd.concat([I_df, R_df, D_df], axis=1, sort=False)
        IRD_df.fillna(0, inplace=True)

        # Calculation of Removed
        IRD_df['Removed'] = IRD_df.apply(lambda row: (row['Reported Recovered'] + row['Reported Died']) if (row['Reported Recovered'] + row['Reported Died']) < row['Case Incidence'] else row['Reported Recovered'], axis=1)
        IRD_df["Active Cases"] = IRD_df[['Case Incidence']].values.cumsum() - IRD_df[['Removed']].values.cumsum()

        return IRD_df

def generate_SEIR():
    """Generates SIR data from COVID 19 Data from DOH"""
    # Opens input file
    source = "covid_19_model/input_generator/res/COVID-Data.csv"
    df = pd.read_csv(source, index_col=0)

    # Gets desired columns
    cases_df = df[['Age','AgeGroup','Sex','DateResultRelease','DateRecover','DateDied', 'RegionRes', 'ProvRes', 'CityMunRes','BarangayPSGC']]
    cases_df['DateResultRelease'] = pd.to_datetime(cases_df['DateResultRelease'])
    cases_df['DateRecover'] = pd.to_datetime(cases_df['DateRecover'])
    cases_df['DateDied'] = pd.to_datetime(cases_df['DateDied'])

    # Initializes a Pandas DataFrame data
    data = pd.DataFrame({
        "Quezon City Districts": quezon_city_districts,
        "PSGC Codes": quezon_city_psgc_codes,
        "Population": quezon_city_population,
        })

    # Gets number of Susceptible, Infected, and Removed
    for index, row in data.iterrows():
        city_df = data_extract_per_bgry(cases_df, row['PSGC Codes'])
        data.at[index, 'Susceptible'] = row['Population'] - (city_df['Active Cases'][city_df.index[-1]] + city_df['Removed'][city_df.index[-1]])
        data.at[index, 'Infected'] = city_df['Active Cases'][city_df.index[-1]]
        data.at[index, 'Removed'] = city_df['Removed'][city_df.index[-1]]

    result = {
        "susceptible": list(data['Susceptible']),
        "exposed": [0]*6,
        "infected": list(data['Infected']),
        "removed": list(data['Removed'])
        }
    return result