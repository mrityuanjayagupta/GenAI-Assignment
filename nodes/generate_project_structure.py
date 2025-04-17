import os
import json
import subprocess
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool

llama_3 = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)


def create_folder_structure(dic):
    def one_directory(dic, path):
        for name, info in dic.items():
            next_path = path + "/" + name
            if isinstance(info, dict):
                if next_path[0] == "/":
                    next_path = next_path[1:]
                os.mkdir(next_path)
                one_directory(info, next_path)

    one_directory(dic, "")


@tool
def generate_project_structure_tool():
    """
    Analyze the extracted details from SRS and return file names of models and routes.

    Returns:
        string with routes and model file names
    """

    prompt = PromptTemplate.from_template(
        """
        Analyze the extracted details from SRS and return file names of models and routes.
        The folder structure is supposed to be in the below format:
        project_root/
        │── app/
        │   ├── api/
        │   │   ├── routes/
        │   │   │   └── __init__.py
        │   ├── models/
        │   │   └── __init__.py
        │   ├── services/
        │   ├── database.py
        │   ├── main.py
        │── tests/
        │── Dockerfile
        │── requirements.txt
        │── .env
        │── README.md


        Strictly provide the extracted information in json string format as given below:
        folder_structure: dictionary containing only the folder structure (no files)
        dependencies: [list of dependencies like fastapi, pydantic, sqlAlchemy, pytest] 
        Strictly include all the python libraries which needs to be installed for development as well as testing]
        Note: Provide only string as the output. No extra text is required.
        Do not use backticks for the output.
    """
    )
    message = prompt.format()
    response = llama_3.invoke(message)
    json_response = response.content
    json_response = json.loads(json_response)
    create_folder_structure(json_response["folder_structure"])
    open("project_root/app/database.py", "a").close()
    open("project_root/app/main.py", "a").close()
    open("project_root/requirements.txt", "a").close()
    open("project_root/.env", "a").close()
    open("project_root/README.md", "a").close()

    with open("project_root/requirements.txt", "w") as f:
        for d in json_response["dependencies"]:
            f.write(d + "\n")
    pip_executable = ".venv\\Scripts\\pip.exe"
    subprocess.run([pip_executable, "install", "-r", "project_root/requirements.txt"])
    return response.content


llama_3_with_tools = llama_3.bind_tools([generate_project_structure_tool])


# Node
def generate_project_structure(state):
    return {"messages": [llama_3_with_tools.invoke(state["messages"])]}
