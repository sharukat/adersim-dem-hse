import uuid
import pandas as pd
from tqdm import tqdm
from typing import List
from langchain_qdrant import Qdrant
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from lib.text_splitter import SemanticChunker


class VectorDB:
    def __init__(self, model: str, dataframe: pd.DataFrame) -> None:
        self.embedding_model = OllamaEmbeddings(model=model)
        self.dataframe = dataframe

    def create_document(
            self,
            index: int,
            row,
            content_field: str = "page_content") -> Document:
        try:
            content = getattr(row, content_field)
            if content is None:
                raise ValueError(f"'{content_field}' is None.")
        except AttributeError:
            raise ValueError(f"'{content_field}' does not exist.")

        return Document(
            page_content=content,
            metadata={
                'video_id': row.video_id,
                'title': row.title,
                'url': row.url,
            },
            id=index,
        )

    def get_documents(self) -> List[Document]:
        documents = []
        for row in tqdm(self.dataframe.itertuples(index=True),
                        total=len(self.dataframe)):
            unique_id = str(uuid.uuid4())
            documents.append(self.create_document(unique_id, row))
        return documents

    def create_chunks(self) -> list:
        chunker = SemanticChunker(
            embeddings=self.embedding_model,
            breakpoint_threshold_type="percentile")
        # Load documents
        documents = self.get_documents()
        chunks = chunker.split_documents(documents)
        return chunks

    def create_vectordb(
            self,
            documents: List[Document]) -> None:
        try:
            Qdrant.from_documents(
                documents=documents,
                collection_name="youtube_collection",
                embedding=self.embedding_model,
                prefer_grpc=False,
                url="http://localhost:6333",  # Connected to docker
            )
            print(f"{len(documents)} documents added to the vector store.")
        except Exception as e:
            raise e
