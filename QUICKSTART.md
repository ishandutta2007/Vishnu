# 🔱 Vishnu (openGotham) — Quick Start Guide

> **Get the Vishnu intelligence platform running on your computer in under 5 minutes.**
> No cloud account, no Docker, no complex setup required.

---

## 📋 What You'll Need (Prerequisites)

Before starting, make sure you have these two programs installed on your computer:

| Software | Version | How to Check | Download Link |
|:---------|:--------|:-------------|:--------------|
| **Python** | 3.10 or newer | Open a terminal and type `python --version` | [python.org/downloads](https://www.python.org/downloads/) |
| **Node.js** | 18 or newer | Open a terminal and type `node --version` | [nodejs.org](https://nodejs.org/) |

> 💡 **Not sure if you have them?** Open a command prompt (Windows) or terminal (Mac/Linux) and type the commands in the "How to Check" column. If you see a version number, you're good!

---

## 🚀 Step-by-Step Setup

### Step 1: Download the Project

**Option A — If you have Git installed:**
```bash
git clone https://github.com/ishandutta2007/Vishnu.git
cd Vishnu
```

**Option B — If you don't have Git:**
1. Go to the [GitHub repository page](https://github.com/ishandutta2007/Vishnu)
2. Click the green **"Code"** button
3. Click **"Download ZIP"**
4. Unzip the folder and open a terminal inside it

---

### Step 2: Start the Backend (API Server)

Open a terminal/command prompt and run these commands **one by one**:

```bash
# Go into the backend folder
cd backend

# Create a virtual environment (a clean space for Python packages)
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install the required Python packages
pip install -r requirements.txt

# Start the server
python run.py
```

✅ **You should see:** `Uvicorn running on http://0.0.0.0:8000`

> 🎯 **Test it:** Open your browser and go to [http://localhost:8000/docs](http://localhost:8000/docs) — you should see the interactive API documentation.

---

### Step 3: Start the Frontend (User Interface)

Open a **new** terminal/command prompt (keep the backend running!) and run:

```bash
# Go into the frontend folder
cd frontend

# Install the required JavaScript packages
npm install

# Start the development server
npm run dev
```

✅ **You should see:** `Local: http://localhost:5173/`

> 🎯 **Open the app:** Go to [http://localhost:5173](http://localhost:5173) in your browser.

---

### Step 4: Load the Demo Data

When you first open Vishnu, the workspace will be empty. To load the built-in intelligence scenario:

1. Look at the **left sidebar**
2. Click the **🚀 Load Demo Data** button (or **🗃️ Load Demo** at the bottom)
3. Watch the graph populate with the **Operation Nightfall** demo scenario!

> 📖 The demo dataset is a fictional intelligence investigation involving a transnational financing network with persons, organizations, locations, vehicles, events, and documents — all interconnected.

---

## 🖥️ Using Vishnu — A Quick Tour

### The Interface

```
┌──────────────────────────────────────────────────────────┐
│  🔱 VISHNU     [  Global Search Bar  ]   📊  🧩  v0.1.0 │  ← Top Bar
├────────┬──────────────────────────────┬──────────────────┤
│        │                              │                  │
│  Left  │     Graph Canvas             │   Entity         │
│ Sidebar│  (click nodes to explore)    │   Dossier        │
│        │                              │  (360° view)     │
│ Entity │                              │                  │
│  List  │                              │  Properties      │
│        │                              │  Relationships   │
│ Search │                              │  Path Finder     │
│ Filter │                              │                  │
│        │                              │                  │
├────────┤                              ├──────────────────┤
│ [Demo] │    [Fit] [Layout] [Zoom]     │                  │
│ [+New] │                              │                  │
└────────┴──────────────────────────────┴──────────────────┘
```

### Key Features

| Feature | How to Use |
|:--------|:-----------|
| **Browse Entities** | Scroll through the left sidebar |
| **Search** | Type in the search box in the sidebar or top bar |
| **Filter by Type** | Click entity type buttons (👤 person, 🏢 organization, etc.) |
| **View Entity Details** | Click any node in the graph or any entity in the sidebar |
| **Explore Connections** | When an entity is selected, its neighborhood is highlighted |
| **Find Shortest Path** | Select an entity → in the dossier panel → select a target → click "Find" |
| **View Key Players** | Click **📊 Key Nodes** in the top bar (betweenness centrality analysis) |
| **Detect Communities** | Click **🧩 Communities** in the top bar |
| **Create New Entities** | Click **+ New Entity** at the bottom of the sidebar |
| **Graph Controls** | Use Fit, Layout, Zoom buttons at bottom-right of the graph |

---

## 📊 API Documentation

The backend provides a complete REST API with interactive documentation:

| URL | Description |
|:----|:------------|
| [http://localhost:8000/docs](http://localhost:8000/docs) | **Swagger UI** — Interactive API testing |
| [http://localhost:8000/redoc](http://localhost:8000/redoc) | **ReDoc** — Beautiful API reference |

### Key API Endpoints

| Endpoint | Method | Description |
|:---------|:-------|:------------|
| `/api/entities` | GET | List all entities (with pagination & filters) |
| `/api/entities` | POST | Create a new entity |
| `/api/entities/{id}` | GET | Get entity details with relationships |
| `/api/relationships` | POST | Create a relationship between entities |
| `/api/graph/data` | GET | Get full graph (Cytoscape.js format) |
| `/api/graph/shortest-path` | GET | Find shortest path between two entities |
| `/api/graph/centrality` | GET | Top entities by betweenness centrality |
| `/api/graph/communities` | GET | Community detection results |
| `/api/search?q=...` | GET | Full-text search across all entities |
| `/api/ingest/csv` | POST | Upload CSV to bulk-create entities |
| `/api/ingest/json` | POST | Upload JSON with entities + relationships |
| `/api/ingest/seed` | POST | Load the demo scenario |
| `/api/entities/duplicates/detect` | GET | Find potential duplicate entities |
| `/api/entities/merge` | POST | Merge two duplicate entities |

---

## 📁 Project Structure

```
Vishnu/
├── backend/                    ← Python API server
│   ├── run.py                  ← Start the server from here
│   ├── requirements.txt        ← Python dependencies
│   ├── app/
│   │   ├── main.py             ← FastAPI app setup
│   │   ├── config.py           ← Configuration (ports, CORS, etc.)
│   │   ├── database.py         ← SQLite database setup
│   │   ├── seed_data.py        ← Demo data (Operation Nightfall)
│   │   ├── models/             ← Database table definitions
│   │   │   ├── entity.py       ← Entity table (persons, orgs, etc.)
│   │   │   └── relationship.py ← Relationship table (edges)
│   │   ├── schemas/            ← API request/response schemas
│   │   │   ├── entity.py
│   │   │   └── relationship.py
│   │   ├── routers/            ← API endpoint definitions
│   │   │   ├── entities.py     ← Entity CRUD + dedup
│   │   │   ├── relationships.py← Relationship CRUD
│   │   │   ├── graph.py        ← Graph analytics endpoints
│   │   │   ├── search.py       ← Search endpoint
│   │   │   └── ingest.py       ← Data ingestion endpoints
│   │   └── services/           ← Business logic
│   │       ├── graph_engine.py ← NetworkX graph analytics
│   │       ├── entity_resolution.py ← Deduplication logic
│   │       └── search_engine.py← Search logic
│   └── venv/                   ← Virtual environment (not in git)
│
├── frontend/                   ← React web interface
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts          ← Build tool configuration
│   ├── tailwind.config.js      ← CSS framework configuration
│   └── src/
│       ├── main.tsx            ← App entry point
│       ├── App.tsx             ← Main app orchestrator
│       ├── api.ts              ← API client
│       ├── types.ts            ← TypeScript type definitions
│       └── components/
│           ├── GraphWorkspace.tsx  ← Cytoscape.js graph canvas
│           ├── Sidebar.tsx        ← Entity list & search
│           ├── EntityDossier.tsx   ← 360° entity profile
│           ├── TopBar.tsx         ← Header & analytics
│           └── CreateEntityModal.tsx ← New entity form
│
├── README.md                   ← Project overview
├── QUICKSTART.md               ← This file
└── .gitignore
```

---

## 🛠️ Technology Stack

| Component | Technology | Why This Choice |
|:----------|:-----------|:----------------|
| **Backend API** | Python + FastAPI | Fastest Python web framework, auto-generates API docs, great type safety |
| **Database** | SQLite | Zero setup — just works. No database server to install. Perfect for getting started |
| **Graph Analytics** | NetworkX | Industry-standard Python graph library. Centrality, shortest path, community detection |
| **Frontend** | React 18 + TypeScript | Type-safe UI with the most popular component framework |
| **Graph Visualization** | Cytoscape.js | Purpose-built for network/graph visualization. Used by researchers worldwide |
| **Styling** | Tailwind CSS | Utility-first CSS for rapid, consistent UI development |
| **Build Tool** | Vite | Lightning-fast dev server with hot module replacement |

> 💰 **Cost: $0** — Every technology used is 100% free and open source. No paid tiers, no API keys, no cloud accounts needed.

---

## ❓ Troubleshooting

### "python is not recognized"
→ Python isn't installed or isn't in your PATH. Download it from [python.org](https://www.python.org/downloads/). On Windows, make sure to check **"Add Python to PATH"** during installation.

### "node is not recognized"  
→ Node.js isn't installed. Download it from [nodejs.org](https://nodejs.org/).

### Backend starts but frontend shows "Failed to fetch"
→ Make sure the backend is running on port 8000 before starting the frontend. The frontend proxies API requests to localhost:8000.

### Port 8000 is already in use
→ Another program is using that port. Either stop that program, or edit `backend/run.py` to change the port number.

### Graph is empty after loading demo data
→ Try refreshing your browser (Ctrl+R or Cmd+R). If the issue persists, check the backend terminal for error messages.

---

## 🔮 What's Next?

This is **Phase 1** of Project Vishnu. Here's what's planned:

- 🗺️ **Geospatial Map View** — Plot entities on a world map with Deck.gl
- 📥 **Advanced Data Ingestion** — Kafka streaming, PDF parsing, web scraping
- 🤖 **AI Co-Pilot** — Natural language queries over your intelligence data (RAG)
- 🔐 **Security & Access Control** — RBAC/ABAC, classification-based access
- ⏳ **Timeline View** — Chronological event correlation
- 🤝 **Real-Time Collaboration** — Multi-user workspaces via WebSocket
