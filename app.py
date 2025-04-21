"""Simple chat example using MCPAgent with built-in memory.
   This example demonstrates how to use MCPAgent with built-in 
   conversation history capabilities for better contextual interactions.
"""

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent,MCPClient
import os

async def run_memory_chat():
   """run a chat using MCPAgent's built-in conversation memory"""
   load_dotenv()
   os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
   #configure file path - change to this your config file
   config_file = "browser_mcp.json"

   #initialize the chat
   print("Initializing chat...")
   
   client = MCPClient.from_config_file(config_file)
   llm=ChatGroq(model="qwen-qwq-32b")

   #start the conversation
   (print("Starting conversation..."))
   agent = MCPAgent(llm=llm,client=client,max_steps=15,memory_enabled=True)

   print("\n==== Interactive MCP Chat ====")
   print("Type 'exit' or quit to end the conversation.\n")
   print("Type 'clear' to clear the memory.\n")
   print("====================================\n")

   while True:
      user_input = input("You: ")
      if user_input.lower() in ["exit","quit"]:
         print("Exiting chat...")
         break
      elif user_input.lower() == "clear":
         agent.clear_conversation_history()
         print("Conversation history cleared.")
         continue
      
      print("\nAssistance:", end="",flush=True)
      try:
         #Run the agent with the user input
         response = await agent.run(user_input)
         print(response)
      except Exception as e:
         print(f"\nError: {e}")

      finally:
        print("\n\n")
        if client and client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
   import asyncio
   asyncio.run(run_memory_chat())
         
   
    
