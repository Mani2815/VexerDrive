import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

def generate_driver_dashboard(driver_metrics_path, output_path):
    df = pd.read_csv(driver_metrics_path)
    
    # Setup Figure
    fig = plt.figure(figsize=(15, 10))
    fig.text(0.5, 0.96, 'Driver Behaviour Dashboard', fontsize=24, fontweight='bold', ha='center')
    fig.text(0.5, 0.92, 'User Question: Who shows the highest-risk driving behaviour and what behaviours contribute to the score?', ha='center', fontsize=14, style='italic', color='dimgrey')
    
    # --- KPIs ---
    total_drivers = len(df)
    avg_score = df['Driver_Risk_Score'].mean()
    safe = len(df[df['Risk_Classification'] == 'Safe'])
    moderate = len(df[df['Risk_Classification'] == 'Moderate'])
    risky = len(df[df['Risk_Classification'] == 'Risky'])
    
    fig.text(0.1, 0.87, f'Total Drivers: {total_drivers}', fontsize=14)
    fig.text(0.3, 0.87, f'Safe: {safe} | Moderate: {moderate} | Risky: {risky}', fontsize=14)
    fig.text(0.7, 0.87, f'Fleet Avg Risk Score: {avg_score:.1f}', fontsize=14, fontweight='bold')
    
    # --- Grid ---
    ax1 = plt.subplot(2, 2, 1)
    ax2 = plt.subplot(2, 2, 2, polar=True)
    ax3 = plt.subplot(2, 2, 3)
    ax4 = plt.subplot(2, 2, 4)
    
    # 1. Bar Chart: Top 10 Riskiest Drivers
    top_risky = df.sort_values(by='Driver_Risk_Score', ascending=False).head(10)
    sns.barplot(x='Driver_Risk_Score', y='Driver_ID', data=top_risky, ax=ax1, palette='Reds_r', hue='Driver_ID', legend=False)
    ax1.set_title('Top 10 Riskiest Drivers')
    ax1.set_xlabel('Risk Score (0-100)')
    ax1.set_ylabel('Driver ID')
    
    # 2. Radar Chart: Behaviour Contribution for the riskiest driver
    riskiest_driver = top_risky.iloc[0]
    categories = ['Braking_Subscore', 'Accel_Subscore', 'Corner_Subscore', 'Speed_Subscore']
    labels = ['Braking', 'Acceleration', 'Cornering', 'Speed Behaviour']
    values = riskiest_driver[categories].values.flatten().tolist()
    values += values[:1] # close the loop
    angles = [n / float(len(categories)) * 2 * np.pi for n in range(len(categories))]
    angles += angles[:1]
    
    ax2.plot(angles, values, linewidth=2, linestyle='solid', label=f"Driver {riskiest_driver['Driver_ID']}")
    ax2.fill(angles, values, 'r', alpha=0.1)
    ax2.set_xticks(angles[:-1])
    ax2.set_xticklabels(labels)
    ax2.set_title(f"Behaviour Contribution: Riskiest Driver ({riskiest_driver['Driver_ID']})")
    ax2.set_ylim(0, 100)
    
    # 3. Scatter: Speed Behaviour vs Risk Score
    sns.scatterplot(x='Speed_Subscore', y='Driver_Risk_Score', hue='Risk_Classification', data=df, ax=ax3, palette={'Safe':'green', 'Moderate':'orange', 'Risky':'red'})
    ax3.set_title('Speed Behaviour vs Risk Score')
    ax3.set_xlabel('High-Speed Exposure Score')
    ax3.set_ylabel('Total Risk Score')
    
    # 4. Table: Drill down
    ax4.axis('tight')
    ax4.axis('off')
    # Update to include subscores
    table_data = df.sort_values('Driver_Risk_Score', ascending=False)[['Driver_ID', 'Braking_Subscore', 'Accel_Subscore', 'Corner_Subscore', 'Speed_Subscore', 'Driver_Risk_Score', 'Risk_Classification']].head(10)
    table_data[['Braking_Subscore', 'Accel_Subscore', 'Corner_Subscore', 'Speed_Subscore']] = table_data[['Braking_Subscore', 'Accel_Subscore', 'Corner_Subscore', 'Speed_Subscore']].round(1)
    # Rename columns for space
    table_data.columns = ['ID', 'Braking', 'Accel', 'Corner', 'Speed', 'Total', 'Class']
    table = ax4.table(cellText=table_data.values, colLabels=table_data.columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.8)
    table.auto_set_column_width(col=list(range(len(table_data.columns))))
    ax4.set_title('Drill Down: Top Drivers')
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.85])
    plt.savefig(output_path)
    plt.close()
    print(f"Driver Dashboard saved to {output_path}")

