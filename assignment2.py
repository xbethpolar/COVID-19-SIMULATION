#Bethsy Assignment 2 - Applied Programming in Python
import pandas as pd
import numpy as np
import random
import csv
import os

from sim_parameters import TRANSITION_PROBS, HOLDING_TIMES
from datetime import datetime, timedelta
from helper import create_plot

def run(countries_csv_name, countries, start_date, end_date, sample_ratio): #main function
    START_DATE = datetime.strptime(start_date, '%Y-%m-%d')
    END_DATE = datetime.strptime(end_date, '%Y-%m-%d')

    total_simulation_days = (END_DATE - START_DATE).days + 1 # it excludes the start day so that why +1

    countries_df = pd.read_csv(countries_csv_name) #read the data in the csv
    #print(countries_df.head())
    
    age_groups = []
    for i in TRANSITION_PROBS.keys():
            age_groups.append(i)
        
    person_age_group = random.choice(age_groups)
    #print(f'this person belongs to this age group: {person_age_group}')
    #print(age_groups)

    #now we have to define the current state based on the group of age, because the probabilities are going to be different for each age group
    if 'H' in TRANSITION_PROBS[person_age_group].keys():
            sub_dict = TRANSITION_PROBS[person_age_group]
            current_state = next(iter(sub_dict)) #sub_dict['H']
            
    else: 
            current_state = 'none'
    #print(current_state)

    #assigns the number of days a person will remain in their current state
    state_remaining_days = HOLDING_TIMES[person_age_group][current_state]
    #print(state_remaining_days)

    def create_samples(countries_df, sample_ratio): #this function creates the samples for each country and each age group
        popu = []

        for _, each_row in countries_df.iterrows():
            sample_per_country = int( each_row['population'] / sample_ratio) # the result its the total samples for that population
            #print(index)
            #print(row['population']) 
            #print(sample_per_country) 

            age_groups = { # extracts age group data from the csv
                    'less_5': each_row['less_5'], 
                    '5_to_14': each_row['5_to_14'],
                    '15_to_24': each_row['15_to_24'],
                    '25_to_64': each_row['25_to_64'],
                    'over_65': each_row['over_65'],
                }
            
            samples_by_age_group = {} #here we calculate how many people belong to each group based on each age group
            for age_group, percent in age_groups.items():
                samples_by_age_group[age_group] = int(sample_per_country * (percent / 100))
                #print(index)
                #print(samples_by_age_group)
                
            popu.append((each_row['country'], samples_by_age_group))
            #print(popu)
        return popu
    
    def get_health_states(TRANSITION_PROBS): #get health statuses from the dictionary
        states = []
        #to get the chain type states I must do a double for loop
        for key in TRANSITION_PROBS[person_age_group]:
            for state in TRANSITION_PROBS[person_age_group][key].keys():
                states.append(str(state))

       # unique_states = set(states)
        #print(f'----{states}')
        return states
    
    def set_state(new_state): # this function sets the new state
         return new_state

    #this function simulates the daily state transition of a person over a period of time
    def simulate_person(TRANSITION_PROBS, HOLDING_TIMES, simulated_days, current_state, person_age_group, state_remaining_days):
        remaining_days = state_remaining_days
        actual = current_state
        daily_states = []

        for _ in range(simulated_days):
            daily_states.append(actual)
            
            if remaining_days > 0:
                remaining_days -= 1
                
            if remaining_days == 0:
                 
                state_options = list(TRANSITION_PROBS[person_age_group][actual].keys())
                state_probs = list(TRANSITION_PROBS[person_age_group][actual].values())

                next_state = str(np.random.choice(state_options, p=state_probs))
                daily_states.append(next_state)
                actual = set_state(next_state)
                remaining_days = HOLDING_TIMES[person_age_group][actual]
                #print(state_probs)
                #print(state_options)
                #print(f'---> {len(state_probs)}')
                #print(f'---> {len(state_options)}')
        return daily_states
    
    def simulated_samples(): # use create_samples() and simulate_person() to simulate the population for each country
            
            samples_simulation_table = []
            population_to_simulate = create_samples(countries_df, sample_ratio)
            
            for country, samples_age_group in population_to_simulate:
                 #print(f'for {country}')
                 for age_group, sample_size in samples_age_group.items():
                        person_age_group = age_group
                        for person_id in range(sample_size):
                            if 'H' in TRANSITION_PROBS[person_age_group].keys():
                                current_state = next(iter(TRANSITION_PROBS[person_age_group].keys())) # TRANSITION_PROBS[person_age_group]['H'].keys()
                            else:
                                 current_state = 'none'
                            
                            state_remaining_days = HOLDING_TIMES[person_age_group][current_state]
                            simulation_per_sample = simulate_person(TRANSITION_PROBS, HOLDING_TIMES, simulated_days=395, current_state=current_state, person_age_group=person_age_group, state_remaining_days=state_remaining_days)
                            
                            for day, health_state in enumerate(simulation_per_sample[:total_simulation_days], start=1):
                                 samples_simulation_table.append({
                                      'country': country, 'age_group': person_age_group, 'person_id': person_id + 1, 'day': day, 'health_state': health_state
                                 })

            samples_table_df = pd.DataFrame(samples_simulation_table)  
            #pd.set_option('display.max_rows', None)
            #pd.set_option('display.max_columns', None)
            #print(samples_table_df)         
            return samples_table_df

         
    def store_simulation_csv(START_DATE): #write the simulation's result in a csv file
        output_file = os.path.join(os.getcwd(), 'a2-covid-simulated-timeseries.csv')
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                   'person_id',
                   'age_group_name',
                   'country',
                   'date',
                   'state',
                   'staying_days',
                   'prev_state',
              ])
       
            for _, row in samples_df.iterrows(): 
                date = (START_DATE + timedelta(days=row['day'] - 1)).strftime('%Y-%m-%d')
                age_group = row['age_group']
                current_state = row['health_state']
                prev_state = prev_state if 'prev_state' in locals() else current_state
                staying_days = HOLDING_TIMES[age_group][current_state]
                writer.writerow([
                  row['person_id'],
                  age_group,
                  row['country'],
                  date,
                  current_state,
                  staying_days,
                  prev_state,
                ])

                prev_state = current_state
    #this function generate  a daily summary of the health states and save it and another csv file            
    def daily_summary(simulation_csv='a2-covid-simulated-timeseries.csv', output_csv='a2-covid-summary-timeseries.csv'):
        simulated_df = pd.read_csv(simulation_csv)
        summary_df = simulated_df.groupby(['date', 'country', 'state',]).size().unstack(fill_value=0).reset_index()
        summary_df.to_csv(output_csv, index= False)
        #print(summary_df.head())
       
        
    samples_df = simulated_samples()
    store_simulation_csv(START_DATE)
    daily_summary()
    get_health_states(TRANSITION_PROBS)
    create_samples(countries_df, sample_ratio)
    simulate_person(TRANSITION_PROBS, HOLDING_TIMES, simulated_days=395, current_state=current_state, person_age_group=person_age_group, state_remaining_days=state_remaining_days)
    create_plot('a2-covid-summary-timeseries.csv', countries)

if __name__ == "__main__": #this executes the run() function if the script is run directly
    run(countries_csv_name='a2-countries.csv', countries=['Argentina', 'Japan'], start_date='2021-04-01', end_date='2022-04-30', sample_ratio=1e6)
