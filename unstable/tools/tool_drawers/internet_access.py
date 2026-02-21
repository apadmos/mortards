import requests

from agent_parts.chat_parts.tool_request import ToolRequest


class InternetAccess:

    def __init__(self, write_sandbox: str = None):
        self.write_sandbox = write_sandbox
        self.has_read = set()

    def get(self, args: ToolRequest):
        url = args.get("url", required=True)
        response = requests.get(url)
        return response.text
