from backend import routes


def test_ensure_index_loaded_rebuilds_index_from_saved_documents():
    routes.vector_store.documents = []
    routes.vector_store.metadata = []
    routes.vector_store.vectorizer = None
    routes.vector_store.embeddings = None

    routes.save_documents([
        {
            "filename": "sample.pdf",
            "text": "DocuTrust is an enterprise AI document assistant.",
            "preview": "DocuTrust",
        }
    ])

    routes.ensure_index_loaded()

    assert len(routes.vector_store.documents) == 1
    assert routes.vector_store.documents[0].startswith("DocuTrust")
