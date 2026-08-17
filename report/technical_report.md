# VexarDrive Data Scientist Intern Assessment
## Final Technical Report

## 1. Executive Summary

This project analyzes a week of telematics data (GPS + IMU) for 30 drivers and 30 vehicles across 450 trips. The primary deliverables are a data-driven **Driver Behaviour Risk Score** and a **Vehicle Health Score**. Our analysis successfully identified specific extreme events (rapid deceleration, rapid acceleration, high rotational-movement) using empirical thresholds derived from Exploratory Data Analysis (EDA). The final dashboards effectively distinguish relative behavioural risk classifications and identify vehicles exhibiting persistent abnormal sensor signatures that may warrant maintenance inspection. 

Importantly, the generated scores represent relative analytical indicators derived from telemetry and are not externally certified safety ratings or confirmed mechanical-failure diagnoses.

## 2. Dataset Overview

- **Drivers**: 30 records
- **Vehicles**: 30 records
- **Trips**: 450 records (15 trips per driver)
- **Telemetry**: ~12,987 minute-by-minute observations combining GPS coordinates, speed, and IMU data (accelerometer and gyroscope).
- **Data Quality**: After correcting the workbook's header formatting (handling null offsets) and validating data types and relationships, no missing values or corrupt records affecting the analytical metrics were identified. 

The analytical tables are joined using the following mapping, where `Trips.Vehicle_ID` represents the actual vehicle associated with each trip:
- `Telemetry.Trip_ID → Trips.Trip_ID`
- `Trips.Driver_ID → Drivers.Driver_ID`
- `Trips.Vehicle_ID → Vehicles.Vehicle_ID`

## 3. Feature Engineering

The raw data lacked explicit orientation information for the IMU sensors and official speed limits. To ensure robustness, we utilized orientation-independent magnitudes:

**Orientation-independent acceleration magnitude**
```text
Accel_Magnitude = sqrt(Accel_X_g² + Accel_Y_g² + Accel_Z_g²)
```
This provides an orientation-independent measure of the combined accelerometer magnitude. Because the accelerometer includes gravitational and motion components and no device orientation calibration is provided, it is treated as a sensor-motion indicator rather than a direct measurement of mechanical vibration or physical force.

**Orientation-independent rotational magnitude**
```text
Gyro_Magnitude = sqrt(Gyro_X_dps² + Gyro_Y_dps² + Gyro_Z_dps²)
```
This acts as an orientation-independent rotational-movement indicator.

**Minute Speed Change**
Minute-to-minute speed changes are used as behavioural acceleration/deceleration proxies. They do not represent instantaneous physical acceleration.

## 4. Driver Behaviour Methodology

### 4.1 Behavioural Metrics
Trip features were aggregated per driver and normalized into exposure-rates (events per 100 telemetry minutes) to reduce bias caused by differences in trip duration and observation volume. Metrics include:
- Rapid Deceleration Events
- Rapid Acceleration Events
- High Rotational-Movement Events
- High-Speed Exposure

### 4.2 Driver Thresholds
Because the assessment does not provide official operational thresholds, empirical thresholds were derived from the observed telemetry distribution. These thresholds are dataset-relative analytical thresholds rather than industry-standard safety limits:
- Rapid deceleration threshold: `-25.50 km/h/min`
- Rapid acceleration threshold: `+25.40 km/h/min`
- Rotational/Cornering threshold: `7.58 dps`

### 4.3 Driver Score Formula
Rates are transformed into normalized 0–100 subscores. The actual implementation caps the rate at the 95th percentile to limit excessive influence from extreme observations while preserving relative differences across drivers, and then applies min-max scaling to 100:

```text
Score_Raw = 100 × (Rate / P95)
Score = min(Score_Raw, 100)
```

The Driver Behaviour Risk Score is then calculated using the exact formula:

```text
Driver Risk Score =
0.30 × Braking/Deceleration Subscore
+ 0.30 × Acceleration Subscore
+ 0.20 × Corner/Rotation Subscore
+ 0.20 × Speed Behaviour Subscore
```

### 4.4 Driver Classification
The risk classification uses tertiles relative to the observed fleet and should not be interpreted as externally certified safety thresholds:
- **Safe**: lower third of the driver-score distribution
- **Moderate**: middle third of the driver-score distribution
- **Risky**: upper third of the driver-score distribution

### 4.5 Driver Traceability Example
Driver D01 displays the following unrounded components:
- Braking = 27.427
- Acceleration = 22.066
- Corner = 82.961
- Speed = 34.915

```text
Risk Score =
(27.427 × 0.30)
+ (22.066 × 0.30)
+ (82.961 × 0.20)
+ (34.915 × 0.20)
```
The final score is `38.42`. Note that the final score is calculated using the underlying unrounded values, though displayed metrics may be rounded for readability.

## 5. Vehicle Health / Maintenance Priority Methodology

The objective is to identify vehicles with persistent abnormal sensor signatures that may warrant inspection.

### 5.1 Vehicle Anomaly Threshold
Trips are evaluated against the following validated threshold:
```text
Trip_Accel_Mag_Mean > 1.046 g
```
1.046 g corresponds to the 90th percentile of the fleet-level distribution of trip-level mean acceleration magnitude. Trips above this threshold exhibit unusually high average acceleration magnitude relative to the observed fleet.

