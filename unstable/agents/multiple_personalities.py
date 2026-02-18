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
            plan = self.chat.get_last_user_message()
            p = f"Please plan the execution for this assignment:\n\n{plan.message}"
            planner = AgentPlanner()
            planner.run(p, nag=False)
            plan = planner.chat.get_last_assistant_message()
            coder = AgentExecution()
            p = f"Execute the FIRST incomplete step of this plan:\n\n{plan.message}"
            coder.run(p, nag=True)
            self.chat.add_system_message("A step of your plan has been completed. "
                                       "Please check the project  update your plan. "
                                       "Respond with \"plan\" on the first line and your updated plan under that", pinned=False)
            self.get_llm_response_to_chat()





if __name__ == "__main__":
    agent = AgentPlanner()
    agent.run()
