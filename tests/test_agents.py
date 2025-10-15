from src.agent import make_researcher, make_critic

def test_agents_init():
    def dummy(messages, params): return "ok"
    r = make_researcher(dummy)
    c = make_critic(dummy)
    assert r.name == "Researcher"
    assert c.name == "Critic"
