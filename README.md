# Minimal Multi-Agent Template (framework-agnostic)

A tiny, dependency-light scaffold for building LLM multi-agent systems. Bring your own LLM function.

- Agent base with tools and memory
- Message bus and round-robin router
- Orchestrator with max turns, timeout, and stop conditions
- Pluggable LLM adapter (OpenAI example included)

## Quick start
```bash
python -m examples.demo

