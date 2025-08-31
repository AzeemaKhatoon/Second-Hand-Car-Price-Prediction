import streamlit as st
import numpy as np
import pandas as pd
import joblib
import base64

# Data of Cars_24
df = pd.read_csv("Cars_24.csv")

# Load the Polynomial Regression model
with open("poly_model.joblib", "rb" ) as file:
    poly_model = joblib.load(file)

# Page Layout
st.set_page_config(page_title="Second Hand Car Price Prediction")

# Title and Subheader
st.title("🚗 Second Hand Car Price Prediction")
st.subheader("Provide information about second-hand car.")

# Background Image Code
def get_base64_of_bin_file(bin_file):
    """
    Reads a binary file and returns its base64 encoded string.
    """
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    """
    Sets a local PNG or JPG image as the background of the Streamlit app using base64.
    """
    bin_str = get_base64_of_bin_file(png_file)
    
    # Adjust mime type based on image type (jpg or png)
    mime_type = "jpeg" if png_file.lower().endswith((".jpg", ".jpeg")) else "png"
    
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/{mime_type};base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Just provide the filename of image (it must be in the same folder or use full path correctly)
set_png_as_page_bg("background.jpg")

# Information related to car
year = st.number_input("📅 Year of Manufacture", min_value=1990, max_value=2022)

km_driven = st.number_input("🏁 Total km car driven", min_value=00, max_value=500000)

mileage = st.number_input("⛽ Mileage", min_value=5.0, max_value=40.0, step=0.1)

engine = st.number_input("⚙️ Engine", min_value=0.0, max_value=7000.0)

max_power = st.number_input("⚡ Maximum Power an Engine", min_value=0.0, max_value=5000.0)

age = st.number_input("⏳ Age of Car", min_value=1.0, max_value=50.0, step=0.5)

make = st.selectbox("🏷️ Car Brand", df["make"].unique())

model = st.selectbox("🚘 Car Model", df.groupby("make")["model"].get_group(make))

car_seller = st.selectbox("👨🏻‍💼 Car Seller", ["Individual","Trustmark_Dealer"])

fuel = st.selectbox("🛢️ Fuel Type", ["Diesel","Electric","LPG","Petrol"])

manual = st.selectbox("🛠️ Manual Transmission", ["Manual", "Automatic"])

gears = st.selectbox("🔩 Gears", ["5", ">5"])

# Seller encoding
Individual = 0
Trustmark_Dealer = 0
if car_seller == "Individual":
    Individual = 1
else:
    Trustmark_Dealer = 1

# Fuel encoding
Diesel, Electric, LPG, Petrol = 0,0,0,0
if fuel == "Petrol":
    Petrol = 1
elif fuel == "Diesel":
    Diesel = 1
elif fuel == "LPG":
    LPG = 1
else:
    Electric = 1

# Manual Transmission encoding
Manual = 1 if manual == "Manual" else 0

# Gears encoding
gear_5 = 0
gear_greater_5 = 0 
if gears == ">5":
    gear_greater_5 = 1
else:
    gear_5 = 1

data = pd.DataFrame([[
    year, km_driven, mileage, engine, max_power, age, make, model,
    Individual, Trustmark_Dealer, Diesel, Electric, LPG, Petrol,
    Manual, gear_5, gear_greater_5
]], columns=[
    "year", "km_driven", "mileage", "engine", "max_power", "age", "make", "model",
    "Individual", "Trustmark_Dealer", "Diesel", "Electric", "LPG", "Petrol",
    "Manual", "5", ">5"
])    

if st.button("💰 Predict Price"):
    pred = poly_model.predict(data)

    # Using metric display for a clean look
    st.success("✅ Prediction Completed!")
    st.metric(label="Predicted Car Price", value=f"{pred[0]:,.2f} lakh")
