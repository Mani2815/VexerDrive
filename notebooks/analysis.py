import sys
import os
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import data_processing
import feature_engineering

# 1. Load Data
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
file_path = os.path.join(repo_root, '../dataset.xlsx')
print(f"Loading data from {file_path}...")
dataframes = data_processing.load_and_clean_data(file_path)

df_tel = dataframes['Telemetry']
df_trips = dataframes['Trips']

# 2. Engineer Telemetry Features
print("Engineering telemetry features...")
df_tel = feature_engineering.engineer_telemetry_features(df_tel)

# 3. EDA - Determine Thresholds for Events
print("\n--- EDA for Event Thresholds ---")
# Speed Change Percentiles
speed_changes = df_tel['Minute_Speed_Change'].dropna()
print(f"Minute Speed Change Percentiles (km/h/min):")
print(speed_changes.quantile([0.01, 0.05, 0.10, 0.50, 0.90, 0.95, 0.99]).to_string())

# Hard Braking: Let's use the 5th percentile (negative speed change)
hard_brake_threshold = speed_changes.quantile(0.05)
print(f"\nSelected Hard Braking Threshold: {hard_brake_threshold:.2f} km/h/min")

# Harsh Acceleration: Let's use the 95th percentile (positive speed change)
harsh_accel_threshold = speed_changes.quantile(0.95)
print(f"Selected Harsh Acceleration Threshold: {harsh_accel_threshold:.2f} km/h/min")

# Gyro Magnitude Percentiles
gyro_mags = df_tel['Gyro_Magnitude'].dropna()
print(f"\nGyro Magnitude Percentiles (dps):")
print(gyro_mags.quantile([0.50, 0.75, 0.90, 0.95, 0.99]).to_string())

# Harsh Cornering: Let's use the 95th percentile
harsh_rot_threshold = gyro_mags.quantile(0.95)
print(f"Selected Harsh Rotation Threshold: {harsh_rot_threshold:.2f} dps")

# 4. Aggregate Trip Features
print("\nAggregating Trip Features...")
trip_features = feature_engineering.aggregate_trip_features(
    df_tel, df_trips, hard_brake_threshold, harsh_accel_threshold, harsh_rot_threshold
)

# EDA for Vehicle Persistence Threshold
print("\n--- EDA for Vehicle Persistence Threshold ---")
# Let's say an "anomalous trip" for a vehicle is one where Trip_Accel_Mag_Mean > 90th percentile of all trips
accel_mean_90th = trip_features['Trip_Accel_Mag_Mean'].quantile(0.90)
trip_features['Is_Anomalous'] = trip_features['Trip_Accel_Mag_Mean'] > accel_mean_90th

vehicle_persistence = trip_features.groupby('Vehicle_ID')['Is_Anomalous'].mean() * 100
print(f"Vehicle Anomaly Persistence Distribution (% anomalous trips per vehicle):")
print(vehicle_persistence.describe().to_string())

# Let's see percentiles of persistence
print("Percentiles of persistence:")
print(vehicle_persistence.quantile([0.50, 0.75, 0.90, 0.95]).to_string())

# Set persistence threshold based on the 75th percentile of persistence, indicating vehicles that are consistently worse than most.
persistence_threshold = vehicle_persistence.quantile(0.75)
if persistence_threshold == 0:
    persistence_threshold = 10.0 # fallback if most vehicles have 0 anomalous trips
print(f"\nSelected Vehicle Persistence Threshold: > {persistence_threshold:.1f}% anomalous trips")

# Save Trip Metrics
output_dir = os.path.join(repo_root, 'outputs')
os.makedirs(output_dir, exist_ok=True)
trip_metrics_path = os.path.join(output_dir, 'trip_metrics.csv')
trip_features.to_csv(trip_metrics_path, index=False)
print(f"\nSaved trip metrics to {trip_metrics_path}")

# Output thresholds to a JSON for scoring scripts to use
import json
with open(os.path.join(output_dir, 'thresholds.json'), 'w') as f:
    json.dump({
        'hard_brake_threshold': hard_brake_threshold,
        'harsh_accel_threshold': harsh_accel_threshold,
        'harsh_rot_threshold': harsh_rot_threshold,
        'accel_mean_90th': accel_mean_90th,
        'persistence_threshold': persistence_threshold
    }, f, indent=4)
print("Saved thresholds.json")
