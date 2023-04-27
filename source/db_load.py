import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('docker_setup/.env')
host = os.environ.get("sql_host")
user = os.environ.get("sql_user")
password = os.environ.get("sql_pass")
database = os.environ.get("sql_db")
port = os.environ.get("sql_port")

def setup_db_connection(host=host, 
                        user=user, 
                        password=password,
                        db=database,
                        port=port):
    
    conn = psycopg2.connect(
        host = host,
        database = db,
        user = user,
        password = password,
        port = port
    )
    return conn

connection = setup_db_connection()

conn_cursor = connection.cursor()

conn_cursor.execute("SELECT * FROM products")

#connection.commit()

#print(conn_cursor.fetchall())

# conn_cursor.close()
# connection.close()

#--------------------------------------------------------------------

test_prods = {
    'Test':5.5,
    'Hello':6.5,
    'Goodbye':7.5
}

def insert_into_product_db():
    try:
        for product, price in test_prods.items():
            cursor = connection.cursor()
            sql = "INSERT INTO products (product_name, product_price) VALUES (%s,%s) RETURNING product_id"
            cursor.execute(sql, (product, price))
            connection.commit()
            
            
    except Exception as e:
        print(f'Failed to open connection: {e}')
        
#insert_into_product_db()

conn_cursor.close()
connection.close()

#-------------------------------------------------------

class WithDB():

# SELECT [SQL] (2 arguments, SELECT = "*" TABLE = "table_name")

    def select_db(select, table):
        
        try:
            print("Connecting to DataBase...")
            host_name = "localhost"
            database_name = "group_project"
            user_name = "brewed"
            user_password = "awakening"
            port="5432"

            with psycopg2.connect(
                        host = host_name,
                        database = database_name,
                        user = user_name,
                        password = user_password,
                        port = port
                    ) as connection:
            
                cursor = connection.cursor()
                
                sql = f"SELECT {select} FROM {table}"
                cursor.execute(sql)
                table_data = cursor.fetchall()
                print(table_data)
                connection.commit()
        
        except Exception as ex:
            print(f"Failed to open connection, please make sure DB is Running: {ex}")
    
WithDB.select_db("*", "products")

#--------------------------------------------------------------------------------------------

# A row example.... edit for one value if it fails so you can check how it works
row = ['Chesterfield','Richard Copeland', "Regular Flavoured iced latte - Hazelnut - 2.75, Large Latte - 2.45", 5.20, 'CARD', 5494173772652516]
# the target table 
table = "raw_data"
#your table db columns  
columns = 'location,full_name,orders,transaction_total,payment_type,card_number'


print(type(columns))

class WithDB():

    def insert_db(row, table, columns):
            
            try:
                print("Connecting to DataBase...")
                host_name = "localhost"
                database_name = "group_project"
                user_name = "brewed"
                user_password = "awakening"
                port="5432"
                
                with psycopg2.connect(
                            host = host_name,
                            database = database_name,
                            user = user_name,
                            password = user_password,
                            port = port
                        ) as connection:
                
                    cursor = connection.cursor()
                    
                    #sql = f"INSERT INTO {table} {columns} VALUES (%s, %s, %s, %s, %s, %s)"
                    #values = columns
                    
                    cursor.execute("INSERT INTO raw_data VALUES (%s, %s, %s, %s, %s, %s)", row)  # correct

                    #cursor.execute(sql,values)
                    # table_data = cursor.fetchall()
                    # print(table_data)
                    connection.commit()
            
            except Exception as ex:
                print(f"Failed to open connection, please make sure DB is Running: {ex}")

WithDB.insert_db(row, table, columns)
