# VexarDrive Data Scientist Assessment - Technical Report

## 1. Executive Summary
This project analyzes a week of telematics data (GPS + IMU) for 30 drivers and 30 vehicles across 450 trips. The primary deliverables are a data-driven **Driver Behaviour Risk Score** and a **Vehicle Health Score**. Our analysis successfully identified specific extreme events (hard braking, harsh acceleration, harsh cornering) using empirical thresholds derived from Exploratory Data Analysis (EDA). The final dashboards effectively distinguish safe driving from high-risk exposure and identify vehicles that require maintenance due to persistent mechanical anomalies.

## 2. Dataset Overview
- **Drivers**: 30 records
- **Vehicles**: 30 records
- **Trips**: 450 records (15 per driver)
- **Telemetry**: ~12,987 minute-by-minute observations combining GPS coordinates, speed, and IMU data (accelerometer and gyroscope).
- **Data Quality**: Extremely high. No missing values or corrupt types were found after adjusting for Excel header offsets.

## 3. Data Preparation
- **Ingestion**: Raw Excel sheets were loaded and normalized. Type casting was strictly enforced for numerical telemetry data.
- **Validation**: Timestamps were converted to datetime objects and sorted chronologically per `Trip_ID` to calculate minute-to-minute changes.

## 4. Feature Engineering
The raw data lacked explicit orientation information for the IMU sensors and speed limits. To ensure robustness:
1. **Accel_Magnitude**: `sqrt(Accel_X_g^2 + Accel_Y_g^2 + Accel_Z_g^2)`. Used as an orientation-independent motion/vibration proxy.
2. **Gyro_Magnitude**: `sqrt(Gyro_X_dps^2 + Gyro_Y_dps^2 + Gyro_Z_dps^2)`. Used as an orientation-independent rotational proxy.
3. **Minute_Speed_Change**: Minute-to-minute speed differential, used to proxy acceleration and deceleration.

## 5. Driver Behaviour Methodology
1. **Metrics**: Trip features were aggregated per driver and normalized into exposure-rates (events per 100 driving minutes). Metrics include Hard Braking Rate, Harsh Acceleration Rate, Harsh Cornering Rate, and High-Speed Exposure Ratio.
2. **Thresholds**: EDA established the 5th percentile for hard braking (-25.50 km/h/min) and the 95th percentile for harsh acceleration (+25.40 km/h/min) and cornering.
3. **Normalization**: Rates were min-max scaled to a 0-100 score, capped at the 95th percentile to handle extreme outliers.
4. **Weights**: Final score combines Braking (30%), Acceleration (30%), Cornering (20%), and Speed Behaviour (20%).

## 6. Vehicle Health Methodology
1. **Anomaly Detection**: A trip was flagged as anomalous if its `Trip_Accel_Mag_Mean` exceeded the 90th percentile of all fleet trips.
2. **Persistence**: We assessed the percentage of anomalous trips per vehicle. The 75th percentile of persistence distribution (13.3%) was selected as the threshold.
3. **Cross-Driver Verification**: A vehicle is only recommended for maintenance if its anomalies persist above the threshold *and* occur across multiple distinct drivers, separating vehicle issues from driver behavior.

## 7. Validation
Confounding effects were minimized through strict cross-entity comparisons. For example, Vehicle `V23` might have anomalies, but we ensured those anomalies were reproducible across different drivers before flagging it. Driver scores rely entirely on exposure normalization to prevent drivers with more trips from receiving artificially high risk scores.

## 8. Dashboard Insights
- **Driver Dashboard**: Shows a clear variance in driving styles. The radar chart successfully isolates drivers who speed but brake gently vs. those who drive slowly but corner aggressively.
- **Vehicle Dashboard**: Identifies vehicles with significant vibration persistence. The cross-driver scatter plot quickly highlights mechanically suspect vehicles.

## 9. Assumptions
- 3D magnitude sufficiently proxies forces independent of device orientation.
- The 95th percentile of behavioral metrics captures genuine risk rather than expected variance.

## 10. Limitations
- **Resolution**: 1-minute telemetry sampling misses micro-events (e.g., a 3-second hard stop). Metrics serve as behavioral *proxies*, not instantaneous physical reconstructions.
- **Context**: Lack of speed limits prevents identification of legal "speeding". We measure High-Speed *Exposure* relative to the fleet.

## 11. Additional Applications
- **Insurance Telematics**: Risk scores can map to premium adjustments.
- **Predictive Maintenance**: With historical breakdown data, the Vehicle Health Score could train an ML model for precise time-to-failure prediction.
