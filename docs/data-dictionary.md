# Data Dictionary

| Field | Meaning / use |
|---|---|
| `order_id` | Order identifier; use distinct count for order totals. |
| `customer_id` | Customer identifier. |
| `order_status` | Order status category. |
| `order_purchase_timestamp` | Purchase date/time; use for monthly trend. |
| `order_approved_at` | Order approval timestamp. |
| `order_delivered_carrier_date` | Handover to carrier timestamp. |
| `order_delivered_customer_date` | Customer delivery timestamp. |
| `order_estimated_delivery_date` | Estimated delivery timestamp. |
| `order_item_id` | Item sequence within an order. |
| `product_id` | Product identifier. |
| `seller_id` | Seller identifier. |
| `shipping_limit_date` | Seller shipping limit timestamp. |
| `price` | Item price; sum for product-price comparisons. |
| `freight_value` | Freight/shipping charge per item row. |
| `product_category_name` | Product category dimension. |
| `product_name_lenght` | Product name length (source field spelling). |
| `product_description_lenght` | Product description length (source field spelling). |
| `product_photos_qty` | Number of product photos. |
| `product_weight_g` | Product weight in grams. |
| `product_length_cm` | Product length in centimeters. |
| `product_height_cm` | Product height in centimeters. |
| `product_width_cm` | Product width in centimeters. |
| `payment_value` | Payment amount field; may be repeated in the joined item-level table. Validate before aggregating. |
