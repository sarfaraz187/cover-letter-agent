import os
from chromadb import Documents, EmbeddingFunction, Embeddings
from chromadb import chromadb
from google.api_core import retry
import google.generativeai as genai
import logging
from utils.utils import extract_text_from_pdf

logger = logging.getLogger(__name__)

# Define a helper to retry when per-minute quota is reached.
is_retriable = lambda e: (isinstance(e, genai.errors.APIError) and e.code in {429, 503})

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

def embed_cv_into_chroma(cv_filename="cv.pdf", collection_name="resumeDB"):
    # Extract CV text
    cv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), cv_filename)
    if not os.path.exists(cv_path):
        logger.error(f"CV file not found at {cv_path}")
        raise FileNotFoundError(f"CV file not found at {cv_path}")

    cv_text = extract_text_from_pdf(cv_path)
    logger.info(f"Extracted {len(cv_text)} characters from CV")

    documents = [cv_text]
    embed_fn = GeminiEmbeddingFunction()
    embed_fn.document_mode = True

    # Setup Chroma DB
    chroma_path = os.path.join('flask-backend', "chroma_db")
    chroma_client = chromadb.PersistentClient(path=chroma_path)
    logger.info(f"Chroma DB path: {os.path.abspath(chroma_path)}")

    db = chroma_client.get_or_create_collection(name=collection_name, embedding_function=embed_fn)
    db.add(documents=documents, ids=[str(i) for i in range(len(documents))])
    logger.info(f"Documents embedded. Collection now has {db.count()} items.")
