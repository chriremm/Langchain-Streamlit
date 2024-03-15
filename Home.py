import streamlit as st

st.header("Home")
st.write("""
Langchain is a powerful framework designed to streamline the development of applications using Language Models (LLMs). It provides a comprehensive integration of various components, simplifying the process of assembling them to create robust applications.

Leveraging the power of Langchain, the creation of chatbots becomes effortless. Here are a few examples of chatbot implementations catering to different use cases:

- **Context aware Chatbot**: Using ConversationBufferWindowMemory to keep track of the previous Messages.
- **Chatbot with streaming**: Using streaming to get a more ChatGPT like Feeling. Keeps track of previous Messages manually.
- **Translator**: Translate Texts in any Language you select. You can also choose between different styles.

To explore sample usage of each chatbot, please navigate to the corresponding chatbot section.
""")