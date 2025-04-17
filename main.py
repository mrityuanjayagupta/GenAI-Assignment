from langgraph.graph import StateGraph, START, END
from groq import Groq


class GraphState(dict):
    pass


def extract_srs_data(state):
    srs_content = state.get("srs_document", "")

    if not srs_content:
        raise ValueError("SRS Document is empty or missing.")
    
    function_requirements = extract_functional_requirements(srs_content)

    state["functional_requirements"] = function_requirements
    return state


def extract_functional_requirements(srs_content):
    prompt = f"""
    Analyze the following Software Requirements Specification (SRS) Document and extract the following:
    1. API Endpoints (GET, POST, PUT, PATCH, DELETE) and their parameters.
    2. Backend Logic (business rules, computations)
    3. Database Schema (tables, relationships, constraints)
    4. Authentication and Authorization requirements (roles, permisssions).

    Here is the SRS document: 
    {srs_content}

    Please provide the extracted information in structured format
    """
    client = Groq()
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )
    print(completion.choices[0].message.content)


graph_builder = StateGraph(GraphState)
graph_builder.add_node("extract_requirements", extract_functional_requirements)
graph_builder.add_edge(START, "extract_requirements")
graph_builder.add_edge("extract_requirements", END)

graph = graph_builder.compile()


initial_state = GraphState({
    "srs_document": """This SRS document includes:
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
})

final_state = graph.invoke(initial_state)
print(final_state)
