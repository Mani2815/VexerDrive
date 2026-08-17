import pandas as pd
import numpy as np
import os
import json

def calculate_driver_scores(trip_metrics_path, drivers_path, output_path):
    """
    Calculates the Driver Behaviour Risk Score based on exposure-normalized rates.
    """
    # Load Data
    trips = pd.read_csv(trip_metrics_path)
    
    # Load Drivers for context
    xl = pd.ExcelFile(drivers_path)
    # the second row is header
    df_raw = xl.parse('Drivers ', header=None)
    header_idx = None
    for idx, row in df_raw.iterrows():
        if row.notnull().sum() > len(row) / 2:
            header_idx = idx
            break
    drivers = xl.parse('Drivers ', header=header_idx).dropna(how='all')
    
    # Aggregate to Driver Level
    driver_agg = trips.groupby('Driver_ID').agg(
        Total_Trips=('Trip_ID', 'count'),
        Total_Minutes=('Telemetry_Minutes', 'sum'),
        Total_Hard_Brakes=('Trip_Extreme_Braking_Count', 'sum'),
        Total_Harsh_Accel=('Trip_Harsh_Acceleration_Count', 'sum'),
        Total_Harsh_Corner=('Trip_Extreme_Rot_Count', 'sum'),
        Total_High_Speed_Mins=('Trip_High_Speed_Minutes', 'sum')
    ).reset_index()
    
    # Calculate Exposure-Normalized Rates (per 100 minutes)
    driver_agg['Hard_Braking_Rate'] = (driver_agg['Total_Hard_Brakes'] / driver_agg['Total_Minutes']) * 100
    driver_agg['Harsh_Accel_Rate'] = (driver_agg['Total_Harsh_Accel'] / driver_agg['Total_Minutes']) * 100
    driver_agg['Harsh_Corner_Rate'] = (driver_agg['Total_Harsh_Corner'] / driver_agg['Total_Minutes']) * 100
    driver_agg['High_Speed_Ratio'] = (driver_agg['Total_High_Speed_Mins'] / driver_agg['Total_Minutes'])
    
    # Min-Max Scaling capped at 95th percentile to create 0-100 Subscores
    def scale_score(series):
        cap = series.quantile(0.95)
        # Avoid division by zero
        if cap == 0:
            return series * 0
        scaled = (series / cap) * 100
        return scaled.clip(upper=100)
        
    driver_agg['Braking_Subscore'] = scale_score(driver_agg['Hard_Braking_Rate'])
    driver_agg['Accel_Subscore'] = scale_score(driver_agg['Harsh_Accel_Rate'])
    driver_agg['Corner_Subscore'] = scale_score(driver_agg['Harsh_Corner_Rate'])
    driver_agg['Speed_Subscore'] = scale_score(driver_agg['High_Speed_Ratio'])
    
    # Final Score Calculation
    # Weights defined based on behavioral relevance and robustness:
    # 30% Braking, 30% Acceleration, 20% Cornering, 20% High Speed
    weights = {
        'Braking': 0.30,
        'Accel': 0.30,
        'Corner': 0.20,
        'Speed': 0.20
    }
    
    driver_agg['Driver_Risk_Score'] = (
        driver_agg['Braking_Subscore'] * weights['Braking'] +
        driver_agg['Accel_Subscore'] * weights['Accel'] +
        driver_agg['Corner_Subscore'] * weights['Corner'] +
        driver_agg['Speed_Subscore'] * weights['Speed']
    ).round(2)
    
    # Classification
    # Use tertiles for relative classification
    tertiles = driver_agg['Driver_Risk_Score'].quantile([0.33, 0.66])
    def classify(score):
        if score <= tertiles[0.33]:
            return 'Safe'
        elif score <= tertiles[0.66]:
            return 'Moderate'
        else:
            return 'Risky'
            
    driver_agg['Risk_Classification'] = driver_agg['Driver_Risk_Score'].apply(classify)
    
    # Merge context
    final_drivers = pd.merge(driver_agg, drivers[['Driver_ID', 'Driver_Name', 'Age', 'License_Experience_Years']], on='Driver_ID', how='left')
    
    # Save output
    final_drivers.to_csv(output_path, index=False)
    print(f"Driver metrics saved to {output_path}")

if __name__ == "__main__":
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    calculate_driver_scores(
        trip_metrics_path=os.path.join(repo_root, 'outputs/trip_metrics.csv'),
        drivers_path=os.path.join(repo_root, '../dataset.xlsx'),
        output_path=os.path.join(repo_root, 'outputs/driver_metrics.csv')
    )
