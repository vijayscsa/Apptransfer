import streamlit as st
import asyncio
from mcp_client import MCPClient

st.set_page_config(page_title="MCP Chatbot", layout="wide")

st.title("🤖 MCP Client Chatbot UI")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

mcp_client = MCPClient()

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Waiting for MCP server..."):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(mcp_client.call_mcp(user_input))
                bot_reply = response.get("result", {}).get("message", "No reply from MCP Server")
            except Exception as e:
                bot_reply = f"⚠ Error contacting MCP Server:\n{e}"

        st.write(bot_reply)

    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
