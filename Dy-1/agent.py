from dotenv import load_dotenv 
from state import STATE
import os
from pathlib import Path
from langchain_groq import ChatGroq
load_dotenv(Path(__file__).resolve().parent.parent / ".env")



llm= ChatGroq(
        api_key = GROQ_API_KEY,
        model = MODEL,
        temperature = 0.5,
    )

def user_inp(state: STATE):
    inp = input("Enter txt : ")
    
    return {
        **state,
        "input": inp
    }

def ag1(state: STATE):
    txt = state["input"]
    out = llm.invoke(txt).content
    
    return {
        **state,
        "output": out
    }
    
    
    
    