from sklearn.metrics.pairwise import cosine_similarity

from ai.embedding import build_embeddings, embed_query


class VectorStore:
    def __init__(self):
        self.documents = []
        self.metadata = []
        self.vectorizer = None
        self.embeddings = None

    def add_documents(self, texts, metadata=None):
        if not texts:
            return

        self.documents.extend(texts)
        self.metadata.extend(metadata or [{"filename": "Uploaded document"} for _ in texts])
        self.vectorizer, self.embeddings = build_embeddings(self.documents)

    def search(self, query, top_k=3):
        if not self.documents or self.vectorizer is None or self.embeddings is None:
            return []

        query_embedding = embed_query(self.vectorizer, query)
        scores = cosine_similarity(query_embedding, self.embeddings).ravel()
        ranked_indices = scores.argsort()[::-1][:top_k]

        results = []
        for index in ranked_indices:
            if scores[index] > 0:
                results.append(
                    {
                        "text": self.documents[index],
                        "score": float(scores[index]),
                        "metadata": self.metadata[index],
                    }
                )

        return results

    def get_documents(self):
        return [{"text": text, "metadata": meta} for text, meta in zip(self.documents, self.metadata)]
