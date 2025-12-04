import os
import time
import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Any

import streamlit as st
import yaml

# --- AI SDKs ---
import google.generativeai as genai
from openai import OpenAI
import anthropic
from xai_sdk import Client as XAIClient
from xai_sdk.chat import user as xai_user, system as xai_system

# Optional: if you use the separate prompts module
try:
    from prompts import BASE_SYSTEM_PROMPT
except ImportError:
    BASE_SYSTEM_PROMPT = ""


# =========================
# 1. CONFIG / CONSTANTS
# =========================

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

# 20 flower-based Nordic themes (simplified)
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

# Two "wow" features:
# 1) Mana Orb & Stress Meter
# 2) Achievement Blossoms (badges based on XP and runs)


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


# =========================
# 2. SESSION INIT
# =========================

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

# =========================
# 3. AGENT CONFIG LOADING
# =========================

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


# =========================
# 4. THEME & STYLING
# =========================

def get_current_theme() -> Dict[str, str]:
    flower_id = st.session_state.app_state.current_flower_id
    for theme in FLOWER_THEMES:
        if theme["id"] == flower_id:
            return theme
    return FLOWER_THEMES[0]


def inject_global_css():
    theme = get_current_theme()
    mode = st.session_state.app_state.theme_mode

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


# =========================
# 5. API KEY HANDLING
# =========================

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

    if key_env:
        st.session_state.app_state.api_keys[provider] = key_env
        return key_env

    return st.session_state.app_state.api_keys.get(provider)


def api_key_input_ui():
    st.subheader("🔐 API Keys (Client-Side Only)")
    st.caption(
        "Keys are kept in memory only. For deployment, prefer environment variables on Hugging Face Spaces."
    )

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


# =========================
# 6. PROVIDER CALLS
# =========================

def call_gemini(model: str, system_prompt: str, user_input: str,
                max_tokens: int, temperature: float, api_key: str) -> str:
    """
    Gemini helper without explicit safety settings.
    Also hides low-level safety/harm-category messages from the UI.
    """
    genai.configure(api_key=api_key)

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


# =========================
# 7. GAMIFIED STATUS / WOW FEATURES
# =========================

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


# =========================
# 8. PIPELINE UI
# =========================

def pipeline_tab():
    st.subheader("🔗 Multi-Agent 510(k) Review Pipeline")

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
# =========================
# 9. NOTE KEEPER
# =========================

def note_keeper_tab():
    st.subheader("🧾 AI Note Keeper")
    col_in, col_out = st.columns(2)

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
- Device name and description
- Intended use & indications for use
- Key risks and mitigations
- Predicate devices
- Standards & guidance documents
- Test types and outcomes
- Critical materials or components
Return JSON with an array of 20 objects: [{ "Entity": "", "Category": "", "Value": "", "Notes": "" }]
Then render them as a Markdown table: | # | Entity | Category | Value | Notes |
"""
    if tool == "Mindmap (Mermaid)":
        return """
Create a hierarchical mindmap of the regulatory content using Mermaid mindmap syntax.
Focus on: Device, Intended Use, Risk, Testing, Documentation, Gaps.
Output ONLY the Mermaid code block, e.g.:

```mermaid
mindmap
  root((Device))
    ...
```
"""
    if tool == "Quiz (5 MCQs)":
        return """
Create 5 multiple-choice questions (MCQs) to test understanding of the regulatory content.
Each question should have 4 options (A-D) and clearly indicate the correct answer.
Use Markdown:

1. Question text
   - A) ...
   - B) ...
   - C) ...
   - D) ...
   **Answer: X**
"""
    return "You are a helpful AI Note Keeper."


# =========================
# 10. DASHBOARD TAB
# =========================

def dashboard_tab():
    st.subheader("📊 Interactive Analytics Dashboard")

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


# =========================
# 11. SETTINGS / LANGUAGE / THEME
# =========================

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


# =========================
# 12. MAIN APP
# =========================

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


if __name__ == "__main__":
    main()