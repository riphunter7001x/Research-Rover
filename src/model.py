from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

# Set the GROQ API key from the environment variables
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize the ChatGroq model with specific parameters
llm = ChatGroq(
    temperature=0.7,            # Set the temperature for the model's output
    model="llama3-70b-8192",    # Specify the model to be used
)


# # Define the processing chain
# chain = (
#     RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
#     | prompt
#     | model
#     | StrOutputParser()
# )