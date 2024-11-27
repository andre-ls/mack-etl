import psycopg2

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


# Configurações de conexão com o banco de dados fonte
def getDatabaseConnections():
    source_conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='postgres',
        host='some-postgres',
        port='5432'
    )

    # Configurações de conexão com o banco de dados alvo
    target_conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='postgres',
        host='star-postgres',
        port='5432'
    )

    return source_conn, target_conn

def read_data_from_source(source_conn,query):
    with source_conn.cursor() as source_cursor:
        source_cursor.execute(query)
        data = source_cursor.fetchall()
        col_names = [desc[0] for desc in source_cursor.description]
    return data, col_names


def generateInsertQuery(table_name,col_names):
    column_positions = ','.join(col_names)
    values_position = ','.join(['%s']*len(col_names))
    return f"INSERT INTO {table_name} ({column_positions}) VALUES ({values_position})"

def write_data_to_target(target_conn,table_name,data,col_names):
    with target_conn.cursor() as target_cursor:
        insertQuery = generateInsertQuery(table_name,col_names)
        for row in data:
            target_cursor.execute(insertQuery,row)
    target_conn.commit()

source_conn, target_conn = getDatabaseConnections()

files = [
    {'star-name' : 'dim_customers' , 'read_query' : dim_customers},
    {'star-name' : 'dim_order_reviews' , 'read_query' : dim_order_reviews},
    {'star-name' : 'dim_products' , 'read_query' : dim_products},
    {'star-name' : 'dim_sellers' , 'read_query' : dim_sellers},
    {'star-name' : 'dim_data' , 'read_query' : dim_data},
    {'star-name' : 'fat_order' , 'read_query' : fat_order}
]

for file in files:
    print(f">>> Processamento da tabela {file['star-name']}")
    data, col_names = read_data_from_source(source_conn, file['read_query'])
    write_data_to_target(target_conn,file['star-name'],data,col_names)

# Fecha as conexões com os bancos de dados
source_conn.close()
target_conn.close()
