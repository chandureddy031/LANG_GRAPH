from langgraph.graph import StateGraph, END
from typing import TypedDict
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

load_dotenv()

MODEL = "openai/gpt-oss-120b"
llm = ChatGroq(
    api_key="",
    model=MODEL,
    temperature=0
)


class LoanState(TypedDict):
    application: str
    credit_flag: str | None = None
    income_flag: str | None = None
    final_result: str | None = None


# ---------- NODE 1 ----------
def receive_application(state: LoanState):
    print("\nApplication Received")
    return state


# ---------- NODE 2 ----------
def check_credit(state: LoanState):

    print("Checking Credit via LLM")

    res = llm.invoke(
        f"""
Classify the applicant credit as ONLY one word:
good or bad

Application:
{state['application']}
"""
    )

    flag = res.content.strip().lower()

    print("Credit Decision →", flag)

    return {
        **state,
        "credit_flag": flag
    }


# ---------- ROUTER 1 ----------
def credit_router(state: LoanState):
    return state["credit_flag"]


# ---------- NODE 3 ----------
def verify_income(state: LoanState):

    print("Verifying Income via LLM")

    res = llm.invoke(
        f"""
Based on this loan application decide ONE:
approve
reject
review

Application:
{state['application']}
"""
    )

    flag = res.content.strip().lower()

    print("Income Decision →", flag)

    return {
        **state,
        "income_flag": flag
    }


# ---------- ROUTER 2 ----------
def income_router(state: LoanState):
    return state["income_flag"]


# ---------- FINAL NODES ----------
def approve_node(state: LoanState):
    print("Loan Approved")
    return {**state, "final_result": "APPROVED"}


def reject_node(state: LoanState):
    print("Loan Rejected")
    return {**state, "final_result": "REJECTED"}


def review_node(state: LoanState):
    print("Loan Needs Manual Review")
    return {**state, "final_result": "UNDER REVIEW"}


# ---------- GRAPH BUILD ----------
builder = StateGraph(LoanState)

builder.add_node("receive", receive_application)
builder.add_node("credit_check", check_credit)
builder.add_node("income_verify", verify_income)

builder.add_node("approve", approve_node)
builder.add_node("reject", reject_node)
builder.add_node("review", review_node)

builder.set_entry_point("receive")

builder.add_edge("receive", "credit_check")


builder.add_conditional_edges(
    "credit_check",
    credit_router,
    {
        "good": "income_verify",
        "bad": "reject"
    }
)

builder.add_conditional_edges(
    "income_verify",
    income_router,
    {
        "approve": "approve",
        "reject": "reject",
        "review": "review"
    }
)

builder.add_edge("approve", END)
builder.add_edge("reject", END)
builder.add_edge("review", END)

graph = builder.compile()


# ---------- RUN ----------
app = input("Enter Loan Application Description:\n")

result = graph.invoke({
    "application": app
})

print("\nFINAL RESULT →", result["final_result"])