import pandas as pd
import numpy as np
import os
import random

# -----------------------------------------------
# CONFIGURATION
# -----------------------------------------------
CITIES = ["Indore", "Bhopal", "Bangalore", "Delhi"]
CUISINES = ["North Indian", "South Indian", "Chinese", "Fast Food", "Biryani"]
START_DATE = "2024-01-01"
END_DATE = "2024-03-30"

def ensure_folders():
    """Kiro Helper: Ensures directory structure exists."""
    os.makedirs("data", exist_ok=True)
    print("✅ Folder structure verified.")

def generate_weather_and_orders():
    """
    Generates synthetic data where Weather DIRECTLY impacts Food Orders.
    This ensures your dashboard tells a clear story.
    """
    dates = pd.date_range(start=START_DATE, end=END_DATE, freq="D")
    
    weather_records = []
    food_records = []
    
    print(f"🔄 Simulating data collection for {len(dates)} days...")

    for date in dates:
        for city in CITIES:
            # 1. Simulating Weather (Hardcoded Seasonality)
            # Randomly assign weather, but biased towards clear days
            weather_type = np.random.choice(["Clear", "Rainy", "Cloudy", "Hot"], p=[0.5, 0.2, 0.2, 0.1])
            
            if weather_type == "Rainy":
                temp = np.random.randint(20, 26)
                rain = np.random.randint(10, 50) # Heavy rain
                weather_factor = 1.5 # 50% more orders when raining
            elif weather_type == "Hot":
                temp = np.random.randint(35, 42)
                rain = 0
                weather_factor = 0.8 # Less orders, people eat light
            else:
                temp = np.random.randint(25, 32)
                rain = 0
                weather_factor = 1.0 # Normal

            # Save Raw Weather Data
            weather_records.append({
                "date": date,
                "city": city,
                "temperature": temp,
                "rainfall": rain,
                "weather_condition": weather_type
            })

            # 2. Simulating Food Orders (Correlated to Weather)
            for cuisine in CUISINES:
                base_orders = np.random.randint(50, 100)
                
                # The "Hardcoded" Insight:
                # If raining, people order more Fast Food & North Indian
                if weather_type == "Rainy" and cuisine in ["Fast Food", "North Indian"]:
                    final_orders = int(base_orders * weather_factor * 1.2)
                else:
                    final_orders = int(base_orders * weather_factor)

                # Order Value Calculation
                avg_price = np.random.randint(200, 500)
                total_value = final_orders * avg_price

                # Save Raw Food Data
                food_records.append({
                    "date": date,
                    "city": city,
                    "cuisine": cuisine,
                    "order_count": final_orders,
                    "order_value": total_value
                })

    # Export to "Raw" CSVs to mimic the start of a pipeline
    pd.DataFrame(weather_records).to_csv("data/weather_raw.csv", index=False)
    pd.DataFrame(food_records).to_csv("data/food_orders_raw.csv", index=False)
    
    print("✅ data/weather_raw.csv created (Simulated API Fetch)")
    print("✅ data/food_orders_raw.csv created (Simulated DB Dump)")

if __name__ == "__main__":
    ensure_folders()
    generate_weather_and_orders()