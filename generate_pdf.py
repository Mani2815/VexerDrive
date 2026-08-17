import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def generate():
    output_path = os.path.join("report", "Technical_Report.pdf")
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=1*inch,
        leftMargin=1*inch,
        topMargin=1*inch,
        bottomMargin=1*inch
    )

    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=26,
        spaceAfter=20,
        textColor=colors.HexColor('#2c3e50'),
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=20,
        spaceAfter=30,
        textColor=colors.HexColor('#3498db'),
        alignment=TA_CENTER
    )
    
    h1_style = ParagraphStyle(
        'H1Style',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        spaceBefore=20,
        spaceAfter=10,
        textColor=colors.HexColor('#2c3e50')
    )
    
    h2_style = ParagraphStyle(
        'H2Style',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        spaceBefore=15,
        spaceAfter=5,
        textColor=colors.HexColor('#34495e')
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#333333')
    )
    
    center_body_style = ParagraphStyle(
        'CenterBodyStyle',
        parent=body_style,
        alignment=TA_CENTER
    )
    
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=9,
        leading=14,
        backColor=colors.HexColor('#f9f9f9'),
        borderColor=colors.HexColor('#dddddd'),
        borderWidth=1,
        borderPadding=10,
        textColor=colors.HexColor('#333333')
    )
    
    elements = []
    
    # Page 1: Cover
    elements.append(Spacer(1, 2*inch))
    elements.append(Paragraph("VEXARDRIVE TECHNOLOGIES", title_style))
    elements.append(Paragraph("Data Scientist Intern Assessment", subtitle_style))
    elements.append(Paragraph("<b>Technical Analysis Report</b><br/>Driver Behaviour Risk & Vehicle Health Analytics", center_body_style))
    elements.append(Spacer(1, 1*inch))
    
    elements.append(Paragraph("30 Drivers<br/>30 Vehicles<br/>450 Trips<br/>GPS + IMU Telemetry", center_body_style))
    elements.append(Spacer(1, 1*inch))
    
    elements.append(Paragraph("Prepared for: VexarDrive Technologies<br/>Assessment: Data Scientist Intern", center_body_style))
    elements.append(PageBreak())
    
    # Page 2: Executive Summary
    elements.append(Paragraph("Executive Summary", h1_style))
    elements.append(Paragraph("Objective", h2_style))
    elements.append(Paragraph("This project analyzes a week of telematics data (GPS + IMU) to produce a data-driven <b>Driver Behaviour Risk Score</b> and a <b>Vehicle Health Score</b>.", body_style))
    
    elements.append(Paragraph("Analytical Approach", h2_style))
    elements.append(Paragraph("Our analysis identified specific extreme events (rapid deceleration, rapid acceleration, high rotational-movement, and high-speed exposure) using empirical thresholds derived from Exploratory Data Analysis (EDA). Because official operational bounds and speed limits were unavailable, the methodology relies on dataset-relative thresholds and exposure-normalized rates to fairly evaluate behaviour.", body_style))
    
    elements.append(Paragraph("Key Outputs", h2_style))
    elements.append(Paragraph("- 30 Drivers<br/>- 30 Vehicles<br/>- 450 Trips<br/>- ~12,987 Telemetry Records", body_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("The final dashboards successfully distinguish relative behavioural risk classifications and identify vehicles exhibiting persistent abnormal sensor signatures that may warrant maintenance inspection.", body_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Importantly, the generated scores represent relative analytical indicators derived from telemetry and are not externally certified safety ratings or confirmed mechanical-failure diagnoses.", body_style))
    elements.append(PageBreak())
    
    # Page 3: Architecture
    elements.append(Paragraph("Data & Analytical Architecture", h1_style))
    elements.append(Paragraph("Table Relationships", h2_style))
    elements.append(Paragraph("The analytical tables are structurally joined using the following mapping:", body_style))
    elements.append(Spacer(1, 10))
    
    map_txt = """Drivers -> Trips (Driver_ID)<br/>
Vehicles -> Trips (Vehicle_ID)<br/>
Trips -> Telemetry (Trip_ID)"""
    elements.append(Paragraph(map_txt, code_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<i>Trips.Vehicle_ID</i> represents the actual vehicle associated with each trip.", body_style))
    
    elements.append(Paragraph("Dataset Quality", h2_style))
    elements.append(Paragraph("After correcting the workbook's header formatting (handling null offsets) and validating data types and relationships, no missing values or corrupt records affecting the analytical metrics were identified.", body_style))
    elements.append(PageBreak())
    
    # Page 4: Feature Engineering
    elements.append(Paragraph("Feature Engineering", h1_style))
    elements.append(Paragraph("The raw data lacked explicit orientation information for the IMU sensors and official speed limits. To ensure robustness, we utilized three core engineered features:", body_style))
    
    elements.append(Paragraph("Acceleration Magnitude", h2_style))
    elements.append(Paragraph("Accel_Magnitude = &radic;(Accel_X_g&sup2; + Accel_Y_g&sup2; + Accel_Z_g&sup2;)", code_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<b>Purpose:</b> Provides an orientation-independent measure of the combined accelerometer magnitude.", body_style))
    elements.append(Paragraph("<b>Interpretation:</b> Because the accelerometer includes gravitational and motion components and no device orientation calibration is provided, it is treated as a sensor-motion indicator rather than a direct measurement of mechanical vibration or physical force.", body_style))

    elements.append(Paragraph("Gyroscope Magnitude", h2_style))
    elements.append(Paragraph("Gyro_Magnitude = &radic;(Gyro_X_dps&sup2; + Gyro_Y_dps&sup2; + Gyro_Z_dps&sup2;)", code_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<b>Purpose:</b> Acts as an orientation-independent rotational-movement indicator.", body_style))
    elements.append(Paragraph("<b>Interpretation:</b> Measures the intensity of rotational forces during cornering or swerving.", body_style))

    elements.append(Paragraph("Minute Speed Change", h2_style))
    elements.append(Paragraph("Speed_Change_per_min = Speed_kmph(t) - Speed_kmph(t-1)", code_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<b>Purpose:</b> Used to proxy acceleration and deceleration events.", body_style))
    elements.append(Paragraph("<b>Limitation:</b> Minute-to-minute speed changes are behavioural proxies. They do not represent instantaneous physical acceleration.", body_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<b>Important Interpretation Note:</b> Sensor-derived values are analytical proxies and should not be interpreted as direct mechanical measurements.", body_style))
    elements.append(PageBreak())
    
    # Page 5: Driver Behaviour
    elements.append(Paragraph("Driver Behaviour Methodology", h1_style))
    
    elements.append(Paragraph("1. Behavioural Metrics", h2_style))
    elements.append(Paragraph("Trip features were aggregated per driver and normalized into <b>exposure-rates</b> (events per 100 telemetry minutes) to reduce bias caused by differences in trip duration and observation volume.", body_style))
    
    elements.append(Paragraph("2. Thresholds", h2_style))
    elements.append(Paragraph("Because the assessment does not provide official operational thresholds, empirical thresholds were derived from the observed telemetry distribution. These thresholds are dataset-relative analytical thresholds rather than industry-standard safety limits:", body_style))
    elements.append(Paragraph("- Rapid deceleration threshold: -25.50 km/h/min<br/>- Rapid acceleration threshold: +25.40 km/h/min<br/>- Rotational/Cornering threshold: 7.58 dps", body_style))

    elements.append(Paragraph("3. High-Speed Exposure", h2_style))
    elements.append(Paragraph("Because no external speed-limit information is available, we evaluate fleet-relative high-speed exposure.", body_style))
    elements.append(Paragraph("- <b>Source variable:</b> Speed_kmph<br/>- <b>Exact threshold:</b> > 40 km/h<br/>- <b>Event definition:</b> A telemetry minute where the speed strictly exceeds 40 km/h.<br/>- <b>Aggregation:</b> Total minutes spent above 40 km/h per driver.<br/>- <b>Exposure normalization:</b> Ratio of high-speed minutes to total driving minutes.", body_style))

    elements.append(Paragraph("4. P95-Relative Normalization", h2_style))
    elements.append(Paragraph("Rates are transformed into normalized 0-100 subscores relative to the 95th-percentile reference value (P95). This limits the influence of extreme observations while preserving relative differences.", body_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Score_Raw = 100 &times; (Rate / P95)<br/>Score = min(Score_Raw, 100)", code_style))
    elements.append(PageBreak())

    # Page 6: Traceability
    elements.append(Paragraph("Driver Score & Traceability", h1_style))
    elements.append(Paragraph("5. Weighted Score", h2_style))
    weights_txt = "Braking / Deceleration: 30%<br/>Acceleration: 30%<br/>Corner / Rotation: 20%<br/>Speed Behaviour: 20%<br/>Total: 100%"
    elements.append(Paragraph(weights_txt, code_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("The weighted structure combines multiple behavioural dimensions while preventing any single metric from completely determining the overall classification. These are the analytical weightings selected for this assessment, not an industry-standard constraint.", body_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("RiskScore = 0.30B + 0.30A + 0.20C + 0.20S<br/><i>(Where B, A, C, and S are the 0-100 normalized subscores)</i>", code_style))

    elements.append(Paragraph("Traceability Example: Driver D01", h2_style))
    trace_txt = """<b>D01 — Score Traceability</b><br/><br/>
Braking: 27.427<br/>
Acceleration: 22.066<br/>
Corner: 82.961<br/>
Speed: 34.915<br/><br/>
Risk Score = (27.427 &times; 0.30) + (22.066 &times; 0.30) + (82.961 &times; 0.20) + (34.915 &times; 0.20)<br/><br/>
<b>Final Score = 38.42</b><br/>
<b>Classification = Moderate</b>"""
    elements.append(Paragraph(trace_txt, code_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<i>Note: Final score uses underlying unrounded values; displayed component values are rounded for readability.</i>", body_style))
    elements.append(PageBreak())

    # Page 7: Vehicle Methodology
    elements.append(Paragraph("Vehicle Health Methodology", h1_style))
    elements.append(Paragraph("The objective is to identify vehicles with persistent abnormal sensor signatures that may warrant inspection.", body_style))
    
    elements.append(Paragraph("Visual Methodology Flow", h2_style))
    flow_txt = "Trip telemetry &rarr; Trip mean acceleration magnitude &rarr; 90th-percentile fleet threshold &rarr; Anomalous trip &rarr; Vehicle-level persistence &rarr; 75th-percentile persistence threshold &rarr; Cross-driver verification &rarr; Maintenance Priority"
    elements.append(Paragraph(flow_txt, code_style))
    
    elements.append(Paragraph("Evaluated Thresholds", h2_style))
    elements.append(Paragraph("- Trip anomaly threshold: 1.046 g<br/>- Persistence threshold: 13.33%", body_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Trips exceeding the 1.046 g threshold exhibit unusually high average acceleration magnitude relative to the observed fleet.", body_style))

    elements.append(Paragraph("Cross-Driver Rule", h2_style))
    elements.append(Paragraph("The cross-driver condition downgrades vehicles whose anomaly evidence is associated with only one driver, reducing the likelihood of attributing driver-specific behaviour to the vehicle.", body_style))
    elements.append(Spacer(1, 10))
    rule_txt = """IF Persistence > 13.33% AND Drivers_With_Anomaly > 1<br/>
&nbsp;&nbsp;&nbsp;&nbsp;THEN Maintenance Recommended<br/>
ELSE IF Persistence > 13.33% AND Drivers_With_Anomaly == 1<br/>
&nbsp;&nbsp;&nbsp;&nbsp;THEN Monitor"""
    elements.append(Paragraph(rule_txt, code_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("These are fleet-relative, dataset-derived analytical thresholds and are not industry-standard mechanical maintenance thresholds.", body_style))
    elements.append(PageBreak())

    # Page 8: Vehicle Validation & Dashboards
    elements.append(Paragraph("Vehicle Validation", h1_style))
    elements.append(Paragraph("V02 / V19 Comparison", h2_style))
    
    data = [
        ['Vehicle', 'Trips', 'Anomalous Trips', 'Persistence', 'Drivers with Anomaly', 'Classification'],
        ['V02', '16', '8', '50.00%', '2', 'Maintenance Recommended'],
        ['V19', '16', '7', '43.75%', '1', 'Monitor']
    ]
    t = Table(data, colWidths=[0.8*inch, 0.7*inch, 1.2*inch, 1*inch, 1.2*inch, 1.6*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#2c3e50')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd'))
    ]))
    elements.append(t)
    elements.append(Spacer(1, 15))
    
    elements.append(Paragraph("While V19 exhibits an anomaly persistence of 43.75% (well above the 13.33% threshold), all anomalous trips were generated by a single assigned driver. V02 satisfies both the persistence and cross-driver criteria and is therefore assigned Maintenance Recommended priority for further inspection.", body_style))
    elements.append(PageBreak())

    # Page 9: Dashboards
    elements.append(Paragraph("Dashboard Insights", h1_style))
    elements.append(Paragraph("Driver Behaviour Dashboard", h2_style))
    
    driver_img_path = os.path.join("dashboard", "driver_dashboard.png")
    if os.path.exists(driver_img_path):
        img1 = RLImage(driver_img_path, width=6*inch, height=3.5*inch, kind='proportional')
        elements.append(img1)
        elements.append(Spacer(1, 10))
    else:
        elements.append(Paragraph("Error: driver_dashboard.png not found.", body_style))
        
    elements.append(Paragraph("The Driver Dashboard visualizes relative behavioural risk, allowing the evaluator to isolate drivers who show high-speed exposure but rapid deceleration versus those who drive slowly but exhibit high rotational-movement.", body_style))
    elements.append(PageBreak())

    # Page 10: Dashboards Cont.
    elements.append(Paragraph("Vehicle Health Status Dashboard", h2_style))
    
    vehicle_img_path = os.path.join("dashboard", "vehicle_dashboard.png")
    if os.path.exists(vehicle_img_path):
        img2 = RLImage(vehicle_img_path, width=6*inch, height=3.5*inch, kind='proportional')
        elements.append(img2)
        elements.append(Spacer(1, 10))
    else:
        elements.append(Paragraph("Error: vehicle_dashboard.png not found.", body_style))
        
    elements.append(Paragraph("The Vehicle Dashboard identifies vehicles with persistent acceleration-magnitude anomalies and telemetry patterns that warrant maintenance inspection. The cross-driver scatter plot effectively segments vehicles that require priority inspection from those flagged merely due to driver confounding.", body_style))
    elements.append(PageBreak())

    # Page 11: Assumptions & Limitations
    elements.append(Paragraph("Assumptions & Limitations", h1_style))
    
    data_al = [
        [Paragraph('<b>Assumptions</b>', body_style), Paragraph('<b>Limitations</b>', body_style)],
        [
            Paragraph("- Accelerometer axis orientation is unknown.<br/>- 3D accelerometer magnitude acts as an orientation-independent sensor-motion indicator.<br/>- Minute-level speed differences are behavioural proxies rather than instantaneous acceleration measurements.<br/>- Official speed limits are unavailable.<br/>- Behavioural thresholds are empirical and dataset-relative.<br/>- Vehicle anomaly thresholds are fleet-relative and dataset-derived.<br/>- Cross-driver persistence reduces but does not eliminate driver-specific confounding.<br/>- Risk/health scores are relative analytical indicators.", body_style),
            Paragraph("- <b>Temporal resolution:</b> One-minute telemetry cannot reconstruct short-duration events.<br/>- <b>Ground truth:</b> No ground-truth risky-driver or mechanical-failure labels are available. The scores are not supervised predictions.<br/>- <b>Context:</b> No road type, weather, traffic, road gradient, or route context.<br/>- <b>Sensor orientation:</b> No phone mounting calibration.<br/>- <b>Vehicle diagnosis:</b> Sensor anomalies may have multiple causes and require physical inspection to diagnose.", body_style)
        ]
    ]
    t_al = Table(data_al, colWidths=[3.2*inch, 3.2*inch])
    t_al.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('RIGHTPADDING', (0,0), (0,-1), 15),
        ('LEFTPADDING', (1,0), (1,-1), 15),
    ]))
    elements.append(t_al)
    elements.append(Spacer(1, 20))
    
    elements.append(Paragraph("Additional Applications", h2_style))
    data_app = [
        ['Application', 'Current Data', 'Additional Data Needed'],
        ['Driver Coaching', 'Yes', '—'],
        ['Fleet Safety Monitoring', 'Yes', '—'],
        ['Maintenance Prioritization', 'Yes', 'Maintenance outcomes for validation'],
        ['Predictive Maintenance', 'Partial', 'Failure/maintenance labels'],
        ['Insurance Risk Analysis', 'Potential', 'Claims/accident outcomes']
    ]
    t_app = Table(data_app, colWidths=[2.5*inch, 1*inch, 3*inch])
    t_app.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f8f9fa')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#2c3e50')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 10),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd'))
    ]))
    elements.append(t_app)
    elements.append(Spacer(1, 20))
    
    elements.append(Paragraph("Conclusion", h2_style))
    elements.append(Paragraph("<b>Final takeaway:</b> The assessment demonstrates an explainable, exposure-aware approach to extracting driver-behaviour and vehicle-maintenance signals from GPS and IMU telemetry while explicitly accounting for data limitations and driver/vehicle confounding.", body_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("The robust cross-driver validation and empirical, data-derived thresholds successfully navigate the lack of ground-truth labels and official operational bounds, producing defensible and highly actionable insights for fleet safety and vehicle maintenance prioritization.", body_style))

    doc.build(elements)
    print("PDF generated successfully at", output_path)

if __name__ == "__main__":
    generate()
