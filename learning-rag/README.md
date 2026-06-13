# Learning RAG with Elastic Docs

Three notebooks that build a search-and-answer system on top of this documentation
repository — starting with the simplest possible approach and working up to the
method best suited to technical content.

---

## What is RAG?

**RAG** stands for Retrieval-Augmented Generation. The name is a mouthful, but the
idea is straightforward.

When you ask a general-purpose AI a question, it answers from what it learned during
training. That has two problems for documentation work: the AI may not know your
specific content, and it can confidently state things that are wrong.

RAG adds a search step before the answer step:

1. **Retrieve** — search your own documents for the passages most relevant to the
   question
2. **Augment** — hand those passages to the AI as context, with an instruction to
   answer only from what you provided
3. **Generate** — the AI produces an answer grounded in your retrieved text, with
   citations back to source documents

The critical insight is that **retrieval quality determines answer quality**. If the
wrong passages come back from search, the AI will either produce a wrong answer or
correctly say "I don't have enough information" — but either way, the search step
failed. Getting retrieval right matters far more than which AI model you use.

Think of it as the difference between asking a colleague to answer off the top of
their head versus asking them to look up the relevant pages first and then
summarize what those pages say.

---

## Why Elastic docs make a good test corpus

Most RAG tutorials use toy datasets — a handful of Wikipedia articles or a small
FAQ. This repo offers something more realistic:

- **Scale and structure.** Thousands of Markdown files organized into sections
  (get-started, solutions, manage-data, and so on), with consistent frontmatter.
- **Multiple distinct domains.** Search, observability, and security content lives
  side by side. A good retrieval system should return the right domain's pages for a
  domain-specific question — not just anything semantically adjacent.
- **Dense technical vocabulary.** Elastic docs use precise terms: *inference
  endpoint*, *ingest pipeline*, *semantic_text*, *ELSER*, *RRF*. These terms are
  uncommon in general-purpose AI training data. Whether a retrieval approach handles
  domain-specific vocabulary well is exactly the question these notebooks explore.
- **Real-world messiness.** The source files contain build-time substitution
  variables like `{{es}}` and `{{kib}}` (explained below). Every realistic corpus
  has some form of this problem.

---

## The question these notebooks try to answer

All three notebooks build the same RAG loop — chunk the docs, index them, retrieve
top passages for a question, build a prompt — but each uses a different retrieval
approach. Running them in order is an experiment:

> **Does the retrieval method matter, and which approach works best for technical
> documentation?**

The progression is:

| Notebook | Retrieval approach | What changes |
|---|---|---|
| 1. Chroma | Dense vectors, local model, vector-only search | Baseline — no cloud required |
| 2. Elasticsearch (dense) | Dense vectors via Elastic Inference, hybrid search | Cloud retrieval, keyword + semantic combined |
| 3. Elasticsearch (ELSER) | Sparse vectors via ELSER, hybrid search | Domain-aware model designed for technical text |

The empirical answer, which you can observe by running all three with the same
question and the same corpus: vector-only search (notebook 1) sometimes surfaces an
irrelevant page at rank 1, while hybrid search (notebooks 2 and 3) consistently
finds the right document. ELSER's advantage shows up most clearly on queries that
use Elastic-specific terminology, because ELSER was trained to understand that
vocabulary.

---

## The three notebooks

### 1. `minimal-rag-on-elastic-docs.ipynb` — Start here

**Retrieval: Chroma + MiniLM (runs entirely on your Mac)**

Downloads a small, free embedding model (~80 MB, one-time), converts doc chunks to
vectors, and stores them in a local Chroma database. No cloud account needed.

Use this notebook to understand the RAG loop itself before adding cloud complexity.
The core concepts — chunking, embedding, similarity search, prompt construction —
are all here in their simplest form.

After running it, the key exercise is reading the retrieved chunks *before* looking
at any AI-generated answer. The quality of those chunks tells you whether the
retrieval worked.

**When to use this approach in practice:** prototyping on a laptop, small corpora
where you control all the data, or environments where a cloud service is not
available.

---

### 2. `minimal-rag-on-elasticsearch.ipynb` — Add cloud retrieval

**Retrieval: Elasticsearch `semantic_text` + hybrid RRF**

