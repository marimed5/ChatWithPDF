from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

model_cache = {}

def build_chain(filepath):
    # Skip initialization of the same file
    if filepath in model_cache:
        return model_cache[filepath]

    loader = PyPDFLoader(filepath)
    pages = loader.load()
    chunks = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=100).split_documents(pages)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_temp")

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.3)
    chain = ConversationalRetrievalChain.from_llm(llm, retriever=db.as_retriever(), return_source_documents=False)

    model_cache[filepath] = chain
    return chain
