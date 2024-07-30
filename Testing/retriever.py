import faiss
import numpy as np
from transformers import AutoTokenizer

class Retriever:
    def __init__(self, documents):
        self.documents = documents
        self.index = None
        self.tokenizer = AutoTokenizer.from_pretrained("distilgpt2")  # Replace with appropriate model name
        self.build_index()

    def build_index(self):
        # Tokenize and encode documents
        embeddings = [self.tokenizer.encode(doc, return_tensors='pt').numpy().mean(axis=1) for doc in self.documents]
        embeddings = np.vstack(embeddings)

        # Create FAISS index
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def retrieve(self, query, top_k=5):
        # Tokenize and encode query
        query_embedding = self.tokenizer.encode(query, return_tensors='pt').numpy().mean(axis=1)
        
        # Ensure the query_embedding is a 2D array with shape (1, d)
        query_embedding = np.expand_dims(query_embedding, axis=0)
        
        # Retrieve similar documents
        distances, indices = self.index.search(query_embedding, top_k)
        return [self.documents[idx] for idx in indices[0]]
