# Agentic AI: Invoice Categorization & Code Generation

## Overview
This project demonstrates a simple **Agentic AI system built using the GPT-4o foundation model** through the OpenAI API (via LiteLLM). The system applies **prompt engineering and tool-based agent design** to automate tasks such as invoice categorization and Python code generation.

The goal of this project is to explore how **foundation models can act as reasoning engines within agent systems** that interact with tools and automate workflows.

---

## Foundation Model Integration
The system uses **GPT-4o** through the LiteLLM API to generate responses and perform reasoning.

```python
from litellm import completion

response = completion(
    model="openai/gpt-4o",
    messages=messages,
    max_tokens=1024,
    api_key=OPENAI_API_KEY
)

## Agent Architecture
User Input
   ↓
Foundation Model (GPT-4o)
   ↓
Agent Logic (prompt + message history)
   ↓
Tool Functions
   ↓
Output

## Technologies

Python

OpenAI API

LiteLLM

GPT-4o

Prompt Engineering

Agent-based AI design

---

