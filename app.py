import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="VexarDrive Assessment Dashboard", layout="wide", page_icon="🛵")

# Ensure paths are relative to app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_data
def load_data():
    driver_path = os.path.join(BASE_DIR, 'outputs/driver_metrics.csv')
    vehicle_path = os.path.join(BASE_DIR, 'outputs/vehicle_metrics.csv')
    
    if not os.path.exists(driver_path) or not os.path.exists(vehicle_path):
        st.error("Could not find the pre-calculated outputs. Please run the analytical pipeline first.")
        st.stop()
        
    df_drivers = pd.read_csv(driver_path)
    df_vehicles = pd.read_csv(vehicle_path)
    return df_drivers, df_vehicles

df_drivers, df_vehicles = load_data()

st.title("VexarDrive Analytical Dashboards")
st.markdown("""
This interactive dashboard presents the results of the **Data Scientist Intern Assessment**. 
It runs entirely off pre-computed analytical metrics, ensuring proprietary raw telemetry data is not exposed at runtime.
""")

tab1, tab2, tab3 = st.tabs(["Driver Behaviour", "Vehicle Health", "Methodology"])

with tab1:
    st.header("Driver Behaviour Dashboard")
    st.markdown("*User Question: Who shows the highest-risk driving behaviour and what behaviours contribute to the score?*")
    
    # KPIs
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric("Total Drivers", len(df_drivers))
    kpi2.metric("Fleet Avg Risk Score", f"{df_drivers['Driver_Risk_Score'].mean():.1f}")
    kpi3.metric("Safe Drivers", len(df_drivers[df_drivers['Risk_Classification'] == 'Safe']))
    kpi4.metric("Moderate Drivers", len(df_drivers[df_drivers['Risk_Classification'] == 'Moderate']))
    kpi5.metric("Risky Drivers", len(df_drivers[df_drivers['Risk_Classification'] == 'Risky']))
    
    st.divider()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Driver Risk Ranking")
        # Bar chart
        fig_bar = px.bar(
            df_drivers.sort_values('Driver_Risk_Score', ascending=True),
            x='Driver_Risk_Score', y='Driver_ID', color='Risk_Classification',
            color_discrete_map={'Safe': 'green', 'Moderate': 'orange', 'Risky': 'red'},
            orientation='h', height=500, title="Risk Scores by Driver"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col2:
        st.subheader("Risk Score Distribution")
        fig_hist = px.histogram(df_drivers, x="Driver_Risk_Score", nbins=10, 
                                color="Risk_Classification", 
                                color_discrete_map={'Safe': 'green', 'Moderate': 'orange', 'Risky': 'red'},
                                title="Distribution of Driver Scores")
        st.plotly_chart(fig_hist, use_container_width=True)
        
    st.divider()
    st.subheader("Driver Drill-Down")
    
    selected_driver = st.selectbox("Select a Driver to inspect:", df_drivers['Driver_ID'].sort_values())
    driver_data = df_drivers[df_drivers['Driver_ID'] == selected_driver].iloc[0]
    
    st.markdown(f"**Driver:** {driver_data['Driver_Name']} | **Classification:** {driver_data['Risk_Classification']} | **Total Risk Score:** {driver_data['Driver_Risk_Score']:.1f}")
    
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        # Radar Chart
        categories = ['Braking_Subscore', 'Accel_Subscore', 'Corner_Subscore', 'Speed_Subscore']
        labels = ['Hard Braking', 'Harsh Acceleration', 'Harsh Cornering', 'High-Speed Exposure']
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=[driver_data[c] for c in categories] + [driver_data[categories[0]]],
            theta=labels + [labels[0]],
            fill='toself',
            name=selected_driver
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            title=f"Behaviour Contribution for {selected_driver}"
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        
    with d_col2:
        st.markdown("### Component Metrics")
        st.dataframe(pd.DataFrame({
            "Metric (per 100 min)": ["Hard Braking Rate", "Harsh Accel Rate", "Harsh Corner Rate", "High Speed Ratio"],
            "Raw Rate": [
                f"{driver_data['Hard_Braking_Rate']:.2f}",
                f"{driver_data['Harsh_Accel_Rate']:.2f}",
                f"{driver_data['Harsh_Corner_Rate']:.2f}",
                f"{driver_data['High_Speed_Ratio']:.2f}"
            ],
            "Normalized Subscore (0-100)": [
                f"{driver_data['Braking_Subscore']:.1f}",
                f"{driver_data['Accel_Subscore']:.1f}",
                f"{driver_data['Corner_Subscore']:.1f}",
                f"{driver_data['Speed_Subscore']:.1f}"
            ]
        }), hide_index=True)


with tab2:
    st.header("Vehicle Health Status Dashboard")
    st.markdown("*User Question: Which vehicles require attention and is the abnormality persistent?*")
    
    # KPIs
    vkpi1, vkpi2, vkpi3, vkpi4, vkpi5 = st.columns(5)
    vkpi1.metric("Total Vehicles", len(df_vehicles))
    vkpi2.metric("Fleet Avg Health Score", f"{df_vehicles['Health_Risk_Score'].mean():.1f}")
    vkpi3.metric("Healthy", len(df_vehicles[df_vehicles['Health_Classification'] == 'Healthy']))
    vkpi4.metric("Monitor", len(df_vehicles[df_vehicles['Health_Classification'] == 'Monitor']))
    vkpi5.metric("Maintenance", len(df_vehicles[df_vehicles['Health_Classification'] == 'Maintenance Recommended']))
    
    st.divider()
    
    vcol1, vcol2 = st.columns([2, 1])
    with vcol1:
        st.subheader("Vehicle Health Ranking")
        fig_vbar = px.bar(
            df_vehicles.sort_values('Health_Risk_Score', ascending=True),
            x='Health_Risk_Score', y='Vehicle_ID', color='Health_Classification',
            color_discrete_map={'Healthy': 'green', 'Monitor': 'orange', 'Maintenance Recommended': 'red'},
            orientation='h', height=500, title="Health Risk by Vehicle"
        )
        st.plotly_chart(fig_vbar, use_container_width=True)
        
    with vcol2:
        st.subheader("Anomaly Persistence vs Odometer")
        fig_vscatter = px.scatter(
            df_vehicles, x="Odometer_KM_Start_of_Week", y="Persistence_Pct",
            color="Health_Classification", size="Total_Trips",
            color_discrete_map={'Healthy': 'green', 'Monitor': 'orange', 'Maintenance Recommended': 'red'},
            hover_data=['Vehicle_ID']
        )
        st.plotly_chart(fig_vscatter, use_container_width=True)
        
    st.divider()
    st.subheader("Vehicle Drill-Down")
    
    selected_vehicle = st.selectbox("Select a Vehicle to inspect:", df_vehicles['Vehicle_ID'].sort_values())
    vehicle_data = df_vehicles[df_vehicles['Vehicle_ID'] == selected_vehicle].iloc[0]
    
    if vehicle_data['Health_Classification'] == 'Maintenance Recommended':
        st.error(f"⚠️ **Maintenance Recommended** for {selected_vehicle} (Score: {vehicle_data['Health_Risk_Score']:.1f})")
    elif vehicle_data['Health_Classification'] == 'Monitor':
        st.warning(f"⚠️ **Monitor** {selected_vehicle} (Score: {vehicle_data['Health_Risk_Score']:.1f})")
    else:
        st.success(f"✅ {selected_vehicle} is **Healthy** (Score: {vehicle_data['Health_Risk_Score']:.1f})")
        
    st.markdown("### Sensor Anomaly Evidence")
    ev_col1, ev_col2, ev_col3, ev_col4 = st.columns(4)
    ev_col1.metric("Total Trips Evaluated", vehicle_data['Total_Trips'])
    ev_col2.metric("Trips with Sensor Anomaly", vehicle_data['Anomalous_Trips'])
    ev_col3.metric("Anomaly Persistence", f"{vehicle_data['Persistence_Pct']:.1f}%", help="Threshold is 13.3%")
    ev_col4.metric("Unique Drivers w/ Anomaly", vehicle_data['Drivers_With_Anomaly'], help="Must be > 1 to rule out driver bias")

with tab3:
    st.header("Methodology & Assumptions")
    st.markdown("""
    ### Driver Scoring
    We evaluated Driver Risk using **exposure-normalized rates** (events per 100 telemetry minutes).
    The final score is a weighted combination of:
    - **Rapid Deceleration** (30% weight)
    - **Harsh Acceleration** (30% weight)
    - **Rotational Behaviour** (20% weight)
    - **High-Speed Exposure** (20% weight)
    
    *Note: We do not assert legal 'Speeding' violations, as no speed limit data was provided. We proxy high-speed exposure relative to the fleet.*
    
    ### Vehicle Scoring
    Vehicle anomalies were identified by comparing each trip's `Accel_Magnitude` to the fleet's 90th percentile threshold (1.046g). 
    A vehicle is flagged for Maintenance if:
    1. **Persistence**: Anomalies occur in >13.3% of its trips (the fleet's 75th percentile).
    2. **Cross-Driver Validation**: The anomalies occur across multiple distinct drivers. This critically prevents us from penalizing a vehicle for the harsh driving style of a single assigned driver.
    
    ### Tech Stack
    This interactive layer is built with **Streamlit** and **Plotly**.
    """)
