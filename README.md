# Health-Record-Summarization
The proposed system in the "AI-Powered Medical Records Summarization" concept is an artificial intelligence-based solution designed to automatically summarize extensive and complex medical records. 
Make sure you have Python's venv package installed. If not, install it by running the following command:

pip install virtualenv
Setup and Run Instructions
To set up and run the project locally, follow the steps below:

Open a new folder, create a virtual environment, and activate it:
python -m venv langchainenv
On Windows:

.\langchainenv\Scripts\activate
On Unix/Linux:

source langchainenv/bin/activate
Clone this repository and navigate to the cloned repository:
git clone https://github.com/PavanSETTEM-003/Langchain_pdf_explorer.git
cd Langchain_pdf_explorer 
Install the required dependencies:
pip install -r requirements.txt
Open the app.py file and add your Hugging Face access key in line number 12
To obtain your access key, go to the following url Hugging face Access Tokens Copy the access key from that page.
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "<your-access-key>"
Start the application:
streamlit run app.py
This will start a local server, and a web page will open in your default browser.

Use the web page interface to upload a PDF file and ask questions about its content.
Note: Ensure you have an active internet connection as the application uses Hugging Face's API for language model inference.

All the dependencies are listed in the requirements.txt file and will be installed during the setup process.
