# PDF Editor Web App 📝

A web-based **PDF Editor** that allows users to upload a PDF, edit its content in a rich text editor (**TinyMCE**), and export/download the edited content as **HTML or PDF**.

---

## 🚀 Features
- 📂 **Upload PDFs** and extract text.
- 📝 **Edit content** in a rich text editor (TinyMCE).
- 🔄 **Download edited content** as HTML.
- 📄 **Export the final version** as a PDF.
- 🔧 **Built using Flask** for backend processing.

---

## 🛠️ Tech Stack
- **Frontend**: HTML, CSS, JavaScript, TinyMCE
- **Backend**: Flask (Python)
- **PDF Processing**: PyMuPDF (fitz), pdf2image
- **Exporting**: WeasyPrint or wkhtmltopdf

---

## 📦 Installation
```bash
git clone https://github.com/pq36/pdf_html_converter
cd pdf-editor-flask
pip install -r requirements.txt
python app.py
```
