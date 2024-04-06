"""
Chunking module:
- Ingest PDF files from a directory and return a list of pages.
- Use Langchain Recursive Chunker to chunk pages into smaller chunks.
- Use Chroma DB to store the chunks.
"""

import os
import shutil
import glob
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class Chunker:
    def __init__(self):
        pass

    def ingest_pdfs(self, directory):
        """
        Ingest PDF files from a directory and return a list of pages.
        """
        pages = []
        for fname in glob.glob(directory + "/*.pdf"	):
            loader = PyPDFLoader(fname)
            pages += loader.load_and_split()
        return pages

    def chunk_pages(self, pages):
        """""
        Use Langchain Recursive Chunker to chunk pages into smaller chunks.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            length_function=len,
            is_separator_regex=False,
        )

        texts = text_splitter.split_documents(pages)
        return texts

    def store_chunks(self, chunks):
        """
        Use Chroma DB to store the chunks.
        """
        embeddings = SentenceTransformerEmbeddings(model_name = "all-MiniLM-L6-v2")
        if os.path.exists("./chroma_db"): shutil.rmtree("./chroma_db")
        _ = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")

    def load_relevant_context(self, query):
        """
        Load relevant context from Chroma DB.
        """
        assert os.path.exists("./chroma_db"), "Chroma DB does not exist"
        embeddings = SentenceTransformerEmbeddings(model_name = "all-MiniLM-L6-v2")
        db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
        docs = db.similarity_search(query)
        return docs


    if __name__ == "__main__":
        pages = ingest_pdfs("data")
        chunks = chunk_pages(pages)
        print(len(chunks))
        store_chunks(chunks)

        doc = load_relevant_query("How do I build the best ideas for a hackathon?")
        print(doc)