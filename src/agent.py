"""
Core Diagnostic Agent — Ollama/Gemini Compatible.

Uses LangGraph's ReAct agent with tool calling.
Works with local Ollama models OR Google Gemini free tier.

Key difference from OpenAI version:
- Ollama's tool calling with llama3.1 works well but can be less reliable 
  than GPT-4 for complex multi-tool sequences. 
- We add explicit tool-calling instructions in the prompt to compensate.
- Gemini fallback is there for when local models struggle.
"""

import os
from typing import Optional

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

from src.llm_provider import get_llm
from src.tools import ALL_TOOLS
from src.prompts import DIAGNOSTIC_AGENT_SYSTEM_PROMPT

load_dotenv()


class VehicleDiagnosticsAgent:
    """
    An autonomous vehicle diagnostics agent.
    
    Works with:
    - Ollama (llama3.1:8b, qwen2.5:7b, mistral:7b) — FREE, local
    - Google Gemini 2.0 Flash — FREE tier (15 RPM)
    
    The __call__ pattern makes this callable:
        agent = VehicleDiagnosticsAgent()
        result = agent("P0300 P0171", "Toyota", "Camry", 2019)
    """
    
    def __init__(self, provider: str | None = None, model: str | None = None):
        """
        Initialize the agent with specified or default LLM provider.
        
        Args:
            provider: "ollama" or "gemini". Defaults to .env setting.
            model: Specific model. Defaults to provider's default.
        """
        self.llm = get_llm(provider=provider, model=model, temperature=0.1)
        self.tools = ALL_TOOLS
        self.provider = provider or os.getenv("LLM_PROVIDER", "ollama")
        
        # Create the ReAct agent
        self.agent = create_react_agent(
            model=self.llm,
            tools=self.tools,
        )
    
    def __call__(
        self,
        codes_str: str,
        make: str,
        model: str,
        year: int,
        mileage: Optional[int] = None,
        simple_mode: bool = False,
    ) -> dict:
        """
        Run a full vehicle diagnosis.
        
        Args:
            codes_str: Space or comma separated OBD-II codes
            make: Vehicle make
            model: Vehicle model
            year: Model year
            mileage: Optional odometer reading
            simple_mode: If True, adds plain-English summary
            
        Returns:
            Dict with diagnosis results and metadata
        """
        # Parse codes
        codes = [c.strip().upper() for c in codes_str.replace(",", " ").split() if c.strip()]
        
        if not codes:
            return {"error": "No valid OBD-II codes provided."}
        
        # Build vehicle info
        vehicle_info = f"{year} {make} {model}"
        if mileage:
            vehicle_info += f" ({mileage:,} miles)"
        
        system_prompt = DIAGNOSTIC_AGENT_SYSTEM_PROMPT.format(vehicle_info=vehicle_info)
        
        # Build user message
        # NOTE: With local models, being MORE explicit about tool usage helps.
        # GPT-4 can infer tool order; llama3.1 benefits from clear instructions.
        user_message = (
            f"Diagnose this vehicle: {vehicle_info}\n"
            f"OBD-II codes retrieved: {', '.join(codes)}\n\n"
            f"Follow these steps IN ORDER:\n"
            f"Step 1: Call the lookup_codes tool with ALL codes: {codes}\n"
            f"Step 2: Call the find_code_relationships tool with the same codes: {codes}\n"
            f"Step 3: Call the estimate_repair tool with codes={codes} and vehicle_year={year}\n"
            f"Step 4: Using ALL the information from the tools above, provide your complete "
            f"diagnostic analysis. Include:\n"
            f"   - What each code means\n"
            f"   - Which codes are root causes vs symptoms\n"
            f"   - Prioritized repair sequence (fix root causes first)\n"
            f"   - Total cost estimate\n"
            f"   - Whether it's safe to drive\n"
            f"   - Overall urgency level\n"
        )
        
        if simple_mode:
            user_message += (
                f"\nStep 5: Also provide a 'plain English' explanation as if talking "
                f"to someone who knows nothing about cars. Use simple analogies."
            )
        
        # Run the agent
        try:
            result = self.agent.invoke({
                "messages": [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_message),
                ]
            })
            
            messages = result["messages"]
            final_message = messages[-1].content if messages else "No response generated."
            
            tool_calls = sum(
                1 for msg in messages 
                if hasattr(msg, "tool_calls") and msg.tool_calls
            )
            
            return {
                "vehicle": vehicle_info,
                "codes": codes,
                "diagnosis": final_message,
                "tool_calls_made": tool_calls,
                "total_messages": len(messages),
                "provider": self.provider,
            }
            
        except Exception as e:
            error_msg = str(e)
            
            # If Ollama fails on tool calling, suggest Gemini fallback
            if self.provider == "ollama" and ("tool" in error_msg.lower() or "function" in error_msg.lower()):
                return {
                    "error": (
                        f"Ollama tool calling failed: {error_msg}\n\n"
                        f"Try: agent = VehicleDiagnosticsAgent(provider='gemini')\n"
                        f"Or try a different model: agent = VehicleDiagnosticsAgent(model='qwen2.5:7b')"
                    ),
                    "provider": self.provider,
                }
            
            return {"error": error_msg, "provider": self.provider}


def create_agent(provider: str | None = None, model: str | None = None) -> VehicleDiagnosticsAgent:
    """Factory function."""
    return VehicleDiagnosticsAgent(provider=provider, model=model)


# ── CLI ──
if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("VEHICLE DIAGNOSTICS AGENT")
    print("=" * 60)
    
    # Quick provider check
    from src.llm_provider import get_available_providers
    providers = get_available_providers()
    for p in providers:
        print(f"  ✅ {p}")
    print()
    
    agent = create_agent()
    
    if len(sys.argv) > 1:
        codes = " ".join(sys.argv[1:])
        print(f"Diagnosing: {codes}\n")
        result = agent(codes, "Test", "Vehicle", 2020, simple_mode=True)
        
        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print(f"Provider: {result['provider']}")
            print(f"Tool calls: {result['tool_calls_made']}")
            print("-" * 60)
            print(result["diagnosis"])
    else:
        print("Interactive mode. Type codes or 'quit' to exit.\n")
        
        while True:
            codes = input("Codes: ").strip()
            if codes.lower() == "quit":
                break
            
            make = input("Make: ").strip() or "Unknown"
            model_name = input("Model: ").strip() or "Unknown"
            year_str = input("Year: ").strip()
            year = int(year_str) if year_str.isdigit() else 2020
            
            print("\n🔧 Analyzing...\n")
            result = agent(codes, make, model_name, year, simple_mode=True)
            
            if "error" in result:
                print(f"❌ {result['error']}\n")
            else:
                print(result["diagnosis"])
                print(f"\n[{result['provider']} | {result['tool_calls_made']} tool calls]\n")
