from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
import streamlit as st
import os
import asyncio
import traceback

# Load environment variables
load_dotenv()

st.title("MCP Chat Assistant - Debug Mode")

# Debug Information Section
st.header("Debug Information")

# Environment Check
st.subheader("Environment Check")
groq_key = os.getenv('GROQ_API_KEY')
st.write(f"GROQ_API_KEY exists: {bool(groq_key)}")
if not groq_key:
    st.error("GROQ_API_KEY is missing!")

# Package Import Check
st.subheader("Package Import Check")
try:
    from langchain_groq import ChatGroq
    st.write("✅ langchain_groq imported successfully")
except Exception as e:
    st.error(f"❌ Error importing langchain_groq: {str(e)}")
    st.code(traceback.format_exc())

try:
    from mcp_use import MCPAgent, MCPClient
    st.write("✅ mcp_use imported successfully")
except Exception as e:
    st.error(f"❌ Error importing mcp_use: {str(e)}")
    st.code(traceback.format_exc())

# LLM Initialization Check
st.subheader("LLM Initialization Check")
try:
    llm = ChatGroq(model="qwen-qwq-32b")
    st.write("✅ LLM initialized successfully")
except Exception as e:
    st.error(f"❌ Error initializing LLM: {str(e)}")
    st.code(traceback.format_exc())

# Config File Check
st.subheader("Config File Check")
try:
    config_file = "browser_mcp.json"
    with open(config_file, 'r') as f:
        st.write(f"✅ Config file {config_file} found and readable")
except Exception as e:
    st.error(f"❌ Error with config file: {str(e)}")
    st.code(traceback.format_exc())

# Initialize Streamlit state
if 'agent' not in st.session_state:
    # Configure file path
    config_file = "browser_mcp.json"
    
    # Initialize the chat
    client = MCPClient.from_config_file(config_file)
    st.session_state.agent = MCPAgent(llm=llm, client=client, max_steps=15, memory_enabled=True)
    st.session_state.messages = []

# Streamlit UI
st.title("MCP Chat Assistant")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # Run the agent with the user input
            response = asyncio.run(st.session_state.agent.run(prompt))
            message_placeholder.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            message_placeholder.error(f"Error: {e}")

# Add a button to clear chat history
if st.button("Clear Chat History"):
    st.session_state.agent.clear_conversation_history()
    st.session_state.messages = []
    st.rerun() 