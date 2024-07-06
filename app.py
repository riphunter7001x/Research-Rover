import streamlit as st
from src.prompt import system_prompt
from src.model import llm
from src.tools import get_papers 
from src.tools import get_retriver
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough

st.title("Research Rover")

# Sidebar for topic input and fetching papers
st.sidebar.header("Research Paper Search and Embedding")
st.sidebar.write("Enter a topic to search for research papers from arXiv and embed them for querying.")

# Input field for the topic
topic = st.sidebar.text_input("Enter the topic for papers:", "")

# Initialize retriever in session state
if "retriever" not in st.session_state:
    st.session_state.retriever = None

# Button to fetch and embed papers
if st.sidebar.button("Fetch & Embed Papers"):
    if topic:
        with st.spinner("Fetching Papers..."):
            text = get_papers(topic)
            st.sidebar.success("Papers fetched")
        with st.spinner("Embedding Papers..."):
            st.session_state.retriever = get_retriver(text)
            st.sidebar.success("Papers embedded")
    else:
        st.sidebar.error("Please enter a topic.")

# Define the processing chain
if st.session_state.retriever:
    print(st.session_state.retriever)
    retriever = st.session_state.retriever
    print(retriever)
    chain = (
        RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
        | system_prompt
        | llm
        | StrOutputParser()
    )

    # Update subheader and description based on the topic
    st.subheader(f"Research on {topic}")
    st.write(f"Explore research papers and insights about {topic}. Ask any question you have about this topic, and the system will provide relevant information based on the embedded research papers.")

    # Chatbot interface
    st.header("Research Paper Query Chatbot")
    st.write(f"Ask questions about {topic}.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input(f"Enter your query about {topic}:"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate and display assistant response with spinner
        with st.spinner("Generating response..."):
            response = chain.invoke(prompt)
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.write("Please fetch and embed papers first by entering a topic in the sidebar.")