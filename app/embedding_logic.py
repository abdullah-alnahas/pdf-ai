from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from FlagEmbedding import BGEM3FlagModel

# Constants
EMBEDDING_MODEL_NAME = 'BAAI/bge-m3'
EMBEDDING_DIMENSIONS = 1024
INDEX_NAME = "paper"

# Initialize the embedding model globally to avoid reinitialization
embedding_model = BGEM3FlagModel(EMBEDDING_MODEL_NAME, use_fp16=True)

def encode_paragraphs(paragraphs):
    """Encodes paragraphs to obtain embeddings."""
    return embedding_model.encode(paragraphs, return_colbert_vecs=True, return_dense=True)

def tokenize_paragraphs(paragraphs):
    """Tokenizes paragraphs."""
    return [embedding_model.tokenizer.tokenize(p) for p in paragraphs]

def generate_mappings_and_embeddings(paragraphs, tokenized_paragraphs, embeddings):
    """Generates mappings and embeddings for paragraphs and tokens."""
    ids = list(range(len(paragraphs))) + list(range(len(paragraphs), len(paragraphs) + sum(len(p) for p in tokenized_paragraphs)))
    texts = paragraphs + [token for paragraph in tokenized_paragraphs for token in paragraph]
    vectors = embeddings['dense_vecs'].tolist() + [
        e.tolist() for pe in embeddings["colbert_vecs"] for e in pe
    ]
    return ids, texts, vectors

def initialize_qdrant_client():
    """Initializes the Qdrant client."""
    client = QdrantClient(":memory:")  # Adjust as necessary for your setup
    client.recreate_collection(
        collection_name=INDEX_NAME,
        vectors_config=VectorParams(size=EMBEDDING_DIMENSIONS, distance=Distance.COSINE),
    )
    return client

def upsert_data_to_qdrant(client, ids, texts, vectors, paragraph_ids):
    """Upserts data into Qdrant."""
    points = [
        PointStruct(id=_id, vector=vector, payload={"text": text, "paragraph_id": _id if _id in paragraph_ids else None})
        for _id, text, vector in zip(ids, texts, vectors)
    ]
    client.upsert(collection_name=INDEX_NAME, points=points)

def search_in_qdrant(client, query):
    """Searches for a query in the indexed data."""
    query_emb = embedding_model.encode([query], return_colbert_vecs=True, return_dense=True)
    query_vec = query_emb["dense_vecs"][0]
    results = client.search(INDEX_NAME, query_vector=query_vec, limit=100)
    return results
