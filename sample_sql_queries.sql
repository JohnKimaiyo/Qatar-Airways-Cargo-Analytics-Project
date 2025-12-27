
-- SAMPLE SQL QUERIES FOR QATAR AIRWAYS CARGO ANALYSIS PROJECT

-- 1. Get daily shipment counts and revenue
SELECT 
    DATE(timestamp_booking) as booking_date,
    COUNT(*) as shipment_count,
    SUM(total_charges_usd) as daily_revenue,
    AVG(total_charges_usd) as avg_shipment_value
FROM shipments_fact
GROUP BY DATE(timestamp_booking)
ORDER BY booking_date DESC;

-- 2. Top performing routes by revenue
SELECT 
    origin_airport,
    destination_airport,
    COUNT(*) as shipment_count,
    SUM(total_charges_usd) as total_revenue,
    AVG(total_charges_usd) as avg_revenue_per_shipment
FROM shipments_fact
GROUP BY origin_airport, destination_airport
ORDER BY total_revenue DESC
LIMIT 10;

-- 3. ULD utilization analysis
SELECT 
    u.uld_type,
    COUNT(DISTINCT s.shipment_id) as shipments_assigned,
    AVG(s.actual_weight_kg / u.max_weight_kg) * 100 as avg_weight_utilization_percent,
    AVG(s.actual_volume_cubic_m / u.max_volume_cubic_m) * 100 as avg_volume_utilization_percent
FROM ulds_dim u
LEFT JOIN shipments_fact s ON u.uld_id = s.uld_id
WHERE s.uld_id IS NOT NULL
GROUP BY u.uld_type
ORDER BY shipments_assigned DESC;

-- 4. On-time performance by flight
SELECT 
    f.flight_number,
    f.origin_airport,
    f.destination_airport,
    AVG(TIMESTAMPDIFF(MINUTE, f.scheduled_departure, f.actual_departure)) as avg_departure_delay_min,
    AVG(TIMESTAMPDIFF(MINUTE, f.scheduled_arrival, f.actual_arrival)) as avg_arrival_delay_min,
    COUNT(s.shipment_id) as total_shipments
FROM flights_dim f
LEFT JOIN shipments_fact s ON f.flight_id = s.flight_id
GROUP BY f.flight_id, f.flight_number, f.origin_airport, f.destination_airport
HAVING total_shipments > 0;

-- 5. Customer segmentation analysis
SELECT 
    c.customer_segment,
    c.contract_type,
    COUNT(DISTINCT s.shipment_id) as total_shipments,
    SUM(s.total_charges_usd) as total_revenue,
    AVG(s.total_charges_usd) as avg_shipment_value,
    COUNT(DISTINCT c.customer_id) as customer_count
FROM customers_dim c
JOIN shipments_fact s ON c.customer_id = s.customer_id
GROUP BY c.customer_segment, c.contract_type
ORDER BY total_revenue DESC;

-- 6. Cargo category performance
SELECT 
    cargo_category,
    COUNT(*) as shipment_count,
    SUM(actual_weight_kg) as total_weight_kg,
    SUM(total_charges_usd) as total_revenue,
    AVG(total_charges_usd / actual_weight_kg) as rate_per_kg
FROM shipments_fact
GROUP BY cargo_category
ORDER BY total_revenue DESC;

-- 7. Delay analysis
SELECT 
    origin_airport,
    AVG(TIMESTAMPDIFF(HOUR, timestamp_received, timestamp_departure)) as avg_ground_time_hrs,
    AVG(TIMESTAMPDIFF(HOUR, timestamp_departure, timestamp_arrival)) as avg_transit_time_hrs,
    AVG(TIMESTAMPDIFF(HOUR, timestamp_arrival, timestamp_delivery)) as avg_delivery_time_hrs,
    COUNT(*) as shipment_count
FROM shipments_fact
WHERE timestamp_delivery IS NOT NULL
GROUP BY origin_airport
ORDER BY avg_ground_time_hrs DESC;
