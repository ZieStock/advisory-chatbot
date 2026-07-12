from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from chatbot.agent_state import AgentState

def BuildAgent(llm, tools):
    workflow = StateGraph(AgentState)
    def agent(state):
        res = llm.invoke(state['messages'])
        return {"messages": [res]}
    tool_node = ToolNode(tools)
    workflow.add_node("tools", tool_node)
    workflow.add_node("agent", agent)
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
    workflow.add_edge("tools", "agent")
    return workflow.compile()