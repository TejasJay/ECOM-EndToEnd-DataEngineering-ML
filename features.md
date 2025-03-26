# Feature Development
---
🔴 (Red) → Real-time or batch-calculated features

⚫ (Black) → Raw features used to calculate red ones

---

### 🧑‍💻 **User Identity & Demographics Features**  
(To personalize experiences & segment users effectively)  
1. ⚫ **user_id** → Unique identifier for each user (**PK**)  
2. ⚫ **user_type** → New vs. returning customer  
3. ⚫ **age_group** → User's age bucket (18-24, 25-34, etc.)  
4. ⚫ **gender** → Male, Female, Non-Binary, etc.  
5. ⚫ **location_country** → Country of the user  
6. ⚫ **location_region** → State or province  
7. ⚫ **device_type** → Mobile, Desktop, Tablet  
8. ⚫ **browser_type** → Chrome, Safari, Firefox, Edge  
9. ⚫ **preferred_language** → Language used by the user  
10. ⚫ **account_creation_date** → When the account was created  
11. 🔴 **num_successful_orders** → Total orders placed by the user (**Batch**)  
12. 🔴 **num_failed_orders** → Orders that failed due to payment/shipping issues (**Batch**)  

---

### 🌐 **Session & Engagement Features**  
(To track user behavior across different sessions & devices)  
13. ⚫ **session_id** → Unique identifier for each session (**PK**)  
14. ⚫ **user_id** → Foreign key linking session to user (**FK**)  
15. ⚫ **session_start_time** → Timestamp when session starts  
16. ⚫ **session_end_time** → Timestamp when session ends  
17. 🔴 **session_duration** → Total time spent per session (**Real-time**)  
18. 🔴 **num_sessions_per_day** → Number of sessions per user per day (**Batch**)  
19. 🔴 **avg_session_gap** → Time between two sessions (**Batch**)  
20. 🔴 **last_activity_timestamp** → Timestamp of last action by the user (**Real-time**)  
21. 🔴 **num_clicks_per_session** → Total clicks in a session (**Real-time**)  
22. 🔴 **num_page_refreshes** → Indicates frustration or site performance issues (**Real-time**)  
23. 🔴 **bounce_rate_flag** → True if the user exits after 1 page view (**Real-time**)  

---

### 📢 **Marketing Attribution Features**  
(To understand how users were acquired & optimize ad spend)  
24. ⚫ **ad_campaign_id** → Unique identifier for ad campaign (**PK**)  
25. ⚫ **user_id** → Foreign key linking marketing attribution to user (**FK**)  
26. ⚫ **referral_source** → Direct, Organic Search, Paid Ads, Social, Email  
27. 🔴 **num_email_clicks** → Clicks from promotional emails (**Batch**)  
28. 🔴 **num_social_shares** → How many times the user shares a product (**Batch**)  
29. ⚫ **utm_source** → Google, Facebook, Instagram, etc.  
30. ⚫ **utm_medium** → CPC, Organic, Referral  
31. ⚫ **utm_campaign** → Name of the marketing campaign  
32. 🔴 **discount_code_used** → If the user applied a promo code (**Real-time**)  

---

### 📦 **Product & Inventory Metadata Features**  
(To optimize recommendations & demand forecasting)  
33. ⚫ **product_id** → Unique identifier for the product (**PK**)  
34. ⚫ **order_id** → Foreign key linking product to order (**FK**)  
35. ⚫ **product_category** → Electronics, Fashion, Home, etc.  
36. ⚫ **product_brand** → Nike, Apple, Samsung, etc.  
37. ⚫ **product_price** → Price of the product  
38. 🔴 **product_discount** → Discount applied (if any) (**Real-time**)  
39. 🔴 **stock_availability** → In Stock / Out of Stock (**Real-time**)  
40. ⚫ **shipping_time_estimate** → Estimated delivery time  
41. 🔴 **num_product_variants** → Size, color, model, etc. (**Batch**)  

---

