create_table = """
CREATE SEQUENCE public.wide_table_wide_pk_seq;

CREATE TABLE public.wide_table (
                order_id VARCHAR NOT NULL,
                wide_PK VARCHAR NOT NULL DEFAULT nextval('public.wide_table_wide_pk_seq'),
                review_answer_timestamp TIMESTAMP NOT NULL,
                review_comment_message VARCHAR,
                seller_city VARCHAR NOT NULL,
                seller_state VARCHAR NOT NULL,
                seller_id VARCHAR NOT NULL,
                seller_zip_code_prefix INTEGER NOT NULL,
                review_score INTEGER NOT NULL,
                review_creation_date DATE NOT NULL,
                review_id VARCHAR NOT NULL,
                review_comment_title VARCHAR,
                customer_city VARCHAR NOT NULL,
                customer_id VARCHAR NOT NULL,
                customer_zip_code_prefix INTEGER NOT NULL,
                customer_state VARCHAR NOT NULL,
                order_status VARCHAR NOT NULL,
                product_height_cm INTEGER,
                product_name_length INTEGER,
                product_weight_g INTEGER,
                product_width_cm INTEGER,
                product_id VARCHAR NOT NULL,
                product_description_length INTEGER,
                product_photos_qty INTEGER,
                product_length_cm INTEGER,
                product_category_name VARCHAR,
                order_purchase_data DATE NOT NULL,
                order_approved_at TIMESTAMP,
                order_delivered_carrier_date TIMESTAMP,
                order_delivered_customer_date TIMESTAMP,
                order_estimated_delivery_date TIMESTAMP NOT NULL,
                payment_sequential INTEGER NOT NULL,
                payment_type VARCHAR NOT NULL,
                payment_installments INTEGER NOT NULL,
                payment_value REAL NOT NULL,
                shipping_limit_date TIMESTAMP NOT NULL,
                price REAL NOT NULL,
                order_purchase_time TIME NOT NULL,
                freight_value REAL NOT NULL,
                insert_time TIMESTAMP default CURRENT_TIMESTAMP,
                data DATE NOT NULL,
                CONSTRAINT order_id PRIMARY KEY (order_id, wide_PK)
);

ALTER SEQUENCE public.wide_table_wide_pk_seq OWNED BY public.wide_table.wide_PK;
"""

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
