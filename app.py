import os
import tempfile
import streamlit as st
from streamlit_chat import message
from rag import ChatPDF

st.set_page_config(page_title="Olympic review chat")

def display_messages():
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()


def process_input():
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
            agent_text = st.session_state["assistant"].ask(user_text)

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))


def initialize_and_persist_pdf():
    newChat = ChatPDF()
    st.session_state["assistant"] = newChat
    st.session_state["messages"] = []
    st.session_state["user_input"] = ""

    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.session_state["ingestion_spinner"], st.spinner(f"Ingesting {file.name}"):
            st.session_state["assistant"].ingest(file_path)
        os.remove(file_path)

def switch_persona():
    if st.session_state["assistant"] is not None:
        st.session_state["assistant"].switch_prompt()
        st.session_state["messages"].append(("Switching prompt to "+st.session_state["assistant"].active_prompt, False))

def page():
    st.header("Olympic games highlights bot")
    st.button("Switch Persona", type="primary", on_click=switch_persona)

    if len(st.session_state) == 0:
        st.session_state["messages"] = []

    
    st.file_uploader(
        "Upload document",
        type=["pdf"],
        key="file_uploader",
        on_change=initialize_and_persist_pdf,
        label_visibility="collapsed",
        accept_multiple_files=True,
    )


    st.session_state["ingestion_spinner"] = st.empty()
    display_messages()
    st.text_input("Message", key="user_input", on_change=process_input)


if __name__ == "__main__":
    page()