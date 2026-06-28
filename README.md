# 📄 DocuTrust – Enterprise AI Document Assistant

DocuTrust is an AI-powered document assistant that enables users to upload PDF files, ask questions in natural language, and receive accurate answers with source references. The project uses a Retrieval-Augmented Generation (RAG) approach to retrieve relevant information from uploaded documents before generating responses, reducing hallucinations and improving answer reliability.
---

## 🚀 Features
* 📂 Upload PDF documents
* 💬 Ask questions in natural language
* 🤖 AI-powered document understanding
* 📖 Answers with source references
* 📜 Chat history
* 🌙 Modern and responsive user interface
* 📊 MongoDB-based document and metadata storage
---

## 🛠️ Tech Stack

### Frontend
* HTML5
* CSS3
* JavaScript

### Backend
* Python
* FastAPI

### AI & NLP
* LangChain
* Google Gemini API
* Sentence Transformers

### Database
* MongoDB
* FAISS Vector Database

---

## 📂 Project Structure

```
DocuTrust/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── backend/
│   ├── main.py
│   ├── routes.py
│   └── database.py
│
├── ai/
│   ├── pdf_loader.py
│   ├── embeddings.py
│   ├── vector_store.py
│   └── rag_pipeline.py
│
├── uploads/
├── vector_db/
├── docs/
├── README.md
└── requirements.txt
```

---

## ⚙️ Workflow

```
User Uploads PDF
        │
        ▼
Extract Text
        │
        ▼
Split into Chunks
        │
        ▼
Generate Embeddings
        │
        ▼
Store in FAISS
        │
        ▼
User Asks Question
        │
        ▼
Retrieve Relevant Chunks
        │
        ▼
Generate AI Response
        │
        ▼
Display Answer with Source Reference
```

---

## 🎯 Objectives
* Simplify document searching using AI.
* Reduce time spent reading lengthy documents.
* Improve the accuracy of AI-generated answers.
* Provide trustworthy responses with document references.
---

## 📌 Future Enhancements
* Multi-document support
* User authentication
* OCR support for scanned PDFs
* Voice-based document queries
* Multi-language support
* Document summarization
* Admin dashboard
* Cloud deployment
---

## ▶️ Installation
1. Clone the repository
```bash
git clone https://github.com/your-username/DocuTrust.git
```
2. Navigate to the project directory
```bash
cd DocuTrust
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Configure your environment variables
Create a `.env` file and add your API keys and database connection string.
```
GEMINI_API_KEY=your_api_key
MONGODB_URI=your_mongodb_connection_string
```
5. Run the backend
```bash
uvicorn backend.main:app --reload
```
6. Open the frontend
Open `frontend/index.html` in your browser or serve it using a local web server.
---


## 👨‍💻 Author:
**Shreya Raj**
B.Tech Information Technology
Internship Final Project – 2026
---

## 📄 License
This project is developed for educational and internship purposes.
