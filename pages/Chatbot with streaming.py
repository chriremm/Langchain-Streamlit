import sys
sys.path.append('..')
import utils
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import ChatMessage
from langchain_openai import ChatOpenAI
import streamlit as st

st.header('Chatbot')

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

class Chatbot_streaming:
    def __init__(self):
        utils.configure_openai_api_key()
        utils.configure_model()
        utils.configure_new_chat()

    @utils.enable_chat_history
    def main(self):

        openai_api_key = st.session_state['OPENAI_API_KEY']
        openai_model = st.session_state['OPENAI_MODEL']
        utils.check_key()
        utils.check_model()

        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query:
            utils.display_msg(user_query, 'user')

            with st.chat_message("assistant"):
                stream_handler = StreamHandler(st.empty())
                llm = ChatOpenAI(model_name=openai_model, openai_api_key=openai_api_key, streaming=True, callbacks=[stream_handler])
                response = llm.invoke(st.session_state.messages)
                st.session_state.messages.append(ChatMessage(role="assistant", content=response.content))
                
        

if __name__ == "__main__":
    bot = Chatbot_streaming()
    bot.main()
