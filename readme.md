
# Research Rover

Research Rover is a Streamlit application that searches for research papers on a specified topic from arXiv, embeds them, and allows users to query these embedded papers through a chatbot interface.

## Features

- Search and retrieve research papers from arXiv based on user-defined topics.
- Embed fetched papers for efficient querying.
- Interactive chatbot for querying embedded research papers.

## Installation

### Prerequisites

- Python 3.10 

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ResearchRover.git
   cd ResearchRover
   ```

2. **Set up a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the root directory and add your `GROQ_API_KEY`:
   ```plaintext
   GROQ_API_KEY=your_groq_api_key
   ```

## Usage

1. **Run the application:**
   ```bash
   streamlit run app.py
   ```

2. **Fetch and Embed Papers:**
   - Enter a topic in the sidebar input field.
   - Click "Fetch & Embed Papers" to retrieve and embed research papers.

3. **Query Papers:**
   - Use the chat interface to ask questions about the fetched papers.


## Example

1. Enter "AI in Health Care" as a topic.
2. Click "Fetch & Embed Papers".
3. Once embedding is complete, query the papers via the chat interface.
