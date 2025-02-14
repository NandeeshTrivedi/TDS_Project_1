import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import requests
import os

os.environ['AIPROXY_TOKEN'] = 'eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjMwMDIzMTZAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.DvLFDgvuV6vp37Tp89HhU-8vYu2FZCTXovK7U6oyjT8'

def get_embedding(text):
    api_url = "http://aiproxy.sanand.workers.dev/openai/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {os.environ['AIPROXY_TOKEN']}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "text-embedding-3-small",
        "input": "king"
    }
    response = requests.post(api_url, headers=headers, json=data)
    return response.json()['data'][0]['embedding']

def find_most_similar_comments(input_file, output_file):
    with open(input_file, 'r') as f:
        comments = f.readlines()
    
    comments = [comment.strip() for comment in comments]
    embeddings = [get_embedding(comment) for comment in comments]
    
    similarity_matrix = cosine_similarity(embeddings)
    np.fill_diagonal(similarity_matrix, -1)  # Exclude self-similarity
    
    max_similarity_index = np.unravel_index(np.argmax(similarity_matrix), similarity_matrix.shape)
    
    with open(output_file, 'w') as f:
        f.write(f"{comments[max_similarity_index[0]]}\n")
        f.write(f"{comments[max_similarity_index[1]]}\n")

    print(f"Most similar comments written to {output_file}")