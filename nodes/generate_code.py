import json
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool

llama_3 = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)


@tool
def generate_code_tool(api_endpoints):
    """
        Generate fastapi code for all api routes

    Args:
        api_endpoints: list of all api routes

    Returns:
        str: string fastapi code for all api routes without backticks
    """ 
    
    prompt = PromptTemplate.from_template(
        """
        Given the following api routes, generate FastAPI code for each route file
        For each endpoint, create:
        - A route file inside routes/
        - A pydantic + SQLAlchemy model inside models/
        - A Service file for business logic inside services/
        
        In every module directory (models/, services/, routes/, api/, and app/), include an __init__.py file that imports all necessary classes and functions used outside the module.
        Each __init__.py should explicitly import (i.e., from .file import ClassName) all relevant classes/functions defined in sibling files of that module that are used outside of that module.
        Note: The output should be a JSON String with the file name as key and the code as the value
        Write the code in single line string using \\n for changing the line
        Format the output like this in the same sequence:
        {{
            "project_root/app/main.py": "generated code for main.py where our app is initialized in FastAPI",
            "project_root/app/api/routes/filename": "generated code for the route file",
            "project_root/app/models/filename": "generated code for the models file"
            "project_root/app/services/filename": "generated code for services file",
            "project_root/app/api/routes/__init__.py": "generated code for __init__.py with all route imports",
            "project_root/app/api/__init__.py": "generated code for api/__init__.py importing routes",  
            "project_root/app/models/__init__.py": "generated code for models/__init__.py importing all models",
            "project_root/app/services/__init__.py": "generated code for services/__init__.py importing all services",  
            "project_root/app/__init__.py": "generated code for app/__init__.py importing api, models, and services",
        }}
        
        API Routes are as follows:
        {api_endpoints}

        Ensure that the code follows best practices for fastapi projects.
        Note: STRICTLY DO NOT USE BACKTICKS AROUND THE OUTPUT
        """
    )
    message = prompt.format(api_endpoints = api_endpoints)
    response = llama_3.invoke(message)
    json_response = json.loads(response.content)
    for file_path, code in json_response.items():
        with open(file_path, "w") as f:
            f.write(code)
    return response.content


llama_3_with_tools = llama_3.bind_tools([generate_code_tool])


# Node
def generate_code(state):
    return {"messages": [llama_3_with_tools.invoke(state["messages"])]}