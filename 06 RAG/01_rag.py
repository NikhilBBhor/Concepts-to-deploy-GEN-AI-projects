from langchain_community.document_loaders import PyPDFLoader # type: ignore
from langchain_text_splitters import RecursiveCharacterTextSplitter # type: ignore
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

file_path = "/workspaces/Concepts-to-deploy-GEN-AI-projects/06 RAG/nodejs.pdf"
loader = PyPDFLoader(file_path) 

docs = loader.load() # by default it loads the pdf each page saparate

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

split_docs = text_splitter.split_documents(documents=docs)

embedder = OpenAIEmbeddings(
    model="text-embedding-3-large"                              
)

############ Need only one time, while creating embeddings #######
# vectore_store = QdrantVectorStore.from_documents(
#     documents=[],
#     collection_name="learning_langchain",
#     url="http://localhost:6333",
#     embedding=embedder,
# )
#
# vectore_store.add_documents(documents=split_docs)
#
# print("Injection Done")

retriever = QdrantVectorStore.from_existing_collection(
    collection_name="learning_langchain",
    url="http://localhost:6333",
    embedding=embedder,
)

relevant_chunks = retriever.similarity_search(
    query="What is FS Module?"
)

print("Relevat chunks:", relevant_chunks)