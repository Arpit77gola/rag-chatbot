# RAG Chatbot — eBay User Agreement Q&A

An AI-powered chatbot that answers questions based on the eBay User Agreement document using a RAG (Retrieval-Augmented Generation) pipeline.

## Architecture
PDF Document → Chunking → Embeddings → FAISS Vector DB
↓
User Query → Embedding → Semantic Search → Retrieved Chunks → LLaMA 3 (Groq) → Streaming Answer

## Tech Stack

- **Embeddings:** all-MiniLM-L6-v2 (sentence-transformers)
- **Vector DB:** FAISS
- **LLM:** LLaMA 3.1 8B via Groq API
- **UI:** Streamlit

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd rag_chatbot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the root folder:

### 4. Add your document
Place your PDF in the `data/` folder and name it `document.pdf`.

### 5. Process the document
```bash
python src/ingest.py
```

### 6. Run the chatbot
```bash
streamlit run app.py
```

## Sample Queries

- "What is eBay's return policy?"
- "Can I sell vehicles on eBay?"
- "What happens if I don't pay for an item?"
- "What is the arbitration process?"
- "How does eBay Money Back Guarantee work?"

## Folder Structure
rag_chatbot/
├── data/          # Input PDF document
├── chunks/        # Processed text chunks
├── vectordb/      # FAISS index and chunks pickle
├── notebooks/     # Preprocessing notebooks
├── src/
│   ├── ingest.py      # Document processing and embedding
│   ├── retriever.py   # Semantic search
│   └── generator.py   # LLM response generation
├── app.py         # Streamlit chatbot UI
├── requirements.txt
└── README.md