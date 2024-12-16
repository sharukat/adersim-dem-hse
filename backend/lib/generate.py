import os

# import re
from typing import List
from dotenv import load_dotenv

# from langchain_qdrant import Qdrant
from langchain_cohere import CohereRerank
from langchain_core.prompts import PromptTemplate
from langchain.retrievers import contextual_compression
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_qdrant import QdrantVectorStore, RetrievalMode
from langchain_core.output_parsers import StrOutputParser, BaseOutputParser

# Load environmental variables
load_dotenv(dotenv_path=".env")
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGCHAIN_ENDPOINT")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["COHERE_API_KEY"] = os.getenv("COHERE_API_KEY")


class Chat:
    def __init__(self, model: str) -> None:
        self.model_name = os.getenv("LLM")
        self.model = ChatOllama(
            model=self.model_name, base_url=os.getenv("OLLAMA_BASE_URL")
        )
        self.embedding_function = OllamaEmbeddings(model=self.model_name)
        self.vectordb = QdrantVectorStore.from_existing_collection(
            embedding=OllamaEmbeddings(model="qwen2.5:32b"),
            collection_name="youtube_collection",
            url="http://localhost:6333",
            retrieval_mode=RetrievalMode.DENSE,
        )

        self.multi_query_llm = ChatOllama(model="llama3.2:3b")

    def retriever(self, question: str):

        # Output parser will split the LLM result into a list of queries
        class LineListOutputParser(BaseOutputParser[List[str]]):
            """Output parser for a list of lines."""

            def parse(self, text: str) -> List[str]:
                lines = text.strip().split("\n")
                return list(filter(None, lines))  # Remove empty lines

        output_parser = LineListOutputParser()

        QUERY_PROMPT = PromptTemplate(
            input_variables=["question"],
            template="""You are an AI language model assistant. Your task is
            to generate five different versions of the given user question
            to retrieve relevant documents from a vector database. By
            generating multiple perspectives on the user question, your goal
            is to help the user overcome some of the limitations of the
            distance-based similarity search. Provide these alternative
            questions separated by newlines.
            Original question: {question}""",
        )

        llm_chain = QUERY_PROMPT | self.multi_query_llm | output_parser

        retriever = MultiQueryRetriever(
            retriever=self.vectordb.as_retriever(
                search_type="mmr", search_kwargs={"k": 20, "fetch_k": 50}
            ),
            llm_chain=llm_chain,
            parser_key="lines",
        )

        compressor = CohereRerank(model="rerank-multilingual-v3.0", top_n=10)
        c_retriever = contextual_compression.ContextualCompressionRetriever(
            base_compressor=compressor, base_retriever=retriever
        )

        reranked_docs = c_retriever.invoke(question)
        # docs = []
        # if reranked_docs:
        #     for doc in reranked_docs:
        #         if doc.metadata['relevance_score'] > 0.5:
        #             docs.append(doc)
        # docs = retriever_from_llm.invoke(question)
        return reranked_docs

    def generate(self, question: str, language: str):
        urls_set = set()
        metadata_list = []
        context = []
        docs = self.retriever(question=question)
        for doc in docs:
            url = doc.metadata["url"]
            if url not in urls_set:
                urls_set.add(url)
                metadata_list.append({
                    'urls': url,
                    'title': doc.metadata['title'],
                    'video_id': doc.metadata['video_id']})

        #     page_content = re.sub(r"Comment:\s*\d+", "", doc.page_content)
            context.append(doc.page_content)

        context = "\n\n".join(context)

        prompt = PromptTemplate.from_template(
            """You are an expert in providing information on AI applications
            and technologies for "Disaster and Emergency Management, and
            Health, Safety and Environment (HSE).

            First, lets think step by step. - Provide a detailed and
            descriptive explanation in `{language}` based ONLY on the
            context, adopting a formal tone.\n\n

            Question:
            `{question}`."""
        )

        chain = prompt | self.model | StrOutputParser()

        response = chain.invoke({"language": language, "question": question})
        return {'response': response, 'meta_data': metadata_list}
