import sys
sys.path.append('..')
import utils
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import ChatMessage
from langchain.prompts.prompt import PromptTemplate

st.header('Chatbot')  # Setting up the web app header.

# List of models available for use in the chatbot.
models = ["gpt-3.5-turbo", "gpt-4"]

class Chatbot:
    """A chatbot that uses LangChain and OpenAI's GPT models to generate responses."""

    def __init__(self):
        # Initial configuration setup for API keys and models.
        utils.configure_openai_api_key()
        utils.configure_model()
        utils.configure_new_chat()
        utils.check_loaded()
        utils.load_old_chats() 
        
    def setup_chain(self):
        """Sets up the conversation chain with a prompt template and memory for context handling."""
        # Store API key and model selection in the session state for persistence.
        st.session_state["current_key"] = st.session_state['OPENAI_API_KEY']
        st.session_state["current_model"] = st.session_state['OPENAI_MODEL']
        
        # Concatenate the history of the conversation to provide context.
        history = ""
        if "loaded" in st.session_state and st.session_state["loaded"]:
            for msg in st.session_state["messages"]:
                role = "Human" if msg.role == "user" else "AI Assistant"
                history += f"{role}: {msg.content}\n"
        
        prompt_intro = f"The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.\n\nCurrent conversation: \n{history}"
        prompt_body = "{history}\nHuman: {input}\nAI Assistant:"
        final_template = prompt_intro + prompt_body
        
        PROMPT = PromptTemplate(input_variables=["history", "input"], template=final_template)
        memory = ConversationBufferWindowMemory(k=10)  # Configure memory to keep the last 10 exchanges.
        llm = ChatOpenAI(model_name=st.session_state["current_model"], temperature=0)
        chain = ConversationChain(prompt=PROMPT, llm=llm, memory=memory, verbose=True) 
        
        return chain
    
    @utils.enable_chat_history
    def main(self):
        """Main method to process user queries and display chatbot responses."""
        # Verify the API key and model are correctly set up.
        utils.check_key()
        utils.check_model()
        
        # Initialize the conversation chain if starting fresh or resuming a loaded chat.
        if len(st.session_state["messages"]) <= 1 or ("loaded" in st.session_state and st.session_state["loaded"]):
            st.session_state["chain"] = self.setup_chain()
            
        chain = st.session_state["chain"]

        # Input field for user queries.
        user_query = st.chat_input(placeholder="Ask me anything!")
        if user_query:
            utils.display_msg(user_query, 'user')  # Display the user query in the chat interface.
            with st.chat_message("assistant"):
                # Generate and display the chatbot's response.
                response = chain.invoke(user_query)
                st.session_state.messages.append(ChatMessage(role="assistant", content=response["response"]))
                st.session_state["chain"] = chain  
                st.rerun()

if __name__ == "__main__":
    bot = Chatbot()
    bot.main()  # Start the chatbot application.
