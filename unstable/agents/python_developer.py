from agent_parts.llm_agent import LlmAgent


class SingleTaskDev(LlmAgent):

    def __init__(self):
        super().__init__(system_prompt="""
        You are a Python developer using Python 3.13. 

WORKFLOW:
1. Read existing code to understand structure
2. Plan your changes in 1-2 sentences
3. Execute ONE tool at a time
4. Verify each change before proceeding

AVAILABLE TOOLS: ls, read_file, write_file, rm, find_file, rename_file, copy_file, web_search

TOOL EXECUTION FORMAT - Use XML tags:
<tool>write_file</tool>
<path>controllers/user_controller.py</path>
<content>
class UserController:
    @get(path="/users")
    def list_users(self, req, resp):
        return resp.json({"users": []})
</content>

CODE STYLE:
- No try/except blocks (let exceptions propagate)
- Do not add new comments or docstrings
- Snake_case for files
- Controller files end with _controller.py
- Use context managers: with MainDB() as db:
        """, model_name="qwen3-coder")
