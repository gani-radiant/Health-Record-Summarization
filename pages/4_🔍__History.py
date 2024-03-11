import streamlit as st
st.title("History😃")
import mysql.connector
import pandas as pd

# Create a MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="pro1"
)
cursor = db.cursor()

sql_query = "SELECT * FROM responses"

# Execute the SQL query
cursor.execute(sql_query)

# Fetch all the rows from the query result
data = cursor.fetchall()

# Close the cursor and connection
cursor.close()
db.close()

# Convert the data to a Pandas DataFrame for easier manipulation
df = pd.DataFrame(data, columns=["ID", "Disease"])
st.table(df)