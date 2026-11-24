# Observed runs

Verified with Python 3.12.7 and Ollama 0.33.2. The local generation runs used `qwen2.5:0.5b` with temperature 0. Quoted answers below are actual model output. The CLI's source list records what went into the prompt.

## Checkout rollback

```sh
question="When should I roll back a checkout deployment, and how often should I post updates during the rollback?"
python3 rag.py "$question" --top-k 2
python3 rag.py "$question" --top-k 4
python3 rag.py "$question" --top-k 4 --model qwen2.5:0.5b --show-prompt
```

The rerun with four results selected these chunks:

```text
0.526  checkout-deploy.md:1-1
0.445  checkout-deploy.md:3-4
0.356  incident-comms.md:3-4
0.329  checkout-deploy.md:6-7
```

At two results, the 15-minute rule was absent from the prompt. At four results, the prompt contained both the rollback threshold and the update interval. The model still omitted the threshold and the requested source IDs:

> To roll back a checkout deployment, you should post updates every 15 minutes during the rollback.

## Webhook signing secret

```sh
python3 rag.py "How long are both webhook signing secrets accepted?" \
  --top-k 1 --model qwen2.5:0.5b --show-prompt
```

The top result was `payments-webhooks.md:3-4` at 0.465. The model answered “24 hours,” correctly reporting the duration. It omitted the requested source ID.

## PostgreSQL parallel restore

```sh
python3 rag.py "Which archive formats can I use for a parallel restore with pg_restore?" \
  --corpus examples/postgresql --top-k 1 --model qwen2.5:0.5b --show-prompt
```

The top result was `backups.md:3-4` at 0.590. It contained the relevant formats. The model answered “A regular file or directory can be used for a parallel restore with pg_restore.” That states an input requirement, but the question asked for archive formats: custom and directory. The note is based on the [official pg_restore documentation](https://www.postgresql.org/docs/current/app-pgrestore.html).

## No lexical match

```sh
python3 rag.py "What is the catering budget?" --model qwen2.5:0.5b
```

Observed output: `No matching chunks. No model call.`
