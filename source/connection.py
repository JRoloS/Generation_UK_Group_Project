# import pymysql
import psycopg2
import os
from dotenv import load_dotenv

# Loads in .env which contains db credentials:
load_dotenv()
host_name = os.environ.get("sql_host")
database_name = os.environ.get("sql_db")
user_name = os.environ.get("sql_user")
user_password = os.environ.get("sql_pass")


# Does what it says on the tin mate:
def setup_db_connection(host=host_name, 
                        user=user_name, 
                        password=user_password,
                        db=database_name):

    connection = psycopg2.connect(
        host = host,
        database = db,
        user = user,
        password = password
    )
    return connection