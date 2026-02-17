from vectorstore_port import VSPort
from model import Website, SearchResult
from llama_index.core import (
    VectorStoreIndex,
    Document,
)
import os

import chromadb
from llama_index.core.node_parser import SentenceSplitter
from utils import clean_html_to_markdown
from llama_index.vector_stores.chroma import ChromaVectorStore
from settings import init_llama_index

init_llama_index()


class ChromaDB(VSPort):

    def __init__(self, top_k: int):
        self.top_k = top_k
        self.chroma_client = chromadb.HttpClient(
            host=os.environ.get("CHROMA_HOST", "localhost"),
            port=int(os.environ.get("CHROMA_PORT", "8000")),
        )
        self.chroma_collection = self.chroma_client.get_or_create_collection(
            "website-data"
        )
        vector_store = ChromaVectorStore(chroma_collection=self.chroma_collection)
        self.index = VectorStoreIndex.from_vector_store(vector_store)

    def insert_website_to_vs(self, website: Website) -> None:
        markdown = clean_html_to_markdown(website.html)
        doc = Document(
            text=markdown,
            metadata={
                "url": website.url,
                "title": website.title,
                "last_accessed": website.access_time.isoformat(),
                "accessed_timestamp": website.access_time.timestamp(),
            },
        )
        parser = SentenceSplitter(chunk_size=1024, chunk_overlap=128)
        nodes = parser.get_nodes_from_documents([doc])
        self.index.insert_nodes(nodes)

    def delete_by_date(self, date: str) -> int:
        """Delete all chunks indexed on a given date (YYYY-MM-DD)."""
        from datetime import datetime, timedelta

        day_start = datetime.fromisoformat(date).timestamp()
        day_end = (datetime.fromisoformat(date) + timedelta(days=1)).timestamp()
        results = self.chroma_collection.get(
            where={
                "$and": [
                    {"accessed_timestamp": {"$gte": day_start}},
                    {"accessed_timestamp": {"$lt": day_end}},
                ]
            },
        )
        ids = results["ids"]
        if ids:
            self.chroma_collection.delete(ids=ids)
        return len(ids)

    def delete_all(self) -> int:
        count = self.chroma_collection.count()
        if count > 0:
            all_docs = self.chroma_collection.get()
            self.chroma_collection.delete(ids=all_docs["ids"])
        return count

    def semantic_search(self, query: str) -> list[SearchResult]:
        retriever = self.index.as_retriever(similarity_top_k=self.top_k)
        nodes = retriever.retrieve(query)
        return [
            SearchResult(
                text=node.text,
                score=node.score,
                url=node.metadata.get("url"),
                title=node.metadata.get("title"),
            )
            for node in nodes
        ]
