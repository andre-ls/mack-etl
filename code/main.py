import psycopg2
import transactional.create_tables as transactional_create
import transactional.insert_data as transactional_insert
import star_schema.create_tables as starschema_create
import star_schema.insert_data as starschema_insert
import wide_table.create_tables as widetable_create
import wide_table.insert_data as widetable_insert

# Conexões com Banco de Dados

transactional_connection = psycopg2.connect("host=some-postgres dbname=postgres user=postgres password=postgres")
starschema_connection = psycopg2.connect("host=star-postgres dbname=postgres user=postgres password=postgres")
widetable_connection = psycopg2.connect("host=wide-postgres dbname=postgres user=postgres password=postgres")

# Setup do Banco de Dados Transacional
transactional_create.createTables(transactional_connection)
transactional_insert.insertData(transactional_connection)

# Setup do Banco de Dados Star Schema
starschema_create.createTables(starschema_connection)
starschema_insert.insertData(transactional_connection,starschema_connection)

# Setup do Banco de Dados Wide Schema
widetable_create.createTable(widetable_connection)
widetable_insert.insertData(transactional_connection,widetable_connection)

# Fechamento de Conexões dos Bancos
transactional_connection.close()
starschema_connection.close()
widetable_connection.close()

