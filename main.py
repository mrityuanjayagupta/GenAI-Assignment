from docx import Document
from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage, HumanMessage
from groq import Groq
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from nodes.create_zip_node import create_zip
from nodes.extract_srs_data import extract_srs_data, extract_functional_requirements
from nodes.generate_code import generate_code, generate_code_tool
from nodes.generate_project_structure import (
    generate_project_structure,
    generate_project_structure_tool,
)
from nodes.generate_unit_tests import generate_unit_tests, generate_unit_tests_tool
from nodes.run_tests import run_tests

import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
os.environ["LANGCHAIN_API_KEY"] = str(os.getenv("LANGCHAIN_API_KEY"))
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "genai-assignment"


class GraphState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


def run_code_generator(srs_content):

    # Build Graph
    builder = StateGraph(MessagesState)

    builder.add_node("extract_srs_data", extract_srs_data)
    builder.add_node("tools", ToolNode([extract_functional_requirements]))
    builder.add_node("generate_project_structure", generate_project_structure)
    builder.add_node(
        "generate_project_structure_tool", ToolNode([generate_project_structure_tool])
    )
    builder.add_node("generate_unit_tests", generate_unit_tests)
    builder.add_node("generate_unit_tests_tool", ToolNode([generate_unit_tests_tool]))
    builder.add_node("generate_code", generate_code)
    builder.add_node("generate_code_tool", ToolNode([generate_code_tool]))
    builder.add_node("run_tests", run_tests)
    builder.add_node("create_zip", create_zip)


    builder.add_edge(START, "extract_srs_data")
    builder.add_edge("extract_srs_data", "tools")
    builder.add_edge("tools", "generate_project_structure")
    builder.add_edge("generate_project_structure", "generate_project_structure_tool")
    builder.add_edge("generate_project_structure_tool", "generate_unit_tests")
    builder.add_edge("generate_unit_tests", "generate_unit_tests_tool")
    builder.add_edge("generate_unit_tests_tool", "generate_code")
    builder.add_edge("generate_code", "generate_code_tool")
    builder.add_edge("generate_code_tool", "run_tests")
    builder.add_edge("run_tests", "create_zip")
    builder.add_edge("extract_srs_data", END)


    graph = builder.compile()
        


    llama_3 = Groq()
    chat_completion = llama_3.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": """Extract the following key information from the following SRS Document:
                1. API Endpoints (GET, POST, PUT, PATCH, DELETE) and their parameters.
                2. Backend Logic (business rules, computations)
                3. Database Schema (tables, relationships, constraints)
                4. Authentication and Authorization requirements (roles, permisssions).

                Summarize and Structure the above information in a clear and concise manner for each component.
                Here is the SRS Document: {srs_content}
                """.format(
                    srs_content=srs_content
                ),
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0,
    )

    messages = [HumanMessage(content=chat_completion.choices[0].message.content)]

    final_state = graph.invoke({"messages": messages})
    for m in final_state["messages"]:
        m.pretty_print()
