import psycopg2
from queries import *

conn = psycopg2.connect("host=some-postgres dbname=postgres user=postgres password=postgres")
cur = conn.cursor()

queries = [olist_customers, olist_geolocation, olist_order_items, olist_order_payments, olist_order_reviews, olist_orders, olist_products, olist_sellers, olist_product_category_name_translation]

for query in queries:
    cur.execute(query)
    conn.commit()
