-- ====================================================================
-- OlistIQ Business Analysis Queries
-- 2. Delivery SLA Performance and Delay Rates by Destination State
-- ====================================================================

SELECT 
    c.customer_state,
    COUNT(o.order_id) AS total_delivered_orders,
    ROUND(AVG(julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp)), 2) AS avg_delivery_days,
    ROUND(AVG(julianday(o.order_estimated_delivery_date) - julianday(o.order_purchase_timestamp)), 2) AS avg_estimated_days,
    SUM(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1 ELSE 0 END) AS delayed_orders_count,
    ROUND(
        SUM(CASE WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1.0 ELSE 0.0 END) 
        / COUNT(o.order_id) * 100.0, 
        2
    ) AS sla_breach_rate_pct
FROM olist_orders_dataset o
JOIN olist_customers_dataset c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY c.customer_state
HAVING COUNT(o.order_id) >= 100
ORDER BY sla_breach_rate_pct DESC;

