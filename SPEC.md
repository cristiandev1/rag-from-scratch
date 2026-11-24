# RAG from Scratch

Teach retrieval-augmented generation using a small, inspectable Python program.

## Acceptance criteria

- Python 3.10+ and its standard library load local Markdown and text files, split them into bounded chunks, and retain file and line references.
- A query uses sparse TF-IDF and cosine similarity to rank those chunks. The CLI exposes the scores and exact context sent to the model.
- Prompt construction assigns source IDs and limits the amount of selected context. Questions with no positive lexical match skip the model.
- An optional local Ollama call uses the standard library HTTP client. Retrieval and prompt inspection work without Ollama.
- Realistic fictional operations runbooks show a direct lookup, a question that needs two sources, and a query with no matches. Deterministic checks cover ranking, source attribution, and prompt construction.
