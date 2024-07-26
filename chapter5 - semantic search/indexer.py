# importing libraries
import random
import torch
import numpy as np
import redis
from redis.commands.search.query import Query
from redis.commands.search.field import TextField, VectorField
from lib import read_file_and_split_sentences, generate_ST_embedding, index_name, r, EMBEDDINGS_FIELD, KEY_PREFIX



# Set a random seed
random_seed = 42
random.seed(random_seed)

# Set a random seed for PyTorch (for GPU as well)
torch.manual_seed(random_seed)
if torch.cuda.is_available():
	torch.cuda.manual_seed_all(random_seed)


# Create a RediSearch index
def create_redisearch_index(index_name):
    try:
        r.ft(index_name).create_index([
            TextField("text"),
            VectorField(EMBEDDINGS_FIELD, 
                        "HNSW", 
                        {
                             "TYPE": "FLOAT32", 
                             "DIM": 768, 
                             "DISTANCE_METRIC": "COSINE"
                        })
        ])
    except Exception as e:
        print(f"Index already exists: {e}")

create_redisearch_index(index_name)

# Using the splitter
file_path = './pg73608.txt'
sentence = read_file_and_split_sentences(file_path)

#iterate over each sentence and index its embedding
for i, text in enumerate(sentence):
    print(f"Sentence {i+1}:")
    print(text)
    print('-' * 20)

    sentence_embedding = generate_ST_embedding(text)
   
    # Save the paragraph and its embedding to Redis
    r.hset(f"{KEY_PREFIX}{index_name}:{i+1}", mapping={
        "text": text,
        "sentence_number": i+1,
        f"{EMBEDDINGS_FIELD}": sentence_embedding.astype(np.float32).tobytes()
    })
