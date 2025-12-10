# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uuid
from graph_engine import create_graph, run_graph, get_state

app = FastAPI(title="Summarization Agent Workflow")

class RunInput(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]

class GraphCreate(BaseModel):
    nodes: list[Dict[str, Any]]
    edges: Dict[str, str]
    loops: list[Dict[str, Any]]
    start: str

@app.post("/graph/create", response_model=Dict[str, str])
def api_create_graph(graph_def: GraphCreate):
    try:
        graph_id = create_graph(graph_def.dict())
        return {"graph_id": graph_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/graph/run", response_model=Dict[str, Any])
def api_run_graph(input: RunInput):
    try:
        run_id = str(uuid.uuid4())
        final_state = run_graph(input.graph_id, input.initial_state, run_id)
        return {
            "final_state": final_state,
            "execution_log": final_state.get('log', [])
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/graph/state/{run_id}", response_model=Dict[str, Any])
def api_get_state(run_id: str):
    try:
        return get_state(run_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
