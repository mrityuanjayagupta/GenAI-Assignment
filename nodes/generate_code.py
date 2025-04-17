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
        str: json string fastapi code for all api routes
    """

    routes = {}
    for endpoint in api_endpoints:
        route_name = endpoint.split()[1].strip('/').replace("/", "_")
        routes[route_name] = f"{route_name}.py"
        
    prompt = PromptTemplate.from_template(
        """
        Given the following api routes, generate FastAPI code for each route file
        For each endpoint, create:
        - A route file inside routes/
        - A pydantic + SQLAlchemy model inside models/
        - A Service file for business logic inside services/
        
        Note: The output should be a JSON String will the file name as key and the code as the value
        Write the code in single line string using \\n for changing the line
        Format the output like this:
        {{
            "project_root/app/api/routes/filename": "generated code for the route file",
            "project_root/app/models/filename": "generated code for the models file"
            "project_root/app/services/filename": "generated code for services file"
        }}
        
        API Routes are as follows:
        {api_endpoints}

        Ensure that the code follows best practices for fastapi projects.
        Note: Do not use backticks for the output.
        """
    )

    message = prompt.format(api_endpoints = api_endpoints)
    response = llama_3.invoke(message)
    print(response.content)
    json_response = json.loads(response.content)
    for file_path, code in json_response.items():
        with open(file_path, "w") as f:
            f.write(code)
    return response.content


llama_3_with_tools = llama_3.bind_tools([generate_code_tool])


# Node
def generate_code(state):
    return {"messages": [llama_3_with_tools.invoke(state["messages"])]}