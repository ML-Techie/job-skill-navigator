import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

COLLECTION_NAME = "test_collection"

# 1. Create collection (if not exists)
if not client.collection_exists(COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=4, distance=Distance.COSINE),
    )
    print(f"✅ Created collection: {COLLECTION_NAME}")
else:
    print(f"ℹ️  Collection already exists: {COLLECTION_NAME}")

# 2. Insert a fake point with a 4-dim vector
client.upsert(
    collection_name=COLLECTION_NAME,
    points=[
        PointStruct(
            id=1,
            vector=[0.1, 0.2, 0.3, 0.4],
            payload={"role": "Python Developer", "city": "Bangalore"},
        )
    ],
)
print("✅ Inserted test point")

# 3. Search to verify
results = client.query_points(
    collection_name=COLLECTION_NAME,
    query=[0.1, 0.2, 0.3, 0.4],
    limit=1,
)
print(f"✅ Search result: {results}")

client.delete_collection("test_collection")
print("✅ Cleaned up test collection")