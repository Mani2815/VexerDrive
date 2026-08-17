import pandas as pd
import json

df_driver = pd.read_csv('outputs/driver_metrics.csv')
print("--- 3 Drivers Trace ---")
for _, row in df_driver.head(3).iterrows():
    print(f"\nDriver: {row['Driver_ID']}")
    print(f"Total Minutes: {row['Total_Minutes']}")
    print(f"Hard Braking Rate: {row['Hard_Braking_Rate']:.2f}")
    print(f"Harsh Accel Rate: {row['Harsh_Accel_Rate']:.2f}")
    print(f"Harsh Corner Rate: {row['Harsh_Corner_Rate']:.2f}")
    print(f"High Speed Ratio: {row['High_Speed_Ratio']:.2f}")
    print(f"Braking Subscore: {row['Braking_Subscore']:.2f} (Weight 0.3)")
    print(f"Accel Subscore: {row['Accel_Subscore']:.2f} (Weight 0.3)")
    print(f"Corner Subscore: {row['Corner_Subscore']:.2f} (Weight 0.2)")
    print(f"Speed Subscore: {row['Speed_Subscore']:.2f} (Weight 0.2)")
    print(f"Final Score: {row['Driver_Risk_Score']}")
    print(f"Classification: {row['Risk_Classification']}")

df_vehicle = pd.read_csv('outputs/vehicle_metrics.csv')
with open('outputs/thresholds.json') as f:
    thresh = json.load(f)
print("\n--- 3 Vehicles Trace ---")
print(f"Thresholds: {thresh}")
for _, row in df_vehicle.head(3).iterrows():
    print(f"\nVehicle: {row['Vehicle_ID']}")
    print(f"Total Trips: {row['Total_Trips']}")
    print(f"Anomalous Trips: {row['Anomalous_Trips']}")
    print(f"Persistence Pct: {row['Persistence_Pct']:.2f}%")
    print(f"Unique Drivers: {row['Total_Drivers']}")
    print(f"Drivers With Anomaly: {row['Drivers_With_Anomaly']}")
    print(f"Health Risk Score: {row['Health_Risk_Score']}")
    print(f"Classification: {row['Health_Classification']}")
