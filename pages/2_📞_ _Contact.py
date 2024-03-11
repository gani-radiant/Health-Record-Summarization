import streamlit as st


import mysql.connector

# Create a MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="pro1"
)
cursor = db.cursor()

# Create a table to store contact messages if it doesn't exist
create_table_query ="""CREATE TABLE IF NOT EXISTS contact_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    message TEXT
)"""
cursor.execute(create_table_query)

# Main Streamlit app
def main():
    st.title("Contact Us😃")

    # Input fields for contact information
    name = st.text_input("Name:")
    email = st.text_input("Email:")
    message = st.text_area("Message:")

    if st.button("Submit"):
        if name and email and message:
            # Store the contact message in the database
            insert_query = "INSERT INTO contact_messages (name, email, message) VALUES (%s, %s, %s)"
            values = (name, email, message)
            cursor.execute(insert_query, values)
            db.commit()

            # Clear the input fields
            name = ""
            email = ""
            message = ""
        else:
            st.warning("Please fill in all fields before submitting.")

#    # Display the contact messages
#     st.subheader("Contact Messages:")
#     cursor.execute("SELECT name, email, message FROM contact_messages")
#     messages = cursor.fetchall()
#     for msg in messages:
#         st.write(f"Name: {msg[0]}")
#         st.write(f"Email: {msg[1]}")
#         st.write(f"Message: {msg[2]}")
#         st.write("------")

if __name__ == "__main__":
    main()