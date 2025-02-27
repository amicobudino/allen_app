import streamlit as st
import pandas as pd
import os

# File path for the CSV
csv_file = os.path.join(os.path.dirname(__file__), 'allergens.csv')

st.title('Allergens CSV Creator')

# Get user input
allergens = st.text_input('Enter allergens separated by space')

if st.button("Save Allergens"):
    # Convert the string to a list
    allergen_list = allergens.split()
    allergen_list = [allergen.strip(',').strip().lower() for allergen in allergen_list]

    # Load or create the CSV file
    if os.path.exists(csv_file):
        allergen_series = pd.read_csv(csv_file, header=None).squeeze("columns")
    else:
        allergen_series = pd.Series(dtype=str)

    # Add new allergens to the series
    allergen_series = pd.concat([allergen_series, pd.Series(allergen_list)], ignore_index=True)

    # Save back to CSV
    allergen_series.to_csv(csv_file, index=False, header=False)

    st.success('Allergens saved to allergens.csv')

# Display existing allergens
if os.path.exists(csv_file):
    st.write("### Current Allergens in CSV:")
    existing_allergens = pd.read_csv(csv_file, header=None).squeeze("columns")
    st.write(existing_allergens)
