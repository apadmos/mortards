from agent_parts.echo_agent import EchoAgent


class TooledAgent(EchoAgent):

    def after_llm_response(self):
        """the response has already been added to the chat, """
        pass
