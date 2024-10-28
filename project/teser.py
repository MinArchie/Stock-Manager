import mysql.connector
from mysql.connector import Error

def create_connection():
    """ Create a database connection to the MySQL database """
    try:
        print("Attempting to connect to the database...")
        connection = mysql.connector.connect(
            host='localhost',
            user='root', 
            password='Swathi1015',  
            database='StockManagementDB',  
            port=3306,  
            connection_timeout=10  # Timeout after 10 seconds
        )


        if connection.is_connected():
            print("Successfully connected to the database")
            connection.close()
    except Error as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    create_connection()