Moves retrieval from Chroma to Elasticsearch. The key change is *hybrid search*:
instead of finding passages by vector similarity alone, this notebook combines a
keyword (BM25) search and a semantic search, then merges the rankings using a
technique called Reciprocal Rank Fusion (RRF).

**Keyword search** matches exact and near-exact words. **Semantic search** finds
passages with similar meaning even when they use different words. **RRF** is a
simple formula that combines two ranked lists into one without needing to calibrate
scores between them. The combined result is more robust than either approach alone.

Elasticsearch handles embedding generation automatically via the Elastic Inference
Service — you index plain text, and the cloud creates the vectors.

**When to use this approach in practice:** most production search use cases where
you want both keyword precision and semantic recall without managing embedding
infrastructure.

---

### 3. `minimal-rag-on-elasticsearch-elser.ipynb` — Add domain awareness

**Retrieval: Elasticsearch ELSER sparse vectors + hybrid RRF**

Replaces dense embeddings with ELSER — Elastic's Learned Sparse EncodeR. Dense
embeddings represent text as a list of numbers (a vector) in a general-purpose
semantic space. Sparse embeddings work differently: ELSER produces a list of
weighted tokens that represent the *meaning* of the text in vocabulary-aware terms.

The practical effect: ELSER is trained to understand that "EIS" and "Elastic
Inference Service" are the same thing, that "ingest pipeline" and "processor
pipeline" are related, and that "ELSER" is a specific Elastic product rather than
a generic word. General-purpose dense models (like MiniLM) have little or no
knowledge of this vocabulary.

The tradeoff is setup time. ELSER is an ML model that runs on your Elasticsearch
cluster, and the first-time download and deployment can take 10–20 minutes.
Indexing is also slower — each document chunk passes through the model at ingest
time.

**When to use this approach in practice:** technical documentation, product-specific
knowledge bases, or any corpus with domain-specific vocabulary that general models
are unlikely to handle well.

---

## The Mustache placeholder issue

The Markdown source files in this repo use substitution variables that are resolved
at build time, not in the source:

```
{{es}}        →  Elasticsearch
{{kib}}       →  Kibana
{{stack}}     →  Elastic Stack
{{apm-server}} →  APM Server
```

These notebooks index the raw source files, so the variables appear literally in
indexed chunks. This creates two retrieval problems:

1. **Vocabulary mismatch.** A query for "Elasticsearch" will not match a chunk that
   contains only `{{es}}`, because the strings are different. The retrieval system
   cannot know they refer to the same thing.
2. **LLM confusion.** When `{{apm-server}}` or `{{observability}}` appears in the
   prompt context, the AI model has to infer what the variable means. Most large
   models will guess correctly for Elastic's well-known variables, but the
   uncertainty affects answer reliability.

For learning purposes this is acceptable — you can still observe retrieval behavior
and compare approaches. For a production system built on this corpus you would
pre-process the source files to expand or strip these variables before indexing.

---

## Prerequisites

### All three notebooks

- Python 3.10 or later
- A terminal and basic comfort with the command line
- The `docs-content` repo cloned locally (you are already here)

### Notebooks 2 and 3 only

- An Elastic Cloud account with a running deployment or Serverless project
- Two environment variables set in your shell before starting Jupyter:

  ```bash
  export ELASTICSEARCH_URL="https://your-deployment.es.region.cloud.es.io:443"
  export ELASTICSEARCH_API_KEY="your-api-key"
  ```

  To generate an API key: in Kibana, open the global search and search for
  **API keys**.

### Notebook 3 only

- ML node capacity on your deployment (required to run the ELSER model). Trial
  deployments include a 4 GB ML node, which is sufficient.
- Patience: the first ELSER deployment typically takes 10–20 minutes while the
  model downloads and starts. Subsequent runs are fast.

---

## Suggested order

If you have 15–30 minutes and no Elastic Cloud account: **run notebook 1 only**.
Focus on reading the retrieved chunks, not the AI answer.

If you have an Elastic Cloud account: **run notebooks 1 and 2** with the same
`CORPUS_FOLDER` and `QUESTION`. Compare which chunks appear at rank 1 in each.

If you want to see the full progression: **run all three** with the same settings,
then read the comparison table in notebook 3 (§8) alongside your own results.

In all cases: the learning is in the retrieved passages, not in the AI's answer.
