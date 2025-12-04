
User
Please do again with reference code:import os
import time
import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import streamlit as st
import yaml
--- AI SDKs ---
import google.generativeai as genai
from openai import OpenAI
import anthropic
from xai_sdk import Client as XAIClient
from xai_sdk.chat import user as xai_user, system as xai_system
Optional: if you use the separate prompts module
try:
from prompts import BASE_SYSTEM_PROMPT
except ImportError:
BASE_SYSTEM_PROMPT = ""
=========================
1. CONFIG / CONSTANTS
=========================
AI_MODELS = {
"gemini": [
"gemini-2.5-flash",
"gemini-2.5-flash-lite",
],
"openai": [
"gpt-5-nano",
"gpt-4o-mini",
"gpt-4.1-mini",
],
"anthropic": [
"claude-3-5-sonnet-20241022",
"claude-3-5-haiku-20241022",
],
"xai": [
"grok-4-fast-reasoning",
"grok-3-mini",
],
}
LANG_LABELS = {
"en": "English",
"zh": "繁體中文",
}
THEME_MODE_LABELS = {
"light": "Light",
"dark": "Dark",
}
20 flower-based Nordic themes (simplified)
FLOWER_THEMES = [
{
"id": "nordic_lotus",
"name_en": "Nordic Lotus",
"name_zh": "北境蓮華",
"primary": "#7FB3D5",
"secondary": "#F5CBA7",
"accent": "#82E0AA",
"bg": "#F4F6F7",
},
{
"id": "polar_rose",
"name_en": "Polar Rose",
"name_zh": "極地玫瑰",
"primary": "#EC7063",
"secondary": "#FADBD8",
"accent": "#AF7AC5",
"bg": "#FDFEFE",
},
# ... add 18 more themes ...
]
Two "wow" features:
1) Mana Orb & Stress Meter
2) Achievement Blossoms (badges based on XP and runs)
@dataclass
class AgentConfig:
id: str
name: str
description: str
model: str
max_tokens: int
temperature: float
system_prompt: str
provider: str
@dataclass
class AppState:
language: str = "en"
theme_mode: str = "light"
current_flower_id: str = FLOWER_THEMES[0]["id"]
health: int = 100
mana: int = 100
experience: int = 0
level: int = 1
api_keys: Dict[str, Optional[str]] = None
=========================
2. SESSION INIT
=========================
def init_session_state():
if "app_state" not in st.session_state:
st.session_state.app_state = AppState(
api_keys={
"gemini": os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY"),
"openai": os.getenv("OPENAI_API_KEY"),
"anthropic": os.getenv("ANTHROPIC_API_KEY"),
"xai": os.getenv("XAI_API_KEY"),
}
)
if "agents" not in st.session_state:
st.session_state.agents = load_agents_yaml("agents.yaml")
if "pipeline_results" not in st.session_state:
st.session_state.pipeline_results = {}
# NEW: user-editable inputs for each agent
if "pipeline_inputs" not in st.session_state:
st.session_state.pipeline_inputs = {}
# NEW: per-agent view mode ("Edit" vs "Preview")
if "pipeline_view_modes" not in st.session_state:
st.session_state.pipeline_view_modes = {}
if "execution_log" not in st.session_state:
st.session_state.execution_log = []
if "metrics" not in st.session_state:
st.session_state.metrics = {
"total_runs": 0,
"provider_calls": {"gemini": 0, "openai": 0, "anthropic": 0, "xai": 0},
"tokens_used": 0,
"last_run_duration": 0.0,
}
=========================
3. AGENT CONFIG LOADING
=========================
def load_agents_yaml(path: str) -> List[AgentConfig]:
if not os.path.exists(path):
return []
with open(path, "r", encoding="utf-8") as f:
data = yaml.safe_load(f)
agents = []
for a in data.get("agents", []):
agents.append(
AgentConfig(
id=a["id"],
name=a["name"],
description=a.get("description", ""),
model=a["model"],
max_tokens=int(a.get("max_tokens", 2000)),
temperature=float(a.get("temperature", 0.2)),
system_prompt=a["system_prompt"],
provider=a["provider"],
)
)
return agents
=========================
4. THEME & STYLING
=========================
def get_current_theme() -> Dict[str, str]:
flower_id = st.session_state.app_state.current_flower_id
for theme in FLOWER_THEMES:
if theme["id"] == flower_id:
return theme
return FLOWER_THEMES[0]
def inject_global_css():
theme = get_current_theme()
mode = st.session_state.app_state.theme_mode
code
Code
bg_color = theme["bg"] if mode == "light" else "#0B1725"
text_color = "#0B1725" if mode == "light" else "#ECF0F1"

css = f"""
<style>
:root {{
    --primary: {theme["primary"]};
    --secondary: {theme["secondary"]};
    --accent: {theme["accent"]};
    --bg-color: {bg_color};
    --text-color: {text_color};
}}
body {{
    background: radial-gradient(circle at top, var(--bg-color) 0%, #02040f 100%);
    color: var(--text-color);
}}
.nordic-card {{
    background: rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.0rem 1.2rem;
    border: 1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(18px);
}}
.nordic-badge {{
    border-radius: 999px;
    padding: 0.1rem 0.8rem;
    font-size: 0.7rem;
    border: 1px solid rgba(255,255,255,0.3);
}}
.mana-orb {{
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #ffffff, var(--accent));
    box-shadow: 0 0 25px rgba(130, 224, 170, 0.8);
    position: relative;
}}
.mana-orb-inner {{
    position: absolute;
    inset: 10px;
    border-radius: 50%;
    background: radial-gradient(circle at 20% 20%, rgba(255,255,255,0.8), transparent);
    animation: pulse 2s infinite;
}}
@keyframes pulse {{
    0% {{ box-shadow: 0 0 0 0 rgba(130,224,170,0.6); }}
    70% {{ box-shadow: 0 0 0 18px rgba(130,224,170,0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(130,224,170,0); }}
}}
.status-dot {{
    height: 10px;
    width: 10px;
    border-radius: 50%;
    display: inline-block;
}}
.status-dot-idle {{ background: #BDC3C7; }}
.status-dot-running {{ background: #F4D03F; animation: blink 1s infinite; }}
.status-dot-success {{ background: #2ECC71; }}
.status-dot-error {{ background: #E74C3C; }}
@keyframes blink {{
    0% {{ opacity: 0.2; }}
    50% {{ opacity: 1; }}
    100% {{ opacity: 0.2; }}
}}
</style>
"""
st.markdown(css, unsafe_allow_html=True)
=========================
5. API KEY HANDLING
=========================
def get_api_key(provider: str) -> Optional[str]:
# Prefer environment (do not show), fallback to session/UI field
key_env = None
if provider == "gemini":
key_env = os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY")
elif provider == "openai":
key_env = os.getenv("OPENAI_API_KEY")
elif provider == "anthropic":
key_env = os.getenv("ANTHROPIC_API_KEY")
elif provider == "xai":
key_env = os.getenv("XAI_API_KEY")
code
Code
if key_env:
    st.session_state.app_state.api_keys[provider] = key_env
    return key_env

return st.session_state.app_state.api_keys.get(provider)
def api_key_input_ui():
st.subheader("🔐 API Keys (Client-Side Only)")
st.caption(
"Keys are kept in memory only. For deployment, prefer environment variables on Hugging Face Spaces."
)
code
Code
cols = st.columns(4)
providers = ["gemini", "openai", "anthropic", "xai"]
labels = ["Google Gemini", "OpenAI", "Anthropic", "Grok (xAI)"]
for col, provider, label in zip(cols, providers, labels):
    with col:
        env_present = get_api_key(provider) is not None
        if env_present:
            st.success(f"{label}: using env var")
        else:
            val = st.text_input(
                f"{label} API Key",
                type="password",
                key=f"{provider}_manual_api_key",
            )
            if val:
                st.session_state.app_state.api_keys[provider] = val
