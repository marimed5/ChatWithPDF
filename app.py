import os
from flask import Flask, request, render_template, redirect, url_for
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

# Load API key
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)

chain = None
chat_history = [("bot", "Chat with Your PDF! Upload a PDF below to get started.")]
filename = None

@app.route("/", methods=["GET", "POST"])
def index():
    global chain, chat_history, filename

    if request.method == "POST":
        # Handle PDF upload
        if "pdf" in request.files and request.files["pdf"].filename:
            pdf = request.files["pdf"]

            upload_folder = os.path.join("static", "uploads")
            os.makedirs(upload_folder, exist_ok=True)

            filename = os.path.splitext(pdf.filename)[0]
            filepath = os.path.join(upload_folder, filename + ".pdf")
            pdf.save(filepath)

            loader = PyPDFLoader(os.path.join("static", "uploads", filename + ".pdf"))
            pages = loader.load()
            chunks = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=100).split_documents(pages)
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            db = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_temp")

            llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.3)
            chain = ConversationalRetrievalChain.from_llm(llm, retriever=db.as_retriever(), return_source_documents=False)

            chat_history = [("bot", f"File '{filename}' uploaded successfully. Ask me anything.")]
            return redirect(url_for("index"))

        # Handle question submission
        elif "query" in request.form and chain:
            query = request.form["query"]
            chat_history.append(("user", query))
            chat_history.append(("bot", "..."))

            try:
                response = chain({"question": query, "chat_history": chat_history})
                chat_history[-1] = ("bot", response["answer"])
            except Exception as e:
                chat_history[-1] = ("bot", f"Error: {str(e)}")

            return redirect(url_for("index"))
            
    return render_template("index.html", history=chat_history, filename=filename)
    
if __name__ == "__main__":
    app.run(debug=True)
