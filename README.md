# multi-agent-lab

[![CI](https://img.shields.io/github/actions/workflow/status/jasmijack/multi-agent-starter/tests.yml?branch=main)](../../actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)

A lightweight, framework-agnostic starter kit for building and experimenting with LLM-based multi-agent systems.

- Agents with tools and memory
- Message bus, router, and orchestrator with stop conditions and timeouts
- Swappable adapters for OpenAI, Anthropic, and Azure OpenAI
- Built-in tools: calculator, web search, file reader
- Examples and tests included

## Quick start
```bash
git clone https://github.com/your-username/multi-agent-lab.git
cd multi-agent-lab
pip install -r requirements.txt

# run the basic demo
python -m examples.demo

# run tests
pytest
