import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_USERNAME')};"
        f"PWD={os.getenv('DB_PASSWORD')}"
    )
    return pyodbc.connect(conn_str)


try:
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT TOP 5 * FROM onboarding")  # Replace with your actual table name
    results = cursor.fetchall()
    print("Results:", results)
except Exception as e:
    print("Error:", e)
    results = []  # Ensure results is always defined
finally:
    if 'connection' in locals() and connection:  # Ensure connection is closed only if it was successfully created
        connection.close()
