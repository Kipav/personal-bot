# Fix for SQLite version issue on Streamlit Cloud
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    # pysqlite3 not available, use default sqlite3
    pass

import streamlit as st
from query_data import query_bot

st.title("Ask about Kirill")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask anything about Kirill..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            
            result = query_bot(prompt)
            
            if result["success"]:
                st.markdown(result["response"])
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": result["response"],
                })
            else:
                st.error(result["response"])
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": result["response"],
                })