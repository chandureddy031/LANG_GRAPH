from langchain_groq import ChatGroq
from langgraph.graph import StateGraph , END
import os
from typing import List , TypedDict
from dotenv import load_dotenv , find_dotenv
load_dotenv(find_dotenv())
from state import STATE
from agent import ag1,user_inp

graph = StateGraph(STATE)

graph.add_node("st",user_inp)
graph.add_node("ans",ag1)
graph.set_entry_point("st")

graph.add_edge("st" , "ans")
graph.add_edge("ans",END)

app = graph.compile()
res = app.invoke({
    "input": "",
    "output": ""
})
print(res)