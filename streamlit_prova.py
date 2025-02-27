import streamlit as st
import pandas as pd
import altair as alt

# Title
st.title("Allergen Frequency Analyzer")

# File Upload
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("## Preview of Uploaded Data")
    st.dataframe(df.head())
    
    # Assuming allergens are in a specific column (modify as needed)
    allergen_column = st.selectbox("Select allergen column", df.columns)
    
    # User Input for Manual Allergen Search
    unique_allergens = df[allergen_column].dropna().unique().tolist()
    user_input = st.multiselect("Enter or select allergens to analyze", options=unique_allergens)
    
    # Option to analyze all allergens
    analyze_all = st.checkbox("Analyze all allergens")

    if user_input or analyze_all:
        # Normalize case variations
        df[allergen_column] = df[allergen_column].str.lower()
        if analyze_all:
            user_input = unique_allergens
        else:
            user_input = [allergen.lower() for allergen in user_input]
        
        # Count occurrences
        allergen_counts = df[allergen_column].value_counts().reset_index()
        allergen_counts.columns = ["Allergen", "Count"]
        
        # Filter by user selection
        allergen_counts = allergen_counts[allergen_counts["Allergen"].isin(user_input)]
        
        # Relative frequency threshold
        total_entries = len(df)
        allergen_counts["Frequency"] = allergen_counts["Count"] / total_entries
        threshold = st.slider("Set frequency threshold", 0.0, 1.0, 0.05)
        filtered_counts = allergen_counts[allergen_counts["Frequency"] > threshold]
        
        # Display results
        st.write("## Allergen Frequency Table")
        st.dataframe(filtered_counts)
        
        # Visualization
        st.write("## Allergen Distribution")
        chart = alt.Chart(filtered_counts).mark_bar().encode(
            x="Allergen", y="Count", tooltip=["Allergen", "Count", "Frequency"]
        ).properties(width=600)
        st.altair_chart(chart)
    else:
        st.warning("Please select at least one allergen to analyze or check the box to analyze all allergens.")
