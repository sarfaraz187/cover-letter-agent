import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from chromadb import Documents, EmbeddingFunction, Embeddings
from chromadb import chromadb
from google.api_core import retry
import google.generativeai as genai
import logging
from utils.utils import extract_text_from_pdf

logger = logging.getLogger(__name__)

# Define a helper to retry when per-minute quota is reached.
is_retriable = lambda e: (isinstance(e, genai.errors.APIError) and e.code in {429, 503})

# Setup Chroma DB
chroma_path = os.path.join('flask-backend', "chroma_db")
chroma_client = chromadb.PersistentClient(path=chroma_path)
logger.info(f"Chroma DB path: {os.path.abspath(chroma_path)}")

def get_client():
    return chroma_client
    
class GeminiEmbeddingFunction(EmbeddingFunction):
    document_mode = True

    @retry.Retry(predicate=is_retriable)
    def __call__(self, input: Documents) -> Embeddings:
        task_type = "retrieval_document" if self.document_mode else "retrieval_query"
        texts = [input] if isinstance(input, str) else input
        results = []
        for text in texts:
            response = genai.embed_content(
                model="text-embedding-004",
                content=text,
                task_type=task_type
            )
            results.append(response["embedding"])
        return results

def chunk_cv_content(cv_content):
    """Split CV content into logical chunks with overlap"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=50,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.create_documents([cv_content], metadatas=[{"source": "cv"}])
    
    print(f"Split CV into {len(chunks)} chunks")
    return chunks

def create_embeddings_and_store(chunks, collection_name="resumeDB"):
    documents = chunks
    embed_fn = GeminiEmbeddingFunction()
    embed_fn.document_mode = True


    # Create a collection with the embedding function
    try:
        # Delete the collection if it already exists
        chroma_client.delete_collection(collection_name)
        print(f"Deleted existing collection '{collection_name}'")
    except:
        pass

    # Create a new collection
    collection = chroma_client.create_collection(
        name=collection_name, 
        embedding_function=embed_fn
    )
    logger.info(f"Created collection '{collection_name}'")

    # Prepare documents for ChromaDB
    documents = []
    metadatas = []
    ids = []
    
    for i, chunk in enumerate(chunks):
        documents.append(chunk.page_content)
        metadatas.append({"section": identify_cv_section(chunk.page_content)})
        ids.append(f"chunk_{i}")
    
    # Add documents to the collection
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(f"Added {len(documents)} documents to ChromaDB collection '{collection_name}'")
    return collection

def identify_cv_section(text):
    """Identify which section of the CV this chunk belongs to"""
    text_lower = text.lower()
    
    if any(keyword in text_lower for keyword in ["work experience", "software developer", "front-end"]):
        return "work_experience"
    elif any(keyword in text_lower for keyword in ["education", "university", "college", "m.eng", "b.tech"]):
        return "education"
    elif any(keyword in text_lower for keyword in ["skill", "react", "javascript", "typescript", "python"]):
        return "skills"
    elif any(keyword in text_lower for keyword in ["project", "assembly end game", "cover letter ai"]):
        return "projects"
    elif any(keyword in text_lower for keyword in ["summary", "passionate"]):
        return "summary"
    elif any(keyword in text_lower for keyword in ["contact", "email", "phone", "+49"]):
        return "contact"
    else:
        return "other"
    
def query_collection(collection, query_text, n_results=3, filter_section=None):
    """Query the collection for relevant CV sections"""
    query_params = {
        "query_texts": [query_text],
        "n_results": n_results
    }
    
    if filter_section:
        query_params["where"] = {"section": filter_section}
    
    results = collection.query(**query_params)
    
    return results

def embed_cv():
    # Later replace this with the an API where i can upload my CV
    logger.info("============ Extracting CV text from PDF ============")
    cv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cv.pdf")
    if not os.path.exists(cv_path):
        logger.error(f"CV file not found at {cv_path}")
        raise FileNotFoundError(f"CV file not found at {cv_path}")

    cv_content = extract_text_from_pdf(cv_path)
    logger.info(f"Extracted {len(cv_content)} characters from CV")


    # Chunk CV content
    chunks = chunk_cv_content(cv_content)
    
    # Create embeddings and store in ChromaDB
    collection = create_embeddings_and_store(chunks)

    # Example queries for cover letter generation
    print("\nExample Queries for Cover Letter Agent:")
    
    # Query for relevant work experience
    print("\n1. Finding relevant work experience for a React developer position:")
    results = query_collection(collection, "React developer experience frontend", filter_section="work_experience")
    for i, doc in enumerate(results['documents'][0]):
        print(f"\nResult {i+1}:")
        print(doc)
    
    # Query for relevant skills
    # print("\n2. Finding relevant technical skills for a fullstack position:")
    # results = query_collection(collection, "fullstack development skills", filter_section="skills")
    # for i, doc in enumerate(results['documents'][0]):
    #     print(f"\nResult {i+1}:")
    #     print(doc)