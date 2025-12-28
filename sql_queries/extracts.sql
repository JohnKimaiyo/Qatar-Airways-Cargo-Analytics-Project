--- Revenue Trends Over Time ---
SELECT 
    FORMAT(CAST(timestamp_booking AS DATE), 'yyyy-MM') AS [Month],
    SUM(total_charges_usd) AS TotalRevenue,
    SUM(fuel_surcharge_usd) AS FuelSurcharge,
    COUNT(shipment_id) AS ShipmentCount
FROM shipments_fact
GROUP BY FORMAT(CAST(timestamp_booking AS DATE), 'yyyy-MM')
ORDER BY [Month];

-- Market Share by Customer Segment --
SELECT 
    c.customer_segment,
    SUM(s.total_charges_usd) AS TotalRevenue,
    COUNT(s.shipment_id) AS TotalShipments
FROM shipments_fact s
JOIN customers_dim c ON s.customer_id = c.customer_id
GROUP BY c.customer_segment
ORDER BY TotalRevenue DESC;

-- Flight Utilization by Aircraft Type --
SELECT 
    fd.aircraft_type,
    AVG(fl.weight_utilization_percent) AS AvgWeightUtilization,
    AVG(fl.fuel_efficiency_kg_per_ton) AS AvgFuelEfficiency
FROM flights_dim fd
JOIN flight_loads_fact fl ON fd.flight_id = fl.flight_id
GROUP BY fd.aircraft_type
ORDER BY AvgWeightUtilization DESC;

--Departure Delay Analysis by Origin Airport --
SELECT 
    origin_airport,
    COUNT(CASE WHEN DATEDIFF(MINUTE, scheduled_departure, actual_departure) > 15 THEN 1 END) AS DelayedFlights,
    AVG(DATEDIFF(MINUTE, scheduled_departure, actual_departure)) AS AvgDelayMinutes
FROM flights_dim
WHERE flight_status = 'Completed'
GROUP BY origin_airport
ORDER BY AvgDelayMinutes DESC;


-- Weather Impact on Operational Revenue --
SELECT 
    weather_condition,
    AVG(total_revenue_usd) AS AvgDailyRevenue,
    AVG(equipment_utilization_rate) * 100 AS AvgEquipmentUtilPercent
FROM daily_operations
GROUP BY weather_condition
ORDER BY AvgDailyRevenue DESC;

-- ULD Maintenance & Ageing Status --
SELECT 
    current_status,
    COUNT(uld_id) AS ULDCount,
    AVG(total_flights) AS AvgFlightsPerUnit,
    MIN(last_inspection_date) AS OldestInspectionDate
FROM ulds_dim
GROUP BY current_status;