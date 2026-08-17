import pandas as pd
import numpy as np
import os
import json

def calculate_vehicle_scores(trip_metrics_path, thresholds_path, vehicles_path, output_path):
    """
    Calculates the Vehicle Health Score and applies the persistence logic.
    """
    trips = pd.read_csv(trip_metrics_path)
    
    with open(thresholds_path, 'r') as f:
        thresholds = json.load(f)
        
    accel_mean_90th = thresholds['accel_mean_90th']
    persistence_threshold = thresholds['persistence_threshold']
    
    # Load Vehicles for context
    xl = pd.ExcelFile(vehicles_path)
    df_raw = xl.parse('Vehicles', header=None)
    header_idx = None
    for idx, row in df_raw.iterrows():
        if row.notnull().sum() > len(row) / 2:
            header_idx = idx
            break
    vehicles = xl.parse('Vehicles', header=header_idx).dropna(how='all')
    
    # Determine anomalous trips
    trips['Is_Anomalous'] = trips['Trip_Accel_Mag_Mean'] > accel_mean_90th
    
    # Aggregate to Vehicle Level
    vehicle_agg = trips.groupby('Vehicle_ID').agg(
        Total_Trips=('Trip_ID', 'count'),
        Anomalous_Trips=('Is_Anomalous', 'sum'),
        Total_Drivers=('Driver_ID', 'nunique'),
        Accel_Mag_Std=('Trip_Accel_Mag_Mean', 'std') # Variability across trips
    ).reset_index()
    
    # Drivers who experienced anomalous trips in this vehicle
    anomalous_trips_df = trips[trips['Is_Anomalous']]
    drivers_with_anomaly = anomalous_trips_df.groupby('Vehicle_ID')['Driver_ID'].nunique().reset_index()
    drivers_with_anomaly.columns = ['Vehicle_ID', 'Drivers_With_Anomaly']
    
    vehicle_agg = pd.merge(vehicle_agg, drivers_with_anomaly, on='Vehicle_ID', how='left')
    vehicle_agg['Drivers_With_Anomaly'] = vehicle_agg['Drivers_With_Anomaly'].fillna(0)
    
    # Calculate Persistence
    vehicle_agg['Persistence_Pct'] = (vehicle_agg['Anomalous_Trips'] / vehicle_agg['Total_Trips']) * 100
    
    # Score logic
    # Score 0-100 based on persistence and variability
    # Max persistence cap at 50% for scaling
    vehicle_agg['Health_Risk_Score'] = (vehicle_agg['Persistence_Pct'] / 50.0 * 100).clip(upper=100).round(2)
    
    # Classification Logic
    def classify_health(row):
        persists = row['Persistence_Pct'] > persistence_threshold
        multiple_drivers = row['Drivers_With_Anomaly'] > 1
        
        # If the vehicle only has 1 driver ever, we can't test cross-driver, so we just rely on persistence
        if row['Total_Drivers'] == 1:
            multiple_drivers = True 
            
        if persists and multiple_drivers:
            return 'Maintenance Recommended'
        elif row['Persistence_Pct'] > (persistence_threshold / 2):
            return 'Monitor'
        else:
            return 'Healthy'
            
    vehicle_agg['Health_Classification'] = vehicle_agg.apply(classify_health, axis=1)
    
    # Merge context
    final_vehicles = pd.merge(vehicle_agg, vehicles[['Vehicle_ID', 'Vehicle_Type', 'Manufacture_Year', 'Odometer_KM_Start_of_Week']], on='Vehicle_ID', how='left')
    
    # Save output
    final_vehicles.to_csv(output_path, index=False)
    print(f"Vehicle metrics saved to {output_path}")

if __name__ == "__main__":
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    calculate_vehicle_scores(
        trip_metrics_path=os.path.join(repo_root, 'outputs/trip_metrics.csv'),
        thresholds_path=os.path.join(repo_root, 'outputs/thresholds.json'),
        vehicles_path=os.path.join(repo_root, '../dataset.xlsx'),
        output_path=os.path.join(repo_root, 'outputs/vehicle_metrics.csv')
    )
