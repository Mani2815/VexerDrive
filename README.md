# VexarDrive Data Scientist Assessment

This repository contains the end-to-end implementation for the VexarDrive Data Scientist Intern Assessment. 

## Structure
- `src/`: Core Python modules for data processing, feature engineering, and scoring.
- `notebooks/`: `analysis.py` containing the EDA and threshold derivations.
- `outputs/`: Generated CSVs containing aggregated metrics and scores.
- `dashboard/`: Exported PNG images of the final analytical dashboards.
- `report/`: Technical report outlining methodologies, assumptions, and limitations.

## Methodology Highlights
1. **Feature Engineering**: Calculates orientation-independent magnitudes (`Accel_Magnitude`, `Gyro_Magnitude`) and utilizes minute-to-minute speed deltas to proxy behavioral events.
2. **Exposure Normalization**: All driver metrics are evaluated as per-minute rates to prevent volume-bias.
3. **Cross-Entity Validation**: Vehicle anomalies are verified across multiple drivers to prevent driver-behavior confounding.

## Dashboards
![Driver Behaviour Dashboard](dashboard/driver_dashboard.png)
![Vehicle Health Dashboard](dashboard/vehicle_dashboard.png)

## How to Reproduce
1. Place `dataset.xlsx` in the root directory (outside the repo folder, e.g. `../dataset.xlsx` relative to `src/`).
2. Install requirements: `pip install -r requirements.txt` (or manually install pandas, numpy, matplotlib, seaborn, openpyxl).
3. Run the pipeline:
   ```bash
   python3 notebooks/analysis.py
   python3 src/driver_scoring.py
   python3 src/vehicle_scoring.py
   python3 src/generate_dashboards.py
   ```
4. Output CSVs will be available in `outputs/` and dashboard images in `dashboard/`.

## AI Tools Used Disclosure
AI tools (Google Gemini) were used during this assessment strictly as a coding assistant. Specifically, AI was used to assist with initial project planning, code scaffolding, and writing matplotlib boilerplate. All core analytical decisions—such as the choice to use empirical thresholds (like the 75th percentile for persistence), the decision to require cross-driver anomaly reproduction, the formulation of orientation-independent magnitudes, and the interpretation of results—were driven, reviewed, and finalized by the candidate. The final submission reflects my own technical judgement and methodology.
