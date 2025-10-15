# Minimal Multi-Agent Template (framework-agnostic)

A tiny, dependency-light scaffold for building LLM multi-agent systems. Bring your own LLM function.

- Agent base with tools and memory
- Message bus and round-robin router
- Orchestrator with max turns, timeout, and stop conditions
- Pluggable LLM adapter (OpenAI example included)

## Quick start
```bash
python -m examples.demo
```
Swap dummy_llm with your provider in adapters/openai_adapter.py and wire it in examples/demo.py.

## Files

- src/core.py – Message, Memory, Tool base, Calculator tool

- src/agent.py – Agent base and a GenericAgent

- src/router.py – Round-robin router

- src/orchestrator.py – Orchestrator runner

- adapters/openai_adapter.py – Example LLM adapter

- examples/demo.py – Researcher + Critic demo

- tests/test_sanity.py – Minimal smoke test
