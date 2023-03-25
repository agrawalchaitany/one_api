import streamlit as st
import pandas as pd

# Load car specifications 
car_specs = st.cache_data(pd.read_csv)("https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data")

# Rename columns
car_specs.columns = ["symboling", "normalized_losses", "make", "fuel_type", "aspiration", "num_doors",
                     "body_style", "drive_wheels", "engine_location", "wheel_base", "length", "width",
                     "height", "curb_weight", "engine_type", "num_cylinders", "engine_size", "fuel_system",
                     "bore", "stroke", "compression_ratio", "horsepower", "peak_rpm", "city_mpg",
                     "highway_mpg", "price"]

# Sidebar
st.sidebar.title("Car Comparison")
brands = car_specs["make"].unique()
selected_brands = st.sidebar.multiselect("Select brands to compare", brands)
st.sidebar.markdown("### Priority Ratings")
mileage_score = st.sidebar.slider("Mileage", 1, 10, 5)
power_score = st.sidebar.slider("Engine Power", 1, 10, 5)
price_score = st.sidebar.slider("Price", 1, 10, 5)

# Filter specifications for selected brands
filtered_specs = car_specs[car_specs["make"].isin(selected_brands)]

# Calculate scores for each component
filtered_specs["Mileage Score"] = mileage_score * (filtered_specs["city_mpg"] + filtered_specs["highway_mpg"]) / 2
filtered_specs["Power Score"] = power_score * filtered_specs["horsepower"]
filtered_specs["Price Score"] = price_score * filtered_specs["price"]

# Calculate overall score for each car
filtered_specs["Total Score"] = filtered_specs.iloc[:, -3:].sum(axis=1)

# Sort cars by total score
filtered_specs = filtered_specs.sort_values(by=["Total Score"], ascending=False)

# Main panel: Display comparison results
st.title("Car Comparison Results")
st.markdown("### Selected Brands")
st.write(selected_brands)
st.markdown("### Importance Ratings")
st.write("Mileage: ", mileage_score)
st.write("Engine Power: ", power_score)
st.write("Price: ", price_score)
st.markdown("### Comparison Results")
st.write(filtered_specs[["make", "fuel_type", "body_style", "drive_wheels", "engine_size", "price", "Total Score"]])
