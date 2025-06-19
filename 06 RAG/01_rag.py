from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

load_dotenv()

embedder = OpenAIEmbeddings(
    model="text-embedding-3-large"                              
)

def chunking(file_path: str):

    loader = PyPDFLoader(file_path) 
    docs = loader.load() # by default it loads(chunks) the pdf each page saparately

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200
    )

    split_docs = text_splitter.split_documents(documents=docs)

    vectore_store = QdrantVectorStore.from_documents(
        documents=[],
        collection_name="learning_langchain",
        url="http://localhost:6333",
        embedding=embedder,
    )

    vectore_store.add_documents(documents=split_docs)

    print("Injection Done")

def retrieve(query: str):
    
    retriever = QdrantVectorStore.from_existing_collection(
        collection_name="learning_langchain",
        url="http://localhost:6333",
        embedding=embedder,
    )

    relevant_chunks = retriever.similarity_search(
        query=query
    )

    print("Relevat chunks:", relevant_chunks)

# file_path = Path(__file__).parent / "nodejs.pdf"
# chunking(file_path)

retrieve("What is FS Module?")