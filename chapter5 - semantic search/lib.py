import torch
import re
from sentence_transformers import SentenceTransformer

import numpy as np
import redis
from redis.commands.search.query import Query
from redis.commands.search.field import TextField, VectorField

r = redis.Redis(
  host='redis-18659.c73.us-east-1-2.ec2.redns.redis-cloud.com',
  port=18659,
  password='VDgT8dXUTK1af9DLMxkUHxy9yjk2zs0v')

index_name = "index_ST_1"
EMBEDDINGS_FIELD = "vectors"
KEY_PREFIX = "sentence_"

model = SentenceTransformer('all-mpnet-base-v2')

# TODO: Function to generate embeddings for a given text
def generate_ST_embedding(text):
    return model.encode([text])

def read_file_and_split_sentences(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        # Read the entire file content
        content = file.read()
        
    # Split content into sentences based on punctuation marks
    sentences = re.split(r'(?<=[.!?])\s+|\n\n+', content)

    
    # Remove any leading or trailing whitespace from each sentence
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    
    return sentences


