from src.agent import make_researcher, make_critic
from src.orchestrator import Orchestrator
from src.router import Router

# Option A – dummy LLM for offline demo
def dummy_llm(messages, params):
    last_user = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
    if "7*6" in last_user or "calculator" in last_user:
        return '{"tool":"calculator","args":{"expr":"7*6"}}'
    if "Tool result" in last_user:
        return "final_answer: 7*6 equals 42."
    return "Plan: compute 7*6 using calculator, then report final_answer."

# Option B – real LLM
# from adapters.openai_adapter import openai_llm
# llm = openai_llm(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

llm = dummy_llm

agents = {
    "Researcher": make_researcher(llm),
    "Critic": make_critic(llm),
}
router = Router(agent_order=["Researcher", "Critic"])
orch = Orchestrator(agents, router, max_turns=6, wallclock_s=15)

if __name__ == "__main__":
    history, final = orch.run("Compute 7*6 and provide one concise sentence.")
    print("---- Conversation ----")
    for m in history:
        print(f"[{m.sender} -> {m.recipient}] {m.content}\n")
    print("---- Final ----")
    print(final)
