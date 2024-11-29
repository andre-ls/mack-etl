import psycopg2
from .queries import create_tables

def createTables(connection):
    print(">> Criação das Tabelas de Star Schema")
    cursor = connection.cursor()
    cursor.execute(create_tables)
    connection.commit()

if __name__ == "__main__":
    conn = psycopg2.connect("host=star-postgres dbname=postgres user=postgres password=postgres")
    createTables(conn)
    conn.close()
