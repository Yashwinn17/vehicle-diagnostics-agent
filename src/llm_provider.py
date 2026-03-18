"""
LLM Provider Factory.

This module abstracts the LLM choice so your agent code never cares
whether it's running on Ollama (local) or Gemini (cloud).

Usage:
    from src.llm_provider import get_llm
    llm = get_llm()                    # Uses default from .env
    llm = get_llm("gemini")            # Force Gemini
    llm = get_llm("ollama", model="qwen2.5:7b")  # Specific Ollama model

This same file will work for EVERY project from Day 1 to Day 84.
Copy it into each new project.
"""

import os
from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel

load_dotenv()


def get_llm(
    provider: str | None = None,
    model: str | None = None,
    temperature: float = 0.1,
) -> BaseChatModel:
    """
    Factory function that returns a configured LLM.
    
    Args:
        provider: "ollama" or "gemini". Defaults to LLM_PROVIDER env var.
        model: Specific model name. Defaults to provider's default.
        temperature: Generation temperature. Low for agents (0.1), higher for creative (0.7).
    
    Returns:
        A LangChain ChatModel ready to use with agents, chains, or direct calls.
    """
    provider = provider or os.getenv("LLM_PROVIDER", "ollama")
    
    if provider == "ollama":
        return _get_ollama(model, temperature)
    elif provider == "gemini":
        return _get_gemini(model, temperature)
    else:
        raise ValueError(f"Unknown provider: {provider}. Use 'ollama' or 'gemini'.")


def _get_ollama(model: str | None, temperature: float) -> BaseChatModel:
    """Configure Ollama (local, free, no API key)."""
    from langchain_ollama import ChatOllama
    
    model = model or os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    return ChatOllama(
        model=model,
        base_url=base_url,
        temperature=temperature,
        # These settings optimize for tool calling with local models:
        num_ctx=8192,           # Context window (8K is safe for 12GB VRAM)
        num_predict=2048,       # Max output tokens
    )


def _get_gemini(model: str | None, temperature: float) -> BaseChatModel:
    """Configure Google Gemini (free tier: 15 RPM, 1M tokens/day)."""
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    model = model or os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not set. Get one free at https://aistudio.google.com/apikey"
        )
    
    return ChatGoogleGenerativeAI(
        model=model,
        google_api_key=api_key,
        temperature=temperature,
        max_output_tokens=2048,
    )


def get_available_providers() -> list[str]:
    """Check which providers are currently available."""
    available = []
    
    # Check Ollama
    try:
        import requests
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        resp = requests.get(f"{base_url}/api/tags", timeout=2)
        if resp.status_code == 200:
            models = [m["name"] for m in resp.json().get("models", [])]
            available.append(f"ollama (models: {', '.join(models)})")
    except Exception:
        pass
    
    # Check Gemini
    if os.getenv("GOOGLE_API_KEY"):
        available.append("gemini (API key set)")
    
    return available


# ── Quick test ──
if __name__ == "__main__":
    print("Checking available LLM providers...\n")
    providers = get_available_providers()
    
    if not providers:
        print("❌ No providers available!")
        print("  → Make sure Ollama is running: ollama serve")
        print("  → Or set GOOGLE_API_KEY in .env")
    else:
        for p in providers:
            print(f"  ✅ {p}")
    
    print("\nTesting default provider...")
    try:
        llm = get_llm()
        response = llm.invoke("Say 'Agent ready' and nothing else.")
        print(f"  ✅ Response: {response.content}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
