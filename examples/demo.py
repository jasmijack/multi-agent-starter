from src.agent import make_researcher, make_critic
from src.orchestrator import Orchestrator
from src.router import Router

def dummy_llm(messages, params):
    # deterministic toy behavior
    last_user = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
    if "7*6" in last_user or "calculator" in last_user:
        return '{"tool":"calculator","args":{"expr":"7*6"}}'
    if "Tool result" in last_user:
        return "final_answer: 7*6 equals 42."
    return "Plan: compute 7*6 using calculator, then report final_answer."

if __name__ == "__main__":
    agents = {"Researcher": make_researcher(dummy_llm), "Critic": make_critic(dummy_llm)}
    router = Router(agent_order=["Researcher", "Critic"])
    orch = Orchestrator(agents, router, max_turns=6, wallclock_s=15)
    history, final = orch.run("Compute 7*6 and provide one concise sentence.")
    print("---- Conversation ----")
    for m in history:
        print(f"[{m.sender} -> {m.recipient}] {m.content}\n")
    print("---- Final ----")
    print(final)
