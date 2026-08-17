import pandas as pd
import numpy as np

def engineer_telemetry_features(df_tel):
    """
    Adds calculated fields to the telemetry dataframe.
    """
    # 1. Accel Magnitude (Orientation-independent motion/vibration proxy)
    df_tel['Accel_Magnitude'] = np.sqrt(
        df_tel['Accel_X_g']**2 + df_tel['Accel_Y_g']**2 + df_tel['Accel_Z_g']**2
    )
    
    # 2. Gyro Magnitude (Orientation-independent rotational proxy)
    df_tel['Gyro_Magnitude'] = np.sqrt(
        df_tel['Gyro_X_dps']**2 + df_tel['Gyro_Y_dps']**2 + df_tel['Gyro_Z_dps']**2
    )
    
    # 3. Minute Speed Change
    # Since data is sorted by Trip_ID and Timestamp, diff within group
    df_tel['Minute_Speed_Change'] = df_tel.groupby('Trip_ID')['Speed_kmph'].diff()
    
    return df_tel

def aggregate_trip_features(df_tel, df_trips, hard_brake_threshold, harsh_accel_threshold, harsh_rot_threshold):
    """
    Aggregates telemetry features to the Trip_ID level using EDA-derived thresholds.
    """
    # Group by Trip
    grouped = df_tel.groupby('Trip_ID')
    
    trip_stats = pd.DataFrame()
    trip_stats['Telemetry_Minutes'] = grouped.size()
    
    # Magnitudes
    trip_stats['Trip_Accel_Mag_Mean'] = grouped['Accel_Magnitude'].mean()
    trip_stats['Trip_Accel_Mag_Std'] = grouped['Accel_Magnitude'].std()
    trip_stats['Trip_Gyro_Mag_Mean'] = grouped['Gyro_Magnitude'].mean()
    trip_stats['Trip_Gyro_Mag_Std'] = grouped['Gyro_Magnitude'].std()
    
    # Events based on thresholds
    # Hard braking: Minute_Speed_Change < Negative Threshold
    trip_stats['Trip_Extreme_Braking_Count'] = grouped.apply(
        lambda x: (x['Minute_Speed_Change'] < hard_brake_threshold).sum()
    )
    
    # Harsh acceleration: Minute_Speed_Change > Positive Threshold
    trip_stats['Trip_Harsh_Acceleration_Count'] = grouped.apply(
        lambda x: (x['Minute_Speed_Change'] > harsh_accel_threshold).sum()
    )
    
    # Harsh rotation: Gyro_Magnitude > Threshold
    trip_stats['Trip_Extreme_Rot_Count'] = grouped.apply(
        lambda x: (x['Gyro_Magnitude'] > harsh_rot_threshold).sum()
    )
    
    # High Speed Exposure: Minutes spent above 45 km/h (Arbitrary high speed proxy for relative comparison)
    # We will refine the exact definition, let's use > 40 as a base, we can adjust.
    trip_stats['Trip_High_Speed_Minutes'] = grouped.apply(
        lambda x: (x['Speed_kmph'] > 40).sum()
    )
    
    # Merge with Trips to get context
    df_trips_subset = df_trips[['Trip_ID', 'Driver_ID', 'Vehicle_ID', 'Duration_Min', 'Distance_KM', 'Avg_Speed_kmph', 'Max_Speed_kmph']].copy()
    
    trip_features = pd.merge(df_trips_subset, trip_stats.reset_index(), on='Trip_ID', how='inner')
    
    return trip_features
