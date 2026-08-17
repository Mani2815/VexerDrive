import pandas as pd
import numpy as np
import os

def load_and_clean_data(file_path):
    """
    Loads the Excel file, resolves header offsets, and returns clean dataframes.
    """
    xl = pd.ExcelFile(file_path)
    sheets = xl.sheet_names
    
    dataframes = {}
    for sheet in sheets:
        # Read without headers to find the actual header row
        df_raw = xl.parse(sheet, header=None)
        
        header_row_idx = None
        for idx, row in df_raw.iterrows():
            if row.notnull().sum() > len(row) / 2: # At least half the columns have values
                header_row_idx = idx
                break
                
        if header_row_idx is not None:
            df = xl.parse(sheet, header=header_row_idx)
            # drop rows where all elements are NaN
            df = df.dropna(how='all')
            dataframes[sheet.strip()] = df
            
    # Clean up Telemetry types
    if 'Telemetry' in dataframes:
        df_tel = dataframes['Telemetry']
        numeric_cols = ['Latitude', 'Longitude', 'Speed_kmph', 'Accel_X_g', 'Accel_Y_g', 'Accel_Z_g', 'Gyro_X_dps', 'Gyro_Y_dps', 'Gyro_Z_dps']
        for col in numeric_cols:
            if col in df_tel.columns:
                df_tel[col] = pd.to_numeric(df_tel[col], errors='coerce')
        # Ensure timestamp is datetime and sort
        df_tel['Timestamp'] = pd.to_datetime(df_tel['Timestamp'])
        df_tel = df_tel.sort_values(by=['Trip_ID', 'Timestamp']).reset_index(drop=True)
        dataframes['Telemetry'] = df_tel
        
    return dataframes

if __name__ == "__main__":
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../dataset.xlsx'))
    # This module is meant to be imported
