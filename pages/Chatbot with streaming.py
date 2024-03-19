import sys
sys.path.append('..') 
import utils
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import ChatMessage
from langchain_openai import ChatOpenAI
import streamlit as st

st.header('Chatbot')  # Display a page header.

class StreamHandler(BaseCallbackHandler):
    """Handles the streaming of new tokens from the language model to update the chat interface in real time."""
    
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Append each new token from the LLM to the chat display."""
        self.text += token
        self.container.markdown(self.text) 

class Chatbot_streaming:
    """Defines the main chatbot functionality with streaming responses."""
    
    def __init__(self):
        # Configuration setup for the OpenAI API key, model, and chat session.
        utils.configure_openai_api_key()
        utils.configure_model()
        utils.configure_new_chat()
        utils.check_loaded()
        utils.load_old_chats()
        

    @utils.enable_chat_history
    def main(self):
        """Main function to handle user input and display chatbot responses."""
        
        # Retrieve OpenAI API key and model from session state.
        openai_api_key = st.session_state['OPENAI_API_KEY']
        openai_model = st.session_state['OPENAI_MODEL']
        
        # Check if the API key and model are valid and configured correctly.
        utils.check_key()
        utils.check_model()

        user_query = st.chat_input(placeholder="Ask me anything!")  # Input field for user queries.
        if user_query:
            # Display the user's question in the chat.
            utils.display_msg(user_query, 'user')

            with st.chat_message("assistant"):
                # Initialize the streaming handler for real-time chat updates.
                stream_handler = StreamHandler(st.empty())
                # Create a LangChain OpenAI chat model with streaming enabled.
                llm = ChatOpenAI(model_name=openai_model, openai_api_key=openai_api_key, streaming=True, callbacks=[stream_handler])
                # Invoke the model with the current chat history and add the response to the chat.
                response = llm.invoke(st.session_state.messages)
                st.session_state.messages.append(ChatMessage(role="assistant", content=response.content))
                

if __name__ == "__main__":
    bot = Chatbot_streaming()
    bot.main()  # Run the chatbot streaming application.
