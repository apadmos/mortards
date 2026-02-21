import requests

from agent_parts.chat_parts.chat_history import ChatHistory
from agent_parts.chat_parts.chat_message import ChatMessage
from agent_parts.chat_parts.tool_request import ToolRequest


class GPT3_OSS_20b:

    def __init__(self):
        self.model_name = "gpt-oss:20b"
        self.ollama_url = "http://localhost:11434/api/chat"

    def send_chat(self, chat: ChatHistory):
        """Most models seem to accept the same payload, but some have a "history" field in
        the response which makes me think even this part should be tailored to the model"""
        print("🤔🤔🤔")
        messages = chat.get_messages()
        messages = [m.to_ollama_dict() for m in messages]
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
        }
        resp = requests.post(self.ollama_url, json=payload, timeout=3000)
        resp.raise_for_status()
        resp = resp.json()
        return resp

    def parse_response(self, resp_json) -> ChatMessage:
        """This model seems to respond with actual tool commands in json, so pull them out"""
        message = resp_json["message"]
        content = message["content"]
        thinking = message.get("thinking")
        tools = message.get("tool_calls")
        tools = self.parse_tool_request(tools) if tools else []
        return ChatMessage(message=content,
                           thinking=thinking,
                           tool_calls=tools,
                           role="assistant", raw=message)

    def parse_tool_request(self, tools):
        """This model seems to reply with:
        {'function':
            {
            'arguments':
                {
                'location': 'google',
                'query': 'current weather in New York'
                },
            'index': 0,
            'name': 'search'
            },
            'id':
            'call_efz6fx6c'
        }
        """
        r = []
        for tool in tools:
            parts = tool["function"]
            id = tool["id"]
            name = parts["name"]
            args = parts["arguments"]
            tr = ToolRequest(name=name, args=args, call_id=id)
            r.append(tr)
        return r
