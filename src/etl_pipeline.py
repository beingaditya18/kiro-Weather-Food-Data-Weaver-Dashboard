import pandas as pd
import os

# -----------------------------------------------
# KIRO-ASSISTED ETL PIPELINE
# -----------------------------------------------

class DataWeaver:
    def __init__(self):
        self.raw_food_path = "data/food_orders_raw.csv"
        self.raw_weather_path = "data/weather_raw.csv"
        self.output_path = "data/merged_data.csv"

    def clean_data(self):
        """Standardizes date formats and text casing."""
        print("🧹 Starting Data Cleaning...")
        
        # Load
        self.df_food = pd.read_csv(self.raw_food_path)
        self.df_weather = pd.read_csv(self.raw_weather_path)
        
        # Clean Dates
        self.df_food['date'] = pd.to_datetime(self.df_food['date'])
        self.df_weather['date'] = pd.to_datetime(self.df_weather['date'])
        
        # Normalize Text
        self.df_food['city'] = self.df_food['city'].str.strip().str.title()
        self.df_weather['city'] = self.df_weather['city'].str.strip().str.title()
        
        print(f"   -> Cleaned {len(self.df_food)} food records")
        print(f"   -> Cleaned {len(self.df_weather)} weather records")

    def weave_data(self):
        """Merges datasets based on semantic keys (Date + City)."""
        print("🧵 Weaving Datasets (Merge Logic)...")
        
        self.merged_df = pd.merge(
            self.df_food,
            self.df_weather,
            on=["date", "city"],
            how="inner"
        )
        
        # Data Integrity Check
        if self.merged_df.empty:
            raise ValueError("❌ Merge failed! No matching dates/cities found.")
            
        print(f"✅ Merge Complete. Final Dataset: {self.merged_df.shape}")

    def save(self):
        self.merged_df.to_csv(self.output_path, index=False)
        print(f"💾 Saved final dataset to: {self.output_path}")

if __name__ == "__main__":
    # Execution Flow
    try:
        pipeline = DataWeaver()
        pipeline.clean_data()
        pipeline.weave_data()
        pipeline.save()
        print("\n🚀 ETL Pipeline execution successful.")
    except Exception as e:
        print(f"❌ Pipeline Failed: {e}")