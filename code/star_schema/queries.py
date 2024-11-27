#Query de Criação de Tabelas do Star Schema
create_tables = """
CREATE TABLE IF NOT EXISTS public.dim_data (
                data DATE NOT NULL,
                ano INTEGER NOT NULL,
                mes INTEGER NOT NULL,
                dia INTEGER NOT NULL,
                dia_util BOOLEAN NOT NULL,
                insert_time TIMESTAMP default CURRENT_TIMESTAMP,
                CONSTRAINT data PRIMARY KEY (data)
);

CREATE TABLE public.dim_order_reviews (
                review_id VARCHAR NOT NULL,
                order_id VARCHAR NOT NULL,
                review_score INTEGER NOT NULL,
                review_comment_title VARCHAR,
                review_comment_message VARCHAR,
                review_creation_date DATE NOT NULL,
                review_answer_timestamp TIMESTAMP NOT NULL,
                insert_time TIMESTAMP default CURRENT_TIMESTAMP,
                CONSTRAINT review_id PRIMARY KEY (review_id, order_id)
);


CREATE TABLE public.dim_sellers (
                seller_id VARCHAR NOT NULL,
                seller_city VARCHAR NOT NULL,
                seller_state VARCHAR NOT NULL,
                insert_time TIMESTAMP default CURRENT_TIMESTAMP,
                seller_zip_code_prefix INTEGER NOT NULL,
                CONSTRAINT seller_id PRIMARY KEY (seller_id)
);

CREATE TABLE public.dim_products (
                product_id VARCHAR NOT NULL,
                product_category_name VARCHAR,
                product_name_length INTEGER,
                product_description_length INTEGER,
                product_photos_qty INTEGER,
                product_weight_g INTEGER,
                product_length_cm INTEGER,
                product_height_cm INTEGER,
                product_width_cm INTEGER,
                insert_time TIMESTAMP default CURRENT_TIMESTAMP,
                CONSTRAINT product_id PRIMARY KEY (product_id)
);

CREATE TABLE public.dim_customers (
                customer_id VARCHAR NOT NULL,
                customer_city VARCHAR NOT NULL,
                customer_state VARCHAR NOT NULL,
                insert_time TIMESTAMP default CURRENT_TIMESTAMP,
                customer_zip_code_prefix INTEGER NOT NULL,
                CONSTRAINT customer_id PRIMARY KEY (customer_id)
);


CREATE SEQUENCE public.fat_order_fato_pk_seq;

CREATE TABLE public.fat_order (
                fato_PK INTEGER NOT NULL DEFAULT nextval('public.fat_order_fato_pk_seq'),
                order_id VARCHAR NOT NULL,
                data DATE NOT NULL,
                product_id VARCHAR NOT NULL,
                seller_id VARCHAR NOT NULL,
                review_id VARCHAR NOT NULL,
                customer_id VARCHAR NOT NULL,
                order_status VARCHAR NOT NULL,
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
                CONSTRAINT order_id PRIMARY KEY (fato_PK, order_id)
);


ALTER SEQUENCE public.fat_order_fato_pk_seq OWNED BY public.fat_order.fato_PK;

ALTER TABLE public.fat_order ADD CONSTRAINT dim_data_fat_order_fk
FOREIGN KEY (data)
REFERENCES public.dim_data (data)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.fat_order ADD CONSTRAINT dim_olist_order_reviews_dataset_fat_order_fk
FOREIGN KEY (review_id, order_id)
REFERENCES public.dim_order_reviews (review_id, order_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.fat_order ADD CONSTRAINT dim_olist_sellers_dataset_fat_order_fk
FOREIGN KEY (seller_id)
REFERENCES public.dim_sellers (seller_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.fat_order ADD CONSTRAINT dim_olist_products_dataset_fat_order_fk
FOREIGN KEY (product_id)
REFERENCES public.dim_products (product_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.fat_order ADD CONSTRAINT dim_olist_customers_dataset_fat_order_fk
FOREIGN KEY (customer_id)
REFERENCES public.dim_customers (customer_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;
"""

#Queries de Leitura de Dados para Inserção nas Tabelas do Star Schema
dim_customers = """
select customer_id, customer_zip_code_prefix, customer_city, customer_state 
from olist_customers oc
"""

dim_order_reviews = """
select review_id, order_id, review_score, review_comment_title, review_comment_message, review_creation_date, review_answer_timestamp 
from olist_order_reviews oor
"""

dim_products = """
select product_id, product_category_name, product_name_length, product_description_length, product_photos_qty, product_weight_g, product_length_cm, product_height_cm, product_width_cm 
from olist_products op
"""

dim_sellers = """
select seller_id, seller_zip_code_prefix, seller_city, seller_state 
from olist_sellers os
"""

dim_data = """
SELECT 
    day as data,
    EXTRACT(YEAR FROM day) AS ano,
    EXTRACT(MONTH FROM day) AS mes,
    EXTRACT(DAY FROM day) AS dia,
    CASE 
        WHEN EXTRACT(DOW FROM day) IN (0, 6) THEN FALSE 
        ELSE TRUE 
    END AS dia_util
FROM 
(
    SELECT day::date
    FROM generate_series('2000-01-01'::date, '2030-12-31'::date, '1 day'::interval) day
) AS all_days;
"""

fat_order = """
select
	DATE(oo.order_purchase_timestamp) as data,
	oo.order_id,
	ooi.product_id, 
	oor.review_id,
	oc.customer_id,
    os.seller_id,
	oo.order_status,
	DATE(oo.order_purchase_timestamp) as order_purchase_data,
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
	ooi.freight_value,
	cast(oo.order_purchase_timestamp as time) as order_purchase_time
from olist_orders oo
inner join olist_order_items ooi on oo.order_id = ooi.order_id
inner join olist_order_reviews oor on oo.order_id = oor.order_id
inner join olist_sellers os on ooi.seller_id = os.seller_id 
inner join olist_customers oc on oo.customer_id = oc.customer_id
inner join olist_order_payments oop on oo.order_id = oop.order_id
"""
