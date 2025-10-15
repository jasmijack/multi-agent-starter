from src.agent import make_researcher, make_critic
from src.router import Router
from src.orchestrator import Orchestrator

def test_orchestrator_final_answer():
    def dummy(messages, params):
        content = next((m["content"] for m in messages if m["role"] == "system"), "")
        if "calculator" in content:
            return '{"tool":"calculator","args":{"expr":"7*6"}}'
        return "final_answer: done."
    agents = {"Researcher": make_researcher(dummy), "Critic": make_critic(dummy)}
    orch = Orchestrator(agents, Router(["Researcher", "Critic"]), max_turns=3, wallclock_s=5)
    _, final = orch.run("test")
    assert "final_answer" in final.lower()
