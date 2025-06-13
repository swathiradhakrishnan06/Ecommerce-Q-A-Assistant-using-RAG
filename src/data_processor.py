import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

class DataProcessor:
    def __init__(self, csv_path="data/goodguys_faq.csv"):
        # Get the absolute path to the project root directory
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.csv_path = os.path.join(self.root_dir, csv_path)
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    
    def load_data(self):
        """Load and process the FAQ data from CSV"""
        # Read the CSV file
        df = pd.read_csv(self.csv_path)
        
        # Combine questions and answers into a single text
        texts = []
        for _, row in df.iterrows():
            text = f"Question: {row['question']}\nAnswer: {row['answer']}"
            texts.append(text)
        
        # Split texts into chunks
        chunks = self.text_splitter.split_text("\n\n".join(texts))
        return chunks
    
    def create_vector_store(self, chunks):
        """Create and persist Chroma vector store"""
        vector_store = Chroma.from_texts(
            texts=chunks,
            embedding=self.embeddings,
            persist_directory=os.path.join(self.root_dir, "data/chroma_db")
        )
        return vector_store 