import psycopg2
from queries import create_tables

conn = psycopg2.connect("host=star-postgres dbname=postgres user=postgres password=postgres")
cur = conn.cursor()
cur.execute(create_tables)
conn.commit()
