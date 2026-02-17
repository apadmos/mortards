
from agent_parts.echo_agent import EchoAgent


class OhceAgent(EchoAgent):


    def process_llm_response(self, response:str) -> str:
        """The response has not been added to the chat yet. It can be acted on, doctored, or replaced"""
        return response[::-1]