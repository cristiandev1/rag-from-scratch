# RAG from Scratch

Build and inspect retrieval-augmented generation with Python's standard library. Read the index, scoring, prompt assembly, and optional model call in [`rag.py`](rag.py).

The examples use fictional operations runbooks about checkout rollbacks, incident updates, and payment webhooks. They contain no production data.

## Run the examples

Python 3.10+ is required. The retrieval and prompt demos need no installation, API key, or network access.

```sh
python3 rag.py "How long are both webhook signing secrets accepted?" --top-k 1

QUESTION="When should I roll back a checkout deployment, and how often should I post updates during the rollback?"
python3 rag.py "$QUESTION" --top-k 2
python3 rag.py "$QUESTION" --top-k 4

python3 rag.py "What is the catering budget?"
python3 -m unittest discover -s tests -v
```

The webhook query ranks the chunk containing the 24-hour policy first. For the checkout query, the top two results omit the incident communications policy. Expanding to four includes the 15-minute update cadence. The catering question has no lexical match, so it exits without calling a model.

To try a public documentation example, search the notes on PostgreSQL backup and restore:

```sh
python3 rag.py "Which archive formats can I use for a parallel restore with pg_restore?" \
  --corpus examples/postgresql --top-k 1
```

The first result is [the parallel restore note](examples/postgresql/backups.md#parallel-restore), which points to the official `pg_restore` manual.

## Add generation locally

Start [Ollama](https://ollama.com/) if it is stopped, then download a model. The model runs outside Python. The CLI sends the exact messages shown by `--show-prompt` as JSON to Ollama on loopback.

```sh
ollama pull qwen2.5:0.5b
python3 rag.py "How long are both webhook signing secrets accepted?" \
  --top-k 1 --model qwen2.5:0.5b --show-prompt
```

You can pass a different locally installed model with `--model`. The [observed runs](docs/observed-runs.md) include a correct short answer and two incomplete answers from the same model. The tests check deterministic retrieval and prompt behavior independently of generation.

## What happens under the hood

1. Read Markdown and text. Split at blank lines and use overlapping word windows for long blocks. Keep source file and line spans.
2. Tokenize, case-fold and discard a small stop list. Count each term per chunk. If a term appears in `df` of `N` chunks, its IDF is `log((1 + N) / (1 + df)) + 1`.
3. Multiply counts by IDF and L2-normalize the sparse vectors. Rank by cosine similarity, which is the dot product of the normalized vectors.
4. Pack positive-scoring chunks into a character budget and assign prompt-local source IDs that point back to file and line spans.
5. Optionally send the prompt to a language model, asking it to cite the source IDs.

Try your own Markdown or text files with `--corpus ./my-docs`. `--context-chars` bounds the characters in the packed source blocks. It excludes the instructions and question and is not a model token limit.

This example uses exact terms and scans an in-memory index. Paraphrases may miss relevant chunks, overlapping passages can repeat context, and a positive score does not measure confidence or prove the answer exists. A source ID in generated prose is a pointer to inspect, not a guarantee that a claim is supported. Treat the included runbooks as trusted demonstration content. Prompt instructions alone do not enforce trust boundaries for arbitrary documents.

## Further reading

- [The original RAG paper](https://arxiv.org/abs/2005.11401)
- [Ollama chat endpoint](https://docs.ollama.com/api/chat)
