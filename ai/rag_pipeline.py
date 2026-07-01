
import re


def _extract_entity_name(context_chunks):
    for chunk in context_chunks:
        match = re.search(r"\b([A-Z][A-Za-z0-9]+(?:\s+[A-Z][A-Za-z0-9]+)*)\b", chunk)
        if match:
            return match.group(1)
    return None


def _normalize_context(context):
    if context is None:
        return []
    if isinstance(context, (list, tuple, set)):
        return [str(item).strip() for item in context if str(item).strip()]

    text = str(context).strip()
    return [text] if text else []


def answer_question(question, context):
    context_chunks = _normalize_context(context)
    if not context_chunks:
        return "I don't have a document context yet. Please upload a PDF first."

    question_terms = set(re.findall(r"[a-zA-Z0-9']+", question.lower()))
    question_is_functional = any(
        term in question.lower()
        for term in ["what do", "what does", "how does", "how do", "purpose", "function", "help", "use", "used for", "capability"]
    )
    scored_sentences = []
    seen_sentences = set()

    for chunk in context_chunks:
        cleaned_chunk = " ".join(str(chunk).split())
        sentences = re.split(r"(?<=[.!?])\s+", cleaned_chunk)
        for sentence in sentences:
            cleaned_sentence = re.sub(r"\s+", " ", sentence).strip()
            if not cleaned_sentence:
                continue

            normalized_sentence = cleaned_sentence.lower()
            if normalized_sentence in seen_sentences:
                continue
            seen_sentences.add(normalized_sentence)

            sentence_terms = set(re.findall(r"[a-zA-Z0-9']+", normalized_sentence))
            overlap = len(question_terms & sentence_terms)
            action_bonus = 3 if question_is_functional and any(
                re.search(rf"\b{re.escape(word)}\b", normalized_sentence)
                for word in ["help", "analyze", "summarize", "answer", "support", "assist", "enable", "provide", "process", "review"]
            ) else 0
            scored_sentences.append((overlap + action_bonus, cleaned_sentence))

    if not scored_sentences:
        answer_text = context_chunks[0]
    else:
        scored_sentences.sort(key=lambda item: item[0], reverse=True)
        if question_is_functional:
            capability_candidates = [
                (score, sentence)
                for score, sentence in scored_sentences
                if any(re.search(rf"\b{re.escape(word)}\b", sentence.lower()) for word in ["help", "analyze", "summarize", "answer", "support", "assist", "enable", "provide", "process", "review"])
            ]
            if capability_candidates:
                scored_sentences = capability_candidates

        selected_sentences = []
        for _, sentence in scored_sentences:
            if sentence.strip() not in selected_sentences:
                selected_sentences.append(sentence.strip())
            if len(selected_sentences) >= 3:
                break

        entity_name = _extract_entity_name(context_chunks)
        if len(selected_sentences) >= 2:
            if question_is_functional and entity_name:
                answer_text = f"{entity_name} can {selected_sentences[0].lower()} {selected_sentences[1].lower()}"
            else:
                answer_text = f"{selected_sentences[0]}. {selected_sentences[1]}"
        elif selected_sentences:
            answer_text = selected_sentences[0]
        else:
            answer_text = context_chunks[0]

    answer_text = re.sub(r"\s+", " ", answer_text).strip()
    if not answer_text.endswith((".", "!", "?")):
        answer_text += "."
    if len(answer_text) > 500:
        answer_text = answer_text[:497] + "..."

    return answer_text
