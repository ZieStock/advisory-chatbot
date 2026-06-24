from langgraph.graph import StateGraph, END
from chatbot.agent_state import AgentState

def BuildAgent(llm):
    workflow = StateGraph(AgentState)
    def agent(state):
        res = llm.invoke(state['messages'])
        return {"messages": [res]}
    workflow.add_node("agent", agent)
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", END)
    return workflow.compile()