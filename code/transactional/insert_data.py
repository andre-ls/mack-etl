import csv
import psycopg2

def generateInsertQuery(table_name,header):
    values_position = ','.join(['%s']*len(header))
    return f"INSERT INTO {table_name} VALUES ({values_position})"

def insertFiles(table_name, file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader) # Skip the header row.
        query = generateInsertQuery(table_name,header)
        for row in reader:
            clean_row = [None if x == "" else x for x in row]
            cur.execute(query,clean_row)
    conn.commit()

def insertData(conn, cursor):
    files = [
        {'name' : 'olist_customers' , 'path' : 'data/olist_customers_dataset.csv'},
        {'name' : 'olist_geolocation' , 'path' : 'data/olist_geolocation_dataset.csv'},
        {'name' : 'olist_order_items' , 'path' : 'data/olist_order_items_dataset.csv'},
        {'name' : 'olist_order_payments' , 'path' : 'data/olist_order_payments_dataset.csv'},
        {'name' : 'olist_order_reviews' , 'path' : 'data/olist_order_reviews_dataset.csv'},
        {'name' : 'olist_orders' , 'path' : 'data/olist_orders_dataset.csv'},
        {'name' : 'olist_products' , 'path' : 'data/olist_products_dataset.csv'},
        {'name' : 'olist_sellers' , 'path' : 'data/olist_sellers_dataset.csv'},
        {'name' : 'olist_product_category_name_translation' , 'path' : 'data/product_category_name_translation.csv'}
    ]

    print(">> Upload dos Dados Transacionais")
    for file in files:
        print(f"    >>> Upload da Tabela {file['name']}")
        insertFiles(file['name'],file['path'])

if __name__ == "__main__":
    conn = psycopg2.connect("host=some-postgres dbname=postgres user=postgres password=postgres")
    cur = conn.cursor()

    insertData(conn, cur)
