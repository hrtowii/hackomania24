"""
RAG todo:
- simple gradio frontend
- add message histora
- Add guardrail
- Add evaluation metrics
"""

from chat import Chatter
from chunking import Chunker

class RAG:
    def __init__(self):
        self.chatter = Chatter()
        self.chunker = Chunker()

    def compose_prompt(self, msg):
        pages = self.chunker.ingest_pdfs("data")
        pages = self.chunker.chunk_pages(pages)
        self.chunker.store_chunks(pages)
        docs = self.chunker.load_relevant_context(msg)
        assert len(docs) > 1, "Should have at least one relevant context."
        return msg + "\nContext:\n" + docs[0].page_content

    def send_msg(self, msg):
        return self.chatter.send_chat(msg)

if __name__ == "__main__":
    rag = RAG()
    prompt = rag.compose_prompt("How do I start a business in Singapore?")
    rag.send_msg(prompt)
