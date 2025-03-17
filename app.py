
import os
os.environ["PATH"] = r"C:\Program Files\GTK3-Runtime Win64\bin;" + os.environ["PATH"]
import ctypes
# Test loading the DLL again
try:
    ctypes.CDLL(r"C:\Program Files\GTK3-Runtime Win64\bin\libgobject-2.0-0.dll")
    print("DLL loaded successfully!")
except OSError as e:
    print("Error loading DLL:", e)

from weasyprint import HTML
print("WeasyPrint imported successfully!")


from flask import Flask, request, render_template, jsonify, send_file, Response
import fitz  # PyMuPDF
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("API_KEY")  # Read API key from .env

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_pdf():
    api_key = request.headers.get("X-API-KEY")
    if api_key != API_KEY:
        return jsonify({"success": False, "error": "Invalid API Key"}), 403

    file = request.files.get("file")
    if not file or not file.filename.endswith(".pdf"):
        return jsonify({"success": False, "error": "Invalid file format"}), 400

    pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(pdf_path)

    try:
        # Extract raw text from PDF
        pdf_doc = fitz.open(pdf_path)
        raw_text = ""
        for page in pdf_doc:
            raw_text += page.get_text("text") + "\n"

        return jsonify({"success": True, "raw_text": raw_text})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/download_html", methods=["POST"])
def download_html():
    html_content = request.form.get("editor_content", "")
    if not html_content:
        return jsonify({"success": False, "error": "No content to export"}), 400

    response = Response(html_content, mimetype='text/html')
    response.headers["Content-Disposition"] = "attachment; filename=edited_document.html"
    return response

@app.route("/export", methods=["POST"])
def export_pdf():
    html_content = request.form.get("editor_content", "")
    if not html_content:
        return jsonify({"success": False, "error": "No content to export"}), 400

    pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], "exported.pdf")
    
    try:
        HTML(string=html_content).write_pdf(pdf_path)
        return send_file(pdf_path, as_attachment=True)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
