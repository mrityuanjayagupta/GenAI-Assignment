from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
import pytest

llama_3 = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)


def run_pytest():
    result = pytest.main(["-q", "--tb=short"])
    return result

# Node
def run_tests(state):
    result = run_pytest()
    if result == 0:
        print("All testcases have passed!")
    else:
        
        print("Some testcases have failed!")
    return state