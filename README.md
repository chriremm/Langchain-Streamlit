# LangChain and Streamlit Chatbot Examples

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://langchain-collection.streamlit.app/)

LangChain is a powerful framework designed to streamline the development of applications using Language Models (LLMs). It provides a comprehensive integration of various components, simplifying the process of assembling them to create robust applications.

## 💬 Sample Chatbot Implementations
This project demonstrates several chatbot implementations leveraging LangChain and Streamlit, including:
- **Context-aware Chatbot** \
  Utilizes `ConversationBufferWindowMemory` to maintain a contextual understanding of the conversation history.
  
- **Chatbot with Streaming** \
  Offers a dynamic, real-time response system to simulate a ChatGPT-like experience, with manual tracking of message history.

- **Translator Chatbot** \
  Translates text into various languages and styles, showcasing the adaptability of LangChain to different language processing tasks.

## <img src="https://streamlit.io/images/brand/streamlit-mark-color.png" width="40" height="22"> Streamlit App
Explore the chatbot examples through our multi-page Streamlit app. Access the app here: [LangChain Collection Streamlit App](https://langchain-collection.streamlit.app/)

## 🖥️ Running Locally
To run the application locally, follow these steps:
```shell
# Clone the repository
$ git clone <repository-url>

# Navigate to the project directory
$ cd <project-directory>

# Install the required dependencies
$ pip install -r requirements.txt

# Run the Streamlit app
$ streamlit run home.py
