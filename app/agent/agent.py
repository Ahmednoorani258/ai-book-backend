from agents import Agent, Runner
from .tools import rag_search
from .setupconfig import config

agent = Agent(
    name="BookAssistant",
    instructions=(
        "Greet the user and assist them with their questions about the book."
        "You answer questions ONLY using context from tools. "
        "Call rag_search when user asks normal questions. "
        # "Call use_selected_text when selected text is provided. "
        "Never hallucinate."
    ),
    tools=[rag_search]
)



async def answer(query: str):
    
    result = await Runner.run(agent, f"Use rag_search tool with query: {query}", run_config=config)
    context = result.final_output

    run = await Runner.run(agent, f"Answer the user using ONLY this context:\n{context}\n\nQuestion: {query}", run_config=config)
    return run.final_output
    # if selected_text:
        # Force agent to use the selected text tool
        # tool_input = {"selected_text": selected_text}
        # agent = await Runner.run(agent, f"Use selected_text tool with text: {selected_text}", run_config=config)
        # context = agent.final_output
    # else:
        # tool_input = {"query": query}
