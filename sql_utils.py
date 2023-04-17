import pymysql
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
HOST = os.environ.get("mysql_host")
USER = os.environ.get("mysql_user")
PASSWORD = os.environ.get("mysql_pass")
WAREHOUSE_DB_NAME = os.environ.get("mysql_db")

DB_DATA = 'mysql+pymysql://' + USER + ':' + PASSWORD + '@' + 'localhost' + ':3306/' \
       + WAREHOUSE_DB_NAME + '?charset=utf8mb4'

def setup_db_connection(host=HOST, user=USER, password=PASSWORD, warehouse_db_name=WAREHOUSE_DB_NAME):
  
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=warehouse_db_name
    )
    cursor = connection.cursor()
    return connection, cursor
def create_db_tables(connection, cursor):
    
    create_sales_data_table = \
    """
        CREATE TABLE IF NOT EXISTS sales_data(
            customer_id int NOT NULL,
            purchase_date date,
            purchase_amount decimal(19,2),
            product_id varchar(10)
        );
    """
    create_customer_spend_table = \
    """
        CREATE TABLE IF NOT EXISTS customer_spend(
            customer_id int NOT NULL,
            average_spend decimal(19,2),
            total_spend decimal(19,2)
        );
    """
    create_customer_products_table = \
    """
        CREATE TABLE IF NOT EXISTS customer_products(
            customer_id int NOT NULL,
            product_id varchar(10),
            quantity int
        );
    """

    cursor.execute(create_sales_data_table)
    cursor.execute(create_customer_spend_table)
    cursor.execute(create_customer_products_table)
    connection.commit()
    cursor.close()
    connection.close()

def create_engine_for_load_step(db_data=DB_DATA):
    return create_engine(db_data)
