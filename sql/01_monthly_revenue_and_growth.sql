-- ====================================================================
-- OlistIQ Business Analysis Queries
-- 1. Monthly Revenue, Order Volume, and Month-over-Month (MoM) Growth
-- ====================================================================

WITH monthly_sales AS (
    SELECT 
        strftime('%Y-%m', o.order_purchase_timestamp) AS order_month,
        COUNT(DISTINCT o.order_id) AS total_orders,
        ROUND(SUM(p.payment_value), 2) AS total_revenue,
        ROUND(AVG(p.payment_value), 2) AS average_order_value
    FROM olist_orders_dataset o
    JOIN olist_order_payments_dataset p ON o.order_id = p.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY strftime('%Y-%m', o.order_purchase_timestamp)
)
SELECT 
    order_month,
    total_orders,
    total_revenue,
    average_order_value,
    ROUND(
        (total_revenue - LAG(total_revenue, 1) OVER (ORDER BY order_month)) 
        / LAG(total_revenue, 1) OVER (ORDER BY order_month) * 100.0, 
        2
    ) AS mom_revenue_growth_pct
FROM monthly_sales
ORDER BY order_month;

