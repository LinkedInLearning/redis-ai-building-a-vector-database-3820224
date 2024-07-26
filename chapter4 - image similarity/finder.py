# importing libraries
import redis
import numpy as np
from lib import index_name, EMBEDDINGS_FIELD, r, KEY_PREFIX, generate_image_embedding
from redis.commands.search.query import Query

#TODOD
def create_vector_query(query_embedding, index_name, top_k):
    return r.ft(index_name).search(
        Query(f" *=> [KNN {top_k} @{EMBEDDINGS_FIELD} $vec AS dist]")
        .return_fields("image_path", "dist")
        .sort_by("dist")
        .dialect(2),
        query_params={"vec": query_embedding}
    )

# Function to perform vector search on Redis
def search_similar_images(query_image_path, index_name, top_k=5):
    query_embedding = generate_image_embedding(query_image_path)
    query_embedding_bytes = query_embedding.astype(np.float32).tobytes()  # Ensuring float32 type

    try:
        search_result = create_vector_query(query_embedding_bytes, index_name, top_k)

        results = []
        for doc in search_result.docs:
            results.append({"image_path": doc.image_path, "distance": float(doc.dist)})
        
        return results

    except Exception as e:
        print(f"Search failed: {e}")
        return []


top_k = 10  # Number of top results to retrieve

query_image_path = "./query_image_cat.jpeg" 
query_image_path = "./query_image_purple_flowers.jpeg" 
similar_images = search_similar_images(query_image_path, index_name, top_k)

# Print the results
if similar_images:
    for i, result in enumerate(similar_images):
        print(f"Result {i+1}:")
        print(f"Image Path: {result['image_path']}")
        print(f"Distance: {result['distance']}")
        print('-' * 20)
else:
    print("No similar images found.")