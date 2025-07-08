import os
from flask import Flask, request, render_template, redirect, url_for
from dotenv import load_dotenv
from pdf_chain import build_chain

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

            chain = build_chain(filepath)
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
