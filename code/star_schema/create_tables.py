import psycopg2
from queries import create_tables

def createTables(conn, cursor):
    cur.execute(create_tables)
    conn.commit()

if __name__ == "__main__":
    conn = psycopg2.connect("host=star-postgres dbname=postgres user=postgres password=postgres")
    cur = conn.cursor()

    createTables(conn, cur)
