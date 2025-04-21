import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("MCP Chat Assistant")

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display assistant response
    with st.chat_message("assistant"):
        response = f"You said: {prompt}\nThis is a test response. API integration coming soon!"
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

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

st.title("Hello World!")
st.write("This is a test app")

if st.button("Click me!"):
    st.write("Button was clicked!") 