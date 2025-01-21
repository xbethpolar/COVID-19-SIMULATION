import streamlit as st
import pandas as pd
import os
from datetime import datetime
import assignment2

def main(): #main function
    st.title("COVID-19")

    SAMPLE_RATIO = st.number_input( #interactive numeric field
        label="Sample Ratio",
        min_value=1,
        value=1_000_000,
        step=1_000,
        #format="%d"
    )

    START_DATE = st.date_input( #interactive calendar 
        label="Start Date",
        value=datetime.strptime('2021-04-01', '%Y-%m-%d').date(),
        min_value=datetime.strptime('2020-01-01', '%Y-%m-%d').date(),
        max_value=datetime.today().date()
    )

    END_DATE = st.date_input(
        label="End Date",
        value=datetime.strptime('2022-04-30', '%Y-%m-%d').date(),
        min_value=START_DATE,
        max_value=datetime.today().date()
    )

    countries_file = 'a2-countries.csv'
    if os.path.exists(countries_file):
        countries_df = pd.read_csv(countries_file)
        country_options = countries_df['country'].unique().tolist() # converts the list of countries to a option list
        
        SELECTED_COUNTRIES = st.multiselect(
            label="Countries",
            options=country_options,
            default=['Argentina', 'Japan']
        )
    else:
        st.error(f"You need to have the file a2-countries.csv.")
        SELECTED_COUNTRIES = []

    if st.button("Run"):
        if len(SELECTED_COUNTRIES) < 2:
            st.warning("Please select at least 2 countries.")
        else:
            with st.spinner('Simulation on course...'):
                start_date_str = START_DATE.strftime('%Y-%m-%d')
                end_date_str = END_DATE.strftime('%Y-%m-%d')

                assignment2.run(
                    countries_csv_name='a2-countries.csv',
                    countries=SELECTED_COUNTRIES,
                    sample_ratio=SAMPLE_RATIO,
                    start_date=start_date_str,
                    end_date=end_date_str
                )
            st.success('Simulation complete.')

            image_file = 'a2-covid-simulation.png'
            if os.path.exists(image_file):
                st.image(image_file, caption='Result from simulation')
            else:
                st.warning("a2-covid-simulation.png doesn't exist.")

if __name__ == "__main__":
    main()
