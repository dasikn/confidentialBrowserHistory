# ConfidentialHistorySearch

A Firefox extension that indexes web pages you visit into a local vector database, making your browsing history searchable via semantic search through an LLM chat interface. All using confidential AI, so your data stays private, because who likes to share their browser history?

## How it works

1. **Browse the web** and click "Index Page" on any page you want to remember
2. The page content is chunked, embedded, and stored in ChromaDB
3. **Ask questions** through any MCP-compatible client (e.g. Open WebUI) and the LLM automatically searches your indexed pages for relevant context

All LLM and embedding requests are encrypted via [Privatemode Proxy](https://www.privatemode.ai/en) before reaching the cloud, ensuring your browsing data stays confidential.

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

| Service                     | Purpose                                                            |
| --------------------------- | ------------------------------------------------------------------ |
| **Firefox Extension**       | Captures page content and sends it for indexing                    |
| **Backend API** (port 8002) | Receives pages, chunks text, stores embeddings                     |
| **MCP Server** (port 8001)  | Exposes semantic search as a tool for any MCP client               |
| **ChromaDB**                | Vector database for storing and querying embeddings                |
| **Privatemode Proxy**       | Encrypts LLM and embedding requests for confidential AI processing |

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

Get your API key at https://www.privatemode.ai/en

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

Point any MCP-compatible client (We suggest Open WebUI because it allows to connect to the confidential AI proxy) to the MCP server.

**Open WebUI (running in Docker):**

Start Open WebUI connected to the Privatemode Proxy:

```bash
docker run -d -p 3000:8080 \
  -e OPENAI_API_BASE_URL=http://host.docker.internal:8080/v1 \
  -e OPENAI_API_KEY=not-needed \
  -e OLLAMA_BASE_URL= \
  -v open-webui-data:/app/backend/data \
  --name open-webui \
  ghcr.io/open-webui/open-webui:main
```

Then add the MCP tool:

1. Go to **Settings > Tools > Add MCP Server**
2. Set the URL to `http://host.docker.internal:8001/mcp`
3. Set both **Name** and **ID** to `browser-history`

> `host.docker.internal` is required because Open WebUI runs in its own container and `localhost` would refer to itself. If you run Open WebUI natively (not in Docker), use `http://localhost:8001/mcp` instead.

To stay confidential, you should use a chat model served as Confidential AI. For example, you can activate Confidential AI in Open WebUI as explained [here](https://www.privatemode.ai/en/tutorials/openwebui-integration). The Privatemode Proxy is already included in the docker-compose, so you just need to configure your MCP client to use it.

### 5. Use it

- **Index a page**: Visit any page and click the "Index Page" button (bottom-right corner)
- **Search**: Ask questions in your MCP client about pages you've indexed
- **Manage history**: Click the extension icon in the toolbar to delete indexed history by date or entirely

## API Endpoints

| Method   | Endpoint                | Description                        |
| -------- | ----------------------- | ---------------------------------- |
| `POST`   | `/index-page`           | Index a web page                   |
| `POST`   | `/search`               | Semantic search over indexed pages |
| `DELETE` | `/history`              | Delete all indexed history         |
| `DELETE` | `/history/{YYYY-MM-DD}` | Delete history for a specific date |
