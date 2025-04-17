from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool

llama_3 = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)


@tool
def generate_unit_tests_tool(api_endpoints):
    """
        Generate pytest based unit testcases for all api routes

    Args:
        api_endpoints: list of all api routes

    Returns:
        str: pytest based unit testcases
    """

    prompt = PromptTemplate.from_template(
        """
        Generate pytest-based test cases for the following endpoints:
        {api_endpoints}

        Ensure that the tests cover:
        - Valid input
        - Edge cases (eg. invalid input, missing fields)
        - Proper Error handling and status codes
        - To import the fastapi app, use path project_root/app/main
        Note: Provide only testcases as the output. Remove all quotes which wrap the test cases.
        """
    )

    message = prompt.format(api_endpoints = api_endpoints)
    response = llama_3.invoke(message)
    with open("project_root/tests/test_generated_api.py", "w") as f:
        f.write(response.content)
    return response.content


llama_3_with_tools = llama_3.bind_tools([generate_unit_tests_tool])


# Node
def generate_unit_tests(state):
    return {"messages": [llama_3_with_tools.invoke(state["messages"])]}