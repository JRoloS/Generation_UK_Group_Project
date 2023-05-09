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
    
    print("Connecting to database....")
    conn = psycopg2.connect(
        host = host,
        database = db,
        user = user,
        password = password,
        port = port
    )
    print("Connection established.")
    return conn

conn = setup_db_connection()

#-------------------------------------

def create_locations_db_table(conn):
    drop_if_location_table_exists = """
        DROP TABLE IF EXISTS "locations" CASCADE;
        DROP SEQUENCE IF EXISTS locations_location_id_seq;
        CREATE SEQUENCE locations_location_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;
    """
    
    create_locations_table = """
        CREATE TABLE "public"."locations" (
        "location_id" integer DEFAULT nextval('locations_location_id_seq') NOT NULL,
        "location_name" character varying(100) NOT NULL,
        CONSTRAINT "locations_pkey" PRIMARY KEY ("location_id")
    ) WITH (oids = false);
    """
    
    cursor = conn.cursor()
    cursor.execute(drop_if_location_table_exists)
    print("'locations' table being created....")
    cursor.execute(create_locations_table)
    print("Table created successfully.")
    conn.commit()
    cursor.close()

create_locations_db_table(conn)

#-------------------------------------

def create_orders_db_table(conn):
    drop_if_orders_table_exists = """
        DROP TABLE IF EXISTS "orders" CASCADE;
        DROP SEQUENCE IF EXISTS orders_order_id_seq;
        CREATE SEQUENCE orders_order_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;
    """
    
    create_orders_table = """
        CREATE TABLE "public"."orders" (
        "order_id" integer DEFAULT nextval('orders_order_id_seq') NOT NULL,
        "date_time" timestamp NOT NULL,
        "location_id" integer NOT NULL,
        "transaction_total" numeric(10,2) NOT NULL,
        "payment_type_id" integer NOT NULL,
        CONSTRAINT "orders_pkey" PRIMARY KEY ("order_id")
    ) WITH (oids = false);
    """
    
    cursor = conn.cursor()
    cursor.execute(drop_if_orders_table_exists)
    print("'orders' table being created....")
    cursor.execute(create_orders_table)
    print("Table created successfully.")
    conn.commit()
    cursor.close()

create_orders_db_table(conn)

#-------------------------------------

def create_orders_products_db_table(conn):
    drop_if_orders_products_table_exists = """
        DROP TABLE IF EXISTS "orders_products" CASCADE;
    """
    
    create_orders_products_table = """
        CREATE TABLE "public"."orders_products" (
        "order_id" integer NOT NULL,
        "product_id" integer NOT NULL,
        "product_price" numeric(10,2)
    ) WITH (oids = false);
    """
    
    cursor = conn.cursor()
    cursor.execute(drop_if_orders_products_table_exists)
    print("'orders_products' database being created....")
    cursor.execute(create_orders_products_table)
    print("Table created successfully.")
    conn.commit()
    cursor.close()

create_orders_products_db_table(conn)

#-------------------------------------------------------------------------------

def create_payment_types_db_table(conn):
    drop_if_payment_types_table_exists = """
        DROP TABLE IF EXISTS "payment_types" CASCADE;
        DROP SEQUENCE IF EXISTS payment_types_payment_type_id_seq;
        CREATE SEQUENCE payment_types_payment_type_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;
    """
    
    create_payment_types_table = """
        CREATE TABLE "public"."payment_types" (
        "payment_type_id" integer DEFAULT nextval('payment_types_payment_type_id_seq') NOT NULL,
        "payment_name" character varying(10),
        CONSTRAINT "payment_types_pkey" PRIMARY KEY ("payment_type_id")
    ) WITH (oids = false);
    """
    
    cursor = conn.cursor()
    cursor.execute(drop_if_payment_types_table_exists)
    print("'payment_types' database being created....")
    cursor.execute(create_payment_types_table)
    print("Table created successfully.")
    conn.commit()
    cursor.close()
    
create_payment_types_db_table(conn)
    
#-------------------------------------------------------------------------------

def create_products_db_table(conn):
    drop_if_products_table_exists = """
        DROP TABLE IF EXISTS "products" CASCADE;
        DROP SEQUENCE IF EXISTS products_product_id_seq;
        CREATE SEQUENCE products_product_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;
    """
    
    create_products_table = """
        CREATE TABLE "public"."products" (
        "product_id" integer DEFAULT nextval('products_product_id_seq') NOT NULL,
        "product_name" character varying(100),
        CONSTRAINT "products_pkey" PRIMARY KEY ("product_id")
    ) WITH (oids = false);
    """
    
    cursor = conn.cursor()
    cursor.execute(drop_if_products_table_exists)
    print("'products' table being created....")
    cursor.execute(create_products_table)
    print("Table created successfully.")
    conn.commit()
    cursor.close()    

create_products_db_table(conn)
    
#---------------------------------------------------------------------------

def add_foreign_key_constraints(conn):
    alter_orders_foreign_keys = """
        ALTER TABLE ONLY "public"."orders" ADD CONSTRAINT "orders_location_id_fkey" FOREIGN KEY (location_id) REFERENCES locations(location_id) NOT DEFERRABLE;
        ALTER TABLE ONLY "public"."orders" ADD CONSTRAINT "orders_payment_type_id_fkey" FOREIGN KEY (payment_type_id) REFERENCES payment_types(payment_type_id) NOT DEFERRABLE;
    """
    
    alter_order_products_foreign_keys = """
        ALTER TABLE ONLY "public"."orders_products" ADD CONSTRAINT "orders_products_order_id_fkey" FOREIGN KEY (order_id) REFERENCES orders(order_id) NOT DEFERRABLE;
        ALTER TABLE ONLY "public"."orders_products" ADD CONSTRAINT "orders_products_product_id_fkey" FOREIGN KEY (product_id) REFERENCES products(product_id) NOT DEFERRABLE;
    """
    
    cursor = conn.cursor()
    print("Key constraints being created....")
    cursor.execute(alter_orders_foreign_keys)
    cursor.execute(alter_order_products_foreign_keys)
    print("Constraints created successfully.")
    conn.commit()
    cursor.close()   

add_foreign_key_constraints(conn)
    
