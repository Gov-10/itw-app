from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from typing import TypedDict
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()
llm= ChatGroq(model="qwen/qwen3-32b", temperature=0, max_tokens=None, reasoning_format="hidden", timeout=None,max_retries=2)

class State(TypedDict):
    skills: list
    year: int
    domain: str
    text: str
    role_type:str
    queries: list

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
    pass
#Iska code kal tak likh dunga
