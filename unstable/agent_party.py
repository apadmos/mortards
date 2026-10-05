from agent_coder import CodingAgent
from agent_planner import PlanningAgent


class AgentParty:

    def __init__(self, sandbox):

        """
        Ah, my first attempt at a multi-agent system.
        The planner will generate a plan, and the coder will execute it.
        It made things worse.
        """

        self.planner = PlanningAgent(sandbox=sandbox)
        self.pythong_coder = CodingAgent(sandbox=sandbox)

    def run(self):
        plan = self.planner.run()
        self.pythong_coder.run(plan)


if __name__ == "__main__":
    sandbox = "../python_src"
    ap = AgentParty(sandbox=sandbox)
    ap.run()
