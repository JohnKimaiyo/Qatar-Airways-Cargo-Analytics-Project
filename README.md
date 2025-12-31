🧩 Project Components
1️⃣ Data Extraction (SQL)

Source data extracted from operational databases using SQL

Includes daily cargo operations, revenue, weather, and operational indicators

SQL scripts are stored in:

2️⃣ Revenue Forecasting Model (Python)

A Random Forest Regression model is used to predict daily cargo revenue.

Key steps include:

Data preprocessing & cleaning

Feature engineering (time-based and categorical features)

Exploratory Data Analysis (EDA)

Model training & evaluation

Feature importance analysis

Features Engineered

Month

Day of week

Weekend indicator

Weather conditions (One-Hot Encoded)

📊 Model Metrics

Mean Absolute Error (MAE)

Root Mean Squared Error (RMSE)

R² Score

Actual vs Predicted Revenue visualization

Feature importance ranking

3️⃣ Business Intelligence Dashboard (Power BI)

An interactive Aviation Logistics Performance Dashboard built in Power BI.

📄 File:

Aviation Logistics Presentation.pdf


Dashboard highlights:

Cargo revenue trends

Operational performance indicators

Forecast vs actual revenue

Management-ready KPIs for decision-making


| Category         | Tools                                            |
| ---------------- | ------------------------------------------------ |
| Data Extraction  | SQL                                              |
| Programming      | Python                                           |
| Libraries        | Pandas, NumPy, Scikit-Learn, Matplotlib, Seaborn |
| Machine Learning | Random Forest Regressor                          |
| Visualization    | Power BI                                         |
| Domain           | Aviation Logistics & Cargo Analytics             |

📈 Business Value

This project demonstrates how data analytics can:

Improve cargo revenue planning

Identify drivers of revenue volatility

Support forecast-based operational decisions

Enhance financial and logistics performance monitoring

How to Run the Project
1. Clone the Repository
git clone https://github.com/JohnKimaiyo/Qatar-Airways-Cargo-Analytics-Project
cd aviation-logistics-analytics

2. Install Dependencies
pip install pandas numpy scikit-learn matplotlib seaborn

3. Run the Model
python "Prediction Model.py"


⚠️ Update the dataset file path in the script to match your local environment.

📌 Future Enhancements

Add time-series models (ARIMA, Prophet, LSTM)

Integrate real-time data pipelines

Deploy model via Django / FastAPI

Embed Power BI dashboard into a web app

Automate data ingestion using open-source ETL tools

👤 Author

John Kipkemboi Kimaiyo
Data & Finance Analytics Professional
📧 Email: kimaiyojohn6@gmail.com

🌐 Portfolio: https://johnkimaiyo-rosy.vercel.app/
