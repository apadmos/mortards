from agent_parts.llm_agent import LLMAgent
from agent_parts.llm_interfaces.qwen3code import Qwen3CoderInterface


class AgentExecution(LLMAgent):

    def __init__(self):
        super().__init__(system_prompt="""
        You are a Python developer using Python 3.13. You are working with the user on a single Python file. 
        
AVAILABLE TOOLS: 
 - check_code (Detects syntax errors of the current code)
 - write_code (get the contents the code you are working on)
 - read_code (reads the current state of the file we are working on)

TOOL EXECUTION FORMAT - Use XML tags:
<tool>write_code</tool>
<content>
code to be written to the code file goes here
</content>

MISTAKES YOU HAVE MADE BEFORE:
- Trying to execute multiple tool calls at once

""", llm_interface=Qwen3CoderInterface())


if __name__ == "__main__":
    agent = AgentExecution()
    agent.run()
