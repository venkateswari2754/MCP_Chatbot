import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

st.title("MCP Chat Assistant - Test Mode")

# Basic environment check
api_key = os.getenv('GROQ_API_KEY')
st.write("Basic Environment Check:")
st.write(f"API Key exists: {bool(api_key)}")

# Simple input/output test
user_input = st.text_input("Type something to test:", "Hello!")
if user_input:
    st.write(f"You typed: {user_input}")

# Display current working directory and files
st.write("Current directory contents:")
try:
    files = os.listdir('.')
    for file in files:
        st.write(f"- {file}")
except Exception as e:
    st.error(f"Error listing directory: {str(e)}") 