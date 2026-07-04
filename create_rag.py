import re

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

NPSOT_DIR = "npsot"
PERSIST_DIR = "./chroma_db"
EMBED_MODEL = "nomic-embed-text"

# Each npsot page starts with a markdown link to its source, e.g. "# [Title](https://npsot.org/...)"
SOURCE_LINK_RE = re.compile(r"^#\s*\[.*?\]\((https?://[^)]+)\)")

# 1. Load every markdown page scraped from npsot.org and chunk it
loader = DirectoryLoader(NPSOT_DIR, glob="*.md", loader_cls=TextLoader)
docs = loader.load()

for doc in docs:
    match = SOURCE_LINK_RE.match(doc.page_content)
    if match:
        doc.metadata["source_url"] = match.group(1)

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_documents(docs)

# 2. Embed and persist to ChromaDB
embeddings = OllamaEmbeddings(model=EMBED_MODEL)
vectorstore = Chroma.from_documents(
    chunks,
    embeddings,
    persist_directory=PERSIST_DIR,
)

if __name__ == "__main__":
    print(f"Indexed {len(docs)} files from '{NPSOT_DIR}' into {len(chunks)} chunks.")
    print(f"Vector store persisted to '{PERSIST_DIR}'.")
