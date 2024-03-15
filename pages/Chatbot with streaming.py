import sys
sys.path.append('..')
import utils
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import ChatMessage
from langchain_openai import ChatOpenAI
import streamlit as st

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

identificator = __file__
if "current_page" not in st.session_state:
    try:
        del st.session_state["messages"]
    except:
        pass
    st.session_state["current_page"] = identificator
if st.session_state["current_page"] != identificator:
    try:
        st.cache_resource.clear()
        del st.session_state["current_page"]
        del st.session_state["messages"]
    except:
        pass
st.header('Chatbot')
models = ["gpt-3.5-turbo", "gpt-4"]

def reset_chat():
    if "messages" in st.session_state:
        del st.session_state["messages"] 

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key:", type="password", placeholder="sk-...", value=st.session_state['OPENAI_API_KEY'] if 'OPENAI_API_KEY' in st.session_state else '',)
    if openai_api_key.startswith('sk-'):
        openai_model = st.selectbox(
                "Select Model:",
                models,
                index = 0,
                
            )
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.button("New Chat", on_click=reset_chat)
    
if openai_api_key.startswith('sk-'):
    st.session_state['OPENAI_API_KEY'] = openai_api_key
    if "cur_key" not in st.session_state or openai_api_key != st.session_state["cur_key"]:
        st.session_state["cur_key"] = openai_api_key
        reset_chat()

    if "cur_model" not in st.session_state or openai_model != st.session_state["cur_model"]:
        st.session_state["cur_model"] = openai_model
        reset_chat()

    if "messages" not in st.session_state:
        st.session_state["messages"] = [ChatMessage(role="assistant", content="How can I help you?")]

    for msg in st.session_state.messages:
        st.chat_message(msg.role).write(msg.content)

    if prompt := st.chat_input():
        st.session_state.messages.append(ChatMessage(role="user", content=prompt))
        st.chat_message("user").write(prompt)

        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        with st.chat_message("assistant"):
            stream_handler = StreamHandler(st.empty())
            llm = ChatOpenAI(model_name=openai_model, openai_api_key=openai_api_key, streaming=True, callbacks=[stream_handler])
            response = llm.invoke(st.session_state.messages)
            st.session_state.messages.append(ChatMessage(role="assistant", content=response.content))
else:
    st.warning('Please enter a valid OpenAI API key!', icon='⚠️')
    st.info("Obtain your key from this link: https://platform.openai.com/account/api-keys")