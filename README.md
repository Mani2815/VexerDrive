# VexarDrive Data Scientist Assessment

This repository contains the end-to-end implementation of the **VexarDrive Technologies Data Scientist Intern Technical Assessment**.

The project analyzes one week of two-wheeler fleet data to produce:

1. **Driver Behaviour Dashboard** — identifies and scores relative risky vs. safe driving patterns.
2. **Vehicle Health Status Dashboard** — identifies vehicles with persistent abnormal sensor signatures that may warrant maintenance inspection.

## Repository Structure

```text
vexardrive-data-scientist-assessment/
│
├── src/
│   ├── data_processing.py
│   ├── feature_engineering.py
│   ├── driver_scoring.py
│   ├── vehicle_scoring.py
│   └── generate_dashboards.py
│
├── notebooks/
│   └── analysis.py
│
├── outputs/
│   ├── trip_metrics.csv
│   ├── driver_metrics.csv
│   └── vehicle_metrics.csv
│
├── dashboard/
│   ├── driver_dashboard.png
│   └── vehicle_dashboard.png
│
├── report/
│   └── technical_report.md
│
├── README.md
└── requirements.txt
```

## Dataset

The assessment dataset contains:

* 30 drivers
* 30 vehicles
* 450 trips
* Per-minute GPS and IMU telemetry

The original assessment dataset is **not included in this public repository**.

The analytical tables are joined using:

```text
Telemetry.Trip_ID → Trips.Trip_ID
Trips.Driver_ID   → Drivers.Driver_ID
Trips.Vehicle_ID  → Vehicles.Vehicle_ID
```

`Trips.Vehicle_ID` is used as the actual vehicle associated with each trip.

## Methodology Highlights

### Feature Engineering

The analysis uses orientation-independent sensor measures where appropriate:

```text
Accel_Magnitude =
sqrt(Accel_X² + Accel_Y² + Accel_Z²)

Gyro_Magnitude =
sqrt(Gyro_X² + Gyro_Y² + Gyro_Z²)
```

Minute-to-minute speed changes are also used to derive acceleration/deceleration behavioural proxies.

The accelerometer axes are not assumed to represent specific physical directions unless supported by the supplied data documentation.

### Exposure Normalization

Behavioural event metrics are normalized by telemetry exposure and expressed as rates per **100 telemetry minutes** to reduce bias caused by differences in trip duration and observation volume.

### Driver Behaviour Scoring

The Driver Behaviour Risk Score combines four exposure-normalized behavioural components:

* Rapid Deceleration / Braking: **30%**
* Rapid Acceleration: **30%**
* Rotational Behaviour: **20%**
* Speed Behaviour: **20%**

The component scores are normalized using the documented scoring methodology before being combined into the final 0–100 risk score.

### Vehicle Health Analysis

Vehicle anomalies are identified using a fleet-derived acceleration-magnitude threshold.

Vehicle-level persistence is then evaluated across trips. A cross-driver requirement is applied so that an anomaly associated with only one driver's behaviour is not automatically interpreted as a vehicle-specific issue.

The resulting classification represents **maintenance priority based on observed telemetry**, not confirmed mechanical failure.

## Dashboards

### Driver Behaviour Dashboard

![Driver Behaviour Dashboard](dashboard/driver_dashboard.png)

### Vehicle Health Status Dashboard

![Vehicle Health Status Dashboard](dashboard/vehicle_dashboard.png)

## Key Analytical Principles

* Exposure-normalized behavioural metrics
* Data-derived rather than arbitrary thresholds
* Orientation-independent sensor features
* Persistent vehicle anomalies rather than isolated observations
* Cross-driver validation to reduce driver-specific confounding
* Transparent and traceable scoring
* Explicit assumptions and limitations

## Limitations

* The dataset does not provide ground-truth labels for risky or safe drivers.
* The dataset does not provide confirmed mechanical-failure labels.
* Driver Risk Scores therefore represent relative analytical behavioural risk rather than certified safety ratings.
* Vehicle Health Scores represent maintenance priority based on telemetry and should not be interpreted as mechanical diagnoses.
* No unsupported legal speed-limit or "speeding" claims are made.
* Accelerometer axis orientation is not assumed without supporting documentation.

## Reproduction

The assessment dataset is not included in this repository.

Place the provided `dataset.xlsx` at the input location expected by the project scripts, then install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the complete pipeline:

```bash
python3 notebooks/analysis.py
python3 src/driver_scoring.py
python3 src/vehicle_scoring.py
python3 src/generate_dashboards.py
```

Generated analytical outputs will be written to:

```text
outputs/
```

and dashboard images to:

```text
dashboard/
```

The pipeline is designed to run without manual modification of intermediate analytical outputs.

## Interactive Streamlit Deployment

An interactive web dashboard is also available, providing drill-down capabilities for both Driver and Vehicle analytics.

**Live Deployment URL:** `[INSERT_STREAMLIT_COMMUNITY_CLOUD_URL_HERE]`

To run the Streamlit app locally:

1. Ensure the analytical pipeline has been run (which populates the `outputs/` folder).
2. Install the web dependencies: `pip install -r requirements.txt` (which now includes `streamlit` and `plotly`).
3. Launch the app:
   ```bash
   streamlit run app.py
   ```
4. The dashboard will automatically open in your browser, running securely off the pre-computed outputs.

## Technical Report

The detailed methodology, formulas, assumptions, validation, findings, limitations, and additional use cases are documented in:

```text
report/technical_report.md
```

## AI Tools Used Disclosure

AI tools, including **Google Gemini and ChatGPT**, were used as supporting tools during the assessment for project planning, code assistance, debugging, documentation, and review.

The core analytical decisions, methodology selection, validation, interpretation of results, and final submission were reviewed and finalized by the candidate.

The final submission reflects the candidate's own technical judgment and methodology.
