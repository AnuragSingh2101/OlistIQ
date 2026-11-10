-- ====================================================================
-- OlistIQ Business Analysis Queries
-- 3. RFM Customer Segmentation (Recency, Frequency, Monetary)
-- ====================================================================

WITH customer_orders AS (
    SELECT 
        c.customer_unique_id,
        MAX(o.order_purchase_timestamp) AS last_purchase_date,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(p.payment_value) AS total_spent
    FROM olist_orders_dataset o
    JOIN olist_customers_dataset c ON o.customer_id = c.customer_id
    JOIN olist_order_payments_dataset p ON o.order_id = p.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
),
reference_date AS (
    SELECT datetime(MAX(order_purchase_timestamp), '+1 day') AS ref_date 
    FROM olist_orders_dataset
),
rfm_scores AS (
    SELECT 
        co.customer_unique_id,
        ROUND(julianday((SELECT ref_date FROM reference_date)) - julianday(co.last_purchase_date)) AS recency_days,
        co.total_orders AS frequency,
        ROUND(co.total_spent, 2) AS monetary,
        NTILE(4) OVER (ORDER BY (julianday((SELECT ref_date FROM reference_date)) - julianday(co.last_purchase_date)) DESC) AS r_score,
        NTILE(4) OVER (ORDER BY co.total_orders ASC) AS f_score,
        NTILE(4) OVER (ORDER BY co.total_spent ASC) AS m_score
    FROM customer_orders co
)
SELECT 
    customer_unique_id,
    recency_days,
    frequency,
    monetary,
    r_score,
    f_score,
    m_score,
    CASE 
        WHEN r_score >= 3 AND (f_score + m_score) >= 6 THEN 'Champions / VIP'
        WHEN r_score >= 3 AND (f_score + m_score) >= 4 THEN 'Loyal Customers'
        WHEN r_score >= 3 THEN 'Potential Loyalists'
        WHEN r_score = 2 THEN 'At Risk / Need Attention'
        ELSE 'Hibernating / Lost'
    END AS customer_segment
FROM rfm_scores
ORDER BY monetary DESC
LIMIT 500;

