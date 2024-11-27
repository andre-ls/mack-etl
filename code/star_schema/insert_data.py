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
    print(f">>> Inserção da tabela {file['star-name']}")
    data, col_names = read_data_from_source(source_conn, file['read_query'])
    write_data_to_target(target_conn,file['star-name'],data,col_names)

# Fecha as conexões com os bancos de dados
source_conn.close()
target_conn.close()