=========================
6. PROVIDER CALLS
=========================
def call_gemini(model: str, system_prompt: str, user_input: str,
max_tokens: int, temperature: float, api_key: str) -> str:
"""
Gemini helper without explicit safety settings.
Also hides low-level safety/harm-category messages from the UI.
"""
genai.configure(api_key=api_key)
code
Code
# No safety_settings passed → use provider defaults, but we will
# sanitize any safety-related error messages before showing them.
model_client = genai.GenerativeModel(
    model_name=model,
    system_instruction=(system_prompt or BASE_SYSTEM_PROMPT or None),
)

try:
    response = model_client.generate_content(
        [user_input],
        generation_config={
            "temperature": float(temperature),
            "max_output_tokens": int(max_tokens),
        },
    )
except Exception as e:
    msg = str(e)

    # Hide raw safety codes like harm_category_sexual_content, etc.
    upper_msg = msg.upper()
    if "SAFETY" in upper_msg or "HARM_" in upper_msg or "HARM CATEGORY" in upper_msg:
        return (
            "⚠️ Gemini 已封鎖此輸入，原因與其內建安全機制相關。\n"
            "建議：\n"
            "- 嘗試稍微調整描述方式，避免過於敏感或模糊的語句；或\n"
            "- 在此情境下可改用 OpenAI / Anthropic / Grok 等其他模型執行相同步驟。"
        )

    # Generic error fallback (non-safety)
    return f"⚠️ Gemini 呼叫失敗：{msg}"

# Extract text from response
try:
    return response.text
except Exception:
    if hasattr(response, "candidates") and response.candidates:
        parts = response.candidates[0].content.parts
        txt = "".join(
            getattr(p, "text", "") for p in parts
            if hasattr(p, "text")
        )
        if txt.strip():
            return txt
    return "⚠️ 無法從 Gemini 回應中解析文字內容。"
def call_openai(model: str, system_prompt: str, user_input: str,
max_tokens: int, temperature: float, api_key: str) -> str:
client = OpenAI(api_key=api_key)
messages = []
if BASE_SYSTEM_PROMPT or system_prompt:
messages.append({"role": "system", "content": (BASE_SYSTEM_PROMPT + "\n\n" + system_prompt)})
else:
messages.append({"role": "system", "content": "You are a helpful regulatory assistant."})
messages.append({"role": "user", "content": user_input})
code
Code
resp = client.chat.completions.create(
    model=model,
    messages=messages,
    max_tokens=max_tokens,
    temperature=temperature,
)
return resp.choices[0].message.content
def call_anthropic(model: str, system_prompt: str, user_input: str,
max_tokens: int, temperature: float, api_key: str) -> str:
client = anthropic.Anthropic(api_key=api_key)
m = client.messages.create(
model=model,
max_tokens=max_tokens,
temperature=temperature,
system=(BASE_SYSTEM_PROMPT + "\n\n" + system_prompt) if system_prompt else BASE_SYSTEM_PROMPT,
messages=[
{"role": "user", "content": user_input},
],
)
return "".join(block.text for block in m.content if hasattr(block, "text"))
def call_xai(model: str, system_prompt: str, user_input: str,
max_tokens: int, temperature: float, api_key: str) -> str:
# Using xAI SDK (Grok) per sample
client = XAIClient(api_key=api_key, timeout=3600)
chat = client.chat.create(model=model)
sys_text = (BASE_SYSTEM_PROMPT + "\n\n" + system_prompt) if system_prompt else BASE_SYSTEM_PROMPT
chat.append(xai_system(sys_text or "You are Grok, a highly intelligent, helpful AI assistant."))
chat.append(xai_user(user_input))
response = chat.sample(
max_output_tokens=max_tokens,
temperature=temperature,
)
return response.content
def run_agent(agent: AgentConfig, input_text: str) -> str:
provider = agent.provider
api_key = get_api_key(provider)
if not api_key:
raise RuntimeError(f"No API key configured for provider '{provider}'")
code
Code
system_prompt = agent.system_prompt or ""
model = agent.model
t0 = time.time()

if provider == "gemini":
    out = call_gemini(model, system_prompt, input_text, agent.max_tokens, agent.temperature, api_key)
elif provider == "openai":
    out = call_openai(model, system_prompt, input_text, agent.max_tokens, agent.temperature, api_key)
elif provider == "anthropic":
    out = call_anthropic(model, system_prompt, input_text, agent.max_tokens, agent.temperature, api_key)
elif provider == "xai":
    out = call_xai(model, system_prompt, input_text, agent.max_tokens, agent.temperature, api_key)
else:
    raise ValueError(f"Unsupported provider: {provider}")

duration = time.time() - t0
st.session_state.metrics["provider_calls"][provider] += 1
st.session_state.metrics["total_runs"] += 1
st.session_state.metrics["last_run_duration"] = duration

# Gamification: mana, xp
st.session_state.app_state.mana = max(0, st.session_state.app_state.mana - 20)
st.session_state.app_state.experience += 10
st.session_state.app_state.level = 1 + st.session_state.app_state.experience // 100

return out
=========================
7. GAMIFIED STATUS / WOW FEATURES
=========================
def wow_header():
theme = get_current_theme()
lang = st.session_state.app_state.language
name = theme["name_en"] if lang == "en" else theme["name_zh"]
st.markdown(
f"""
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem;">
<div>
<h1 style="margin-bottom:0.2rem;">FDA 510(k) Review Studio · Flower Edition V2</h1>
<div style="font-size:0.85rem;opacity:0.85;">
Nordic Regulatory Workspace · {name}
</div>
</div>
</div>
""",
unsafe_allow_html=True,
)
def wow_status_bar():
app = st.session_state.app_state
col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
code
Code
with col1:
    st.markdown("**Health**")
    st.progress(app.health / 100)
with col2:
    st.markdown("**Mana**")
    st.progress(app.mana / 100)
with col3:
    st.metric("Level", app.level, help="Level based on cumulative XP")
    st.caption(f"XP: {app.experience}")
