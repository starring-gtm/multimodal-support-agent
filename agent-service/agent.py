import os
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langgraph.graph import StateGraph, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from tools import search_knowledge_base, escalate_to_team, classify_image, transcribe_voice

load_dotenv()

tools = [search_knowledge_base, escalate_to_team, classify_image, transcribe_voice]

llm = ChatNVIDIA(
    model="nvidia/nemotron-3.5-lightning-30b-a3b",
    api_key=os.getenv("NVIDIA_API_KEY"),
    max_completion_tokens=2048,
)
llm_with_tools = llm.bind_tools(tools)

SYSTEM_PROMPT = """You are a support agent for NovaLink Fiber, an internet service provider.
A customer has submitted a support ticket. Your job is to diagnose their issue and either
resolve it or escalate it to the right team.

If the ticket includes an audio file path, call transcribe_voice first to understand what
the customer said, and treat that transcription as their issue description.

If the ticket includes an image path, call classify_image to understand what it shows,
and use those details (e.g. light colors, visible damage) when searching the knowledge base.

Then take exactly ONE of these two actions:

1. RESOLVE: If the knowledge base gives troubleshooting steps the customer can follow
   themselves, give them those steps directly as your final answer.

2. ESCALATE: If resolving requires account-specific data you don't have access to,
   OR the knowledge base has no relevant match, OR the issue explicitly requires
   human/technician intervention — call the escalate_to_team tool immediately.
   Do not ask the customer clarifying questions first.

Do not deliberate at length. Process any attachments once, search once, then decide and act.
"""

# 3. The "agent" node: calls the LLM with the current conversation state
def agent_node(state: MessagesState):
    messages = state["messages"]
    # prepend system prompt only if not already there
    if not any(m.type == "system" for m in messages):
        from langchain_core.messages import SystemMessage
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# 4. Build the graph
graph_builder = StateGraph(MessagesState)
graph_builder.add_node("agent", agent_node)
graph_builder.add_node("tools", ToolNode(tools))

graph_builder.set_entry_point("agent")
graph_builder.add_conditional_edges("agent", tools_condition)  # routes to "tools" or END
graph_builder.add_edge("tools", "agent")  # after tool runs, go back to agent to reason again

graph = graph_builder.compile()

# if __name__ == "__main__":
#     from langchain_core.messages import HumanMessage

#     result = graph.invoke({
#         "messages": [HumanMessage(content="Ticket #42: I was charged twice this month and I don't understand why, my invoice doesn't show the extra charge at all.")]
#     })
#     for m in result["messages"]:
#         print(f"--- {m.type} ---")
#         if hasattr(m, "tool_calls") and m.tool_calls:
#             for tc in m.tool_calls:
#                 print(f"  Tool call: {tc['name']}({tc['args']})")
#         print(m.content)
#         print()

# if __name__ == "__main__":
#     print(classify_image.invoke({"image_path": "/Users/gautamchaudhary/Documents/Projects/Multimodal support agent/agent-service/images/all-lights-on-1024x538.jpg"}))

if __name__ == "__main__":
    from langchain_core.messages import HumanMessage

    result = graph.invoke({
        "messages": [HumanMessage(
            content="Ticket #77: My internet feels slow lately. I attached a photo of my router. Image path: /Users/gautamchaudhary/Documents/Projects/Multimodal support agent/agent-service/images/all-lights-on-1024x538.jpg"
        )]
    })

    for m in result["messages"]:
        print(f"--- {m.type} ---")
        if hasattr(m, "tool_calls") and m.tool_calls:
            for tc in m.tool_calls:
                print(f"  Tool call: {tc['name']}({tc['args']})")
        print(m.content)
        print()