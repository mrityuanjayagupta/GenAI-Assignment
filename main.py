from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from nodes.extract_srs_data import extract_srs_data, extract_functional_requirements




class GraphState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]




# Build Graph
builder = StateGraph(MessagesState)

builder.add_node("extract_srs_data", extract_srs_data)
builder.add_node("tools", ToolNode([extract_functional_requirements]))

builder.add_edge(START, "extract_srs_data")
builder.add_conditional_edges("extract_srs_data", tools_condition)
builder.add_edge("tools", END)

graph = builder.compile()


messages = [HumanMessage(content = '''
    """This SRS document includes:
    1. API Endpoints: 
        - GET /users
        - POST /users
        - PUT /users/{id}

    2. Backend Logic: 
        - Users must be unique
        - Compute total order value

    3. Database Schema
        - Users, tables, Orders table
        - One to many relationship between Users and Orders

    4. Authentivation Requirements: 
        - Role-based authentication (Admin, User)    
        
    """
    '''
)]

final_state = graph.invoke({"messages": messages})
for m in final_state["messages"]:
    m.pretty_print()
