"""
Streamlit UI for the Vehicle Diagnostics Agent.
Supports Ollama (local) and Gemini (free tier).

Run: streamlit run app.py
"""

import streamlit as st
from src.agent import create_agent

# ── Page Config ──
st.set_page_config(
    page_title="AI Vehicle Diagnostician",
    page_icon="🔧",
    layout="wide",
)

st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: 700; color: #1a1a2e; margin-bottom: 0; }
    .sub-header { font-size: 1.1rem; color: #666; margin-top: 0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🔧 AI Vehicle Diagnostician</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Enter OBD-II codes. Get expert diagnosis in seconds. Runs 100% local with Ollama.</p>', unsafe_allow_html=True)
st.divider()

# ── Sidebar ──
with st.sidebar:
    st.header("Vehicle Information")
    make = st.text_input("Make", placeholder="e.g., Toyota")
    model = st.text_input("Model", placeholder="e.g., Camry")
    year = st.number_input("Year", min_value=1990, max_value=2026, value=2020)
    mileage = st.number_input("Mileage (optional)", min_value=0, max_value=500000, value=0, step=1000)
    
    st.divider()
    st.header("AI Settings")
    
    provider = st.selectbox(
        "LLM Provider",
        ["ollama", "gemini"],
        index=0,
        help="Ollama = free, local, private. Gemini = free tier, cloud, better for complex cases."
    )
    
    if provider == "ollama":
        model_choice = st.selectbox(
            "Ollama Model",
            ["llama3.1:8b", "qwen2.5:7b", "mistral:7b"],
            index=0,
            help="llama3.1 = best for tool calling. qwen2.5 = strong backup. mistral = good for reports."
        )
    else:
        model_choice = st.selectbox(
            "Gemini Model",
            ["gemini-2.5-flash-lite"],
            index=0,
            help="Uses the Gemini model currently available to your API key."
        )
    
    simple_mode = st.toggle("Explain like I'm not a mechanic", value=True)
    
    st.divider()
    st.caption("Built by Yashwin Vasanth | Day 1 of 84")
    st.caption("Running on Ollama (local) + Gemini (free tier)")

# ── Main Input ──
col1, col2 = st.columns([3, 1])
with col1:
    codes_input = st.text_input(
        "Enter OBD-II Codes",
        placeholder="e.g., P0300 P0171 P0420",
    )
with col2:
    st.write("")
    st.write("")
    diagnose_btn = st.button("🔍 Diagnose", type="primary", use_container_width=True)

# ── Examples ──
with st.expander("💡 Try these example scenarios"):
    ex_cols = st.columns(3)
    with ex_cols[0]:
        st.markdown("**Misfire + Lean**")
        st.code("P0300 P0171 P0174")
        st.caption("Vacuum leak scenario")
    with ex_cols[1]:
        st.markdown("**Electrical Cascade**")
        st.code("P0562 U0100 U0101")
        st.caption("Alternator/battery failure")
    with ex_cols[2]:
        st.markdown("**Timing Chain**")
        st.code("P0016 P0011 P0300")
        st.caption("Stretched timing chain")

# ── Diagnosis ──
if diagnose_btn and codes_input:
    provider_label = f"{'🏠 Ollama' if provider == 'ollama' else '☁️ Gemini'} ({model_choice})"
    
    with st.spinner(f"🔧 Diagnosing with {provider_label}..."):
        try:
            agent = create_agent(provider=provider, model=model_choice)
            result = agent(
                codes_str=codes_input,
                make=make or "Unknown",
                model=model or "Unknown",
                year=year,
                mileage=mileage if mileage > 0 else None,
                simple_mode=simple_mode,
            )
            
            if "error" in result:
                st.error(result["error"])
                if provider == "ollama":
                    st.info("💡 Tip: If Ollama tool calling fails, try switching to Gemini in the sidebar, or try a different Ollama model.")
            else:
                st.divider()
                
                met_cols = st.columns(4)
                with met_cols[0]:
                    st.metric("Codes Analyzed", len(result["codes"]))
                with met_cols[1]:
                    st.metric("Tool Calls", result["tool_calls_made"])
                with met_cols[2]:
                    st.metric("Provider", result["provider"])
                with met_cols[3]:
                    st.metric("Model", model_choice)
                
                st.divider()
                st.subheader("📋 Diagnostic Report")
                st.markdown(result["diagnosis"])
                
                with st.expander("🤖 Agent Decision Log"):
                    st.json({
                        "codes_submitted": result["codes"],
                        "vehicle": result["vehicle"],
                        "tool_calls": result["tool_calls_made"],
                        "provider": result["provider"],
                        "model": model_choice,
                    })
                    
        except Exception as e:
            st.error(f"Error: {str(e)}")
            if provider == "ollama":
                st.info("Make sure Ollama is running: `ollama serve`")
            else:
                st.info("Make sure GOOGLE_API_KEY is set in your .env file.")

elif diagnose_btn:
    st.warning("Enter at least one OBD-II code.")

st.divider()
st.caption("⚠️ For informational purposes only. Always consult a certified mechanic for safety-critical repairs.")
