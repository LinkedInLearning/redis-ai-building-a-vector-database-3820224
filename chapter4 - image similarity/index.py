# importing libraries
import numpy as np
from redis.commands.search.field import TextField, VectorField

from lib import  index_name, r,  EMBEDDINGS_FIELD, KEY_PREFIX, generate_image_embedding


# Create a RediSearch index
def create_redisearch_index(index_name):
    try:
        r.ft(index_name).create_index([
            TextField("image_path"),
            VectorField(EMBEDDINGS_FIELD, 
                        "HNSW", 
                        {
                            "TYPE": "FLOAT32", 
                            "DIM": 1000, 
                            "DISTANCE_METRIC": "COSINE"
                        })
        ])
    except Exception as e:
        print(f"Index already exists: {e}")

# Function to store image embeddings in Redis
def store_image_embeddings(image_paths):
    for i, image_path in enumerate(image_paths):
        embedding = generate_image_embedding(image_path)
        r.hset(f"{KEY_PREFIX}{index_name}:{i+1}", mapping={
            "image_path": image_path,
            f"{EMBEDDINGS_FIELD}": embedding.astype(np.float32).tobytes()  # Ensuring float32 type
        })
    print(f"Stored {len(image_paths)} images and their embeddings in Redis.")


create_redisearch_index(index_name)

# Example image paths
image_paths = [
    "./db2/image1.jpeg",
    "./db2/image2.jpeg",
    "./db2/image3.jpeg",
    "./db2/image4.jpeg",
    "./db2/image5.jpeg",
    "./db2/image6.jpeg",
    "./db2/image7.jpeg",
    "./db2/image8.jpeg",
    "./db2/image9.jpeg",
    "./db2/image10.jpeg",
    "./db2/image11.jpeg",
    "./db2/image12.jpeg",
    "./db2/image13.jpeg",
    "./db2/image14.jpeg",
    "./db2/image15.jpeg",
    "./db2/image16.jpeg",
    "./db2/image17.jpeg",
    "./db2/image18.jpeg",
    "./db2/image19.jpeg",
    "./db2/image20.jpeg",
    "./db2/image21.jpeg",
    "./db2/image22.jpeg",
    "./db2/image23.jpeg",
    "./db2/image24.jpeg",
    "./db2/image25.jpeg",
    "./db2/image25.jpeg",
    "./db2/image27.jpeg",
    "./db2/image28.jpeg"
]

store_image_embeddings(image_paths)


