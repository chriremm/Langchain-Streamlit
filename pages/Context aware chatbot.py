import sys
sys.path.append('..')
import utils
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory


st.header('Chatbot')

models = ["gpt-3.5-turbo", "gpt-4"]

class Chatbot:

    def __init__(self):
        utils.configure_openai_api_key()
        openai_model = st.sidebar.selectbox(
            "Select Model:",
            models,
            index = 0
        )
        st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
        st.sidebar.button("New Chat", on_click=utils.reset_chat)
        if openai_model:
            st.session_state['OPENAI_MODEL'] = openai_model
            self.openai_model = st.session_state['OPENAI_MODEL']
        
    
    @st.cache_resource
    def setup_chain(_self):
        st.session_state["current_key"] = st.session_state['OPENAI_API_KEY']
        st.session_state["current_model"] = st.session_state['OPENAI_MODEL']
        # print(f"new chain, model: {st.session_state['OPENAI_MODEL']}, key: {st.session_state['OPENAI_API_KEY']}")
        memory = ConversationBufferWindowMemory(k=10)
        llm = ChatOpenAI(model_name=_self.openai_model, temperature=0)
        chain = ConversationChain(llm=llm, memory=memory, verbose=True)
        return chain
    
    @utils.enable_chat_history
    def main(self):
        chain = self.setup_chain()
        
        if "current_key" not in st.session_state or st.session_state["current_key"] != st.session_state['OPENAI_API_KEY']:
            print("different key")
            st.cache_resource.clear()
            del st.session_state["messages"]
            st.rerun()
            chain = self.setup_chain

        if "current_model" not in st.session_state or st.session_state["current_model"] != st.session_state['OPENAI_MODEL']:
            print("different model")
            st.cache_resource.clear()
            del st.session_state["messages"]
            st.rerun()
            chain = self.setup_chain

        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query:
            utils.display_msg(user_query, 'user')
            with st.chat_message("assistant"):
                # st_cb = StreamHandler(st.empty())
                response = chain.invoke(user_query)
                res = response["response"]
                # utils.display_msg(user_query, 'assistant')
                st.session_state.messages.append({"role": "assistant", "content": res})
                st.rerun()



if __name__ == "__main__":
    bot = Chatbot()
    bot.main()



