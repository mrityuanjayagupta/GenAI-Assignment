from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool

llama_3 = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)


@tool
def extract_functional_requirements(srs_content):
    """
    Analyze the SRS Content and extract functional requirements from it

    Args:
        srs_content (str): srs text

    Returns:
        str: extracted functional requirements in structured format
    """

    prompt = PromptTemplate.from_template(
        """
        Strictly Analyze the following Software Requirements Specification (SRS) Document and extract the following:
        1. API Endpoints (GET, POST, PUT, PATCH, DELETE) and their parameters.
        2. Backend Logic (business rules, computations)
        3. Database Schema (tables, relationships, constraints)
        4. Authentication and Authorization requirements (roles, permisssions).

        Here is the SRS document: 
        {srs_content}

        Strictly provide the extracted information in json format as given below:
            routes: [list of all routes/apis - each route should be in json having request_type, request_url, paramters, headers and body],
            models: [list of all models - each model should be in json having table_name, relationships, constraints]
            dependencies: [list of all dependencies which are required to be installed]
            functionalities: [list of all key functionalities]

        Provide only json as the output. No extra text is required.
    """
    )

    message = prompt.format(srs_content=srs_content)
    response = llama_3.invoke(message)
    return response.content


llama_3_with_tools = llama_3.bind_tools([extract_functional_requirements])


# Node
def extract_srs_data(state):
    return {"messages": [llama_3_with_tools.invoke(state["messages"])]}
