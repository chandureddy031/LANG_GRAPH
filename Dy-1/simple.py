from typing import TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph , END

MODEL = ""
GROQ_API_KEY=""

llm= ChatGroq(
        api_key = GROQ_API_KEY,
        model = MODEL,
        temperature = 0.5,
    )

class GraphState(TypedDict):
    
    input : str
    output : str
    
def get_txt(state :GraphState):
    user_inp = input("Enter the text : ")
    state["input"] = user_inp
    return {
        **state,
        "input": user_inp
    }

def clean_text(state:GraphState):
    txt = state["input"]
    txt = txt.strip()
    return {
        **state,
        "input": txt
    }

def upper_case(state:GraphState):
    txt = state["input"]
    txt = txt.upper()
    return {
        **state,
        "input": txt
    }
def summarize(state : GraphState):
    txt = state["input"]
    r = llm.invoke(f"Summarize this text concisely:{txt}")
    return {
        **state,
        "output": r.content
    }
    
    
graph = StateGraph(GraphState)

graph.add_node("get", get_txt)
graph.add_node("clean", clean_text)
graph.add_node("upper", upper_case)
graph.add_node("sum", summarize)

graph.set_entry_point("get")

graph.add_edge("get", "clean")
graph.add_edge("clean", "upper")
graph.add_edge("upper", "sum")
graph.add_edge("sum", END)

app = graph.compile()
res = app.invoke({
    "input" : "",
    "output" : ""
})
print(res["output"])
print(res["input"])