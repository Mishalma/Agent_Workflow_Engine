# 🤖 Agent Workflow Engine

> A lightweight, LangGraph-inspired workflow orchestration engine built with FastAPI. Design complex agent workflows with nodes, edges, conditional branching, and loops—all through a simple REST API.

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.124+-green.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.0+-purple.svg)](https://github.com/langchain-ai/langgraph)

---

## 🌟 Features at a Glance

| Feature | Description | Status |
|---------|-------------|--------|
| 🔗 **Graph-Based Workflows** | Define workflows as nodes and edges | ✅ |
| 📊 **State Management** | Shared state flows through all nodes | ✅ |
| 🔀 **Conditional Branching** | Route based on state values (gt/lt) | ✅ |
| 🔄 **Loop Support** | Repeat nodes until conditions are met | ✅ |
| 🛠️ **Tool Registry** | Pre-registered Python functions | ✅ |
| 🚀 **REST API** | Create and execute workflows via HTTP | ✅ |
| 📝 **Execution Logging** | Track every step of workflow execution | ✅ |
| 💾 **Checkpointing** | State persistence with LangGraph | ✅ |

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd aiagent_project

# Install dependencies with uv (recommended)
uv sync

# Or use pip
pip install -r requirements.txt
```

### Start the Server

```bash
uv run uvicorn main:app --reload
```

🎉 Server running at **http://127.0.0.1:8000**

📚 Interactive API docs at **http://127.0.0.1:8000/docs**

### Run the Example

```bash
# In a new terminal
uv run python example_workflow.py
```

Expected output:
```
================================================================================
AGENT WORKFLOW ENGINE - EXAMPLE EXECUTION
================================================================================

📊 Creating summarization workflow graph...
✅ Graph created with ID: xxx-xxx-xxx

🚀 Running workflow with sample text...
   Input text length: 1798 characters

📝 EXECUTION LOG:
--------------------------------------------------------------------------------
Step 1: split (tool: split_text)
        → Updated: chunks
Step 2: summarize (tool: generate_summaries)
        → Updated: summaries
Step 3: merge (tool: merge_summaries)
        → Updated: merged_summary
Step 4: refine (tool: refine_summary)
        → Updated: final_summary, length

✅ Workflow completed successfully!
```

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| **[QUICKSTART.md](QUICKSTART.md)** | Get up and running in 5 minutes |
| **[API_REFERENCE.md](API_REFERENCE.md)** | Complete API endpoint documentation |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | System design and technical details |
| **[PROJECT_STATUS.md](PROJECT_STATUS.md)** | Implementation status and metrics |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Layer                          │
│                       (main.py)                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ POST /create │  │  POST /run   │  │ GET /state   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Graph Engine Layer                        │
│                  (graph_engine.py)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • Build graphs from definitions                     │  │
│  │  • Compile with LangGraph                            │  │
│  │  • Execute with state management                     │  │
│  │  • Handle conditional routing & loops                │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     Tool Registry                           │
│                      (tools.py)                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  split_text  │  │ gen_summary  │  │merge_summary │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Core Concepts

### 1️⃣ Nodes
Nodes are the building blocks of your workflow. Each node wraps a tool (Python function) that processes state.

```python
def my_tool(state: dict) -> dict:
    # Read from state
    input_data = state.get('input_key')
    
    # Process
    result = process(input_data)
    
    # Return updates
    return {'output_key': result}
```

### 2️⃣ Edges
Edges define the flow between nodes.

```json
{
  "edges": {
    "node_a": "node_b",
    "node_b": "node_c"
  }
}
```

### 3️⃣ State
A shared dictionary that flows through all nodes. Each node can read and update state.

```python
{
  "input_text": "Hello world",
  "chunks": [...],
  "summaries": [...],
  "log": [...]
}
```

### 4️⃣ Conditional Branching
Route execution based on state values.

```json
{
  "loops": [
    {
      "after": "refine",
      "condition": {
        "key": "length",
        "op": "gt",
        "value": 200
      },
      "back_to": "refine"
    }
  ]
}
```

---

## 🛠️ Available Tools

| Tool | Input | Output | Description |
|------|-------|--------|-------------|
| `split_text` | `input_text` | `chunks` | Split text into 500-char chunks |
| `generate_summaries` | `chunks` | `summaries` | Create summaries (first 100 chars) |
| `merge_summaries` | `summaries` | `merged_summary` | Combine all summaries |
| `refine_summary` | `merged_summary` | `final_summary`, `length` | Reduce length by 30% |

---

## 📡 API Endpoints

### Create a Graph
```http
POST /graph/create
Content-Type: application/json

{
  "nodes": [
    {"name": "process", "tool": "split_text"}
  ],
  "edges": {},
  "loops": [],
  "start": "process"
}
```

**Response:**
```json
{
  "graph_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Run a Workflow
```http
POST /graph/run
Content-Type: application/json

{
  "graph_id": "550e8400-e29b-41d4-a716-446655440000",
  "initial_state": {
    "input_text": "Your text here..."
  }
}
```

**Response:**
```json
{
  "final_state": {
    "input_text": "...",
    "chunks": [...],
    "log": [...]
  },
  "execution_log": [
    {
      "node": "process",
      "tool": "split_text",
      "result": {...}
    }
  ]
}
```

### Get Workflow State
```http
GET /graph/state/{run_id}
```

---

## 💡 Example: Summarization Pipeline

The included example demonstrates a 4-step text summarization workflow:

```
Input Text (1798 chars)
    ↓
┌─────────────┐
│ 1. Split    │ → Divide into 500-char chunks
└─────────────┘
    ↓
┌─────────────┐
│ 2. Summarize│ → Generate summaries (100 chars each)
└─────────────┘
    ↓
┌─────────────┐
│ 3. Merge    │ → Combine all summaries
└─────────────┘
    ↓
┌─────────────┐
│ 4. Refine   │ → Reduce length by 30%
└─────────────┘
    ↓
Final Summary (373 chars)
```

Run it:
```bash
uv run python example_workflow.py
```

---

## 🔧 Extending the Engine

### Add a New Tool

1. **Define the function** in `tools.py`:
```python
def my_custom_tool(state: dict) -> dict:
    data = state.get('input_data')
    result = custom_processing(data)
    return {'output_data': result}
```

2. **Register it**:
```python
tools['my_custom_tool'] = my_custom_tool
```

3. **Use it in a graph**:
```json
{
  "nodes": [
    {"name": "custom_step", "tool": "my_custom_tool"}
  ]
}
```

---

## 🎨 What Makes This Special

### ✨ Clean Architecture
- **Separation of Concerns**: API, Engine, and Tools are independent
- **Modular Design**: Easy to extend and maintain
- **Type Safety**: Pydantic models and TypedDict state

### 🚀 Production-Ready
- **Error Handling**: Graceful failures with clear messages
- **State Persistence**: Checkpointing with LangGraph
- **Recursion Protection**: Prevents infinite loops
- **Validation**: Request/response validation with Pydantic

### 📚 Well-Documented
- 5 comprehensive markdown files
- Interactive API documentation (Swagger UI)
- Working examples with real output
- Architecture diagrams and explanations

---

## 🔮 Future Enhancements

### High Priority
- [ ] **Async Execution** - Convert tools to async for better performance
- [ ] **WebSocket Streaming** - Real-time step-by-step updates
- [ ] **Persistent Storage** - SQLite/Postgres instead of in-memory
- [ ] **Dynamic Tool Loading** - Register tools via API
- [ ] **Better Error Recovery** - Retry logic and rollback

### Medium Priority
- [ ] **Background Tasks** - Long-running workflows with Celery
- [ ] **Graph Visualization** - Generate workflow diagrams
- [ ] **Metrics & Monitoring** - Execution time, success rates
- [ ] **Authentication** - API key or JWT-based auth
- [ ] **Rate Limiting** - Protect against abuse

### Nice to Have
- [ ] **Parallel Execution** - Run independent nodes concurrently
- [ ] **Subgraphs** - Nest workflows within workflows
- [ ] **Human-in-the-Loop** - Pause for user input
- [ ] **Version Control** - Track graph definition changes
- [ ] **Testing Suite** - Comprehensive unit and integration tests

---

## 🧪 Testing

### Manual Testing
```bash
# Test graph creation
curl -X POST http://127.0.0.1:8000/graph/create \
  -H "Content-Type: application/json" \
  -d @example_graph.json

# Test workflow execution
curl -X POST http://127.0.0.1:8000/graph/run \
  -H "Content-Type: application/json" \
  -d '{
    "graph_id": "your-graph-id",
    "initial_state": {"input_text": "Test"}
  }'
```

### Using Python
```python
import requests

# Create graph
response = requests.post(
    "http://127.0.0.1:8000/graph/create",
    json={
        "nodes": [{"name": "split", "tool": "split_text"}],
        "edges": {},
        "loops": [],
        "start": "split"
    }
)
graph_id = response.json()["graph_id"]

# Run workflow
result = requests.post(
    "http://127.0.0.1:8000/graph/run",
    json={
        "graph_id": graph_id,
        "initial_state": {"input_text": "Hello, world!"}
    }
).json()

print(result["final_state"])
```

---

## 📦 Project Structure

```
aiagent_project/
├── 📄 main.py                 # FastAPI REST API (47 lines)
├── ⚙️ graph_engine.py         # Core workflow engine (98 lines)
├── 🛠️ tools.py                # Tool registry (33 lines)
├── 🎯 example_workflow.py     # Demo script (156 lines)
├── 📋 example_graph.json      # Sample graph definition
├── 📦 pyproject.toml          # Dependencies
├── 📖 README.md               # This file
├── 🚀 QUICKSTART.md           # 5-minute setup guide
├── 📚 API_REFERENCE.md        # Complete API docs
├── 🏗️ ARCHITECTURE.md         # System design details
└── ✅ PROJECT_STATUS.md       # Implementation status
```

---

## 🤝 Contributing

This is an internship assignment project, but suggestions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - feel free to use this project for learning and development.

---

## 🙏 Acknowledgments

- **LangGraph** - For the excellent graph execution framework
- **FastAPI** - For the modern, fast web framework
- **Pydantic** - For data validation and settings management

---

## 📞 Support

- 📖 Check the [documentation](./QUICKSTART.md)
- 🐛 Report issues on GitHub
- 💬 Ask questions in discussions

---

<div align="center">

**Built with ❤️ for the AI Engineering Internship**

⭐ Star this repo if you find it helpful!

</div>
