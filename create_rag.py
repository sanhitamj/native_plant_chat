from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1. Load and chunk your documents
loader = TextLoader("native_plants.txt")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(docs)

# 2. Embed and store in ChromaDB
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma.from_documents(
    chunks,
    embeddings,
    persist_directory="./chroma_db"
)

# 3. Retrieve relevant chunks and pass to LLM
retriever = vectorstore.as_retriever()
query = "What plants attract monarch butterflies?"
relevant_docs = retriever.invoke(query)
context = "\n".join([d.page_content for d in relevant_docs])

# 4. Generate response with context injected into prompt
llm = OllamaLLM(model="tinyllama")
response = llm.invoke(f"Context:\n{context}\n\nQuestion: {query}")

