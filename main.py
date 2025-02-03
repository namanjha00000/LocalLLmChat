import streamlit as st
import ollama
import json
import os
from utils import *

CHAT_HISTORY_DIR = "chat_sessions"
if not os.path.exists(CHAT_HISTORY_DIR):
    os.makedirs(CHAT_HISTORY_DIR)

    chat_file_path = os.path.join(CHAT_HISTORY_DIR, 'Chat 1.json')

    with open(chat_file_path, 'w') as file:
        # Add content to the file (empty JSON object here as an example)
        file.write('[{"role": "assistant", "content": "Hello! How can I assist you today?"}]')


st.set_page_config(page_title="Local LLM Chat", page_icon="🤖")        # Set page config
st.markdown(
    r"""
    <style>
        .stAppDeployButton {display:none;}
        #MainMenu {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


st.sidebar.title("📂 Chat Sessions")
chat_sessions = load_chat_sessions(CHAT_HISTORY_DIR)
print(chat_sessions)
selected_chat = st.sidebar.selectbox("Choose a chat:",chat_sessions, index=0)


#new chat creator
chat_id = "Chat " + str(len(chat_sessions) + 1)
if st.sidebar.button("New Chat"):
    st.session_state.chat_id = chat_id
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]
    save_chat(chat_id, st.session_state.messages, CHAT_HISTORY_DIR)
    st.rerun()
else:
    chat_id = selected_chat



st.sidebar.markdown(
    """
    <div style="margin-top: 45vh;"></div>
    """,
    unsafe_allow_html=True
)



# Get the list of available models
model_list_response = ollama.list()
available_models = [model.model for model in model_list_response.models]

# Sidebar for model selection
st.sidebar.title("⚙️ Model")
model_name = st.sidebar.selectbox("Please select a model:", available_models, index=0)

# Input box for new model name
new_model_name = st.sidebar.text_input("Or type a new model name and press Enter:", value="")

# Check if the user has entered a new model name and pressed Enter
if new_model_name:
    if new_model_name not in available_models:
        try:
            install_model(new_model_name)
            model_list_response = ollama.list()
            available_models = [model.model for model in model_list_response.models]
            st.rerun()
        except:
            st.sidebar.warning(f"No such model {new_model_name} deos not exists!")

    else:
        st.sidebar.warning(f"Model {new_model_name} already exists!")

# Display the selected model
st.write(f"Selected Model: {model_name}")

if "chat_id" not in st.session_state or st.session_state.chat_id != chat_id:     # Save chat history to file

    st.session_state.chat_id = chat_id
    st.session_state.messages = load_chat(chat_id, CHAT_HISTORY_DIR)



for message in st.session_state.messages:           # Display chat messages
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_container = st.empty()  # Placeholder for streaming response
        full_response = ""

        response_stream = ollama.chat(model=model_name, messages=st.session_state.messages, stream=True)
        for chunk in response_stream:
            full_response += chunk["message"]["content"]
            response_container.markdown(full_response + "▌") 

        response_container.markdown(full_response)  

    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Save chat history
    save_chat(st.session_state.chat_id, st.session_state.messages, CHAT_HISTORY_DIR)
