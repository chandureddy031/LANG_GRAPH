from langgraph.graph import StateGraph,END
from typing import List , TypedDict , Annotated
import operator
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()


MODEL = ""
GROQ_API_KEY=""

llm= ChatGroq(
        api_key = GROQ_API_KEY,
        model = MODEL,
        temperature = 0.5,
    )

class ResearchState(TypedDict):
    topic : str
    findings : Annotated[List[str],operator.add]
    
def search_node(state : ResearchState):
    print("Research-Startred")
    
    return {
        "findings" : [
            f" Raw results  {state['topic']}"
        ]
    }

def analyze_node(state: ResearchState):

    print("Analyze node executed")
    res = llm.invoke(f'get the analyzed data ain a line {state["topic"]}')
    return {
        "findings": [
            res.content
        ]
    }

def summarize_node(state: ResearchState):

    print("Summarize node executed")
    res = llm.invoke(f"Summarizr the Condensed insights prepared {state['topic']}")
    return {
        "findings": [
            res.content
        ]
    }
def compile_report_node(state: ResearchState):

    print("Compile report node executed")
    res = llm.invoke(f"compile the report based on the previous results {state['findings']}")
    return {
        "findings": [
            res.content
        ]
    }
    
builder = StateGraph(ResearchState)

builder.add_node("search", search_node)
builder.add_node("analyze", analyze_node)
builder.add_node("summarize", summarize_node)
builder.add_node("compile", compile_report_node)

builder.set_entry_point("search")

builder.add_edge("search", "analyze")
builder.add_edge("analyze", "summarize")
builder.add_edge("summarize", "compile")
builder.add_edge("compile", END)

graph = builder.compile()

inp = input("Enter the topic : ")
result = graph.invoke({
    "topic": inp,
    "findings": []
})

print(result)