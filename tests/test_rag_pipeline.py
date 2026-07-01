from ai.rag_pipeline import answer_question


def test_answer_question_returns_contextual_reply():
    context = "DocuTrust is an enterprise AI document assistant."
    answer = answer_question("What is DocuTrust?", context)

    assert "DocuTrust" in answer
    assert len(answer) > 0


def test_answer_question_combines_multiple_relevant_contexts():
    context = [
        "DocuTrust is an enterprise AI document assistant.",
        "It helps teams analyze contracts and compliance documents.",
        "It can summarize uploaded PDFs and answer questions.",
    ]
    answer = answer_question("What does DocuTrust do?", context)

    assert "DocuTrust" in answer
    assert "analyze" in answer.lower()
    assert "summarize" in answer.lower()
    assert "[" not in answer
    assert "]" not in answer
    assert len(answer) < 220
    assert answer.count("DocuTrust") <= 2
