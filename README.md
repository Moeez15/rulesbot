# 🎲 RulesBot

> A board game rules assistant — because "just read the rulebook" isn't always helpful at 11pm on game night.

RulesBot answers natural language questions about board game rules using a RAG (Retrieval-Augmented Generation) pipeline. Ask it anything: it retrieves relevant rule passages and generates an answer grounded in the actual text.

---

## Getting Started

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
# or: .venv\Scripts\activate   # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** `sentence-transformers` will download the embedding model (~80MB) on first run. This only happens once — it's cached locally afterward.

### 3. Add your Groq API key

```bash
cp .env.example .env
```

Open `.env` and replace `your_key_here` with your key from [console.groq.com](https://console.groq.com). No credit card required.

### 4. Run the app

```bash
python app.py
```

---

## Project Structure

```
ai201-lab1-rulesbot-starter/
├── app.py              # Gradio UI and startup logic — fully built
├── config.py           # Settings (models, paths, retrieval params) — fully built
├── ingest.py           # Document loading + chunking
├── retriever.py        # Vector store + semantic search
├── generator.py        # LLM response generation
├── docs/               # Board game rule documents (pre-loaded)
│   ├── catan.txt
│   ├── clue.txt
│   ├── codenames.txt
│   ├── monopoly.txt
│   ├── pandemic.txt
│   ├── risk.txt
│   ├── ticket_to_ride.txt
│   └── uno.txt
├── specs/              # Design documents
│   ├── system-design.md
│   ├── chunk-document-spec.md   
│   ├── retrieve-spec.md         
│   └── generate-response-spec.md 
```

## Start with the Specs

Read `specs/system-design.md`. It explains why the technical decisions were made. The spec becomes the brief you hand to your AI tool when ready to implement.

---

## Re-ingesting After Changes

ChromaDB persists to disk in `./chroma_db`. If you change your chunking strategy and want to re-ingest, delete that folder and restart the app:

```bash
rm -rf chroma_db/   # Mac/Linux
# or: rmdir /s chroma_db   # Windows
python app.py
```

---

## Rule Books Included

| Game | File |
|------|------|
| Catan | `docs/catan.txt` |
| Clue | `docs/clue.txt` |
| Codenames | `docs/codenames.txt` |
| Monopoly | `docs/monopoly.txt` |
| Pandemic | `docs/pandemic.txt` |
| Risk | `docs/risk.txt` |
| Ticket to Ride | `docs/ticket_to_ride.txt` |
| Uno | `docs/uno.txt` |
