from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss


# ==========================================
# 1. KNOWLEDGE BASE CONFIGURATION
# ==========================================

KB_FOLDER = Path(__file__).resolve().parents[2] / "00_reference_data" / "knowledge_base"


# ==========================================
# 2. LOAD ARTICLES
# ==========================================

documents = []

for file_path in KB_FOLDER.glob("*.md"):
    text = file_path.read_text(encoding="utf-8")

    documents.append({
        "source": file_path.name,
        "text": text
    })

print("Total articles loaded:", len(documents))


# ==========================================
# 3. CHUNK ARTICLES
# ==========================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = []

for doc in documents:
    split_texts = splitter.split_text(doc["text"])

    for chunk in split_texts:
        chunks.append({
            "source": doc["source"],
            "text": chunk
        })

print("Total chunks created:", len(chunks))


# ==========================================
# 4. LOAD EMBEDDING MODEL
# ==========================================

print("\nLoading embedding model...")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded successfully!")


# ==========================================
# 5. GENERATE EMBEDDINGS
# ==========================================

chunk_texts = [chunk["text"] for chunk in chunks]

embeddings = embedding_model.encode(
    chunk_texts,
    show_progress_bar=True
)

embeddings = np.array(embeddings, dtype="float32")

print("Embeddings generated successfully!")


# ==========================================
# 6. CREATE FAISS INDEX
# ==========================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

print("FAISS index created successfully!")
print("Total vectors stored:", index.ntotal)


# ==========================================
# 7. KNOWLEDGE BASE SEARCH FUNCTION
# ==========================================

def search_knowledge_base(query, top_k=3):

    query_embedding = embedding_model.encode([query])

    query_embedding = np.array(
        query_embedding,
        dtype="float32"
    )

    top_k = min(top_k, index.ntotal)

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for position, i in enumerate(indices[0]):

        chunk = chunks[i]

        results.append({
            "source": chunk["source"],
            "text": chunk["text"],
            "distance": float(distances[0][position])
        })

    return results


# ==========================================
# 8. TEST RETRIEVAL (ONLY WHEN RUN DIRECTLY)
# ==========================================

if __name__ == "__main__":

    test_ticket = (
        "My internet is down and the LOS light on my modem is red."
    )

    print("\nTest Ticket:")
    print(test_ticket)

    results = search_knowledge_base(
        test_ticket,
        top_k=3
    )

    print("\nRetrieved Knowledge:")

    for result in results:

        print("\nSource:", result["source"])
        print("Distance:", result["distance"])
        print(result["text"])
        print("-" * 50)