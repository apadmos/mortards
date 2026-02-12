import ast
import json
import re

from tool_functions import ToolFunctions


class InterfaceException(Exception):
    """Custom exception for interface-related errors."""

    def __init__(self, suggested_message, exception):
        self.suggested_message = suggested_message
        self.exception = exception
        super().__init__(self.suggested_message)


class ToolInterface(object):

    def __init__(self, sandbox: str):
        self.tools = ToolFunctions(sandbox=sandbox)

    def parse_json_blocks(self, chat_message: str) -> list[dict]:

        json_objects = []

        # Find all ```json code blocks
        pattern = r'```json\s*(.*?)\s*```'
        matches = re.findall(pattern, chat_message, re.DOTALL)

        # Parse each found JSON section
        for json_string in matches:
            json_string.strip()
            try:
                parsed_json = json.loads(json_string)
                json_objects.append(parsed_json)
            except json.JSONDecodeError as e:
                try:
                    parsed_json = json.loads(json_string + "}")
                    json_objects.append(parsed_json)
                except Exception as e:
                    print("Attempt to fix invalid JSON failed.")
                    raise InterfaceException(f"Please fix the invalid JSON block in your response: {e}"
                                             f"JSON Received: "
                                             f"{json_string}", e)
        return json_objects

    def execute_python_blocks(self, chat_message: str) -> list:

        """hook for executing functions like delete_file(name="something")"""

        namespace = {
            'delete_file': self.tools.delete_file,
            'read_file': self.tools.read_file,
            'write_file': self.tools.write_file,
            'list_directory': self.tools.list_directory,
            'find_file': self.tools.find_file,
            'rename_file': self.tools.rename_file,
            'copy_file': self.tools.copy_file,
            # add other allowed functions here
        }

        if "```python\n" in chat_message:
            blocks = chat_message.split("```python\n")
        else:
            blocks = [chat_message]

        responses = []
        for block in blocks:
            block = block.strip().strip("'`")
            if block and "(" in block and ")" in block:
                try:
                    tree = ast.parse(block)
                    for node in tree.body:
                        if isinstance(node, ast.Expr):
                            # Evaluate expression and capture result
                            result = eval(compile(ast.Expression(node.value), '<string>', 'eval'), namespace)
                            result = f"Result of {node.value.func.id}: {result}"
                            responses.append(result)
                        else:
                            # Execute statements (assignments, loops, etc.) without capturing return
                            exec(compile(ast.Module([node], type_ignores=[]), '<string>', 'exec'), namespace)
                            responses.append(f"Executed: {ast.unparse(node)[:50]}...")
                except Exception as e:
                    pass
        return responses

    def first_found(self, d: dict, keys: list[str]) -> str | None:
        for key in keys:
            if key in d:
                return d[key]

    def execute_block(self, block_dict):
        action = block_dict.get("action")
        if action:
            params = block_dict.get("parameters")
            first_param = list(params.values())[0] if params else None
            file_path = self.first_found(params, ["path", "filepath", "file_name", "file_path", "filename"])
            if action in ["list_directory", "list_files", "ls", "list_dir", "dir"]:
                return action, self.tools.list_directory(first_param)
            if action in ["write_file", "write"]:
                contents = self.first_found(params, ["content", "file_content", "contents", "file_contents"])
                return action, self.tools.write_file(path=file_path, content=contents)
            if action in ["read_file", "read", "cat"]:
                return action, self.tools.read_file(first_param)
            if action in ["delete_file", "delete", "rm"]:
                return action, self.tools.delete_file(first_param)

            raise InterfaceException(f"The action \"{action}\" is not implemented. "
                                     f"Please show me a python function that can perform this action.", None)
