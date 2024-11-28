import psycopg2
from queries import *

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
        host='wide-postgres',
        port='5432'
    )

    return source_conn, target_conn

def read_data_from_source(source_conn, query):
    cursor = source_conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    return data, col_names

def generateInsertQuery(table_name,col_names):
    column_positions = ','.join(col_names)
    values_position = ','.join(['%s']*len(col_names))
    return f"INSERT INTO {table_name} ({column_positions}) VALUES ({values_position})"

def write_data_to_target(target_conn,table_name,data,col_names):
    cursor = target_conn.cursor()
    insertQuery = generateInsertQuery(table_name,col_names)
    for row in data:
        cursor.execute(insertQuery,row)
    target_conn.commit()

def insertDataToWideTable(sourceConn, targetConn):
    print(">> Inserção de Dados do Wide Table")
    data, col_names = read_data_from_source(source_conn, wide_table)
    write_data_to_target(target_conn,'wide_table',data,col_names)

if __name__ == "__main__":
    source_conn, target_conn = getDatabaseConnections()
    insertDataToWideTable(source_conn, target_conn)
    source_conn.close()
    target_conn.close()
