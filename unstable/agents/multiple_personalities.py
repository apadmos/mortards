from agent_parts.llm_agent import LlmAgent
from agents.execution import AgentExecution


class AgentPlanner(LlmAgent):

    def __init__(self):
        super().__init__(system_prompt="""
Your primary task is to evaluate a user or agent prompt and determine if it is a complicated task that requires pre-planning or a straight forward task that can be immediately executed.
If the assignment is simple you must return the word "execute" as the first line of your response and then restate the assignment clearly in the rest of your message.
If the assignment is complex you must return the word "plan" as the first line of your response and then restate the assignment clearly in the rest of your message.
""", model_name="gpt-oss:20b")

    def after_llm_response(self):
        """The response has not been added to the chat yet. It can be acted on, doctored, or replaced"""
        latest_resp = self.chat.get_last_assistant_message()
        if latest_resp.startswith("execute"):
            plan = self.chat.get_last_assistant_message()
            p = f"Execute this task please:\n\n{plan.message}"
            coder = AgentExecution()
            coder.run(p)
        else:
            planner = AgentPlanner()
            planner.run()
            plan = planner.chat.get_last_assistant_message()
            coder = AgentExecution()
            p = f"Execute the FIRST undone step of this plan:\n\n{plan.message}"
            coder.run(p)




if __name__ == "__main__":
    agent = AgentPlanner()
    agent.run()
