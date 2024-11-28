import psycopg2
from queries import create_table

def createTable(connection):
    print(">> Criação de Wide Table")
    cursor = connection.cursor()
    cursor.execute(create_table)
    connection.commit()

if __name__ == "__main__":
    conn = psycopg2.connect("host=wide-postgres dbname=postgres user=postgres password=postgres")
    createTable(conn)
    conn.close()
