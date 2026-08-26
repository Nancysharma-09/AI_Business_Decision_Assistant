-- ============================================
-- AI BUSINESS DECISION ASSISTANT
-- RETAIL BUSINESS SQL ANALYSIS
-- ============================================

-- How many different customers are in our dataset?
SELECT COUNT(DISTINCT Customer_ID)
FROM retail_sales;
 
-- How many total transactions/rows are in our dataset?
 SELECT COUNT(*)
FROM retail_sales;
 
-- What is total revenue?
 SELECT SUM(Revenue) AS total_revenue
FROM retail_sales;

-- Which countries generate the most revenue?
SELECT Country, SUM(Revenue) AS total_revenue
FROM retail_sales
GROUP BY Country
ORDER BY total_revenue DESC
LIMIT 10;

-- Which products generate the most revenue?
SELECT Description, SUM(Revenue) AS total_revenue
FROM retail_sales
GROUP BY Description
ORDER BY total_revenue DESC
LIMIT 10;

-- How does revenue change month by month?
SELECT Sales_period, SUM(Revenue) AS total_revenue
FROM retail_sales
GROUP BY Sales_period
ORDER BY Sales_period;

-- Who are our highest-value customers?
SELECT Customer_ID, SUM(Revenue) AS total_revenue
FROM retail_sales
WHERE Customer_ID IS NOT NULL
  AND TRIM(Customer_ID) <> ''
GROUP BY Customer_ID
ORDER BY total_revenue DESC
LIMIT 10;

-- How much revenue comes from these unusual transaction descriptions?
SELECT Description, COUNT(*) AS transaction_count
FROM retail_sales
WHERE Description LIKE '%POSTAGE%'
   OR Description LIKE '%Manual%'
   OR Description LIKE '%Adjust%'
GROUP BY Description
ORDER BY transaction_count DESC;

SELECT SUM(Revenue) AS non_product_revenue
FROM retail_sales
WHERE Description LIKE '%POSTAGE%'
   OR Description = 'Manual'
   OR Description LIKE 'Adjustment%'
   OR Description = 'Adjust bad debt';

-- Which actual products generate the most revenue?
SELECT Description, SUM(Revenue) AS total_revenue
FROM retail_sales
WHERE Description NOT LIKE '%POSTAGE%'
  AND Description <> 'Manual'
  AND Description NOT LIKE 'Adjustment%'
  AND Description <> 'Adjust bad debt'
GROUP BY Description
ORDER BY total_revenue DESC
LIMIT 10;

-- Which products have the highest total quantity sold?
SELECT Description, SUM(Quantity) AS total_quantity
FROM retail_sales
WHERE Description NOT LIKE '%POSTAGE%'
  AND Description <> 'Manual'
  AND Description NOT LIKE 'Adjustment%'
  AND Description <> 'Adjust bad debt'
GROUP BY Description
ORDER BY total_quantity DESC
LIMIT 10;

-- Which hours of the day have the highest number of transactions?
SELECT Hour, COUNT(*) AS transaction_count
FROM retail_sales
GROUP BY Hour
ORDER BY transaction_count DESC;

-- Which days of the week have the highest number of transactions?
SELECT Day_Name, COUNT(*) AS transaction_count
FROM retail_sales
GROUP BY Day_Name
ORDER BY transaction_count DESC;

-- Which countries have the highest number of units sold?
SELECT Country, SUM(Quantity) AS total_quantity
FROM retail_sales
GROUP BY Country
ORDER BY total_quantity DESC
LIMIT 10;
 
-- What is the average revenue generated per invoice?
SELECT 
    SUM(Revenue) / COUNT(DISTINCT Invoice) AS average_order_value
FROM retail_sales;

-- How many unique invoices were generated in each month?
SELECT 
    Sales_period,
    COUNT(DISTINCT Invoice) AS total_orders
FROM retail_sales
GROUP BY Sales_period
ORDER BY Sales_period;

-- Which month had the highest average order value?
SELECT 
    Sales_period,
    SUM(Revenue) / COUNT(DISTINCT Invoice) AS average_order_value
FROM retail_sales
GROUP BY Sales_period
ORDER BY average_order_value DESC
LIMIT 10;

-- How many invoices does each customer have?
SELECT 
    Customer_ID,
    COUNT(DISTINCT Invoice) AS total_orders
FROM retail_sales
WHERE Customer_ID IS NOT NULL
  AND TRIM(Customer_ID) <> ''
GROUP BY Customer_ID
ORDER BY total_orders DESC
LIMIT 10;

-- Which customers generate the highest average revenue per order?
SELECT 
    Customer_ID,
    SUM(Revenue) / COUNT(DISTINCT Invoice) AS avg_order_value
FROM retail_sales
WHERE Customer_ID IS NOT NULL
  AND TRIM(Customer_ID) <> ''
GROUP BY Customer_ID
ORDER BY avg_order_value DESC
LIMIT 10;

-- How many orders did these high-average-value customers actually make?
SELECT 
    Customer_ID,
    COUNT(DISTINCT Invoice) AS total_orders,
    SUM(Revenue) AS total_revenue
FROM retail_sales
WHERE Customer_ID IS NOT NULL
  AND TRIM(Customer_ID) <> ''
GROUP BY Customer_ID
HAVING Customer_ID IN ('16446', '15749', '15098', '13687', '12918')
ORDER BY total_revenue DESC;

-- Which countries have the highest average revenue per invoice?
SELECT 
    Country,
    SUM(Revenue) / COUNT(DISTINCT Invoice) AS average_order_value
FROM retail_sales
GROUP BY Country
ORDER BY average_order_value DESC
LIMIT 10;

-- Which products have high revenue but relatively low sales quantity?
SELECT 
    Description,
    SUM(Quantity) AS total_quantity,
    SUM(Revenue) AS total_revenue
FROM retail_sales
WHERE Description NOT LIKE '%POSTAGE%'
  AND Description <> 'Manual'
  AND Description NOT LIKE 'Adjustment%'
  AND Description <> 'Adjust bad debt'
GROUP BY Description
ORDER BY total_revenue DESC
LIMIT 10;