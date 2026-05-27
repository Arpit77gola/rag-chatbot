import os
from pypdf import PdfReader
from  langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np

def load_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )
    return splitter.split_text(text)

def create_embeddings(chunks):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks, show_progress_bar=True)
    return embeddings, model

def save_vectordb(chunks, embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    
    faiss.write_index(index, "vectordb/index.faiss")
    
    with open("vectordb/chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)
    
    # Save chunks as text files
    for i, chunk in enumerate(chunks):
        with open(f"chunks/chunk_{i}.txt", "w", encoding="utf-8") as f:
            f.write(chunk)
    
    print(f"Done! {len(chunks)} chunks saved.")

if __name__ == "__main__":
    pdf_path = "data/document.pdf"
    text = load_pdf(pdf_path)
    chunks = chunk_text(text)
    embeddings, model = create_embeddings(chunks)
    save_vectordb(chunks, embeddings)