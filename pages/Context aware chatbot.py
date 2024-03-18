import sys
sys.path.append('..')
import utils
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import ChatMessage

st.header('Chatbot')

models = ["gpt-3.5-turbo", "gpt-4"]

class Chatbot:

    def __init__(self):
        utils.configure_openai_api_key()
        utils.configure_model()
        utils.configure_new_chat()
        
    
    def setup_chain(_self):
        st.session_state["current_key"] = st.session_state['OPENAI_API_KEY']
        st.session_state["current_model"] = st.session_state['OPENAI_MODEL']
        # print(f"new chain, model: {st.session_state['OPENAI_MODEL']}, key: {st.session_state['OPENAI_API_KEY']}")
        memory = ConversationBufferWindowMemory(k=10)
        llm = ChatOpenAI(model_name=st.session_state["current_model"], temperature=0)
        chain = ConversationChain(llm=llm, memory=memory, verbose=True)
        return chain
    
    @utils.enable_chat_history
    def main(self):
        if len(st.session_state["messages"]) <= 1:
            st.session_state["chain"] = self.setup_chain()
        chain = st.session_state["chain"]
        utils.check_key()
        utils.check_model()

        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query:
            utils.display_msg(user_query, 'user')
            with st.chat_message("assistant"):
                response = chain.invoke(user_query)
                st.session_state.messages.append(ChatMessage(role="assistant", content=response["response"]))
                st.rerun()


if __name__ == "__main__":
    bot = Chatbot()
    bot.main()



