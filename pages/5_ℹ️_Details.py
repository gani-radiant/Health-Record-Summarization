import streamlit as st
import pandas as pd
import plotly
import plotly.express as px
from PIL import Image
import mysql.connector

# Establishing a connection to the MySQL database
conn = mysql.connector.connect(
         host="localhost",
    user="root",
    password="12345678",
    database="pro1"
    )

# Creating a cursor object
c = conn.cursor()

# Function to create the table
def create_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS detailstable (
            name VARCHAR(255),
            gender VARCHAR(255),
            dob DATE,
            contact VARCHAR(255),
            blood_group VARCHAR(255),
            pat_his TEXT,
            doc_name VARCHAR(255)
        )
    ''')

# Function to add data to the table
def add_data(name, gender, dob, contact, blood_group, pat_his, doc_name):
    c.execute('''
        INSERT INTO detailstable(name, gender, dob, contact, blood_group, pat_his, doc_name) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (name, gender, dob, contact, blood_group, pat_his, doc_name))
    conn.commit()

# Function to view all data
def view_all_data():
    c.execute('SELECT * FROM detailstable')
    data = c.fetchall()
    return data

# Function to view distinct names
def view_all_data_names():
    c.execute('SELECT DISTINCT name FROM detailstable')
    data = c.fetchall()
    return data

# Function to get data by name
def get_name(name):
    c.execute('SELECT * FROM detailstable WHERE name=%s', (name,))
    data = c.fetchall()
    return data

# Function to edit data by name
def edit_name_data(new_name, new_gender, new_dob, new_contact, new_blood_group, new_pat_his, new_doc_name, name):
    c.execute('''
        UPDATE detailstable 
        SET name=%s, gender=%s, dob=%s, contact=%s, blood_group=%s, pat_his=%s, doc_name=%s
        WHERE name=%s
    ''', (new_name, new_gender, new_dob, new_contact, new_blood_group, new_pat_his, new_doc_name, name))
    conn.commit()

# Function to delete data by name
def delete_data(name):
    c.execute('DELETE FROM detailstable WHERE name=%s', (name,))
    conn.commit()

def main():
    st.title("HEALTH RECORDS🤔")

    menu = ["ADD", "DISPLAY", "UPDATE", "DELETE", "ABOUT"]
    choice = st.sidebar.selectbox("MENU", menu)
    create_table()

    if choice == "ADD":
        st.subheader("ADD PATIENT DETAILS")
        col1, col2 = st.columns(2)


        with col1:
            name = st.text_input("NAME")
            gender = st.radio("GENDER",("MALE","FEMALE"))
            dob = st.text_input("DATE OF BIRTH")
            contact = st.text_input("CONTACT")

        with col2:
            blood_group = st.selectbox("BLOOD GROUP", ["O+", "O-", "A+","A-","B+","B-","AB+","AB-"])
            pat_his = st.text_area("PATIENT HISTORY")
            doc_name = st.text_input("DOCTOR NAME")

        if st.button("ADD DETAILS"):
            add_data(name,gender,dob,contact,blood_group,pat_his,doc_name)
            st.success("SUCCESSFULLY ADDED: {}".format(name))


    elif choice == "DISPLAY":

        with st.expander("VIEW ALL"):
            result = view_all_data()
            df = pd.DataFrame(result, columns=["NAME", "GENDER", "DOB", "CONTACT", "BLOOD GROUP", "PATIENT HISTORY", "DOCTOR NAME"])
            st.dataframe(df)

        with st.expander("RECORD ANALYSIS"):
            gender_df = df['GENDER'].value_counts().to_frame()
            gender_df = gender_df.reset_index()
            st.dataframe(gender_df)

            p2 = px.pie(gender_df, names='index', values='GENDER')
            st.plotly_chart(p2, use_container_width=True)

            bloodgroup_df = df['BLOOD GROUP'].value_counts().to_frame()
            bloodgroup_df = bloodgroup_df.reset_index()
            st.dataframe(bloodgroup_df)

            p2 = px.pie(bloodgroup_df, names='index', values='BLOOD GROUP')
            st.plotly_chart(p2, use_container_width=True)

    elif choice == "UPDATE":
        st.subheader("EDIT PATIENT DETAILS")
        with st.expander("CURRENT DATA"):
            result = view_all_data()
            df = pd.DataFrame(result, columns=["NAME", "GENDER", "DOB", "CONTACT", "BLOOD GROUP", "PATIENT HISTORY", "DOCTOR NAME"])
            st.dataframe(df)

        list_of_names = [i[0] for i in view_all_data_names()]
        selected_name = st.selectbox("NAME", list_of_names)
        name_result = get_name(selected_name)


        if name_result:
            name = name_result[0][0]
            gender = name_result[0][1]
            dob = name_result[0][2]
            contact = name_result[0][3]
            blood_group = name_result[0][4]
            pat_his = name_result[0][5]
            doc_name = name_result[0][6]


            col1, col2 = st.beta_columns(2)

            with col1:
                new_name = st.text_input("NAME",name)
                new_gender = st.radio("GENDER", ("MALE", "FEMALE"))
                new_dob = st.text_input("DATE OF BIRTH",dob)
                new_contact = st.text_input("CONTACT",contact)

            with col2:
                new_blood_group = st.selectbox("BLOOD GROUP", ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"])
                new_pat_his = st.text_area("PATIENT HISTORY",pat_his)
                new_doc_name = st.text_input("DOCTOR NAME",doc_name)

            if st.button("UPDATE DETAILS"):
                edit_name_data(new_name, new_gender, new_dob, new_contact, new_blood_group, new_pat_his, new_doc_name, name, gender, dob, contact, blood_group, pat_his, doc_name)
                st.success("SUCCESSFULLY UPDATED: {}".format(name))

            with st.expander("UPDATED DATA"):
                result = view_all_data()
                df = pd.DataFrame(result, columns=["NAME", "GENDER", "DOB", "CONTACT", "BLOOD GROUP", "PATIENT HISTORY", "DOCTOR NAME"])
                st.dataframe(df)

    elif choice == "DELETE":
        st.subheader("DELETE PATIENT DETAILS")
        with st.expander("VIEW DATA"):
            result = view_all_data()
            df = pd.DataFrame(result, columns=["NAME", "GENDER", "DOB", "CONTACT", "BLOOD GROUP", "PATIENT HISTORY", "DOCTOR NAME"])
            st.dataframe(df)

        unique_list = [i[0] for i in view_all_data_names()]
        delete_by_data_name = st.selectbox("SELECT NAME", unique_list)
        if st.button("DELETE"):
            delete_data(delete_by_data_name)
            st.warning("DELETED: '{}'".format(delete_by_data_name))

        with st.expander("UPDATED DATA"):
            result = view_all_data()
            df = pd.DataFrame(result, columns=["NAME", "GENDER", "DOB", "CONTACT", "BLOOD GROUP", "PATIENT HISTORY", "DOCTOR NAME"])
            st.dataframe(df)

    else:
        st.subheader("ABOUT ELECTRONIC HEALTH RECORD")
        

if __name__ == '__main__':
    main()