from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
import streamlit as st
import os
import asyncio

# Load environment variables
load_dotenv()

# Add debug information
st.write("Debug Info:")
st.write(f"GROQ_API_KEY exists: {bool(os.getenv('GROQ_API_KEY'))}")

try:
    # Initialize LLM
    llm = ChatGroq(model="qwen-qwq-32b")
    st.write("LLM initialized successfully")
except Exception as e:
    st.error(f"Error initializing LLM: {str(e)}")

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