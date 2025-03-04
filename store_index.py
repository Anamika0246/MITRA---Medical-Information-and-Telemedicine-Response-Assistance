from src.helper import load_pdf_file, text_split, download_hugging_face_embeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os
from langchain_core.documents import Document



load_dotenv()
#print("Loaded .env file")

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
#print(f"Pinecone API Key: {PINECONE_API_KEY[:5]}... (masked for security)")

DATA_PATH = os.path.join(os.getcwd(), "Data")
#print(f"Data path set: {DATA_PATH}")

extracted_data = load_pdf_file(data=DATA_PATH)
#print(f"Loaded {len(extracted_data)} documents from PDFs")

text_chunks = text_split(extracted_data)
#print(f"Split text into {len(text_chunks)} chunks")



docs = [Document(page_content=str(chunk)) for chunk in text_chunks]

embeddings = download_hugging_face_embeddings()

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "mitra"

# Create Pinecone index
pc.create_index(
    name=index_name,
    dimension=384, 
    metric="cosine", 
    spec=ServerlessSpec(
        cloud="aws", 
        region="us-east-1"
    ) 
)

# Store embeddings in Pinecone
docsearch = PineconeVectorStore.from_documents(
    documents=docs,
    index_name=index_name,
    embedding=embeddings
)
print("done store_index.py...")