### 5.2 Vehicle Persistence
Vehicle anomalies are evaluated across their entire trip history using the formula:
```text
Persistence (%) = Anomalous Trips / Total Trips × 100
```
```text
Persistence Threshold = 13.33%
```
The 13.33% threshold corresponds to the 75th percentile of the observed vehicle-level anomalous-trip persistence distribution. This is a fleet-relative, dataset-derived analytical threshold and is not an industry-standard maintenance threshold.

### 5.3 Cross-Driver Verification
The classification logic strictly applies the following rule:
```text
IF
Persistence > 13.33%
AND
Drivers_With_Anomaly > 1

THEN
Maintenance Recommended
```
Otherwise, a high-persistence anomaly associated with only one driver is downgraded to: **Monitor**

Requiring anomaly evidence across multiple drivers reduces the likelihood that driver-specific behaviour is incorrectly attributed to the vehicle.

### 5.4 Example of Cross-Driver Validation
**Vehicle V02**
- 16 total trips, 8 anomalous trips
- Persistence = 50%
- 2 drivers with anomalies
- Persistence > 13.33%
- Drivers with anomaly > 1
- Classification = **Maintenance Recommended**

**Vehicle V19**
- 16 total trips, 7 anomalous trips
- Persistence = 43.75%
- Anomalies associated with only 1 driver
- Persistence > 13.33%
- Cross-driver condition not satisfied
- Classification = **Monitor**

This demonstrates that the vehicle score does not simply equate anomaly frequency with mechanical problems.

## 6. Validation

**Data validation:** 
- Row counts, table joins, and relationships were programmatically validated. 
- Type casting prevented strings in numerical fields. 

**Score validation:** 
- Subscore domains successfully bounded between 0 and 100.
- All driver scores properly undergo exposure normalization to negate the impact of differing trip durations.

**Vehicle validation:**
- Persistence and multiple-trip evidence successfully enforce that anomalies are recurring patterns and not isolated instances.
- The cross-driver condition effectively downgrades vehicles driven solely by aggressive drivers.

**Dashboard validation:**
- All numbers natively trace back to generated CSV outputs. No manually entered analytical values are present.

## 7. Assumptions

1. Accelerometer axis orientation is unknown.
2. 3D accelerometer magnitude is used as an orientation-independent sensor-motion indicator.
3. Minute-level speed differences are behavioural proxies rather than instantaneous acceleration measurements.
4. Official speed limits are unavailable.
5. Behavioural thresholds are empirical and dataset-relative.
6. Vehicle anomaly thresholds are fleet-relative and dataset-derived.
7. Cross-driver persistence reduces but does not eliminate driver-specific confounding.
8. Risk/health scores are relative analytical indicators.

## 8. Limitations

- **Temporal resolution**: One-minute telemetry cannot reconstruct short-duration events.
- **Ground truth**: There are no confirmed risky-driver labels, accident outcomes, mechanical-failure labels, or maintenance failure labels. Therefore the scores are not supervised predictions or confirmed diagnoses.
- **Context**: No speed limits, road type, weather, traffic, road gradient, or route context.
- **Sensor orientation**: No phone mounting/orientation calibration.
- **Vehicle diagnosis**: Sensor anomalies may have multiple causes and require inspection/maintenance data for confirmation.

## 9. Dashboard Insights

- **Driver Dashboard**: Enables visual identification of varied driving styles, isolating drivers who show high-speed exposure but rapid deceleration vs. those who drive slowly but exhibit high rotational-movement.
- **Vehicle Dashboard**: Identifies vehicles with persistent acceleration-magnitude anomalies and telemetry patterns that warrant maintenance inspection. The cross-driver scatter plot quickly highlights these vehicles against those flagged merely due to a single assigned driver.

## 10. Additional Applications

- **Insurance Telematics**: Behavioural indicators could support future insurance-risk analysis after validation against accident and claims outcomes and subject to appropriate regulatory and actuarial requirements.
- **Predictive Maintenance**: With historical maintenance, breakdown, and component-replacement labels, the telemetry features could support supervised predictive-maintenance models and time-to-failure estimation.
- **Other Uses**: Driver coaching, Fleet safety monitoring, Route-risk analysis, Maintenance prioritization, Anomaly monitoring, Operational fleet optimization.

## 11. Methodology Summary

| Component | Metric               | Method                          | Output                   |
| --------- | -------------------- | ------------------------------- | ------------------------ |
| Driver    | Rapid deceleration   | Empirical percentile threshold  | Exposure-normalized rate |
| Driver    | Rapid acceleration   | Empirical percentile threshold  | Exposure-normalized rate |
| Driver    | Rotational movement  | Empirical threshold             | Exposure-normalized rate |
| Driver    | Speed behaviour      | Fleet-relative exposure         | Normalized score         |
| Driver    | Overall risk         | 30/30/20/20 weighted score      | 0–100                    |
| Vehicle   | Acceleration anomaly | 90th percentile                 | Trip anomaly flag        |
| Vehicle   | Persistence          | Anomalous trips / total trips   | Percentage               |
| Vehicle   | Maintenance priority | Persistence + cross-driver rule | Classification           |

