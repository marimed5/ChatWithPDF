# Chat with Your PDF

Interact with your PDF! This Flask-based web app lets you upload a PDF, view it in the browser, and ask questions about it using Google’s Gemini LLM through Retrieval-Augmented Generation (RAG). Powered by LangChain, Chroma, and Gemini.

---

## Features

- Upload and view a PDF inline
- Ask natural-language questions about your PDF
- RAG-powered answers using Gemini + Chroma vector DB
- Persistent chat history

---

## Tech Stack

- **LLM**: Google Gemini (`langchain-google-genai`)
- **Backend**: Flask (Python)
- **Document Parsing**: LangChain + PyPDFLoader
- **Vector Store**: Chroma
- **Frontend**: HTML + CSS
- **Embeddings**: Gemini `embedding-001`

---

## Running the project

### 1. Install required packages

### 2. Add your Gemini API key

Create a `.env` file in the project folder with:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Run the program

python app.py
