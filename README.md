# ConfidentialHistorySearch

A Firefox extension that indexes web pages you visit into a local vector database, making your browsing history searchable via semantic search through an LLM chat interface.

## How it works

1. **Browse the web** and click "Index Page" on any page you want to remember
2. The page content is chunked, embedded, and stored in ChromaDB
3. **Ask questions** through any MCP-compatible client (e.g. Open WebUI) and the LLM automatically searches your indexed pages for relevant context

All LLM and embedding requests are encrypted via [Privatemode Proxy](https://github.com/edgelesssys/privatemode) before reaching the cloud, ensuring your browsing data stays confidential.

## Architecture

```
Firefox Extension ──POST /index-page──> Backend API (:8002) ──> ChromaDB
                                              │                     │
                                              │ embeddings          │
                                              v                     │
                                        Privatemode Proxy (:8080)   │
                                              ^           ^         │
                                   embeddings │           │ LLM     │
                                              │           │         │
              MCP Client ──MCP──> MCP Server (:8001) ─────┼─────────┘
                   │                                      │
                   └──────────────────────────────────────-┘
```

| Service | Purpose |
|---|---|
| **Firefox Extension** | Captures page content and sends it for indexing |
| **Backend API** (port 8002) | Receives pages, chunks text, stores embeddings |
| **MCP Server** (port 8001) | Exposes semantic search as a tool for any MCP client |
| **ChromaDB** | Vector database for storing and querying embeddings |
| **Privatemode Proxy** | Encrypts LLM and embedding requests for confidential AI processing |

## Setup

### Prerequisites

- Docker and Docker Compose
- Firefox

### 1. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

```
PRIVATEMODE_API_KEY=your-api-key-here
```

### 2. Start the backend

```bash
docker compose up -d
```

This starts all services. First run will pull images and may take a few minutes.

### 3. Install the Firefox extension

1. Open Firefox and go to `about:debugging#/runtime/this-firefox`
2. Click **Load Temporary Add-on**
3. Select `extension/manifest.json`

### 4. Connect an MCP client

Point any MCP-compatible client (e.g. Open WebUI, Claude Desktop) to `http://localhost:8001/mcp`.

### 5. Use it

- **Index a page**: Visit any page and click the "Index Page" button (bottom-right corner)
- **Search**: Ask questions in your MCP client about pages you've indexed
- **Manage history**: Click the extension icon in the toolbar to delete indexed history by date or entirely

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/index-page` | Index a web page |
| `POST` | `/search` | Semantic search over indexed pages |
| `DELETE` | `/history` | Delete all indexed history |
| `DELETE` | `/history/{YYYY-MM-DD}` | Delete history for a specific date |
