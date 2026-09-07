from .llm import ask

def edit_instruction(instruction, current_context):
    system = """You are a conversational editing agent. Given an existing artifact context and a requested change,
return a concise edit plan. Preserve structure, tone, and formatting unless the user explicitly asks to change them."""
    return ask(system, f"Existing context:\n{current_context}\n\nRequested edit:\n{instruction}")
