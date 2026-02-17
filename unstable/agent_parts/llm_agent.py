import os
from email.message import Message

import requests

from agent_parts.chat_history import ChatHistory
from agent_parts.echo_agent import EchoAgent


class LlmAgent(EchoAgent):

    def __init__(self, system_prompt:str, model_name:str="gpt-oss:20b"):
        super().__init__(system_prompt)
        self.model_name = model_name
        self.ollama_url = "http://localhost:11434/api/chat"


    def get_llm_response_to_chat(self) -> dict:
        print("🤔🤔🤔")
        messages = self.chat.get_messages()
        messages = [m.to_ollama_dict() for m in messages]
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
        }
        resp = requests.post(self.ollama_url, json=payload, timeout=3000)
        resp.raise_for_status()
        resp = resp.json()
        msg = resp["message"]
        return msg

    def process_llm_response(self, response:dict) -> dict:
        return response




if __name__ == "__main__":
    ea = LlmAgent(system_prompt="You are a generic chat agent. Accuracy is more important than confidence."
                                "If you are not confident in an answer, reply that you do not know and would like help researching."
                                "You have one tool available: <tool>internet_search</tool>")
    ea.run()