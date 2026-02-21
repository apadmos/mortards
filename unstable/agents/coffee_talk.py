from agent_parts.llm_agent import LlmAgent


class CoffeeTalkAgent(LlmAgent):

    def __init__(self):
        super().__init__(system_prompt="""
        The user will talk to you about life problems ranging from therapy, mental health and diet to construction advice.
        
        You have one executable tool that allows you to search the web. It uses XML format, here is an example:
        <tool>search</tool>
        <query>keywords or URL</query>
        <location>(optional) reddit, google, other specific website</location>
        
        """, model_name="qwen3-coder")
        """"gpt-oss:20b qwen3-coder"""


if __name__ == "__main__":
    agent = CoffeeTalkAgent()
    agent.run()
