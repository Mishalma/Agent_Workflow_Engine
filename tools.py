# tools.py
def split_text(state: dict) -> dict:
    text = state.get('input_text', '')
    chunk_size = 500
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return {'chunks': chunks}

def generate_summaries(state: dict) -> dict:
    chunks = state.get('chunks', [])
    summaries = [chunk[:100] + '...' for chunk in chunks if chunk.strip()]
    return {'summaries': summaries}

def merge_summaries(state: dict) -> dict:
    summaries = state.get('summaries', [])
    merged = ' '.join(summaries)
    return {'merged_summary': merged}

def refine_summary(state: dict) -> dict:
    merged = state.get('merged_summary', '')
    if not merged:
        return {'final_summary': '', 'length': 0}
    new_length = int(len(merged) * 0.9)  # Truncate to 90%
    refined = merged[:new_length]
    return {'final_summary': refined, 'length': len(refined)}

tools = {
    'split_text': split_text,
    'generate_summaries': generate_summaries,
    'merge_summaries': merge_summaries,
    'refine_summary': refine_summary,
}
