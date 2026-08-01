# RAG learning session — recovery notes

Recovered summary of the **"Testing RAG experience"** Cursor chat (in case the tab lost content).
Use this as your reference; notebooks and outputs on disk are unchanged.

---

## What you built

### 1. Chroma notebook (`minimal-rag-on-elastic-docs.ipynb`)

- **Corpus:** `get-started/` then `solutions/` (`MAX_FILES = 100` → ~665 chunks)
- **Store:** Chroma on disk (`chroma_elastic_solutions/`)
- **Embeddings:** Local `all-MiniLM-L6-v2` via sentence-transformers
- **Retrieve:** Vector-only (`collection.query`)
- **Augment + generate:** §6 prompt → optional Ollama

### 2. Elasticsearch notebook (`minimal-rag-on-elasticsearch.ipynb`)

- **Same chunking** as Chroma (§3)
- **Index:** `elastic-rag-solutions` on Elastic Cloud (9.5.0)
- **Mapping:** `content` (text) + `semantic_text` (`copy_to` → Elastic Inference embeddings)
- **Retrieve:** Hybrid RRF — keyword on `content` + semantic on `semantic_text`
- **Result:** `index.md` ranked **#1** (vs Chroma where LLM matrix page was #1, `index.md` #2)
- **Both** still retrieved `index.md` in top-k → good grounded answers

### 3. ELSER notebook (you have `minimal-rag-on-elasticsearch-elser.ipynb` open)

- Sparse semantic path (separate from dense `semantic_text` lab)

---

## RAG in one story

| Step | Letter | What happens |
|------|--------|----------------|
| Chunk docs | — | Markdown → passages + `source` path |
| Index | — | Embeddings stored (Chroma folder or ES index) |
| **Retrieve** | **R** | Question → find top-k chunks |
| **Augment** | **A** | Instructions + CONTEXT + QUESTION (plain text) |
| **Generate** | **G** | LLM answer (Ollama or chat) |

**LLM never sees raw vectors** — only retrieved text.

---

## Production vs your Mac

| Your Mac | Production (e.g. docs assistant) |
|----------|----------------------------------|
| Jupyter on laptop | User browser → API backend |
| Chroma folder / ES index on Cloud | Managed search cluster |
| Index when you run §4 | Index on doc publish / schedule |
| You type QUESTION | Each user question triggers retrieve → prompt → LLM |

---

## Key concepts (recent Q&A)

### Dense vector

- Long list of numbers (mostly non-zero) representing meaning
- Chroma + MiniLM and Elastic `semantic_text` use **dense** embeddings
- Used for similarity search; not sent to the LLM

### Semantic search vs vector search

- **Semantic search** = goal (match by meaning)
- **Vector search** = technique (compare embeddings)
- **Keyword search** = exact terms (BM25 on `content`)
- **Hybrid** = both + merge (RRF) — why Elastic ranked `index.md` higher

### Chunk content vs filename

- Retrieval scores **passage text**, not file names
- Rank #1 can be wrong while rank #2 has the gold answer — inspect §5 before trusting answers
- `TOP_K = 1` is riskier than `TOP_K = 5`

---

## Notebook section guides (Elastic notebook — what changed)

| § | Topic |
|---|--------|
| 1 | `pip install elasticsearch` (same `.venv` as Chroma) |
| 2 | `ELASTICSEARCH_URL`, `ELASTICSEARCH_API_KEY`, `INDEX_NAME` |
| 3 | Same chunking as Chroma |
| 4 | Create index, bulk ingest, Elastic embeds `semantic_text` |
| 5 | Hybrid RRF search |
| 6–7 | Same prompt + Ollama as Chroma |
| 8 | Compare Chroma vs Elastic |

**Chroma notebook:** `CORPUS_FOLDER`, `COLLECTION_NAME`, `chroma_*` folder.

---

## Interview one-liners

**Chroma:**

> Built a prototype RAG pipeline on a slice of Elastic’s docs clone (`get-started/` / `solutions/`), using Chroma for retrieval and Ollama for grounded answers.

**Chroma + Elastic:**

> Ran the same corpus twice: local vector search vs Elasticsearch `semantic_text` with hybrid RRF; both retrieved `solutions/index.md`, but hybrid ranked the overview page first.

---

## Files in `learning-rag/`

| File | Role |
|------|------|
| `minimal-rag-on-elastic-docs.ipynb` | Chroma + Ollama |
| `minimal-rag-on-elasticsearch.ipynb` | Elastic hybrid |
| `minimal-rag-on-elasticsearch-elser.ipynb` | ELSER variant |
| `requirements.txt` / `requirements-elasticsearch.txt` | Dependencies |
| `sample-context.md` | Saved CONTEXT example for prompt practice |
| `.venv/` | Shared Python environment |

---

## Paste-in for a new chat

> Non-developer, learning for Elastic TW role. Completed RAG: Chroma notebook on `solutions/`, Elasticsearch notebook with `semantic_text` + hybrid RRF (`elastic-rag-solutions`). Compared retrieval: `index.md` higher with Elastic hybrid. Read section walkthroughs §1–§8. Next: dense vs sparse (ELSER), or prompt/skills work.

---

## Recovering the Cursor chat itself

1. **Chat history** in Cursor sidebar — reopen the "Testing RAG experience" thread if it still exists.
2. **Scroll up** in the thread — sometimes UI glitches hide content but history remains.
3. **This file** + notebooks — permanent copy on disk.
4. Agent transcripts (partial): other tabs may be in `~/.cursor/projects/.../agent-transcripts/` — this long RAG thread may not be fully exported yet.

---

*Generated as a recovery aid — personal learning only (CC BY-NC-ND on doc content).*
