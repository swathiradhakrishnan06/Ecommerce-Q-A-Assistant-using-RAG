import os
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from data_processor import DataProcessor

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Good Guys FAQ Assistant",
    page_icon="🛍️",
    layout="wide"
)

# Initialize session state
if "conversation" not in st.session_state:
    st.session_state.conversation = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def initialize_rag():
    # Initialize the LLM
    llm = ChatGroq(model="llama-3.3-70b-versatile"
    )
    
    # Initialize the data processor
    processor = DataProcessor()
    chunks = processor.load_data()
    vector_store = processor.create_vector_store(chunks)
    
    # Initialize conversation memory
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    # Create the conversation chain
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory
    )
    
    return conversation_chain

# Main app
st.title("🛍️ Good Guys FAQ Assistant")
st.write("Ask me anything about products, services, or policies!")

# Initialize the RAG pipeline if not already done
if st.session_state.conversation is None:
    with st.spinner("Initializing the FAQ assistant..."):
        st.session_state.conversation = initialize_rag()

# Chat interface
user_question = st.text_input("Your question:")

if user_question:
    # Get response from the conversation chain
    response = st.session_state.conversation({"question": user_question})
    
    # Add to chat history
    st.session_state.chat_history.append(("You", user_question))
    st.session_state.chat_history.append(("Assistant", response["answer"]))

# Display chat history
for role, message in st.session_state.chat_history:
    if role == "You":
        st.write(f"👤 **You:** {message}")
    else:
        st.write(f"🤖 **Assistant:** {message}") 