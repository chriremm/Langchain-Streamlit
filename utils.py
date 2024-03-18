import os
import random
import streamlit as st
from langchain.schema import ChatMessage
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

models = ["gpt-3.5-turbo", "gpt-4"]

def short_summary():
    chat = ChatOpenAI(model_name=models[0], temperature=0)
    messages = [SystemMessage(content="You will receive a list of messages, each with a role user or assistant.  Return only a summary with a lenght of three to five words."),
                HumanMessage(content=str(st.session_state["messages"]))]
    res = chat.invoke(messages)
    return res.content

def reset_chat():
    if "messages" in st.session_state:
        if not "loaded" in st.session_state or not st.session_state["loaded"]:
            if len(st.session_state["messages"]) > 1:
                if st.session_state["current_page"]  not in st.session_state:
                    st.session_state[st.session_state["current_page"]] = [st.session_state["messages"]]
                    st.session_state["page_names"] = [short_summary()]
                else:
                    st.session_state[st.session_state["current_page"]].append(st.session_state["messages"])
                    st.session_state["page_names"].append(short_summary())
        elif "loaded" in st.session_state and st.session_state["loaded"]:
            st.session_state[st.session_state["current_page"]][st.session_state["loaded_from"]] = st.session_state["messages"] 
            
        
        del st.session_state["messages"]
        st.session_state["loaded"] = False

def enable_chat_history(func):
    if os.environ.get("OPENAI_API_KEY"):
        

        # to clear chat history after swtching chatbot
        current_page = func.__qualname__

        
        if "current_page" not in st.session_state:
            try:
                del st.session_state["messages"]
            except:
                pass
            st.session_state["current_page"] = current_page
        elif st.session_state["current_page"] != current_page:
            # if not "loaded" in st.session_state or not st.session_state["loaded"]:
            #     if len(st.session_state["messages"]) > 1:
            #         if st.session_state["current_page"]  not in st.session_state:
            #             st.session_state[st.session_state["current_page"] ] = [st.session_state["messages"]]
            #         else:
            #             st.session_state[st.session_state["current_page"] ].append(st.session_state["messages"])
            # elif "loaded" in st.session_state and st.session_state["loaded"]:
            #     st.session_state[st.session_state["current_page"]][st.session_state["loaded_from"]] = st.session_state["messages"] 
            # st.session_state["loaded"] = False
            # try:
            #     del st.session_state["messages"]
            # except:
            #     pass
            reset_chat()
            st.session_state["current_page"] = current_page

        

        # to show chat history on ui ChatMessage(role="assistant", content="How can I help you?")
        if "messages" not in st.session_state:
            st.session_state["messages"] = [ChatMessage(role="assistant", content="How can I help you?")]
            
        for msg in st.session_state.messages:
            st.chat_message(msg.role).write(msg.content)

    def execute(*args, **kwargs):
        func(*args, **kwargs)
    return execute


def display_msg(msg, author):
    """Method to display message on the UI

    Args:
        msg (str): message to display
        author (str): author of the message -user/assistant
    """
    st.session_state.messages.append(ChatMessage(role=author, content=msg))
    st.chat_message(author).write(msg)

def configure_openai_api_key():
    openai_api_key = st.sidebar.text_input(
        label="OpenAI API Key:",
        type="password",
        value=st.session_state['OPENAI_API_KEY'] if 'OPENAI_API_KEY' in st.session_state else '',
        placeholder="sk-...",
        # on_change=api_key_change
        )
    if openai_api_key.startswith('sk-'):
        st.session_state['OPENAI_API_KEY'] = openai_api_key
        if not 'OPENAI_API_KEY' in os.environ or os.environ['OPENAI_API_KEY'] != openai_api_key:
            os.environ['OPENAI_API_KEY'] = openai_api_key
            st.rerun()
    else:
        st.warning('Please enter a valid OpenAI API key!', icon='⚠️')
        st.info("Obtain your key from this link: https://platform.openai.com/account/api-keys")
        st.stop()
    return openai_api_key


def configure_model():
    if 'OPENAI_API_KEY' in os.environ:
        openai_model = st.sidebar.selectbox(
            "Select Model:",
            models,
            index = 0
        )
        st.session_state['OPENAI_MODEL'] = openai_model


        
    
def configure_new_chat():
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    st.sidebar.button("New Chat", on_click=reset_chat)    

def check_key():
    if "current_key" not in st.session_state or st.session_state["current_key"] != st.session_state['OPENAI_API_KEY']:
        reset_chat()
        st.rerun()

def check_model():
    if "current_model" not in st.session_state or st.session_state["current_model"] != st.session_state['OPENAI_MODEL']:  
        reset_chat()
        st.rerun()

def load_old_chats():
    current_page = st.session_state["current_page"]
    if current_page in st.session_state:
            i = len(st.session_state[current_page]) -1
            for page in reversed(st.session_state[current_page]):
                if st.sidebar.button(st.session_state["page_names"][i], key=str(i)):
                    reset_chat()
                    st.session_state["loaded"] = True
                    st.session_state["loaded_from"] = i
                    st.session_state["messages"] = st.session_state[current_page][i]
                    st.rerun()
                i = i-1