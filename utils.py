import streamlit as st
import ollama
import json
import os

def load_chat_sessions(CHAT_HISTORY_DIR):
    files = [
        (f.replace(".json", ""), os.path.getmtime(os.path.join(CHAT_HISTORY_DIR, f)))
        for f in os.listdir(CHAT_HISTORY_DIR) if f.endswith(".json")
    ]
    sorted_files = sorted(files, key=lambda x: x[1], reverse=True)  # Sort by modified time (latest first)
    return [f[0] for f in sorted_files]


def save_chat(chat_id, messages, CHAT_HISTORY_DIR):
    file_path = os.path.join(CHAT_HISTORY_DIR, f"{chat_id}.json")
    with open(file_path, "w") as file:
        json.dump(messages, file)


def install_model(model_name):
    st.sidebar.info(f"Installing the model: {model_name}...")
    ollama.pull(model_name)
    st.sidebar.success(f"Model {model_name} installed successfully!")


def load_chat(chat_id, CHAT_HISTORY_DIR):
    file_path = os.path.join(CHAT_HISTORY_DIR, f"{chat_id}.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return [{"role": "assistant", "content": "Hello! How can I assist you today?"}]