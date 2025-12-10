# Agent Workflow Engine

A simplified LangGraph-style workflow engine built with FastAPI. This project demonstrates graph-based agent workflows with state management, conditional branching, and looping capabilities.

## Features

✅ **Graph Engine**: Define workflows as nodes and edges  
✅ **State Management**: Shared state flows through all nodes  
✅ **Conditional Branching**: Route based on state values  
✅ **Looping Support**: Repeat nodes until conditions are met  
✅ **Tool Registry**: Pre-registered Python functions as tools  
✅ **REST API**: Create and execute workflows via FastAPI  
✅ **Execution Logging**: Track each step of workflow execution  

## Project Structure

```
aiagent_project/
├── main.py              # FastAPI endpoints
├── graph_engine.py      # Core workflow engine
├── tools.py             # Tool registry (functions)
├── example_workflow.py  # Demo workflow script
├── example_graph.json   # Sample graph definition
├── pyproject.toml       # Dependencies
├── README.md            # This file
├── QUICKSTART.md        # Quick start guide
├── API_REFERENCE.md     # API documentation
└── ARCHITECTURE.md      # System design docs
```

## How to Run

See [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions.

**TL;DR:**
```bash
# Install and start
uv sync
uv run uvicorn main:app --reload

# Run example (in another terminal)
uv run python example_workflow.py
```

The API will be available at `http://127.0.0.1:8000`

Interactive docs: `http://127.0.0.1:8000/docs`

## API Endpoints

### 1. Create a Graph
**POST** `/graph/create`

Define a workflow with nodes, edges, and optional loops.

```json
{
  "nodes": [
    {"name": "split", "tool": "split_text"},
    {"name": "summarize", "tool": "generate_summaries"},
    {"name": "merge", "tool": "merge_summaries"},
    {"name": "refine", "tool": "refine_summary"}
  ],
  "edges": {
    "split": "summarize",
    "summarize": "merge",
    "merge": "refine"
  },
  "loops": [
    {
      "after": "refine",
      "condition": {"key": "length", "op": "gt", "value": 200},
      "back_to": "refine"
    }
  ],
  "start": "split"
}
```

**Response:**
```json
{
  "graph_id": "uuid-here"
}
```

### 2. Run a Graph
**POST** `/graph/run`

Execute a workflow with initial state.

```json
{
  "graph_id": "uuid-from-create",
  "initial_state": {
    "input_text": "Your long text here..."
  }
}
```

**Response:**
```json
{
  "final_state": {
    "input_text": "...",
    "chunks": [...],
    "summaries": [...],
    "merged_summary": "...",
    "final_summary": "...",
    "length": 180,
    "log": [...]
  },
  "execution_log": [
    {"node": "split", "tool": "split_text", "result": {...}},
    {"node": "summarize", "tool": "generate_summaries", "result": {...}}
  ]
}
```

### 3. Get Workflow State
**GET** `/graph/state/{run_id}`

Retrieve the current state of a workflow run.

## Example Workflow: Summarization + Refinement

The included example implements a text summarization pipeline:

1. **Split**: Divide text into chunks (500 chars each)
2. **Summarize**: Generate summaries for each chunk (first 100 chars + "...")
3. **Merge**: Combine all summaries into one
4. **Refine**: Reduce summary length by 30%

The engine supports loops (see graph_engine.py), but the example uses a simple linear workflow for clarity.

Run the example:
```bash
uv run python example_workflow.py
```

## What the Engine Supports

### Nodes
- Each node wraps a tool (Python function)
- Nodes receive and modify shared state
- Automatic execution logging

### Edges
- **Linear**: Direct node-to-node connections
- **Conditional**: Branch based on state values
- **Loops**: Repeat nodes until conditions are met

### State
- Dictionary-based state management
- State flows through all nodes
- Each node can read/write any state key

### Tools
- Pre-registered Python functions
- Simple dict → dict interface
- Easy to extend with new tools

### Branching & Looping
- Conditional routing: `if state[key] > value → route_a else route_b`
- Operators: `gt` (greater than), `lt` (less than)
- Loop back to any previous node

## Architecture Decisions

### Why LangGraph?
Used LangGraph as the underlying graph execution engine for:
- Proven state management
- Built-in checkpointing
- Clean graph abstraction

### State Design
- Simple dict-based state for flexibility
- Could be upgraded to Pydantic models for validation
- Log stored in state for execution tracking

### Storage
- In-memory storage for simplicity
- Easy to swap for SQLite/Postgres
- Checkpointer enables state persistence

## What I'd Improve With More Time

### High Priority
1. **Async Execution**: Make all node functions async for better performance
2. **WebSocket Streaming**: Real-time step-by-step execution updates
3. **Persistent Storage**: SQLite/Postgres for graphs and runs
4. **Error Handling**: Better error recovery and retry logic
5. **Tool Registration API**: Dynamic tool registration via endpoint

### Medium Priority
6. **Background Tasks**: Long-running workflows with Celery/FastAPI BackgroundTasks
7. **State Validation**: Pydantic models for type-safe state
8. **Graph Visualization**: Generate workflow diagrams
9. **Metrics & Monitoring**: Execution time, success rates
10. **Authentication**: API key or JWT-based auth

### Nice to Have
11. **Parallel Execution**: Run independent nodes concurrently
12. **Subgraphs**: Nest workflows within workflows
13. **Human-in-the-Loop**: Pause for user input
14. **Version Control**: Track graph definition changes
15. **Testing Suite**: Comprehensive unit and integration tests

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[API_REFERENCE.md](API_REFERENCE.md)** - Complete API documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and architecture
- **Interactive Docs** - Visit `/docs` when server is running

## Dependencies

- **FastAPI**: REST API framework
- **LangGraph**: Graph execution engine
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

## License

MIT
