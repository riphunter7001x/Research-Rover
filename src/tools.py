import os
import time
import logging
import arxiv
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_qdrant import Qdrant
from langchain_cohere import CohereEmbeddings
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()
os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_papers(query: str) -> str:
    # """ 
    # Downloads and processes papers from arXiv based on the query.

    # Args:
    #     query (str): The search query to fetch papers.

    # Returns:
    #     str: The concatenated content of all papers.
  
    # Replace spaces with underscores in the query to create a valid directory name
        # Set up the directory path relative to the current working directory
    base_dir = os.getcwd()
    dirpath = os.path.join(base_dir, f"arxiv_papers_for_{query.replace(' ', '_')}")

    if not os.path.exists(dirpath):
        os.makedirs(dirpath)


    # Initialize arxiv client and search for papers
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=10,
        sort_order=arxiv.SortOrder.Descending
    )

   # Download and save the papers
    for result in client.results(search):
        while True:
            try:
                paper_id = result.get_short_id()
                # Truncate and sanitize title to avoid overly long filenames
                title = result.title.replace(' ', '_').replace('/', '_').replace(':', '').replace('?', '')[:30]
                filepath = os.path.join(dirpath, f"{paper_id}_{title}.pdf")
                result.download_pdf(dirpath=dirpath, filename=f"{paper_id}_{title}.pdf")
                logging.info(f"-> Paper id {paper_id} with title '{result.title}' is downloaded.")
                break
            except (FileNotFoundError, ConnectionResetError) as e:
                logging.error(f"Error occurred: {e}")
                time.sleep(5)
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")
                break
            
    papers = []
    loader = DirectoryLoader(dirpath, glob="./*.pdf", loader_cls=PyPDFLoader)
    try:
        papers = loader.load()
    except Exception as e:
        logging.error(f"Error loading files: {e}")

    logging.info(f"Total number of pages loaded: {len(papers)}")

    # Concatenate all pages' content into a single string
    full_text = ''.join(paper.page_content for paper in papers)

    # Remove empty lines and join lines into a single string
    full_text = " ".join(line for line in full_text.splitlines() if line)

    return full_text


def get_retriver(full_text: str, topic) -> None:
    # """Splits the text into chunks and creates a Qdrant vector store.

    # Args:
    #     full_text (str): The full text content of the papers.
    # """
    try:
        # Split the text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        paper_chunks = text_splitter.create_documents([full_text])
    except Exception as e:
        logging.error(f"Error splitting text into chunks: {e}")
        return
    
    try:
        # Create Qdrant vector store
        qdrant = Qdrant.from_documents(
            documents=paper_chunks,
            embedding=CohereEmbeddings(model="embed-english-light-v3.0"),
            path=f"./db_{topic.replace(' ', '_')}",
            collection_name = "arxiv_papers"
        )
        return qdrant.as_retriever(k=5)
    except Exception as e:
        logging.error(f"Error creating Qdrant vector store: {e}")