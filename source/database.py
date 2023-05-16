import psycopg2
import os
#-------------------------------------------------------------
#from dotenv import load_dotenv

#[!] FOR LOCAL POSTGRESQL DATABASE TESTING ONLY:

# load_dotenv()
# host_name = os.environ.get("sql_host")
# database_name = os.environ.get("sql_db")
# user_name = os.environ.get("sql_user")
# user_password = os.environ.get("sql_pass")
# port = os.environ.get('sql_port')

#------------------------------------------------------------

def setup_db_connection(host, 
                        user, 
                        password,
                        db,
                        port,
                        invocation_id):
    
    print(f"Connecting to database...., invocation_id = {invocation_id}")
    conn = psycopg2.connect(
        host = host,
        database = db,
        user = user,
        password = password,
        port = port
    )
    print(f"Connection established., invocation_id = {invocation_id}")
    return conn

# call method
#conn = setup_db_connection()

#------------------------------------------------------------------------------

# Used to call ALL DATABASE CREATE FUNCTIONS BELOW for Redshift:

def create_redshift_database_schema(cursor, invocation_id):
    
    create_locations_db_table(cursor, invocation_id)
    create_orders_db_table(cursor, invocation_id)
    create_orders_products_db_table(cursor, invocation_id)
    create_payment_types_db_table(cursor, invocation_id)
    create_products_db_table(cursor, invocation_id)
    cursor.connection.commit()
    #add_foreign_key_constraints(cursor)

#-----------------------------------------------------------------------------

def create_locations_db_table(cursor, invocation_id):
    
    create_locations_table = """
        CREATE TABLE IF NOT EXISTS "public"."locations" (
        "location_id" int identity(1, 1),
        "location_name" VARCHAR(100) NOT NULL,
        CONSTRAINT "locations_pkey" PRIMARY KEY ("location_id")
    );
    """
    
    print(f"'locations' table being created...., invocation_id = {invocation_id}")
    cursor.execute(create_locations_table)
    print(f"Table created successfully., invocation_id = {invocation_id}")
    

# call method
#create_locations_db_table(conn)

#-------------------------------------

def create_orders_db_table(cursor, invocation_id):
    
    create_orders_table = """
        CREATE TABLE IF NOT EXISTS "public"."orders" (
        "order_id" int identity(1, 1),
        "date_time" timestamp NOT NULL,
        "location_id" integer NOT NULL,
        "transaction_total" numeric(10,2) NOT NULL,
        "payment_type_id" integer NOT NULL,
        CONSTRAINT "orders_pkey" PRIMARY KEY ("order_id"),
        CONSTRAINT "orders_location_id_fkey" FOREIGN KEY (location_id) REFERENCES locations(location_id) NOT DEFERRABLE,
        CONSTRAINT "orders_payment_type_id_fkey" FOREIGN KEY (payment_type_id) REFERENCES payment_types(payment_type_id) NOT DEFERRABLE
    );
    """

    print(f"'orders' table being created...., invocation_id = {invocation_id}")
    cursor.execute(create_orders_table)
    print(f"Table created successfully., invocation_id = {invocation_id}")
    

# call method
#create_orders_db_table(conn)

#-------------------------------------

def create_orders_products_db_table(cursor, invocation_id):
    
    create_orders_products_table = """
        CREATE TABLE IF NOT EXISTS "public"."orders_products" (
        "order_id" integer NOT NULL,
        "product_id" integer NOT NULL,
        "product_price" numeric(10,2),
        CONSTRAINT "orders_products_order_id_fkey" FOREIGN KEY (order_id) REFERENCES orders(order_id) NOT DEFERRABLE
    );
    """
    
    print(f"'orders_products' database being created...., invocation_id = {invocation_id}")
    cursor.execute(create_orders_products_table)
    print(f"Table created successfully., invocation_id = {invocation_id}")
    

# call method
#create_orders_products_db_table(conn)

#-------------------------------------------------------------------------------

def create_payment_types_db_table(cursor, invocation_id):
    
    create_payment_types_table = """
        CREATE TABLE IF NOT EXISTS "public"."payment_types" (
        "payment_type_id" int identity(1, 1),
        "payment_name" VARCHAR(10),
        CONSTRAINT "payment_types_pkey" PRIMARY KEY ("payment_type_id")
    );
    """
    
    print(f"'payment_types' database being created...., invocation_id = {invocation_id}")
    cursor.execute(create_payment_types_table)
    print(f"Table created successfully., invocation_id = {invocation_id}")
    
# call method
#create_payment_types_db_table(conn)
    
#-------------------------------------------------------------------------------

def create_products_db_table(cursor, invocation_id):
    
    create_products_table = """
        CREATE TABLE IF NOT EXISTS "public"."products" (
        "product_id" int identity(1, 1),
        "product_name" VARCHAR(100),
        CONSTRAINT "products_pkey" PRIMARY KEY ("product_id"),
        CONSTRAINT "orders_products_product_id_fkey" FOREIGN KEY (product_id) REFERENCES products(product_id) NOT DEFERRABLE
    );
    """
    
    print(f"'products' table being created...., invocation_id = {invocation_id}")
    cursor.execute(create_products_table)
    print(f"Table created successfully., invocation_id = {invocation_id}")  

# call method
#create_products_db_table(conn)
    
#---------------------------------------------------------------------------

# def add_foreign_key_constraints(cursor):
#     alter_orders_foreign_keys = """
#         ALTER TABLE "public"."orders" ADD CONSTRAINT "orders_location_id_fkey" FOREIGN KEY (location_id) REFERENCES locations(location_id) NOT DEFERRABLE;
#         ALTER TABLE "public"."orders" ADD CONSTRAINT "orders_payment_type_id_fkey" FOREIGN KEY (payment_type_id) REFERENCES payment_types(payment_type_id) NOT DEFERRABLE;
#     """
    
#     alter_order_products_foreign_keys = """
#         ALTER TABLE "public"."orders_products" ADD CONSTRAINT "orders_products_order_id_fkey" FOREIGN KEY (order_id) REFERENCES orders(order_id) NOT DEFERRABLE;
#         ALTER TABLE "public"."orders_products" ADD CONSTRAINT "orders_products_product_id_fkey" FOREIGN KEY (product_id) REFERENCES products(product_id) NOT DEFERRABLE;
#     """
    
#     print("Key constraints being created....")
#     cursor.execute(alter_orders_foreign_keys)
#     cursor.execute(alter_order_products_foreign_keys)
#     print("Constraints created successfully.")
   

# call method
#add_foreign_key_constraints(conn)
    
#------------------------------------------------------------------------------