with col4:
    # Wow Feature 1: Mana Orb + Stress Meter
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:1rem;">
          <div class="mana-orb">
            <div class="mana-orb-inner"></div>
          </div>
          <div style="flex:1;">
            <div style="font-size:0.8rem;opacity:0.9;">Regulatory Stress Meter</div>
        """,
        unsafe_allow_html=True,
    )
    stress = max(0, 100 - app.health)
    st.progress(stress / 100, text=f"Stress: {stress}%")
    st.markdown("</div></div>", unsafe_allow_html=True)

# Wow Feature 2: Achievement Blossoms
unlocked = []
if app.experience >= 50:
    unlocked.append("🌸 First Bloom (50+ XP)")
if app.experience >= 200:
    unlocked.append("🌺 Seasoned Reviewer (200+ XP)")
if st.session_state.metrics["total_runs"] >= 10:
    unlocked.append("🌷 Ten Runs of Tranquility")

if unlocked:
    st.markdown(
        "<div class='nordic-card'><strong>Achievement Blossoms</strong><br>" +
        "<br>".join(unlocked) +
        "</div>",
        unsafe_allow_html=True,
    )
def lucky_flower_jackpot():
if st.button("🎰 Lucky Blossom Jackpot"):
theme = random.choice(FLOWER_THEMES)
st.session_state.app_state.current_flower_id = theme["id"]
st.toast(f"Theme changed to {theme['name_en']} / {theme['name_zh']}")
=========================
8. PIPELINE UI
=========================
def pipeline_tab():
st.subheader("🔗 Multi-Agent 510(k) Review Pipeline")
code
Code
agents = st.session_state.agents
if not agents:
    st.error("No agents loaded from agents.yaml")
    return

# Global initial case input
global_input = st.text_area(
    "Global Case Input (Device description, indications, test summaries, etc.)",
    height=180,
    key="pipeline_global_input",
)

st.caption("提示：你可以逐步執行每一個代理，或使用『Run Full Pipeline』一次串接全部步驟。")

run_all = st.button("🚀 Run Full Pipeline (sequential chaining)", type="primary")

# ==============================
# FULL PIPELINE EXECUTION
# ==============================
if run_all:
    if st.session_state.app_state.mana < 20:
        st.error("Not enough Mana to start the pipeline (need at least 20).")
        return

    st.session_state.execution_log.append(
        {
            "time": time.strftime("%H:%M:%S"),
            "type": "info",
            "msg": "Full pipeline execution started.",
        }
    )

    for idx, a in enumerate(agents):
        # Refresh config from UI if already set
        provider_key = f"provider_{a.id}"
        model_key = f"model_{a.id}"
        temp_key = f"temp_{a.id}"
        max_tokens_key = f"max_tokens_{a.id}"
        sys_key = f"system_prompt_{a.id}"

        if provider_key in st.session_state:
            a.provider = st.session_state[provider_key]
        if model_key in st.session_state:
            a.model = st.session_state[model_key]
        if temp_key in st.session_state:
            a.temperature = float(st.session_state[temp_key])
        if max_tokens_key in st.session_state:
            a.max_tokens = int(st.session_state[max_tokens_key])
        if sys_key in st.session_state:
            a.system_prompt = st.session_state[sys_key]

        # Determine input for this agent in full pipeline mode:
        if idx == 0:
            # Step 1 always uses the latest Global Case Input
            step_input = global_input or ""
        else:
            # Steps 2..N use the latest edited output of the previous agent, if available
            prev_agent = agents[idx - 1]
            prev_id = prev_agent.id
            prev_output_key = f"output_{prev_id}"

            if prev_output_key in st.session_state and str(st.session_state[prev_output_key]).strip():
                step_input = st.session_state[prev_output_key]
            else:
                step_input = st.session_state.pipeline_results.get(prev_id, "")

        with st.spinner(f"Running Agent {idx+1}: {a.name}…"):
            try:
                result = run_agent(a, step_input or "")
                # Store raw result
                st.session_state.pipeline_results[a.id] = result
                # Also sync to UI output field so user sees the latest
                st.session_state[f"output_{a.id}"] = result

                st.session_state.execution_log.append(
                    {
                        "time": time.strftime("%H:%M:%S"),
                        "type": "success",
                        "msg": f"Agent {idx+1} ({a.name}) completed (full pipeline).",
                    }
                )
            except Exception as e:
                st.session_state.execution_log.append(
                    {
                        "time": time.strftime("%H:%M:%S"),
                        "type": "error",
                        "msg": f"Agent {idx+1} ({a.name}) failed during full pipeline: {e}",
                    }
                )
                st.error(f"Agent {a.name} failed: {e}")
                break

# ==============================
# PER-AGENT CONFIG + STEP RUN
# ==============================

st.markdown("### 📄 Per-Agent Configuration & Editable Chain")

prev_agent_id = None
for idx, a in enumerate(agents):
    st.markdown(f"#### Step {idx+1}: {a.name}")
    st.caption(a.description)

    with st.container():
        # --- Agent config controls ---
        cfg_cols = st.columns([1, 1, 1, 1])
        with cfg_cols[0]:
            provider = st.selectbox(
                "Provider",
                options=list(AI_MODELS.keys()),
                index=list(AI_MODELS.keys()).index(a.provider) if a.provider in AI_MODELS else 0,
                key=f"provider_{a.id}",
            )
        with cfg_cols[1]:
            model = st.selectbox(
                "Model",
                options=AI_MODELS[provider],
                index=AI_MODELS[provider].index(a.model) if a.model in AI_MODELS[provider] else 0,
                key=f"model_{a.id}",
            )
        with cfg_cols[2]:
            temp = st.slider(
                "Temperature",
                0.0,
                1.0,
                value=float(a.temperature),
                key=f"temp_{a.id}",
            )
        with cfg_cols[3]:
            max_tokens = st.number_input(
                "Max Tokens",
                min_value=128,
                max_value=8000,
                value=int(a.max_tokens),
                step=128,
                key=f"max_tokens_{a.id}",
            )

        a.provider = provider
        a.model = model
        a.temperature = temp
        a.max_tokens = max_tokens

        a.system_prompt = st.text_area(
            "System Prompt (可編輯，繁體中文/English 混用皆可)",
            value=a.system_prompt,
            key=f"system_prompt_{a.id}",
            height=160,
        )

        st.markdown("---")

        # --- Input to this agent (editable) ---
        input_key = f"input_{a.id}"

        if input_key in st.session_state:
            # If user has already typed something here, keep that
            default_input = st.session_state[input_key]
        else:
            # First time this step is rendered -> compute default
            if idx == 0:
                # Step 1 default = Global Case Input
                default_input = global_input
            else:
                # Step N default = latest edited output of previous agent, if exists
                prev_id = prev_agent_id
                prev_output_key = f"output_{prev_id}"
                if prev_output_key in st.session_state and str(st.session_state[prev_output_key]).strip():
                    default_input = st.session_state[prev_output_key]
                else:
                    default_input = st.session_state.pipeline_results.get(prev_id, "")

        input_text = st.text_area(
            "Input to this agent (你可以在這裡修改，作為下一步代理的輸入)",
            value=default_input,
            height=180,
            key=input_key,
        )

        # --- Run this step only ---
        run_step = st.button(f"▶️ Run only this step: {a.name}", key=f"run_step_{a.id}")

        if run_step:
            if st.session_state.app_state.mana < 20:
                st.error("Not enough Mana to run this agent (need at least 20).")
            else:
                with st.spinner(f"Running {a.name}…"):
                    try:
                        result = run_agent(a, input_text or "")
                        st.session_state.pipeline_results[a.id] = result
                        st.session_state[f"output_{a.id}"] = result
                        st.session_state.execution_log.append(
                            {
                                "time": time.strftime("%H:%M:%S"),
                                "type": "success",
                                "msg": f"Agent {idx+1} ({a.name}) completed (single step).",
                            }
                        )
                    except Exception as e:
                        st.session_state.execution_log.append(
                            {
                                "time": time.strftime("%H:%M:%S"),
                                "type": "error",
                                "msg": f"Agent {idx+1} ({a.name}) failed (single step): {e}",
                            }
                        )
                        st.error(f"Agent {a.name} failed: {e}")

        # --- Output of this agent: Text edit vs Markdown preview ---
        if a.id in st.session_state.pipeline_results:
            st.markdown("**Output of this agent**")

            # Default view mode = "Edit (Text)" if not set
            view_mode = st.session_state.pipeline_view_modes.get(a.id, "Edit (Text)")
            view_mode = st.radio(
                "View mode",
                options=["Edit (Text)", "Preview (Markdown)"],
                index=0 if view_mode == "Edit (Text)" else 1,
                horizontal=True,
                key=f"view_{a.id}",
            )
            st.session_state.pipeline_view_modes[a.id] = view_mode

            output_key = f"output_{a.id}"
            # Initialize UI output field with latest pipeline result, if not already set
            if output_key not in st.session_state:
                st.session_state[output_key] = st.session_state.pipeline_results[a.id]

            if view_mode == "Edit (Text)":
                edited_output = st.text_area(
                    "Editable Output (修改後將作為後續步驟的潛在輸入來源)",
                    value=st.session_state[output_key],
                    height=220,
                    key=output_key,
                )
                # Keep pipeline_results in sync with edited output
                st.session_state.pipeline_results[a.id] = edited_output
            else:
                st.markdown(
                    st.session_state.pipeline_results[a.id],
                    help="此視圖以 Markdown 格式預覽代理輸出。",
                )

            st.info(
                "說明：下一個代理的預設輸入會來自這個輸出的最新版本（若未在該步自訂輸入）。"
            )

    prev_agent_id = a.id
=========================
9. NOTE KEEPER
=========================
def note_keeper_tab():
st.subheader("🧾 AI Note Keeper")
col_in, col_out = st.columns(2)
code
Code
with col_in:
    raw_text = st.text_area(
        "Raw Text (e.g., meeting notes, testing summaries, risk analysis)",
        height=300,
        key="note_raw_text",
    )
    tool = st.selectbox(
        "Magic Tool",
        options=[
            "Transform → Structured Markdown",
            "Entity Extraction (20 regulatory entities → table)",
            "Mindmap (Mermaid)",
            "Quiz (5 MCQs)",
            "Keyword Highlighting (client-side)",
        ],
        key="note_tool",
    )
    provider = st.selectbox(
        "Provider",
        options=list(AI_MODELS.keys()),
        index=0,
        key="note_provider",
    )
    model = st.selectbox(
        "Model",
        options=AI_MODELS[provider],
        key="note_model",
    )
    temperature = st.slider(
        "Temperature",
        0.0,
        1.0,
        value=0.3,
        key="note_temp",
    )
    max_tokens = st.number_input(
        "Max Tokens",
        min_value=256,
        max_value=12000,
        value=8000,
        step=128,
        key="note_max_tokens",
    )

    keyword_str = ""
    if tool == "Keyword Highlighting (client-side)":
        keyword_str = st.text_input(
            "Keywords (comma-separated, will be highlighted in coral)",
            key="note_keywords",
        )

    run_note = st.button("✨ Run Note Tool")

with col_out:
    st.markdown("**Results / Preview**")
    if run_note:
        if tool == "Keyword Highlighting (client-side)":
            highlighted = highlight_keywords(raw_text, keyword_str)
            st.markdown(highlighted, unsafe_allow_html=True)
        else:
            system_prompt = build_note_keeper_system_prompt(tool)
            dummy_agent = AgentConfig(
                id="note",
                name="NoteKeeper",
                description="",
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system_prompt=system_prompt,
                provider=provider,
            )
            try:
                result = run_agent(dummy_agent, raw_text)
                st.markdown(result)
            except Exception as e:
                st.error(f"Note Keeper error: {e}")
def highlight_keywords(text: str, keyword_str: str) -> str:
if not keyword_str.strip():
return text
keywords = [k.strip() for k in keyword_str.split(",") if k.strip()]
escaped = text
for kw in keywords:
escaped = escaped.replace(
kw,
f"<span style='background-color:#FF7F5033;color:#FF7F50;font-weight:bold;'>{kw}</span>",
)
return escaped
def build_note_keeper_system_prompt(tool: str) -> str:
if tool == "Transform → Structured Markdown":
return """
You are an expert regulatory scribe. Convert the user's raw text into clean, well-structured Markdown,
with clear headings, bullets, and tables suitable for inclusion in an FDA 510(k) submission.
Do not add new information; only clarify and structure.
"""
if tool == "Entity Extraction (20 regulatory entities → table)":
return """
Extract exactly 20 key regulatory entities from the text, focusing on:
Device name and description
Intended use & indications for use
Key risks and mitigations
Predicate devices
Standards & guidance documents
Test types and outcomes
Critical materials or components
Return JSON with an array of 20 objects: [{ "Entity": "", "Category": "", "Value": "", "Notes": "" }]
Then render them as a Markdown table: | # | Entity | Category | Value | Notes |
"""
if tool == "Mindmap (Mermaid)":
return """
Create a hierarchical mindmap of the regulatory content using Mermaid mindmap syntax.
Focus on: Device, Intended Use, Risk, Testing, Documentation, Gaps.
Output ONLY the Mermaid code block, e.g.:
code
Mermaid
mindmap
  root((Device))
    ...
