from crewai.tools import BaseTool, tool
from typing import Callable, Dict, List

def test_creating_a_tool_using_annotation():
    @tool("Name of my tool")
    def my_tool(question: str) -> str:
        """Clear description for what this tool is useful for, your agent will need this information to use it."""
        return question

    # Assert all the right attributes were defined
    assert my_tool.name == "Name of my tool"
    assert (
        my_tool.description
        == "Tool Name: Name of my tool\nTool Arguments: {'question': {'description': None, 'type': 'str'}}\nTool Description: Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    assert my_tool.args_schema.model_json_schema()["properties"] == {
        "question": {"title": "Question", "type": "string"}
    }
    assert (
        my_tool.func("What is the meaning of life?") == "What is the meaning of life?"
    )

    converted_tool = my_tool.to_structured_tool()
    assert converted_tool.name == "Name of my tool"

    assert (
        converted_tool.description
        == "Tool Name: Name of my tool\nTool Arguments: {'question': {'description': None, 'type': 'str'}}\nTool Description: Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    assert converted_tool.args_schema.model_json_schema()["properties"] == {
        "question": {"title": "Question", "type": "string"}
    }
    assert (
        converted_tool.func("What is the meaning of life?")
        == "What is the meaning of life?"
    )

def test_creating_a_tool_using_baseclass():
    class MyCustomTool(BaseTool):
        name: str = "Name of my tool"
        description: str = "Clear description for what this tool is useful for, your agent will need this information to use it."

        def _run(self, question: str) -> str:
            return question

    my_tool = MyCustomTool()
    # Assert all the right attributes were defined
    assert my_tool.name == "Name of my tool"

    assert (
        my_tool.description
        == "Tool Name: Name of my tool\nTool Arguments: {'question': {'description': None, 'type': 'str'}}\nTool Description: Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    assert my_tool.args_schema.model_json_schema()["properties"] == {
        "question": {"title": "Question", "type": "string"}
    }
    assert my_tool.run("What is the meaning of life?") == "What is the meaning of life?"

    converted_tool = my_tool.to_structured_tool()
    assert converted_tool.name == "Name of my tool"

    assert (
        converted_tool.description
        == "Tool Name: Name of my tool\nTool Arguments: {'question': {'description': None, 'type': 'str'}}\nTool Description: Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    assert converted_tool.args_schema.model_json_schema()["properties"] == {
        "question": {"title": "Question", "type": "string"}
    }
    assert (
        converted_tool._run("What is the meaning of life?")
        == "What is the meaning of life?"
    )

def test_setting_cache_function():
    class MyCustomTool(BaseTool):
        name: str = "Name of my tool"
        description: str = "Clear description for what this tool is useful for, your agent will need this information to use it."
        cache_function: Callable = lambda: False

        def _run(self, question: str) -> str:
            return question

    my_tool = MyCustomTool()
    # Assert all the right attributes were defined
    assert not my_tool.cache_function()

def test_default_cache_function_is_true():
    class MyCustomTool(BaseTool):
        name: str = "Name of my tool"
        description: str = "Clear description for what this tool is useful for, your agent will need this information to use it."

        def _run(self, question: str) -> str:
            return question

    my_tool = MyCustomTool()
    # Assert all the right attributes were defined
    assert my_tool.cache_function()

def test_tool_with_multiple_args_and_complex_return():
    @tool("Complex Tool")
    def complex_tool(name: str, age: int, is_student: bool) -> List[Dict[str, str]]:
        """A tool that takes multiple arguments and returns a complex type."""
        return [{"name": name, "status": f"{'Student' if is_student else 'Non-student'} aged {age}"}]

    # Check if the tool attributes are correctly set
    assert complex_tool.name == "Complex Tool"
    assert "Tool Name: Complex Tool" in complex_tool.description
    assert "name: {'description': None, 'type': 'str'}" in complex_tool.description
    assert "age: {'description': None, 'type': 'int'}" in complex_tool.description
    assert "is_student: {'description': None, 'type': 'bool'}" in complex_tool.description

    # Check if the args_schema is correctly generated
    schema = complex_tool.args_schema.model_json_schema()
    assert schema["properties"] == {
        "name": {"title": "Name", "type": "string"},
        "age": {"title": "Age", "type": "integer"},
        "is_student": {"title": "Is Student", "type": "boolean"}
    }

    # Test running the tool
    result = complex_tool.run(name="Alice", age=25, is_student=True)
    assert result == [{"name": "Alice", "status": "Student aged 25"}]

    # Convert to structured tool and test
    structured_tool = complex_tool.to_structured_tool()
    assert structured_tool.name == "Complex Tool"
    assert "Tool Name: Complex Tool" in structured_tool.description
    structured_result = structured_tool.func(name="Bob", age=30, is_student=False)
    assert structured_result == [{"name": "Bob", "status": "Non-student aged 30"}]