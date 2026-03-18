from langgraph.graph import StateGraph, END
from typing import TypedDict

class GraphState(TypedDict):
    user: str
    route: str
    response: str

def router_node(state: GraphState):

    msg = state['user'].lower()

    if "error" in msg or "code" in msg or "bug" in msg:
        route = "technical"

    elif "payment" in msg or "refund" in msg or "invoice" in msg:
        route = "billing"

    else:
        route = "general"

    print(f"Router decided route --> {route}")

    return {
        **state,
        "route": route
    }

def technical_node(state: GraphState):
    print("Technical node executed")

    return {
        **state,
        "response": "Technical team will solve your issue"
    }

def billing_node(state: GraphState):
    print("Billing node executed")

    return {
        **state,
        "response": "Billing Team Will Check Your Payment"
    }

def general_node(state: GraphState):
    print("General node executed")

    return {
        **state,
        "response": "Customer support will assist you"
    }

def route_decider(state: GraphState):
    return state["route"]


builder = StateGraph(GraphState)

builder.add_node("router_node", router_node)
builder.add_node("technical", technical_node)
builder.add_node("billing", billing_node)
builder.add_node("general", general_node)

builder.set_entry_point("router_node")

builder.add_conditional_edges(
    "router_node",
    route_decider,
    {
        "technical": "technical",
        "billing": "billing",
        "general": "general"
    }
)

builder.add_edge("technical", END)
builder.add_edge("billing", END)
builder.add_edge("general", END)

graph = builder.compile()

res = graph.invoke({
    "user": "My Payment failed yesterday"
})

print(res)