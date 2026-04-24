from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from typing import TypedDict, Optional
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os, json
load_dotenv()
llm= ChatGroq(model="qwen/qwen3-32b", temperature=0, max_tokens=None, reasoning_format="hidden", timeout=None,max_retries=2)

class State(TypedDict):
    skills: list
    year: int
    domain: str
    text: str
    role_type:Optional[str]=None
    queries: Optional[list]=[]

def role_node(state: State):
    role=None
    year=state["year"]
    if not year: 
        role = "internship"
    elif year<=3:
        role = "internship"
    elif year==4:
        role="internship+full-time"
    else:
        role="full-time"
    return {"role_type": role}

def query_node(state: State):
    queries=[]
    skills=", ".join(state["skills"])
    domain=state["domain"]
    role_type=state["role_type"]
    prompt=f""" 
        Your job is to generate optimize job search queries based on the given parameters: 
        1. skills: {skills}
        2. domain: {domain}
        3. role_type: {role_type}
Rules: Generate 5 optimized job search queries. Return ONLY a JSON List
    """
    res=llm.invoke(prompt)
    try:
        queries= json.loads(res.content)
    except:
        queries=[res.content]
    return {"queries": queries}

graph=StateGraph(State)
graph.add_node("role", role_node)
graph.add_node("query", query_node)
graph.set_entry_point("role")
graph.set_finish_point("query")
graph.add_edge("role", "query")
graph.add_edge("query", END)
lang_app=graph.compile()
