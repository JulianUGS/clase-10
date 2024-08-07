import streamlit as st
from main import *
from PIL import Image
import time

img = Image.open("./imagen.png")

st.set_page_config(page_title="Diario del Cazador", page_icon=img)


usuario = "🪡"
bot = "🩻"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
col1, col2, col3 = st.columns([20, 5, 10])
with col1:
    st.title("Diario del Cazador")
with col2:
    pass
with col3:
    st.image(img, width=200)
    if st.button("Borrar Historial"):
        st.session_state.messages = []
        chat_history = []
        memory.clear()
        
st.divider()
    
    
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    avatar = usuario if message['role'] == "user" else bot
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        
# Accept user input
if prompt := st.chat_input("Que necesitás saber?"):
    while prompt is None:
        time.sleep()
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user", avatar=usuario):
        st.markdown(prompt)
        
        chat_history = "\n".join([message["content"] for message in st.session_state.messages if message["role"] == "user"])

    with st.chat_message("assistant", avatar=bot):
        contenedor_mensaje = st.empty()
        full_response= ""
        
        assistant_response = chatbot(prompt, chat_history)
        
        st.markdown(assistant_response)
    
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    
    # Uncomment if you want to hide Streamlit style elements
hide_st_style = """
             <style>
             #MainMenu {visibility: hidden;}
             footer {visibility: hidden;}
             header {visibility: hidden;}
             </style>
             """
st.markdown(hide_st_style, unsafe_allow_html=True)