### 📡 **Real-Time Behavior Tracking Features**  
(To capture micro-movements & enhance personalization in real-time)  
42. ⚫ **tracking_id** → Unique identifier for tracking events (**PK**)  
43. ⚫ **user_id** → Foreign key linking tracking event to user (**FK**)  
44. ⚫ **session_id** → Foreign key linking tracking event to session (**FK**)  
45. 🔴 **mouse_hover_time** → How long a user hovers over a product (**Real-time**)  
46. 🔴 **scroll_depth** → % of page scrolled (engagement metric) (**Real-time**)  
47. 🔴 **cart_view_time** → Time spent on cart before checking out (**Real-time**)  
48. 🔴 **num_clicks_before_purchase** → How many interactions before conversion (**Real-time**)  
49. 🔴 **checkout_completion_time** → Time taken from checkout initiation to payment (**Real-time**)  
50. 🔴 **payment_processing_time** → Time for payment confirmation (**Real-time**)  

---

### 🛒 **Order & Purchase Features**  
(Core transactional and checkout-related details)  
51. ⚫ **order_id** → Unique identifier for each order (**PK**)  
52. ⚫ **user_id** → Foreign key linking order to user (**FK**)  
53. ⚫ **session_id** → Foreign key linking order to session (**FK**)  
54. 🔴 **order_status** → Completed, Abandoned, Failed (**Real-time**)  
55. 🔴 **num_items_in_order** → Number of products in the order (**Real-time**)  
56. 🔴 **order_total_value** → Total amount paid for the order (**Real-time**)  
57. ⚫ **payment_method** → Credit Card, PayPal, Wallet, etc.  
58. 🔴 **payment_status** → Successful, Pending, Failed (**Real-time**)  
59. 🔴 **discount_applied** → Discount amount applied (if any) (**Real-time**)  
60. ⚫ **shipping_address** → Shipping address for the order  
61. ⚫ **billing_address** → Billing address for the order  
62. ⚫ **order_created_time** → Timestamp when the order was placed  
63. ⚫ **order_completed_time** → Timestamp when payment was confirmed  

---

### 🚨 **Fraud & Security Features**  
(To identify high-risk behavior & prevent abuse)  
64. ⚫ **fraud_event_id** → Unique identifier for fraud detection (**PK**)  
65. ⚫ **user_id** → Foreign key linking fraud event to user (**FK**)  
66. ⚫ **session_id** → Foreign key linking fraud event to session (**FK**)  
67. 🔴 **num_chargebacks** → Number of disputed transactions (**Batch**)  
68. 🔴 **num_different_payment_methods_used** → High variation may indicate fraud (**Batch**)  
69. 🔴 **num_accounts_per_device** → If multiple accounts are created from the same device (**Batch**)  
70. 🔴 **high_shipping_address_mismatch** → Frequent address changes before purchase (**Batch**)  
71. 🔴 **num_login_attempts_failed** → If multiple failed login attempts occur (**Real-time**)  
72. 🔴 **suspicious_activity_flag** → Boolean flag if user behavior triggers risk models (**Real-time**)  

---

### 🌎 **External Data Enrichment Features**  
(To enhance data accuracy with third-party sources)  
73. ⚫ **external_data_id** → Unique identifier for external data (**PK**)  
74. ⚫ **order_id** → Foreign key linking external data to order (**FK**)  
75. 🔴 **weather_at_purchase** → Weather condition during purchase (**Real-time**)  
76. 🔴 **holiday_season_flag** → True if purchase was made during a shopping holiday (**Batch**)  
77. 🔴 **economic_trend_index** → Based on real-world economic indicators (**Batch**)  
78. 🔴 **competitor_price_comparison** → Price difference with competing websites (**Batch**)  

---

### 🔮 **Advanced AI-Based ML Features**  
(To build sophisticated recommendation engines & behavioral predictions)  
79. ⚫ **ml_feature_id** → Unique identifier for ML-generated insights (**PK**)  
80. ⚫ **user_id** → Foreign key linking ML insights to user (**FK**)  
81. 🔴 **predicted_purchase_probability** → Likelihood of a user making a purchase (**Batch**)  
82. 🔴 **churn_risk_score** → Risk of the user leaving the platform (**Batch**)  
83. 🔴 **discount_sensitivity_score** → How likely a user is to wait for discounts (**Batch**)  
84. 🔴 **fraud_risk_score** → AI-based risk assessment for fraud detection (**Batch**)  
85. 🔴 **next_best_product_recommendation** → AI-predicted best recommendation (**Batch**)  

---
