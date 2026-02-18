from agents.execution import AgentExecution
from agents.planning import AgentPlanner

if __name__ == "__main__":
    """The response has not been added to the chat yet. It can be acted on, doctored, or replaced"""
    while True:
        planner = AgentPlanner()
        planner.run()
        plan = planner.chat.get_last_assistant_message()
        while True:
            coder = AgentExecution()
            p = f"Execute the FIRST incomplete step of this plan:\n\n{plan.message}"
            coder.run(p, nag=True)
            c = input("continue:")
            if c == "exit":
                planner.chat.add_system_message("A step of your plan has been completed. "
                                                "Please check the project  update your plan. "
                                                "Respond with \"plan\" on the first line and your updated plan under that",
                                                pinned=False)
                break
        c = input("continue:")
        if c == "exit":
            break




