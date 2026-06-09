from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved rule chunks.

    TODO — Milestone 3:

    `retrieved_chunks` is the list returned by retrieve(). Each item is a dict:
      - "text"     : the chunk text
      - "game"     : the game name
      - "distance" : similarity score (you can use this to filter weak matches)

    Before writing code, talk through these with your group:
      - How will you format the chunks into a context block for the prompt?
      - What instructions will stop the model from answering beyond what the
        rules say? (Grounding is the whole point — a confident wrong answer
        is worse than an honest "I don't know.")
      - How will you surface which game each answer comes from?

    Your response should:
      1. Answer using only the retrieved context — not the model's general knowledge
      2. Make clear which game the answer comes from
      3. Say so clearly when the answer isn't in the loaded rules

    Return the response as a plain string.
    """
    if not retrieved_chunks:
        return (
            "I couldn't find anything relevant in the loaded rule books. "
            "Try rephrasing your question — or check that your ingestion pipeline is working."
        )

    # Sort chunks by distance ascending (smaller = more similar)
    sorted_chunks = sorted(retrieved_chunks, key=lambda c: c["distance"])

    context_parts = []
    for i, chunk in enumerate(sorted_chunks, 1):
        context_parts.append(f"[Chunk {i} — Game: {chunk['game']} | Distance: {chunk['distance']:.4f}]\n{chunk['text']}")
    context_block = "\n\n---\n\n".join(context_parts)

    system_message = (
        "You are a board game rules assistant. "
        "You must answer the user's question using ONLY the retrieved rule text provided below. "
        "Do not use your general knowledge of board games or any information not present in the retrieved text. "
        "If the retrieved text does not contain enough information to answer the question, say clearly: "
        "'I could not find an answer to that in the loaded rule books.' "
        "When citing a rule, use the format: 'According to the [Game Name] rules, …'"
    )

    user_message = (
        f"Retrieved rule context (ordered by relevance, most relevant first):\n\n"
        f"{context_block}\n\n"
        f"Question: {query}"
    )

    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
    )

    answer = response.choices[0].message.content
    top_game = sorted_chunks[0]["game"]
    return f"{answer} (According to the {top_game} rules…)"
