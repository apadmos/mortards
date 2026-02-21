from agent_parts.llm_agent import LLMAgent
from agent_parts.llm_interfaces.gpt_oss_20b import GPT3_OSS_20b


class CoffeeTalkAgent(LLMAgent):

    def __init__(self):
        super().__init__(system_prompt="""
        The user will talk to you about life problems ranging from therapy, mental health and diet to construction advice.
        
        You have one executable tool called "requests.get". It is the Python requests library
        and it allows you to make arbitrary web requests on the public internet.
        
        TOOL EXECUTION FORMAT IS JSON
        """, llm_interface=GPT3_OSS_20b())


if __name__ == "__main__":
    agent = CoffeeTalkAgent()
    agent.run()
