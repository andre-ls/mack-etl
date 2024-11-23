CREATE TABLE public.dim_data (
                data DATE NOT NULL,
                ano INTEGER NOT NULL,
                mes INTEGER NOT NULL,
                dia INTEGER NOT NULL,
                dia_util BOOLEAN NOT NULL,
                CONSTRAINT data PRIMARY KEY (data)
);


CREATE TABLE public.dim_order_reviews (
                review_id VARCHAR NOT NULL,
                review_score INTEGER NOT NULL,
                review_comment_title VARCHAR,
                review_comment_message VARCHAR,
                review_creation_date DATE NOT NULL,
                review_answer_timestamp TIMESTAMP NOT NULL,
                CONSTRAINT review_id PRIMARY KEY (review_id)
);


CREATE TABLE public.dim_sellers (
                seller_id VARCHAR NOT NULL,
                seller_zip_code_prefix INTEGER NOT NULL,
                seller_city VARCHAR NOT NULL,
                seller_state VARCHAR NOT NULL,
                CONSTRAINT seller_id PRIMARY KEY (seller_id)
);


CREATE TABLE public.dim_products (
                product_id VARCHAR NOT NULL,
                product_category_name VARCHAR NOT NULL,
                product_name_lenght INTEGER NOT NULL,
                product_description_lenght INTEGER NOT NULL,
                product_photos_qty INTEGER NOT NULL,
                product_weight_g INTEGER NOT NULL,
                product_length_cm INTEGER NOT NULL,
                product_height_cm INTEGER NOT NULL,
                product_width_cm INTEGER NOT NULL,
                CONSTRAINT product_id PRIMARY KEY (product_id)
);


CREATE TABLE public.dim_geolocation (
                geolocation_zip_code_prefix INTEGER NOT NULL,
                geolocation_lat INTEGER NOT NULL,
                geolocation_lng INTEGER NOT NULL,
                geolocation_city VARCHAR NOT NULL,
                geolocation_state VARCHAR NOT NULL,
                CONSTRAINT geolocation_zip_code_prefix PRIMARY KEY (geolocation_zip_code_prefix)
);


CREATE TABLE public.dim_customers (
                customer_id VARCHAR NOT NULL,
                customer_zip_code_prefix INTEGER NOT NULL,
                customer_city VARCHAR NOT NULL,
                customer_state VARCHAR NOT NULL,
                CONSTRAINT customer_id PRIMARY KEY (customer_id)
);


CREATE SEQUENCE public.fat_order_fato_pk_seq;

CREATE TABLE public.fat_order (
                fato_PK INTEGER NOT NULL DEFAULT nextval('public.fat_order_fato_pk_seq'),
                seller_geolocation_zip_code_prefix INTEGER NOT NULL,
                customer_geolocation_zip_code_prefix INTEGER NOT NULL,
                data DATE NOT NULL,
                order_id INTEGER NOT NULL,
                product_id VARCHAR NOT NULL,
                seller_id VARCHAR NOT NULL,
                review_id VARCHAR NOT NULL,
                customer_id VARCHAR NOT NULL,
                order_status VARCHAR NOT NULL,
                order_purchase_data DATE NOT NULL,
                order_approved_at TIMESTAMP NOT NULL,
                order_delivered_carrier_date TIMESTAMP NOT NULL,
                order_delivered_customer_date TIMESTAMP NOT NULL,
                order_estimated_delivery_date TIMESTAMP NOT NULL,
                payment_sequential INTEGER NOT NULL,
                payment_type VARCHAR NOT NULL,
                payment_installments INTEGER NOT NULL,
                payment_value REAL NOT NULL,
                shipping_limit_date TIMESTAMP NOT NULL,
                price REAL NOT NULL,
                freight_value REAL NOT NULL,
                order_purchase_time TIME NOT NULL,
                CONSTRAINT order_id PRIMARY KEY (fato_PK)
);


ALTER SEQUENCE public.fat_order_fato_pk_seq OWNED BY public.fat_order.fato_PK;

ALTER TABLE public.fat_order ADD CONSTRAINT dim_data_fat_order_fk
FOREIGN KEY (data)
REFERENCES public.dim_data (data)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.fat_order ADD CONSTRAINT dim_olist_order_reviews_dataset_fat_order_fk
FOREIGN KEY (review_id)
REFERENCES public.dim_order_reviews (review_id)
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

ALTER TABLE public.fat_order ADD CONSTRAINT dim_geolocation_fat_order_fk
FOREIGN KEY (customer_geolocation_zip_code_prefix)
REFERENCES public.dim_geolocation (geolocation_zip_code_prefix)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.fat_order ADD CONSTRAINT dim_geolocation_fat_order_fk1
FOREIGN KEY (seller_geolocation_zip_code_prefix)
REFERENCES public.dim_geolocation (geolocation_zip_code_prefix)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE public.fat_order ADD CONSTRAINT dim_olist_customers_dataset_fat_order_fk
FOREIGN KEY (customer_id)
REFERENCES public.dim_customers (customer_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;
