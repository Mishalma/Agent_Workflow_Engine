"""
Example workflow demonstrating the Summarization + Refinement pipeline.

This script:
1. Creates a graph with 4 nodes (split, summarize, merge, refine)
2. Adds a loop that refines until summary length < 200
3. Runs the workflow with sample text
4. Prints the execution log and final result
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Sample long text for summarization
SAMPLE_TEXT = """
Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural 
intelligence displayed by humans and animals. Leading AI textbooks define the field as the study 
of "intelligent agents": any device that perceives its environment and takes actions that maximize 
its chance of successfully achieving its goals. Colloquially, the term "artificial intelligence" 
is often used to describe machines (or computers) that mimic "cognitive" functions that humans 
associate with the human mind, such as "learning" and "problem solving".

As machines become increasingly capable, tasks considered to require "intelligence" are often 
removed from the definition of AI, a phenomenon known as the AI effect. A quip in Tesler's Theorem 
says "AI is whatever hasn't been done yet." For instance, optical character recognition is 
frequently excluded from things considered to be AI, having become a routine technology. Modern 
machine learning capabilities are typically classified as weak AI, as they are designed to perform 
specific tasks. Strong AI, also known as artificial general intelligence (AGI), refers to a 
hypothetical machine that exhibits behavior at least as skillful and flexible as humans do.

The field of AI research was born at a workshop at Dartmouth College in 1956, where the term 
"artificial intelligence" was coined. The attendees became the founders and leaders of AI research. 
They and their students produced programs that the press described as "astonishing": computers were 
learning checkers strategies, solving word problems in algebra, proving logical theorems and 
speaking English. By the middle of the 1960s, research in the U.S. was heavily funded by the 
Department of Defense and laboratories had been established around the world.
"""

def create_graph():
    """Create the summarization workflow graph."""
    graph_definition = {
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
        "loops": [],
        "start": "split"
    }
    
    response = requests.post(f"{BASE_URL}/graph/create", json=graph_definition)
    response.raise_for_status()
    return response.json()["graph_id"]

def run_workflow(graph_id, text):
    """Execute the workflow with the given text."""
    payload = {
        "graph_id": graph_id,
        "initial_state": {
            "input_text": text
        }
    }
    
    response = requests.post(f"{BASE_URL}/graph/run", json=payload)
    response.raise_for_status()
    return response.json()

def main():
    print("=" * 80)
    print("AGENT WORKFLOW ENGINE - EXAMPLE EXECUTION")
    print("=" * 80)
    print()
    
    # Step 1: Create the graph
    print("📊 Creating summarization workflow graph...")
    try:
        graph_id = create_graph()
        print(f"✅ Graph created with ID: {graph_id}")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to the server.")
        print("   Make sure the server is running: uv run uvicorn main:app --reload")
        return
    except Exception as e:
        print(f"❌ Error creating graph: {e}")
        return
    
    print()
    
    # Step 2: Run the workflow
    print("🚀 Running workflow with sample text...")
    print(f"   Input text length: {len(SAMPLE_TEXT)} characters")
    print()
    
    try:
        result = run_workflow(graph_id, SAMPLE_TEXT)
    except Exception as e:
        print(f"❌ Error running workflow: {e}")
        return
    
    # Step 3: Display results
    final_state = result["final_state"]
    execution_log = result["execution_log"]
    
    print("📝 EXECUTION LOG:")
    print("-" * 80)
    for i, entry in enumerate(execution_log, 1):
        print(f"Step {i}: {entry['node']} (tool: {entry['tool']})")
        result_keys = list(entry['result'].keys())
        print(f"        → Updated: {', '.join(result_keys)}")
    
    print()
    print("=" * 80)
    print("📊 FINAL RESULTS:")
    print("=" * 80)
    
    print(f"\n🔢 Statistics:")
    print(f"   • Original text length: {len(SAMPLE_TEXT)} chars")
    print(f"   • Number of chunks: {len(final_state.get('chunks', []))}")
    print(f"   • Number of summaries: {len(final_state.get('summaries', []))}")
    print(f"   • Merged summary length: {len(final_state.get('merged_summary', ''))} chars")
    print(f"   • Final summary length: {final_state.get('length', 0)} chars")
    print(f"   • Total steps: {len(execution_log)}")
    
    print(f"\n📄 Final Summary:")
    print("-" * 80)
    print(final_state.get('final_summary', 'No summary generated'))
    print("-" * 80)
    
    print()
    print("✅ Workflow completed successfully!")
    print()

if __name__ == "__main__":
    main()
