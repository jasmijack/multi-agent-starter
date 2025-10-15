from src.agent import make_researcher, make_critic
from src.router import Router
from src.orchestrator import Orchestrator

def test_final_answer():
    def dummy_llm(messages, params):
        if any("calculator" in m["content"] for m in messages):
            return '{"tool":"calculator","args":{"expr":"7*6"}}'
        return "final_answer: 42"
    agents = {"Researcher": make_researcher(dummy_llm), "Critic": make_critic(dummy_llm)}
    orch = Orchestrator(agents, Router(["Researcher", "Critic"]), max_turns=3, wallclock_s=5)
    _, final = orch.run("test")
    assert "final_answer" in final.lower()
