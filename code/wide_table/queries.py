wide_table = """
select 
	DATE(oo.order_purchase_timestamp) as data,
	oo.order_id,
	op.product_id,
	op.product_category_name, 
	op.product_name_length, 
	op.product_description_length, 
	op.product_photos_qty, 
	op.product_weight_g, 
	op.product_length_cm, 
	op.product_height_cm, 
	op.product_width_cm,
	oor.review_id,
	oor.order_id, 
	oor.review_score, 
	oor.review_comment_title, 
	oor.review_comment_message, 
	oor.review_creation_date, 
	oor.review_answer_timestamp,
	oc.customer_id,
	oc.customer_zip_code_prefix, 
	oc.customer_city, 
	oc.customer_state,
	os.seller_id,
	os.seller_zip_code_prefix, 
	os.seller_city, 
	os.seller_state,
	oo.order_status,
	DATE(oo.order_purchase_timestamp) as order_purchase_data,
	cast(oo.order_purchase_timestamp as time) as order_purchase_time,
	oo.order_approved_at,
	oo.order_delivered_carrier_date,
	oo.order_delivered_customer_date,
	oo.order_estimated_delivery_date,
	oop.payment_sequential,
	oop.payment_type,
	oop.payment_installments,
	oop.payment_value,
	ooi.shipping_limit_date,
	ooi.price,
	ooi.freight_value
from olist_orders oo
inner join olist_order_items ooi on oo.order_id = ooi.order_id
inner join olist_order_reviews oor on oo.order_id = oor.order_id
inner join olist_sellers os on ooi.seller_id = os.seller_id 
inner join olist_customers oc on oo.customer_id = oc.customer_id
inner join olist_order_payments oop on oo.order_id = oop.order_id
inner join olist_products op on ooi.product_id = op.product_id
"""
