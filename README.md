# Agent Workflow Engine

A simplified LangGraph-style workflow engine built with FastAPI. Define agent workflows as graphs with nodes, edges, conditional branching, and loops.

---

## How to Run

### Prerequisites
- Python 3.13+
- `uv` package manager (or pip)

### Installation & Startup

```bash
# Install dependencies
uv sync

# Start the server
uv run uvicorn main:app --reload
```

Server runs at: **http://127.0.0.1:8000**  
API docs at: **http://127.0.0.1:8000/docs**

### Run the Example

```bash
# In a new terminal
uv run python example_workflow.py
```

This executes a text summarization workflow: Split → Summarize → Merge → Refine

---

## What the Engine Supports

### Core Features

**Nodes**
- Each node wraps a Python function (tool)
- Nodes read and modify shared state
- Automatic execution logging

**State Management**
- Dictionary-based state flows through all nodes
- TypedDict schema with proper merging
- Checkpointing for state persistence

**Edges**
- Linear connections: `node_a → node_b`
- Define execution order

**Conditional Branching**
- Route based on state values
- Operators: `gt` (greater than), `lt` (less than)
- Example: if `length > 200`, loop back to refine

**Loops**
- Repeat nodes until conditions are met
- Recursion limit protection (default: 100)

**Tool Registry**
- Pre-registered Python functions
- Simple interface: `dict → dict`
- Included tools:
  - `split_text` - Split text into chunks
  - `generate_summaries` - Create summaries
  - `merge_summaries` - Combine summaries
  - `refine_summary` - Reduce length

### API Endpoints

**POST /graph/create**
- Input: Graph definition (nodes, edges, loops, start)
- Output: `graph_id`

**POST /graph/run**
- Input: `graph_id` + `initial_state`
- Output: `final_state` + `execution_log`

**GET /graph/state/{run_id}**
- Output: Current workflow state

### Example Graph Definition

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

---

## What I Would Improve With More Time

### High Priority

**1. Async Execution**
- Convert all tool functions to async
- Non-blocking workflow execution
- Better performance for I/O-bound operations

**2. WebSocket Streaming**
- Real-time step-by-step execution updates
- Stream logs as workflow progresses
- Better UX for long-running workflows

**3. Persistent Storage**
- Replace in-memory storage with SQLite/Postgres
- Survive server restarts
- Query historical workflow runs

**4. Better Error Handling**
- Retry logic for transient failures
- Partial state recovery
- More descriptive error messages
- Structured error types

**5. Dynamic Tool Registration**
- API endpoint to register new tools
- Load tools from external modules
- Hot-reload tool definitions

### Medium Priority

**6. Background Task Processing**
- Use Celery or FastAPI BackgroundTasks
- Queue long-running workflows
- Return immediately with job ID

**7. State Validation**
- Pydantic models for state schema
- Type checking at runtime
- Better error messages for invalid state

**8. Graph Visualization**
- Generate workflow diagrams (Mermaid/GraphViz)
- Visual debugging of execution paths
- Export to PNG/SVG

**9. Metrics & Monitoring**
- Execution time per node
- Success/failure rates
- Resource usage tracking
- Integration with Prometheus/Grafana

**10. Authentication & Authorization**
- API key or JWT-based auth
- Per-user graph isolation
- Rate limiting

### Nice to Have

**11. Parallel Execution**
- Run independent nodes concurrently
- Automatic dependency detection
- Significant performance gains

**12. Subgraphs**
- Nest workflows within workflows
- Reusable workflow components
- Better modularity

**13. Human-in-the-Loop**
- Pause workflow for user input
- Approval gates
- Interactive debugging

**14. Version Control**
- Track graph definition changes
- Rollback to previous versions
- A/B testing different workflows

**15. Comprehensive Testing**
- Unit tests for all components
- Integration tests for workflows
- Load testing for scalability
- CI/CD pipeline

---

## Project Structure

```
aiagent_project/
├── main.py              # FastAPI endpoints
├── graph_engine.py      # Core workflow engine
├── tools.py             # Tool registry
├── example_workflow.py  # Demo script
├── example_graph.json   # Sample graph
└── pyproject.toml       # Dependencies
```

---

## Additional Documentation

- **QUICKSTART.md** - Detailed setup guide
- **API_REFERENCE.md** - Complete API documentation
- **ARCHITECTURE.md** - System design and technical details

---

Built with FastAPI, LangGraph, and Pydantic.
