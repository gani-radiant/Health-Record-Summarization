import streamlit as st
st.title("About Us😃")
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


lottie_url_hello = "https://lottie.host/6c3ab376-ba68-4c61-a86f-588a6b5e5e92/jg6ZGgjpBN.json"
lottie_hello = load_lottieurl(lottie_url_hello)

st_lottie(lottie_hello, key="hello")

import streamlit as st

# Create an empty list to store contact messages.
contact_messages = []

# Main Streamlit app
def main():
    st.title("Medical Recommendation Website")

    st.write("Welcome to **NEXSUS**, where cutting-edge technology meets healthcare. We are a team of dedicated professionals on a mission to revolutionize the way medical information is processed, making it more accessible and understandable for everyone. At [Your Website Name], we understand the challenges that both healthcare providers and patients face when dealing with medical reports. Often, these documents are complex, lengthy, and filled with technical jargon, making it difficult to extract crucial information quickly. That's where we come in. ")
    
    st.markdown("## Our Mission")
    st.write("Our mission is to harness the power of artificial intelligence to simplify the healthcare journey. We aim to bridge the gap between complex medical information and real-world understanding by providing accurate and concise summaries of medical reports. We believe that everyone has the right to access and comprehend their healthcare information, and our technology empowers individuals to do just that. ")
    st.markdown("## Our Team")
    st.write("Meet the dedicated individuals behind Our team consists of AI experts, healthcare professionals, and technology enthusiasts who are passionate about making a positive impact on healthcare. We are committed to pushing the boundaries of what AI can achieve in the medical field. ")
    
   

    

if __name__ == "__main__":
    main()
