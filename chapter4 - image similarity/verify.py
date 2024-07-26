from lib import index_name, r, read_file_and_split_paragraphs

# Example usage:
file_path = './pg73608.txt'
paragraphs = read_file_and_split_paragraphs(file_path)



def verify_storage(index_name):
    for i in range(1, len(paragraphs) + 1):
        key = f"paragraph:{i}"
        stored_embedding = r.hget(key, "embeddings")
        stored_text = r.hget(key, "text")
        print(f"Paragraph {i}: {stored_text}")
        print(f"Stored Embedding (length): {len(stored_embedding)}")
        print('-' * 20)

verify_storage(index_name)