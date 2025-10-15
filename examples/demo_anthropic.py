from adapters.anthropic_adapter import anthropic_llm
from src.agent import make_researcher, make_critic
from src.router import Router
from src.orchestrator import Orchestrator

if __name__ == "__main__":
    llm = anthropic_llm()
    agents = {"Researcher": make_researcher(llm), "Critic": make_critic(llm)}
    router = Router(agent_order=["Researcher", "Critic"])
    orch = Orchestrator(agents, router, max_turns=8, wallclock_s=30)
    _, final = orch.run("Plan and compute 50*3, then provide a one-sentence final_answer.")
    print(final)
