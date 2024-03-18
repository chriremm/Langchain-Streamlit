import sys
sys.path.append('..')
import utils
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import ChatMessage
from langchain.prompts.prompt import PromptTemplate

st.header('Chatbot')

models = ["gpt-3.5-turbo", "gpt-4"]

class Chatbot:

    def __init__(self):
        utils.configure_openai_api_key()
        utils.configure_model()
        utils.configure_new_chat()
        if "loaded" in st.session_state and st.session_state["loaded"]:
            loaded_from = st.session_state["loaded_from"]
            st.sidebar.info(f"Currently loaded from chat {loaded_from}.")
        utils.load_old_chats()
        
        
    
    def setup_chain(_self):
        st.session_state["current_key"] = st.session_state['OPENAI_API_KEY']
        st.session_state["current_model"] = st.session_state['OPENAI_MODEL']
        # print(f"new chain, model: {st.session_state['OPENAI_MODEL']}, key: {st.session_state['OPENAI_API_KEY']}")
        h = "" 
        if "loaded" in st.session_state and st.session_state["loaded"]:
            for msg in st.session_state["messages"]:
                if msg.role == "user":
                    h += f"Human: {msg.content}\n"
                else:
                    h += f"AI Assistant: {msg.content}\n"
        print(f"h: {h}")
        temp1 = f"The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.\n\nCurrent conversation: \n{h}"
        
        temp2 = """{history}
Human: {input}
AI Assistant:"""
        final_temp = temp1 + temp2
        PROMPT = PromptTemplate(input_variables=["history", "input"], template=final_temp)
        memory = ConversationBufferWindowMemory(k=10)
        llm = ChatOpenAI(model_name=st.session_state["current_model"], temperature=0)
        chain = ConversationChain(prompt=PROMPT,llm=llm, memory=memory, verbose=True)
        return chain
    
    @utils.enable_chat_history
    def main(self):
        utils.check_key()
        print("check")
        utils.check_model()
        
        if len(st.session_state["messages"]) <= 1 or ("loaded" in st.session_state and st.session_state["loaded"]):
            st.session_state["chain"] = self.setup_chain()
            
        chain = st.session_state["chain"]

        

        

        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query:
            utils.display_msg(user_query, 'user')
            with st.chat_message("assistant"):
                response = chain.invoke(user_query)
                st.session_state.messages.append(ChatMessage(role="assistant", content=response["response"]))
                st.session_state["chain"] = chain
                st.rerun()


if __name__ == "__main__":
    bot = Chatbot()
    bot.main()



