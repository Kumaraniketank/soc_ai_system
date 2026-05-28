from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document


with open("rag/data/mitre_attack.txt", "r", encoding="utf-8") as f:
    text = f.read()


splitter = CharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = splitter.split_text(text)

documents = [Document(page_content=chunk) for chunk in chunks]


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


vectorstore = FAISS.from_documents(
    documents,
    embeddings
)

vectorstore.save_local("rag/faiss_index")

print("FAISS index created successfully")