def generate_vehicle_dashboard(vehicle_metrics_path, output_path):
    df = pd.read_csv(vehicle_metrics_path)
    
    fig = plt.figure(figsize=(15, 10))
    fig.text(0.5, 0.96, 'Vehicle Health Status Dashboard', fontsize=24, fontweight='bold', ha='center')
    fig.text(0.5, 0.92, 'User Question: Which vehicles require attention and is the abnormality persistent?', ha='center', fontsize=14, style='italic', color='dimgrey')
    
    # --- KPIs ---
    total_vehicles = len(df)
    avg_score = df['Health_Risk_Score'].mean()
    healthy = len(df[df['Health_Classification'] == 'Healthy'])
    monitor = len(df[df['Health_Classification'] == 'Monitor'])
    maintenance = len(df[df['Health_Classification'] == 'Maintenance Recommended'])
    
    fig.text(0.1, 0.87, f'Total Vehicles: {total_vehicles}', fontsize=14)
    fig.text(0.3, 0.87, f'Healthy: {healthy} | Monitor: {monitor} | Maintenance: {maintenance}', fontsize=14)
    fig.text(0.7, 0.87, f'Fleet Avg Health Score: {avg_score:.1f}', fontsize=14, fontweight='bold')
    
    # --- Grid ---
    ax1 = plt.subplot(2, 2, 1)
    ax2 = plt.subplot(2, 2, 2)
    ax3 = plt.subplot(2, 2, 3)
    ax4 = plt.subplot(2, 2, 4)
    
    # 1. Bar Chart: Top Maintenance Needed
    top_maintenance = df.sort_values(by='Health_Risk_Score', ascending=False).head(10)
    sns.barplot(x='Health_Risk_Score', y='Vehicle_ID', data=top_maintenance, ax=ax1, palette='OrRd_r', hue='Vehicle_ID', legend=False)
    ax1.set_title('Top 10 Vehicles by Health Risk')
    ax1.set_xlabel('Health Risk Score (0-100)')
    ax1.set_ylabel('Vehicle ID')
    
    # 2. Scatter: Odometer vs Health Score
    sns.scatterplot(x='Odometer_KM_Start_of_Week', y='Health_Risk_Score', hue='Health_Classification', data=df, ax=ax2, palette={'Healthy':'green', 'Monitor':'orange', 'Maintenance Recommended':'red'})
    ax2.set_title('Health Score vs Odometer')
    ax2.set_xlabel('Odometer (KM)')
    ax2.set_ylabel('Health Risk Score')
    
    # 3. Scatter: Persistence vs Drivers With Anomaly (Cross-driver check)
    sns.scatterplot(x='Drivers_With_Anomaly', y='Persistence_Pct', hue='Health_Classification', size='Total_Trips', sizes=(20, 200), data=df, ax=ax3, palette={'Healthy':'green', 'Monitor':'orange', 'Maintenance Recommended':'red'})
    ax3.set_title('Anomaly Persistence vs Cross-Driver Consistency')
    ax3.set_xlabel('Number of Unique Drivers Experiencing Anomaly')
    ax3.set_ylabel('Anomaly Persistence (%)')
    
    # 4. Table: Drill down
    ax4.axis('tight')
    ax4.axis('off')
    table_data = df.sort_values('Health_Risk_Score', ascending=False)[['Vehicle_ID', 'Health_Risk_Score', 'Persistence_Pct', 'Drivers_With_Anomaly', 'Health_Classification']].head(10)
    table_data['Persistence_Pct'] = table_data['Persistence_Pct'].round(1).astype(str) + '%'
    table = ax4.table(cellText=table_data.values, colLabels=['ID', 'Score', 'Persistence', 'Anomaly Drivers', 'Status'], loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.8)
    table.auto_set_column_width(col=list(range(len(table_data.columns))))
    ax4.set_title('Drill Down: Critical Vehicles')
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.85])
    plt.savefig(output_path)
    plt.close()
    print(f"Vehicle Dashboard saved to {output_path}")

if __name__ == "__main__":
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    generate_driver_dashboard(os.path.join(repo_root, 'outputs/driver_metrics.csv'), os.path.join(repo_root, 'dashboard/driver_dashboard.png'))
    generate_vehicle_dashboard(os.path.join(repo_root, 'outputs/vehicle_metrics.csv'), os.path.join(repo_root, 'dashboard/vehicle_dashboard.png'))