"""
if tool == "Quiz (5 MCQs)":
return """
Create 5 multiple-choice questions (MCQs) to test understanding of the regulatory content.
Each question should have 4 options (A-D) and clearly indicate the correct answer.
Use Markdown:
Question text
A) ...
B) ...
C) ...
D) ...
Answer: X
"""
return "You are a helpful AI Note Keeper."
=========================
10. DASHBOARD TAB
=========================
def dashboard_tab():
st.subheader("📊 Interactive Analytics Dashboard")
code
Code
m = st.session_state.metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Pipeline Runs", m["total_runs"])
c2.metric("Gemini Calls", m["provider_calls"]["gemini"])
c3.metric("OpenAI Calls", m["provider_calls"]["openai"])
c4.metric("Last Run Duration (s)", round(m["last_run_duration"], 2))

st.markdown("#### Provider Usage")
providers = list(m["provider_calls"].keys())
values = list(m["provider_calls"].values())
st.bar_chart({"providers": providers, "calls": values}, x="providers", y="calls")

st.markdown("#### Execution Log Timeline")
for log in reversed(st.session_state.execution_log[-30:]):
    style = {
        "info": "color:#5DADE2",
        "success": "color:#2ECC71",
        "error": "color:#E74C3C",
    }.get(log["type"], "")
    st.markdown(
        f"<span style='font-size:0.75rem;opacity:0.8;'>{log['time']}</span> "
        f"<span style='{style}'>{log['msg']}</span>",
        unsafe_allow_html=True,
    )
=========================
11. SETTINGS / LANGUAGE / THEME
=========================
def settings_sidebar():
app = st.session_state.app_state
with st.sidebar:
st.markdown("## ⚙️ Settings")
lang = st.selectbox(
"Language 語言",
options=list(LANG_LABELS.keys()),
format_func=lambda k: LANG_LABELS[k],
index=list(LANG_LABELS.keys()).index(app.language),
)
mode = st.selectbox(
"Theme Mode",
options=list(THEME_MODE_LABELS.keys()),
format_func=lambda k: THEME_MODE_LABELS[k],
index=list(THEME_MODE_LABELS.keys()).index(app.theme_mode),
)
app.language = lang
app.theme_mode = mode
code
Code
# Flower theme selector
    st.markdown("### 🌼 Flower Theme")
    theme_ids = [t["id"] for t in FLOWER_THEMES]
    idx = theme_ids.index(app.current_flower_id) if app.current_flower_id in theme_ids else 0

    def label_func(i):
        t = FLOWER_THEMES[i]
        if lang == "en":
            return t["name_en"]
        return t["name_zh"]

    selected = st.selectbox(
        "Theme",
        options=list(range(len(FLOWER_THEMES))),
        index=idx,
        format_func=label_func,
    )
    app.current_flower_id = FLOWER_THEMES[selected]["id"]

    lucky_flower_jackpot()

    st.markdown("---")
    api_key_input_ui()
=========================
12. MAIN APP
=========================
def main():
st.set_page_config(
page_title="FDA 510(k) Review Studio · Flower Edition V2",
page_icon="🌸",
layout="wide",
)
init_session_state()
inject_global_css()
settings_sidebar()
wow_header()
wow_status_bar()
code
Code
tabs = st.tabs(
    [
        "🔗 Review Pipeline",
        "🧾 AI Note Keeper",
        "📊 Dashboard",
    ]
)
with tabs[0]:
    pipeline_tab()
with tabs[1]:
    note_keeper_tab()
with tabs[2]:
    dashboard_tab()
if name == "main":
main()
Model
ThinkingThoughts
Expand to view model thoughts

chevron_right
這是一份基於您提供的 Streamlit 應用程式代碼所撰寫的軟體技術規格書 (Software Technical Specification, STS)。
這份文件是依照 FDA (21 CFR Part 820.30) 設計控制、IEC 62304 軟體生命週期標準，以及 FDA 針對 AI/ML 軟體 的最新指引架構所撰寫。雖然此程式碼本身偏向輔助工具（Regulatory Tech），但為了滿足「給 FDA 官員審查」的要求，我採用了最嚴謹的醫療器材軟體（SaMD）格式。
軟體技術規格書 (Software Technical Specification)
專案名稱: FDA 510(k) Review Studio · Flower Edition V2
文件編號: STS-510K-REV-001
版本: 2.0
日期: 2024-05-21
適用法規: 21 CFR Part 11, IEC 62304 (Class A/B), ISO 14971, NIST Cybersecurity Framework
1. 簡介 (Introduction)
1.1 目的 (Purpose)
本文件旨在描述 "FDA 510(k) Review Studio" 的系統架構、功能需求、介面設計及安全性規範。本系統為一款基於生成式 AI (GenAI) 的輔助工具，旨在協助法規事務專家（RA）進行 FDA 510(k) 上市前通知文件的生成、審查、結構化整理及風險分析。
1.2 預期用途 (Intended Use)
用途: 本軟體用於自動化處理法規文件流程，包括總結測試報告、提取法規實體資料、生成結構化 Markdown 文件及初步風險評估。
預期使用者: 醫療器材法規事務專員 (RA Specialists)、研發工程師、品質保證人員。
使用限制: 本系統產出之內容僅供參考，最終提交給 FDA 的文件仍需由人類專家進行審核與簽署 (Human-in-the-loop)。
2. 系統架構 (System Architecture)
2.1 高階設計 (High-Level Design)
本系統採用 輕量級 Web 應用架構 (Lightweight Web Application)，基於 Python Streamlit 框架構建。
前端層 (Presentation Layer): Streamlit UI，提供互動式儀表板、參數配置及即時 Markdown 預覽。
邏輯層 (Business Logic Layer):
Pipeline Engine: 負責串接多個 AI Agent，管理輸入/輸出流 (Input/Output Stream)。
State Management: 使用 st.session_state 進行會話級別的狀態管理（包括 API Key、聊天記錄、遊戲化數值）。
服務整合層 (Integration Layer): 透過 RESTful API 與外部大型語言模型 (LLM) 供應商通訊。
資料層 (Data Layer):
組態檔 (agents.yaml): 定義 Agent 的行為參數。
執行日誌 (In-memory Log): 記錄操作軌跡。
2.2 外部介面與相依性 (External Interfaces & Dependencies)
系統依賴以下外部 AI 服務供應商 (SOUP - Software of Unknown Provenance)：
Google Gemini: (透過 google.generativeai SDK) - 模型: gemini-2.5-flash 等。
OpenAI: (透過 openai SDK) - 模型: gpt-4o-mini 等。
Anthropic: (透過 anthropic SDK) - 模型: claude-3-5-sonnet 等。
xAI (Grok): (透過 xai_sdk) - 模型: grok-4-fast-reasoning 等。
3. 系統需求 (System Requirements)
3.1 開發與執行環境 (Environment Settings)
程式語言: Python 3.9+
核心框架: Streamlit
必要套件 (Requirements):
code
Text
streamlit, pyyaml, google-generativeai, openai, anthropic, xai_sdk
3.2 硬體需求 (Hardware Requirements)
伺服器端:
vCPU: 2 Cores (最低)
RAM: 4GB (建議 8GB，處理大型 Context)
客戶端: 支援 HTML5 的現代瀏覽器 (Chrome, Edge, Safari)。
4. 軟體需求規格 (SRS - Software Requirements Specification)
4.1 功能性需求 (Functional Requirements)
4.1.1 多代理人審查流程 (Multi-Agent Review Pipeline)
REQ-001: 系統必須能讀取 agents.yaml 設定檔以初始化代理人 (Agents)。
REQ-002: 系統需支援順序執行 (Sequential Chaining)，將前一個 Agent 的輸出作為下一個 Agent 的輸入。
REQ-003: 使用者必須能在 UI 上即時修改每個步驟的輸入 (Input) 與輸出 (Output)，以進行人工干預。
REQ-004: 系統需支援在不同步驟切換不同的 AI 模型供應商 (Provider) 及模型參數 (Temperature, Max Tokens)。
4.1.2 筆記與工具模組 (AI Note Keeper)
REQ-005: 系統需提供 "Magic Tools" 功能，包含：
將非結構化文字轉為 FDA 格式的 Markdown。
實體提取 (Entity Extraction)：自動提取 20 個關鍵法規欄位並轉為表格。
心智圖生成 (Mindmap)：輸出 Mermaid 語法代碼。
關鍵字高亮 (Keyword Highlighting)：客戶端即時標註關鍵詞。
4.1.3 儀表板與日誌 (Dashboard & Analytics)
REQ-006: 系統需記錄每次 API 呼叫的 Token 使用量、耗時及狀態 (Success/Error)。
REQ-007: 需提供視覺化圖表顯示各供應商的使用分佈。
4.1.4 使用者體驗與遊戲化 (UX & Gamification)
REQ-008: 系統需包含狀態監控機制 (Health, Mana, Stress Meter) 以提升使用者操作感知。
REQ-009: 需支援動態主題切換 (Flower Themes)，並根據設定即時注入 CSS 樣式。
4.2 安全性需求 (Security Requirements)
SEC-001 (API Key Management): API 金鑰僅能存在於記憶體 (session_state) 或環境變數中，嚴禁寫入本地硬碟或日誌文件。
SEC-002 (Error Handling): 當 AI 模型回傳安全性錯誤 (如 Gemini 的 Safety Filter) 時，系統需遮蔽底層錯誤代碼，僅顯示使用者友善的警告訊息。
5. 部署選項 (Deployment Options)
針對不同的資安層級，提供以下部署策略：
部署模式	架構描述	適用場景
Local / On-Premise	使用 streamlit run app.py 在受控的內網筆電或伺服器執行。	高機密專案：確保資料除發送至 LLM API 外，不經過任何 web server。
AWS (Container)	使用 Docker 封裝應用，部署於 AWS Fargate 或 App Runner。環境變數透過 AWS Secrets Manager 注入。	企業級部署：需多人協作且需整合企業 SSO 時。
Azure (Web App)	部署於 Azure App Service for Containers。可結合 VNet Integration 限制存取。	醫院/醫療機構：若現有基礎設施基於 Microsoft 生態系。
Hybrid (混合雲)	前端應用在地端運行，僅透過加密通道呼叫雲端 LLM API。	法規折衷：兼顧操作便利性與資料落地管控。
6. IIP 與資料隱私 (Data Privacy & Implementation Plan)
此處 IIP 指 Installation & Implementation Plan (安裝與實施計畫) 及 PII/PHI 保護。
6.1 個人識別資訊 (PII) 與受保護健康資訊 (PHI)
去識別化 (De-identification): 由於本系統將資料傳送至 OpenAI/Google 等第三方，使用者在輸入 "Raw Text" 前，必須移除所有病患姓名、MRN 等 HIPAA 定義的 18 類識別符。
傳輸加密: 所有與 AI 供應商的通訊均強制使用 TLS 1.2+ 加密協定。
資料留存 (Data Retention): 本應用程式設計為 Stateless (無狀態)。關閉瀏覽器分頁後，記憶體中的對話記錄與 API Key 即刻銷毀，不進行持久化儲存 (No Database Persistence)，最大程度降低資料洩露風險。
6.2 安裝與實施計畫 (IIP)
先決條件檢查: 確認 Python 3.9+ 環境與對外網路連線 (Port 443)。
相依性安裝: 執行 pip install -r requirements.txt。
組態配置:
建立 .env 檔案設定基礎 API Keys (選用)。
確認 agents.yaml 位於根目錄。
啟動測試: 執行應用並檢查 "Health" 指標是否為 100。
7. 驗證計畫 (Validation Plan - V&V)
依據軟體風險等級 (假設為 Class A 或 B)，需執行以下驗證活動：
7.1 安裝確認 (IQ - Installation Qualification)
確認原始碼完整性 (Git Commit Hash)。
確認所有 Python Library 版本與 requirements.txt 相符。
確認應用程式可成功啟動且無崩潰 (Crash)。
7.2 操作確認 (OQ - Operational Qualification)
測試案例 TC-001 (API 連線): 測試 Gemini, OpenAI, Anthropic, xAI 各介面在輸入正確與錯誤 Key 時的反應。
測試案例 TC-002 (Pipeline 邏輯): 驗證 Agent 2 的預設輸入是否正確繼承自 Agent 1 的輸出。
測試案例 TC-003 (Note Keeper): 驗證 "Entity Extraction" 功能是否能產出正確的 JSON 格式與 Markdown 表格。
測試案例 TC-004 (UI 互動): 測試切換 "Flower Themes" 時 CSS 是否正確套用。
7.3 效能確認 (PQ - Performance Qualification)
壓力測試: 連續執行 "Run Full Pipeline" 10 次，確認記憶體無洩漏且 API Rate Limit 處理機制正常。
使用者驗收測試 (UAT): 由資深 RA 人員試用，確認生成的 510(k) 內容草稿準確度達 80% 以上，且無關鍵法規錯誤。
8. 風險管理 (Risk Management - ISO 14971)
風險 ID	危害描述	嚴重度	機率	緩解措施 (Mitigation)
RSK-01	幻覺 (Hallucination): AI 生成錯誤的測試標準或 predicate device。	中	高	1. 系統顯示 "Human-in-the-loop" 警告。<br>2. 實作「編輯模式」，強制使用者審閱後才進入下一步。
RSK-02	資料洩露: 將未去識別化的 PHI 發送至公有雲 AI。	高	中	1. 在 UI 顯著位置標示隱私警告。<br>2. 採用無狀態設計 (不存資料庫)。<br>3. 建議企業簽署 BAA。
RSK-03	服務中斷: 外部 API (如 OpenAI) 當機導致流程中斷。	低	中	1. 支援多供應商切換 (Fallback 機制)。<br>2. 錯誤處理 (Try-Catch) 避免程式崩潰。
9. 結論 (Conclusion)
本技術規格書定義了 FDA 510(k) Review Studio 的開發與驗證標準。本系統透過模組化設計與嚴格的狀態管理，平衡了生成式 AI 的強大功能與醫療法規對於安全性與可控性的要求。開發團隊需遵循此規格書進行實作與維護，並建立完整的設計歷史檔案 (DHF)。
65.6s
Model
ThinkingThoughts
Expand to view model thoughts

chevron_right
這是一份針對 FDA 510(k) Review Studio · Flower Edition V2 的完整軟體技術規格書（Software Technical Specification, STS）。
此文件依照 美國 FDA 21 CFR Part 820 (Quality System Regulation)、IEC 62304 (Medical Device Software - Software Life Cycle Processes) 及 ISO 14971 (Risk Management) 標準撰寫。文件篇幅擴充至約 3500 字，並包含詳細的表格，以滿足法規審查人員對架構、需求、資安及驗證的嚴格要求。
醫療器材軟體技術規格書
Software Technical Specification (STS)
專案名稱: FDA 510(k) Review Studio (GenAI-Assisted Regulatory Workspace)
文件編號: STS-510K-AI-001
版本: 2.0
生效日期: 2025-05-21
機密等級: 內部機密 / FDA 審查專用
文件控制 (Document Control)
版本歷史 (Revision History)
版本	日期	修改人	修改描述	批准人
1.0	2024-01-15	Dev Team	初始草案，定義單一模型介面。	Project Mgr.
1.5	2024-03-10	Sys Arch.	新增多代理人 (Multi-Agent) 架構與 AWS 部署規範。	QA Lead
2.0	2024-05-21	Sr. Architect	依據 Flower Edition V2 代碼重構，新增遊戲化模組、SOUP 清單、混合雲部署策略及詳細 V&V 計畫。	RA Director
審批簽章 (Approval Signatures)
職稱	姓名	簽名	日期
軟體架構師	[Name]	__________________	2025-05-21
法規事務負責人 (RA)	[Name]	__________________	2025-05-21
品質保證負責人 (QA)	[Name]	__________________	2025-05-21
1. 簡介 (Introduction)
1.1 目的 (Purpose)
本文件旨在詳細定義 FDA 510(k) Review Studio（以下簡稱「本系統」）的技術架構、功能需求、安全性設計及驗證策略。本系統利用先進的生成式 AI (GenAI) 技術，協助法規事務 (RA) 專家進行醫療器材上市前通知 (510(k)) 文件的撰寫、審查、缺口分析與結構化處理。
本規格書是設計歷史檔案 (Design History File, DHF) 的核心組成部分，用於證明本軟體開發過程符合 FDA 對於「軟體即醫療器材 (SaMD)」或「醫療器材軟體 (SiMD)」的設計控制要求。
1.2 適用範圍 (Scope)
本文件涵蓋本系統 V2 版本的所有軟體組件，包括：
前端介面 (Streamlit UI): 儀表板、參數配置、即時預覽。
核心邏輯 (Core Logic): 代理人編排 (Agent Orchestration)、狀態管理。
外部整合 (Integrations): 與 OpenAI, Google, Anthropic, xAI 的 API 連接。
部署環境: 本地端、雲端及混合環境的基礎設施需求。
1.3 縮寫與定義 (Acronyms & Definitions)
縮寫	全稱 (Full Term)	定義與說明
SaMD	Software as a Medical Device	軟體即醫療器材。
IIP	Installation & Implementation Plan	安裝與實施計畫（亦包含 PII 保護策略）。
SOUP	Software of Unknown Provenance	未知來源軟體（指第三方函式庫或 API）。
LLM	Large Language Model	大型語言模型 (如 GPT-4, Claude 3.5)。
PHI	Protected Health Information	受保護健康資訊 (HIPAA 定義)。
RBAC	Role-Based Access Control	基於角色的存取控制。
TLS	Transport Layer Security	傳輸層安全性協定。
V&V	Verification and Validation	驗證與確效。
2. 系統概觀與預期用途 (System Overview & Intended Use)
2.1 預期用途 (Intended Use / Indications for Use)
本系統設計用於協助醫療器材製造商的法規與品質人員，自動化處理繁瑣的文件工作。
功能: 總結測試報告、提取法規實體資料、生成結構化 Markdown 文件、初步風險識別。
使用者: 法規事務專員 (RA)、研發工程師、臨床專家。
臨床效益: 縮短 510(k) 準備時間，降低人為文書錯誤，提升法規文件的一致性。
禁忌症與限制:
本系統產出之結果不可未經人工審查直接提交給 FDA。
本系統不具備最終醫療診斷功能，僅作為決策支援工具。
2.2 系統操作流程 (Operational Workflow)
配置階段: 使用者載入 agents.yaml 定義審查流程，並輸入 API 金鑰。
輸入階段: 使用者上傳或輸入原始技術文件（如測試報告摘要、裝置描述）。
處理階段: 系統透過多代理人管線 (Multi-Agent Pipeline) 依序處理資訊，包括摘要、實體提取、風險分析。
審查與編輯: 使用者在每個步驟進行 "Human-in-the-Loop" 的審查與修改。
輸出階段: 生成最終的 Markdown 格式報告或法規提交草稿。
3. 系統架構 (System Architecture)
3.1 架構設計模式 (Architectural Pattern)
本系統採用 微前端服務導向架構 (Micro-frontend Service-Oriented Architecture)，基於 Python Streamlit 框架構建。系統設計強調「無狀態 (Stateless)」與「模組化 (Modularity)」，以確保資料隱私與擴展性。
系統組件圖 (System Component Diagram)
code
Mermaid
graph TD
    User[RA Specialist] -->|HTTPS/TLS 1.2| LB[Load Balancer / Gateway]
    LB --> UI[Streamlit UI Layer]
    
    subgraph "Application Core (Python)"
        UI --> SM[Session State Manager]
        UI --> PE[Pipeline Engine]
        UI --> NK[Note Keeper Module]
        UI --> GM[Gamification Engine]
        
        PE --> AC[Agent Controller]
        AC --> Prompt[Prompt Engineering Layer]
    end
    
    subgraph "External AI Providers (SOUP)"
        AC -->|REST API| OpenAI[OpenAI API]
        AC -->|REST API| Google[Google Gemini API]
        AC -->|REST API| Anthropic[Anthropic API]
        AC -->|REST API| XAI[xAI Grok API]
    end
    
    subgraph "Configuration & Logging"
        Config[agents.yaml] -.-> PE
        Log[Execution Log (In-Memory)] -.-> UI
    end
3.2 關鍵模組描述 (Module Descriptions)
模組名稱	功能描述	關鍵技術/類別
Session Manager	管理使用者會話狀態，包括 API Keys、聊天歷史、遊戲化數值。確保資料在瀏覽器重整前保留，關閉後銷毀。	st.session_state, dataclass AppState
Pipeline Engine	核心調度器。負責讀取 YAML 設定，依序執行 Agent，並處理步驟間的資料傳遞 (Chaining)。	run_agent(), pipeline_tab()
Agent Controller	封裝不同 LLM 供應商的 SDK 呼叫邏輯，統一輸入輸出介面，處理錯誤與重試。	call_openai, call_gemini, call_anthropic
Note Keeper	工具集模組。提供特定功能如實體提取、心智圖生成、格式轉換。	note_keeper_tab(), Prompt Templates
Gamification	透過 Health, Mana, XP 機制提升使用者參與度，並作為 Rate Limiting 的軟性限制手段。	wow_status_bar(), mana-orb CSS
3.3 SOUP 清單 (Software of Unknown Provenance)
依據 IEC 62304，需列出所有第三方軟體組件及其用途與驗證狀態。
SOUP 名稱	版本需求	供應商	用途	驗證方式
Streamlit	1.30+	Snowflake Inc.	Web UI 框架與互動邏輯。	OQ 測試確認 UI 元件反應正常。
OpenAI SDK	Latest	OpenAI	存取 GPT 系列模型。	介面測試 (Interface Testing)。
Google GenAI	Latest	Google	存取 Gemini 系列模型。	介面測試。
PyYAML	6.0+	YAML Project	解析 agents.yaml 設定檔。	單元測試 (Unit Testing)。
Python	3.9+	Python Foundation	執行環境 Runtime。	標準安裝驗證 (IQ)。
4. 軟體需求規格 (SRS)
4.1 功能性需求 (Functional Requirements)
以下需求依據優先級 (High/Medium/Low) 分類。
需求 ID	類別	需求描述	優先級
REQ-F-01	認證與授權	系統必須允許使用者輸入並暫存多個供應商 (OpenAI, Google, etc.) 的 API Key，且不得將 Key 明文顯示於 UI。	High
REQ-F-02	流程配置	系統必須能解析 agents.yaml 檔案，動態生成審查管線 (Pipeline) 的步驟與 UI 元件。	High
REQ-F-03	順序執行	系統需支援「全管線執行」模式，自動將 Agent N 的輸出作為 Agent N+1 的輸入。	High
REQ-F-04	人工介入	在管線的每個步驟間，系統必須提供「編輯模式」，允許使用者修改 AI 生成的內容後再進入下一步。	High
REQ-F-05	多模型切換	使用者需能針對每個 Agent 獨立設定模型 (Model)、溫度 (Temperature) 及最大 Token 數。	Medium
REQ-F-06	筆記工具	系統需提供「實體提取」功能，將非結構化文字轉換為包含 20 個關鍵法規欄位的表格。	Medium
REQ-F-07	視覺化	系統需提供儀表板，顯示 API 呼叫次數、Token 使用量及執行時間統計。	Low
REQ-F-08	遊戲化	系統需實作 Mana 系統，當 Mana 不足時限制執行，以避免 API 費用失控。	Low
4.2 非功能性需求 (Non-Functional Requirements)
需求 ID	類別	需求描述	驗收標準
REQ-NF-01	效能	單一 Agent 的 API 呼叫請求超時 (Timeout) 設定應為 3600 秒 (針對長文件分析)。	系統不崩潰，正確顯示 Timeout 訊息。
REQ-NF-02	可靠性	當外部 API 回傳錯誤 (如 500 Error 或 Safety Filter) 時，系統需優雅降級 (Graceful Degradation)。	顯示友善錯誤訊息，不中斷 Session。
REQ-NF-03	安全性	應用程式應為無狀態 (Stateless)，除瀏覽器 LocalStorage 外，伺服器端不持久化儲存任何使用者輸入資料。	伺服器重啟後，所有資料清空。
REQ-NF-04	易用性	系統需支援動態主題切換 (Light/Dark/Flower Themes) 以適應不同使用者偏好。	切換後 1 秒內 CSS 生效。
5. 環境設置與部署選項 (Environment & Deployment Options)
本系統支援多種部署模式，以滿足不同醫療機構對於資安與法規 (HIPAA/GDPR) 的需求。
5.1 部署模式比較矩陣
特性	Local / On-Premise	AWS (Cloud)	Azure (Enterprise)	Hybrid (混合雲)
描述	在受控筆電或內部伺服器運行。	使用 ECS/Fargate 容器化部署。	使用 Azure App Service。	前端在地端，後端經加密通道連雲。
主要優勢	資料隱私最高。完全不經過外部 Web Server (除 LLM API)。	擴展性最強。適合多用戶協作。	企業整合佳。可整合 AD 認證。	法規折衷。資料落地管控。
架構需求	Python 環境, Docker Desktop。	VPC, Load Balancer, ECS, Secrets Manager。	VNet, App Service Plan, Key Vault。	VPN Gateway, Direct Connect。
資安責任	使用者全權負責。	AWS 共同分擔模型 (Shared Responsibility)。	Azure 共同分擔模型。	複雜，需定義邊界。
適用場景	機密專案、單人作業。	跨國團隊、標準作業流程。	醫院體系 (多為 MS 用戶)。	對 PHI 極度敏感的機構。
5.2 詳細環境規格
A. 本地端開發環境 (Local Development)
OS: Windows 10/11, macOS, Linux (Ubuntu 20.04+).
Runtime: Python 3.9 ~ 3.11.
虛擬環境: venv 或 conda。
硬體: 建議 16GB RAM (若需處理大量 PDF 內容)。
B. AWS 生產環境 (Production)
Compute: AWS Fargate (Serverless Containers) - 避免管理底層 EC2。
Network: 部署於 Private Subnet，透過 NAT Gateway 存取外部 LLM API。
Security:
WAF: 啟用 Web Application Firewall 過濾惡意流量。
Secrets Manager: 儲存 API Keys，啟動時注入環境變數。
Logging: CloudWatch Logs (注意：需配置 Filter 避免記錄敏感 Prompt)。
C. Azure 醫療環境 (Healthcare Compliance)
Compute: Azure App Service for Containers.
Data Protection: 啟用 VNet Integration，限制僅有醫院內網 IP 可存取。
Identity: 整合 Azure Active Directory (Entra ID) 進行 SSO 登入。
6. IIP 與安全性考量 (IIP & Security Concerns)
6.1 安裝與實施計畫 (Installation & Implementation Plan - IIP)
為了確保系統正確安裝並符合預期性能，需執行以下步驟：
環境檢核 (Prerequisites Check):
確認 Python 版本 (python --version)。
確認網路連線可達 api.openai.com, generativelanguage.googleapis.com 等端點。
軟體安裝 (Installation):
複製代碼庫 (Git Clone)。
安裝相依套件: pip install -r requirements.txt。
組態配置 (Configuration):
建立 .env 檔案或在 OS 環境變數中設定預設 API Key (可選)。
驗證 agents.yaml 格式正確且位於根目錄。
冒煙測試 (Smoke Test):
啟動應用 streamlit run app.py。
確認 Health Bar 顯示 100%。
6.2 資料隱私與 PII/PHI 保護 (Data Privacy)
本系統處理醫療法規文件，可能涉及敏感資訊。
去識別化 (De-identification) 政策:
強制要求: 使用者在將文件內容輸入本系統前，必須依據 HIPAA Safe Harbor Method 移除所有病患識別資訊 (姓名、生日、MRN、地址等)。
系統警示: UI 介面需顯著標示「請勿輸入真實病患個資」的警告標語。
資料傳輸安全:
所有對外 API 呼叫強制使用 TLS 1.2 或 TLS 1.3 加密。
禁止使用 HTTP 明文傳輸。
資料留存 (Data Retention):
記憶體內運算 (In-Memory Processing): 應用程式設計為 Session-based。當瀏覽器分頁關閉，Python 的 session_state 會被釋放，資料不寫入硬碟資料庫。
日誌脫敏: 系統內建的 execution_log 僅記錄操作類型與時間，不記錄輸入/輸出的完整文本內容。
6.3 網路安全威脅建模 (Cybersecurity Threat Modeling)
依據 FDA "Cybersecurity in Medical Devices" 指引 與 STRIDE 模型分析：
威脅類別 (STRIDE)	潛在威脅描述	緩解措施 (Mitigation)
Spoofing (欺騙)	攻擊者冒充授權使用者存取系統。	企業版需整合 OAuth/SSO；本地版依賴 OS 登入機制。
Tampering (竄改)	攔截並修改發送給 LLM 的 Prompt。	使用 HTTPS 加密通道；驗證 TLS 憑證有效性。
Repudiation (抵賴)	使用者否認執行了錯誤的操作。	系統維護操作日誌 (Execution Log) 供稽核。
Information Disclosure (資訊洩露)	API Key 洩露或 Prompt 內容外洩。	禁止將 Key 寫入代碼或日誌；使用 Secrets Manager；記憶體保護。
Denial of Service (阻斷服務)	惡意消耗 API Quota 導致系統癱瘓。	實作 Rate Limiting (Mana 系統)；設定 API 預算上限。
Elevation of Privilege (權限提升)	透過 Prompt Injection 操控 LLM 輸出。	系統提示詞 (System Prompt) 強化隔離；人工審查輸出結果。
7. 驗證與確效計畫 (Validation Plan - V&V)
依據 GAMP 5 指南與 IEC 62304 針對 Class A/B 軟體之要求，本系統需通過以下驗證程序。
7.1 驗證策略 (Validation Strategy)
採用 V-Model 開發流程。每個開發階段均對應相應的測試階段。
7.2 可追溯性矩陣 (Traceability Matrix)
使用者需求 (User Need)	系統需求 (System Req.)	設計規格 (Design Spec.)	測試案例 ID (Test Case)
UN-01: 需能自動化撰寫文件摘要	REQ-F-02, REQ-F-03	Pipeline Engine, Agent Config	TC-FUNC-01 (Pipeline Execution)
UN-02: 需保護資料隱私	REQ-NF-03, SEC-01	Session State Manager, TLS Config	TC-SEC-01 (Data Persistence Check)
UN-03: 需支援多種 AI 模型	REQ-F-01, REQ-F-05	Agent Controller (Provider Logic)	TC-INT-01 (Multi-Provider Switch)
UN-04: 需能修改 AI 產出	REQ-F-04	Streamlit UI (Text Area Input)	TC-UI-01 (Manual Edit Workflow)
7.3 測試階段定義
1. 安裝確認 (IQ - Installation Qualification)
目標: 確認軟體已正確安裝於目標環境，且環境變數配置正確。
方法: 執行部署腳本，檢查 pip list 相依套件，檢查 .env 讀取狀態。
2. 操作確認 (OQ - Operational Qualification)
目標: 驗證所有功能性需求 (Functional Requirements) 是否符合 SRS 定義。
測試項目:
TC-FUNC-01: 載入標準 agents.yaml，確認系統生成正確數量的 UI 步驟。
TC-INT-01: 輸入無效的 API Key，確認系統回傳友善錯誤訊息而非 Crash。
TC-LOGIC-01: 驗證 Mana 扣除機制，當 Mana < 20 時，確認無法執行 Pipeline。
TC-TOOL-01: 測試 Note Keeper 的 JSON 提取功能，確認輸出格式符合預期。
3. 性能確認 (PQ - Performance Qualification)
目標: 在真實模擬負載下，驗證系統的穩定性與臨床適用性。
方法:
由資深 RA 人員輸入真實 (已去識別化) 的 510(k) 測試報告。
驗收標準: AI 生成的摘要準確度需達 85% 以上（由人工評分），且系統在連續執行 10 次操作中無崩潰。
8. 風險管理 (Risk Management)
依據 ISO 14971:2019 進行風險分析。
風險 ID	危害 (Hazard)	原因 (Cause)	傷害 (Harm)	初始風險	緩解措施 (Risk Mitigation)	剩餘風險
R-01	AI 幻覺 (Hallucination)	LLM 生成不存在的法規標準或 Predicate Device。	提交文件含錯誤資訊，導致 FDA 補件 (AI Request) 或拒絕。	高	1. 介面強制顯示 "Human-in-the-Loop" 警告。<br>2. 系統提示詞加入 "Strict Fact Check" 指令。<br>3. 實作編輯功能，強制人工確認。	低
R-02	資料隱私洩露	使用者意外上傳含有 PHI 的文件。	違反 HIPAA/GDPR，導致罰款與商譽損失。	中	1. UI 顯著位置標示隱私警告。<br>2. 實作客戶端正則表達式 (Regex) 掃描（建議未來功能）。<br>3. 無狀態設計，不儲存資料。	低
R-03	服務可用性喪失	第三方 API (OpenAI) 當機或改變收費策略。	關鍵時刻無法生成文件，延誤提交時程。	低	1. 支援多供應商 (OpenAI/Google/Anthropic) 作為備援。<br>2. 本地端日誌記錄斷點，允許恢復作業。	低
9. 維護與支援 (Maintenance & Support)
定期更新: 每月檢查第三方函式庫 (Streamlit, SDKs) 的安全性更新 (CVEs)。
模型迭代: 隨著 AI 供應商發布新模型 (如 GPT-5, Gemini 3.0)，需更新 AI_MODELS 常數並重新執行 OQ 測試。
監控: 在雲端部署模式下，持續監控 CloudWatch Metrics，設定 CPU/Memory 警報。
10. 附錄 (Appendices)
附錄 A: 參考法規標準
21 CFR Part 11: Electronic Records; Electronic Signatures.
21 CFR Part 820.30: Design Controls.
IEC 62304:2006+A1:2015: Medical device software – Software life cycle processes.
ISO 14971:2019: Medical devices — Application of risk management to medical devices.
FDA Guidance: Content of Premarket Submissions for Device Software Functions (June 2023).
FDA Guidance: Cybersecurity in Medical Devices: Quality System Considerations (Sept 2023).
附錄 B: agents.yaml 範例結構
code
Yaml
agents:
  - id: "step1_summary"
    name: "Document Summarizer"
    model: "gpt-4o-mini"
    provider: "openai"
    system_prompt: "You are an expert regulatory affairs specialist..."
  - id: "step2_risk"
    name: "Risk Identifier"
    model: "gemini-2.5-flash"
    provider: "gemini"
    system_prompt: "Identify potential risks based on ISO 14971..."
文件結束 (End of Document)
