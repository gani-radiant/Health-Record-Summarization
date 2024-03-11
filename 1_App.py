import streamlit as st
from PyPDF2 import PdfReader
import tempfile
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub

import mysql.connector

# Function to establish a database connection
def establish_connection():
    connection = mysql.connector.connect(
         host="localhost",
    user="root",
    password="12345678",
    database="pro1"
    )
    return connection

# Function to store the response in the database table
def store_response_in_database(response):
    connection = establish_connection()
    cursor = connection.cursor()

    # Define your MySQL table schema if it doesn't exist
    create_table_query = """
        CREATE TABLE IF NOT EXISTS responses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            response_text TEXT
        )
    """
    cursor.execute(create_table_query)

    # Insert the response into the table
    insert_query = "INSERT INTO responses (response_text) VALUES (%s)"
    cursor.execute(insert_query, (response,))
    
    # Commit the transaction and close the connection
    connection.commit()
    connection.close()

import time
import requests

import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_url_hello = "https://lottie.host/e4893a05-8a58-423e-8f29-8c1d4cef3e6e/qrXwbeHoU7.json"
lottie_hello = load_lottieurl(lottie_url_hello)

st_lottie(lottie_hello, key="hello")


import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

embedding = HuggingFaceEmbeddings()

def main():
    # Display the header for the application
    st.header("AI-Powered Medical Records Summarization")
    # Allow the user to upload a PDF file
    pdf = st.file_uploader("Upload your Medical Records", type="pdf")

    if pdf is not None:
        # Save the uploaded PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_pdf:
            temp_pdf.write(pdf.read())
            temp_pdf_path = temp_pdf.name

        # Load the PDF document from the temporary file
        loader = UnstructuredPDFLoader(temp_pdf_path)
        document = loader.load()

        # Convert the document into chunks of the desired size
        text_splitter = CharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
        docs = text_splitter.split_documents(document)

        # Create a vector store from the document chunks
        db = FAISS.from_documents(docs, embedding)

        # Initialize the Hugging Face model for question answering
        llm = HuggingFaceHub(
            repo_id="lmsys/fastchat-t5-3b-v1.0",
            model_kwargs={"temperature": 0, "max_length": 400}
        )
        # Load the question answering chain
        chain = load_qa_chain(llm, chain_type="stuff")

        # Accept user's question/query
        query = st.text_input("Ask questions")

        if query:
            # Perform similarity search in the document database
            docs = db.similarity_search(query)
            # Generate the response using the question answering chain
            response = chain.run(input_documents=docs, question=query)
            # Display the response to the user
            cleaned_response = response.replace("<pad>", "")
            st.write(cleaned_response)
            # Store the response in the database
            store_response_in_database(cleaned_response)

        # Remove the temporary PDF file
        os.remove(temp_pdf_path)
    else:
        st.write("Upload Medical Record to continue.")

if __name__ == "__main__":
    main()



# import base64
# import os
# import tempfile
# import mysql.connector
# import requests
# import streamlit as st
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.document_loaders import UnstructuredPDFLoader
# from langchain.vectorstores import FAISS
# from langchain.chains.question_answering import load_qa_chain
# from langchain import HuggingFaceHub
# from PyPDF2 import PdfReader
# import plotly.express as px
# import pydeck as pdk  # Import pydeck for Lottie animations

# df = px.data.iris()

# # Function to establish a database connection
# def establish_connection():
#     connection = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="12345678",
#         database="pro1"
#     )
#     return connection

# # Function to store the response in the database table
# def store_response_in_database(response):
#     connection = establish_connection()
#     cursor = connection.cursor()

#     # Define your MySQL table schema if it doesn't exist
#     create_table_query = """
#         CREATE TABLE IF NOT EXISTS responses (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             response_text TEXT
#         )
#     """
#     cursor.execute(create_table_query)

#     # Insert the response into the table
#     insert_query = "INSERT INTO responses (response_text) VALUES (%s)"
#     cursor.execute(insert_query, (response,))
    
#     # Commit the transaction and close the connection
#     connection.commit()
#     connection.close()

# # Load Lottie animation using pydeck
# def load_lottieurl(url: str):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()

# # Main function
# def main():
#     # Display the header for the application
#     st.header("AI-Powered Medical Records Summarization")
    
#     # Load Lottie animation
#     lottie_url_hello = "https://lottie.host/e4893a05-8a58-423e-8f29-8c1d4cef3e6e/qrXwbeHoU7.json"
#     lottie_hello = load_lottieurl(lottie_url_hello)
    
#     # Display Lottie animation using pydeck
#     deck = pdk.Deck(layers=[], initial_view_state=pdk.ViewState(latitude=0, longitude=0))
#     deck.pdk_as_json["layers"] = [pdk.Layer(type="Lottie", data=lottie_hello)]
#     st.pydeck_chart(deck)

#     # Allow the user to upload a PDF file
#     pdf = st.file_uploader("Upload your Medical Records", type="pdf")

#     if pdf is not None:
#         # Save the uploaded PDF to a temporary file
#         with tempfile.NamedTemporaryFile(delete=False) as temp_pdf:
#             temp_pdf.write(pdf.read())
#             temp_pdf_path = temp_pdf.name

#         # Load the PDF document from the temporary file
#         loader = UnstructuredPDFLoader(temp_pdf_path)
#         document = loader.load()

#         # Convert the document into chunks of the desired size
#         text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
#         docs = text_splitter.split_documents(document)

#         # Create a vector store from the document chunks
#         db = FAISS.from_documents(docs, embedding)

#         # Initialize the Hugging Face model for question answering
#         llm = HuggingFaceHub(
#             repo_id="lmsys/fastchat-t5-3b-v1.0",
#             model_kwargs={"temperature": 0, "max_length": 400}
#         )
#         # Load the question answering chain
#         chain = load_qa_chain(llm, chain_type="stuff")

#         # Accept user's question/query
#         query = st.text_input("Ask questions")

#         if query:
#             # Perform similarity search in the document database
#             docs = db.similarity_search(query)
#             # Generate the response using the question answering chain
#             response = chain.run(input_documents=docs, question=query)
#             # Display the response to the user
#             cleaned_response = response.replace("<pad>", "")
#             st.write(cleaned_response)
#             # Store the response in the database
#             store_response_in_database(cleaned_response)

#         # Remove the temporary PDF file
#         os.remove(temp_pdf_path)
#     else:
#         st.write("Upload Medical Record to continue.")

# if __name__ == "__main__":
#     main()
