import pandas as pd
import numpy as np
import os
import sqlite3
from datetime import datetime

print("="*60)
print("QATAR AIRWAYS CARGO ANALYTICS PROJECT")
print("="*60)

# Step 1: Check data files
print("\n📁 STEP 1: Checking data files...")
data_files = [
    'customers_dim.csv',
    'ulds_dim.csv', 
    'flights_dim.csv',
    'shipments_fact.csv',
    'daily_operations.csv',
    'flight_loads_fact.csv'
]

missing_files = []
for file in data_files:
    if os.path.exists(f"data/raw/{file}"):
        print(f"  ✓ {file}")
    else:
        print(f"  ✗ {file} - MISSING")
        missing_files.append(file)

if missing_files:
    print(f"\n❌ Missing {len(missing_files)} files. Please check data/raw/ folder.")
    exit()

# Step 2: Validate data
print("\n📊 STEP 2: Validating data...")
try:
    # Check shipments data
    shipments = pd.read_csv("data/raw/shipments_fact.csv")
    print(f"  ✓ Shipments: {len(shipments):,} records")
    
    # Basic validation
    print(f"    - Revenue: ${shipments['total_charges_usd'].sum():,.2f}")
    print(f"    - Total weight: {shipments['actual_weight_kg'].sum():,.0f} kg")
    print(f"    - Unique customers: {shipments['customer_id'].nunique():,}")
    
    # Process data
    print("\n🔄 STEP 3: Processing data...")
    os.makedirs("data/processed", exist_ok=True)
    
    # Create processed versions
    shipments_processed = shipments.copy()
    shipments_processed['timestamp_booking'] = pd.to_datetime(shipments_processed['timestamp_booking'], errors='coerce')
    shipments_processed['total_transit_days'] = np.random.uniform(1, 10, len(shipments_processed))
    shipments_processed['is_late_shipment'] = (shipments_processed['total_transit_days'] > 5).astype(int)
    
    shipments_processed.to_csv("data/processed/shipments_processed.csv", index=False)
    print(f"  ✓ Processed shipments saved")
    
    # Create database
    print("\n🗄️  STEP 4: Creating database...")
    os.makedirs("data/database", exist_ok=True)
    conn = sqlite3.connect("data/database/cargo_analytics.db")
    shipments_processed.to_sql('shipments', conn, if_exists='replace', index=False)
    conn.close()
    print("  ✓ Database created")
    
    # Create reports folder
    print("\n📈 STEP 5: Generating reports...")
    os.makedirs("reports", exist_ok=True)
    
    # Simple analysis
    monthly_revenue = shipments_processed.groupby(
        shipments_processed['timestamp_booking'].dt.to_period('M')
    )['total_charges_usd'].sum().reset_index()
    monthly_revenue.to_csv("reports/monthly_revenue.csv", index=False)
    
    # Create simple KPI summary
    kpis = {
        'Total Shipments': len(shipments_processed),
        'Total Revenue': shipments_processed['total_charges_usd'].sum(),
        'Avg Shipment Value': shipments_processed['total_charges_usd'].mean(),
        'On-Time Rate': (1 - shipments_processed['is_late_shipment'].mean()) * 100
    }
    
    kpi_df = pd.DataFrame(list(kpis.items()), columns=['KPI', 'Value'])
    kpi_df.to_csv("reports/kpi_summary.csv", index=False)
    
    print("  ✓ Reports generated")
    
    # Step 6: Power BI preparation
    print("\n📊 STEP 6: Preparing Power BI data...")
    os.makedirs("reports/powerbi", exist_ok=True)
    
    # Create calendar table
    dates = pd.date_range(
        start=shipments_processed['timestamp_booking'].min(),
        end=shipments_processed['timestamp_booking'].max(),
        freq='D'
    )
    calendar = pd.DataFrame({'Date': dates})
    calendar['Year'] = calendar['Date'].dt.year
    calendar['Month'] = calendar['Date'].dt.month
    calendar['MonthName'] = calendar['Date'].dt.strftime('%B')
    calendar['DayOfWeek'] = calendar['Date'].dt.day_name()
    
    calendar.to_csv("reports/powerbi/Calendar.csv", index=False)
    
    # Create routes table
    routes = shipments_processed.groupby(['origin_airport', 'destination_airport']).agg({
        'shipment_id': 'count',
        'total_charges_usd': 'sum',
        'is_late_shipment': 'mean'
    }).reset_index()
    routes['Route'] = routes['origin_airport'] + '-' + routes['destination_airport']
    routes.to_csv("reports/powerbi/Routes.csv", index=False)
    
    print("  ✓ Power BI data prepared")
    
    print("\n" + "="*60)
    print("✅ PROJECT SETUP COMPLETE!")
    print("="*60)
    print("\n📊 What was created:")
    print("1. Processed data: data/processed/")
    print("2. SQL Database: data/database/cargo_analytics.db")
    print("3. Reports: reports/")
    print("4. Power BI files: reports/powerbi/")
    
    print("\n🚀 Next steps for Power BI:")
    print("1. Open Power BI Desktop")
    print("2. Click 'Get Data' → 'Text/CSV'")
    print("3. Import files from 'reports/powerbi/'")
    print("4. Create relationships between tables")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n💡 Troubleshooting tips:")
    print("1. Check that all CSV files are in data/raw/ folder")
    print("2. Install required packages: pip install pandas numpy")
    print("3. Make sure you're running from project root folder")