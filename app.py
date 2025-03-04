from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq  
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import os
from pinecone import Pinecone, ServerlessSpec

app = Flask(__name__)

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
PINECONE_ENV = os.getenv("PINECONE_ENV", "us-west1-gcp")

# Ensure API keys are set
if not PINECONE_API_KEY or not GROQ_API_KEY:
    raise ValueError("Missing API keys for Pinecone or Groq")

# Set API keys in the environment
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY



# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Optional: Ensure index exists
index_name = "mitra"  
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,  
        metric="euclidean",
        spec=ServerlessSpec(cloud="aws", region="us-west-2"),
    )

# Connect to the existing index
index = pc.Index(index_name)


# Use Hugging Face embeddings
embeddings = download_hugging_face_embeddings()

# Load existing Pinecone index
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

# Configure retriever
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 5})

# Initialize Groq LLM
llm = ChatGroq(model="llama3-8b-8192", temperature=0.4, max_tokens=1000, api_key=GROQ_API_KEY)

# Set up prompt template
# Set up prompt template with 'context'
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful medical assistant."),
    ("human", "{input}\n\nRelevant information:\n{context}"),
])

# Create document retrieval and response generation chain
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

app = Flask(__name__, template_folder="templates") 
# Define Flask routes
@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/get", methods=["POST"])
def chat():
    try:
        msg = request.form["msg"]
        print(f"User input: {msg}")
        response = rag_chain.invoke({"input": msg})
        answer = response.get("answer", "Sorry, I couldn't generate a response.")
        print(f"Response: {answer}")
        return str(answer)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

# Run Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
