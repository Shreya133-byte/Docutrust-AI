from sklearn.feature_extraction.text import TfidfVectorizer


def build_embeddings(documents):
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(documents)
    return vectorizer, matrix


def embed_query(vectorizer, query):
    return vectorizer.transform([query])
