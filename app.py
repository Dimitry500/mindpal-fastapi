from fastapi import FastAPI
import pyodbc
import os

app = FastAPI()

SQL_SERVER = os.getenv("SQL_SERVER", "localhost")
SQL_DATABASE = os.getenv("SQL_DATABASE", "SalesTestDB")
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SQL_SERVER};"
    f"UID={SQL_USER};"
    f"PWD={SQL_PASSWORD};"
)

@app.get("/reviews")
def get_reviews():
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        query = "SELECT * FROM [dbo].[Sales]"
        cursor.execute(query)

        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        return rows

    except Exception as e:
        return {"error": str(e)}
