# graph_engine.py
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import Dict, Any
import uuid
from tools import tools

# Global storage
graphs: Dict[str, Any] = {}
checkpointer = MemorySaver()

def build_graph(graph_def: Dict[str, Any]) -> StateGraph:
    # Define state schema with proper reducer
    from typing import Annotated, TypedDict
    from operator import add
    
    class WorkflowState(TypedDict, total=False):
        input_text: str
        chunks: list
        summaries: list
        merged_summary: str
        final_summary: str
        length: int
        log: Annotated[list, add]
    
    builder = StateGraph(WorkflowState)

    # Map node names to tools
    node_tools = {node['name']: node['tool'] for node in graph_def['nodes']}

    # Add nodes (wrap tools with logging)
    for node_def in graph_def['nodes']:
        tool_name = node_def['tool']
        node_name = node_def['name']

        def create_node(tn=tool_name, nn=node_name):
            def node_func(state: Dict[str, Any]) -> Dict[str, Any]:
                # Run tool with full state
                tool_result = tools[tn](state)
                # Log entry
                entry = {'node': nn, 'tool': tn, 'result': tool_result}
                # Return updates (log will be appended, others will be replaced)
                return {**tool_result, 'log': [entry]}

            return node_func

        builder.add_node(node_name, create_node())

    # Linear edges
    builder.add_edge(START, graph_def['start'])
    for from_node, to_node in graph_def['edges'].items():
        builder.add_edge(from_node, to_node)

    # Conditional loops (branching)
    for loop_def in graph_def.get('loops', []):
        after = loop_def['after']
        cond = loop_def['condition']
        key = cond['key']
        op = cond['op']
        value = cond['value']
        back_to = loop_def['back_to']

        def create_condition(k=key, o=op, v=value):
            def condition(state: Dict[str, Any]) -> str:
                val = state.get(k, 0)
                if (o == 'gt' and val > v) or (o == 'lt' and val < v):
                    return 'loop'
                return 'end'

            return condition

        cond_func = create_condition()
        builder.add_conditional_edges(
            after,
            cond_func,
            {'loop': back_to, 'end': END}
        )

    return builder

def create_graph(graph_def: Dict[str, Any]) -> str:
    graph_id = str(uuid.uuid4())
    builder = build_graph(graph_def)
    # Compile with higher recursion limit for loops
    compiled = builder.compile(checkpointer=checkpointer)
    graphs[graph_id] = compiled
    return graph_id

def run_graph(graph_id: str, initial_state: Dict[str, Any], run_id: str) -> Dict[str, Any]:
    if graph_id not in graphs:
        raise ValueError(f"Graph {graph_id} not found")
    config = {"configurable": {"thread_id": run_id}, "recursion_limit": 100}
    initial = initial_state.copy()
    # Don't pre-initialize log, let the reducer handle it
    result = graphs[graph_id].invoke(initial, config)
    # Convert result to plain dict for JSON serialization
    return dict(result)

def get_state(run_id: str) -> Dict[str, Any]:
    config = {"configurable": {"thread_id": run_id}}
    checkpoint = checkpointer.get(config)
    if checkpoint is None:
        raise ValueError(f"Run {run_id} not found")
    return checkpoint.state  # Current state dict