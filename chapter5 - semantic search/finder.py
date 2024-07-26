# importing libraries
import redis
import numpy as np
from lib import generate_ST_embedding, index_name, EMBEDDINGS_FIELD, r, KEY_PREFIX
from redis.commands.search.query import Query


#TODO
def search_similar_sentences(query, index_name, top_k = 5):
    query_embedding = generate_ST_embedding(query)
    query_embedding_bytes = query_embedding.astype(np.float32).tobytes()

    knn_query = Query(f"*=>[KNN {top_k} @{EMBEDDINGS_FIELD} $vec AS dist]").sort_by("dist").return_fields("text", "sentence_number", "dist").dialect(2)
    search_results = r.ft(index_name).search(
        knn_query,
        query_params={"vec": query_embedding_bytes}
    )
    results = []
    for doc in search_results.docs:
        results.append({"text": doc.text, "distance": float(doc.dist), "number": int(doc.sentence_number)})

    return results

#Gets the previous and next line of the one given, for context
def find_context(sentence_number):
    prev = ""
    next = ""
    if(sentence_number - 1 >= 0):
        prev = r.hget(f"{KEY_PREFIX}{index_name}:{sentence_number - 1}", "text")

    next = r.hget(f"{KEY_PREFIX}{index_name}:{sentence_number + 1}", "text")

    return prev, next

#Potential queries
#query = "originally published"
#query = "When was this book published?"
query = "What language is the book written in?"

top_k = 1  # Number of top results to retrieve

# Main loop
while True:
    query = input("Enter your query (type 'exit' to quit): ")
    if query.lower() == "exit":
        break

    #Perform the search
    similar_sentences = search_similar_sentences(query, index_name, top_k)
    for i, result in enumerate(similar_sentences):
        #print(f"Distance: {result['distance']}")
        prev_sentence, next_sentence = find_context(result['number'])
        print(prev_sentence)
        print(f"=={result['text']}==")
        print(next_sentence)
        print('-' * 20)
       

