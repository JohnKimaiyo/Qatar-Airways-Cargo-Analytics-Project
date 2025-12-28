# Create this script in your project root folder, then run it
validation_script = '''
import pandas as pd
import numpy as np
from datetime import datetime
import os

class DataValidator:
    def __init__(self, data_path):
        self.data_path = data_path
        
    def validate_all(self):
        print("=" * 60)
        print("DATA VALIDATION REPORT")
        print("=" * 60)
        
        files = {
            'customers': 'customers_dim.csv',
            'ulds': 'ulds_dim.csv',
            'flights': 'flights_dim.csv',
            'shipments': 'shipments_fact.csv',
            'daily_ops': 'daily_operations.csv',
            'flight_loads': 'flight_loads_fact.csv'
        }
        
        for name, file in files.items():
            print(f"\\n{'='*40}")
            print(f"Validating: {file}")
            print('='*40)
            
            try:
                df = pd.read_csv(os.path.join(self.data_path, file))
                self._validate_dataframe(name, df)
            except Exception as e:
                print(f"Error loading {file}: {e}")
    
    def _validate_dataframe(self, name, df):
        # Basic info
        print(f"Rows: {len(df):,}, Columns: {len(df.columns)}")
        
        # Check for nulls
        null_counts = df.isnull().sum()
        total_nulls = null_counts.sum()
        print(f"Total null values: {total_nulls:,}")
        
        if total_nulls > 0:
            print("\\nTop columns with nulls:")
            for col, count in null_counts[null_counts > 0].head(5).items():
                print(f"  {col}: {count:,} ({count/len(df)*100:.1f}%)")
        
        # Check for duplicates
        duplicate_rows = df.duplicated().sum()
        print(f"Duplicate rows: {duplicate_rows:,}")
        
        # Check data types
        print("\\nData types:")
        for col in df.columns:
            dtype = str(df[col].dtype)
            unique = df[col].nunique()
            print(f"  {col}: {dtype} (Unique values: {unique:,})")
        
        # Specific validations based on table
        if name == 'shipments':
            self._validate_shipments(df)
        elif name == 'flights':
            self._validate_flights(df)
    
    def _validate_shipments(self, df):
        print("\\n--- Shipments Specific Validation ---")
        
        # Check weight/volume relationships
        weight_volume_ratio = (df['actual_weight_kg'] / df['actual_volume_cubic_m']).mean()
        print(f"Avg weight/volume ratio: {weight_volume_ratio:.2f} kg/m³")
        
        # Check revenue calculations
        expected_revenue = df['revenue_usd'] + df['fuel_surcharge_usd'] + df['security_surcharge_usd']
        diff = abs(df['total_charges_usd'] - expected_revenue).sum()
        print(f"Revenue calculation accuracy: {diff:.2f} total difference")
        
        # Check timestamps logical order
        df['timestamp_booking'] = pd.to_datetime(df['timestamp_booking'])
        df['timestamp_received'] = pd.to_datetime(df['timestamp_received'])
        
        invalid_order = (df['timestamp_received'] < df['timestamp_booking']).sum()
        print(f"Invalid timestamp order (received before booking): {invalid_order:,}")
        
        # Check status distribution
        print("\\nStatus distribution:")
        status_counts = df['status'].value_counts()
        for status, count in status_counts.items():
            print(f"  {status}: {count:,} ({count/len(df)*100:.1f}%)")
    
    def _validate_flights(self, df):
        print("\\n--- Flights Specific Validation ---")
        
        # Check delay statistics
        df['scheduled_departure'] = pd.to_datetime(df['scheduled_departure'])
        df['actual_departure'] = pd.to_datetime(df['actual_departure'])
        
        df['departure_delay_min'] = (df['actual_departure'] - df['scheduled_departure']).dt.total_seconds() / 60
        avg_delay = df['departure_delay_min'].mean()
        print(f"Average departure delay: {avg_delay:.1f} minutes")
        
        on_time = (df['departure_delay_min'] <= 15).sum()
        print(f"On-time departures (≤15 min): {on_time:,} ({on_time/len(df)*100:.1f}%)")

if __name__ == "__main__":
    # Adjusting path to match your folder structure
    validator = DataValidator('data/raw')
    validator.validate_all()
'''

# SAVE THE SCRIPT WITH UTF-8 ENCODING
with open('scripts/etl/validate_data.py', 'w', encoding='utf-8') as f:
    f.write(validation_script)
    
print("Success! Validation script created in scripts/etl/validate_data.py")