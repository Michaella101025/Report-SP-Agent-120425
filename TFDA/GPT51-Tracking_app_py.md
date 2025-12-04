1. `app.py`：完整 Streamlit App（含 AI Note Keeper、新增功能、31 Agents UI 支援、多家模型選擇、API Key 管理、WOW UI 架構）。  
2. `agents.yaml`：進階版，包含 31 個中文代理人設定。

你可以直接把這兩個檔案放到 Hugging Face Space 專案裡執行（記得在 `requirements.txt` 加上 `streamlit`, `pyyaml`, 以及各家 LLM SDK/HTTP client）。

---

## 1. `app.py`

```python
import os
import random
from typing import Dict, Any, List

import streamlit as st
import yaml

# =========================
# 基本設定
# =========================

st.set_page_config(
    page_title="BioChain Analyst Pro v2.0",
    layout="wide",
)

# =========================
# 多語系 (簡化版，預設繁體中文)
# =========================

TRANSLATIONS = {
    "zh-TW": {
        "title": "醫療器材供應鏈追蹤系統 v2.0 - BioChain Analyst Pro",
        "dashboard": "儀表板",
        "data_studio": "資料工作室",
        "network_graph": "供應鏈網路圖",
        "time_trends": "時間趨勢",
        "ai_agents": "AI 代理人控制台",
        "ai_note_keeper": "AI 筆記管家",
        "system_logs": "系統與紀錄",
        "theme_selector": "花卉主題選擇器 (Jackslot)",
        "spin_random_theme": "隨機抽主題",
        "apply_theme": "套用主題",
        "select_theme": "選擇主題",
        "api_keys": "API 金鑰管理",
        "dataset": "資料集",
        "upload_csv": "上傳 CSV",
        "or_use_mock": "或使用內建示範資料",
        "ai_agents_pipeline": "多代理人 AI 分析流程",
        "execution_mode": "執行模式",
        "run_all_enabled": "依序執行所有已啟用代理人",
        "run_single": "逐一執行代理人",
        "enable_agent": "啟用此代理人",
        "prompt_template": "Prompt 模板",
        "max_tokens": "Max Tokens",
        "use_prev_output_as_input": "將上一個代理人的輸出作為輸入（可再編輯）",
        "agent_input": "此代理人的輸入內容（可手動編輯）",
        "run_agent": "執行此代理人",
        "view_mode": "輸出檢視模式",
        "plain_text": "純文字",
        "markdown": "Markdown 渲染",
        "agent_output": "代理人輸出結果",
        "you_can_edit_and_copy_output_for_next_agent": "你可以編輯上方輸出，再複製成下一個代理人的輸入。",
        "ai_key_from_env": "已從伺服器環境載入 API Key。",
        "ai_key_input": "請輸入 API Key（只會存在此瀏覽器工作階段）",
        "language": "介面語言",
        "light_mode": "淺色模式",
        "dark_mode": "深色模式",
        # AI Note Keeper
        "note_keeper_title": "AI 筆記管家",
        "note_raw_input": "貼上原始文字筆記",
        "note_to_markdown": "AI 轉換為 Markdown 筆記",
        "note_edit_mode": "筆記編輯 / 檢視模式",
        "note_edit_text": "文字編輯模式",
        "note_preview_md": "Markdown 預覽模式",
        "current_note_md": "目前 Markdown 筆記",
        "ai_formatting": "AI 排版優化",
        "ai_formatting_desc": "使用 AI 重新整理標題、段落與項目符號，但不改變事實內容。",
        "ai_keywords": "AI 關鍵字標註",
        "ai_keywords_desc": "輸入欲標註的關鍵字與顏色，系統會在筆記中高亮顯示。",
        "keywords_input": "輸入關鍵字（以逗號或換行分隔）",
        "keywords_color": "選擇關鍵字高亮顏色",
        "apply_keywords": "套用關鍵字標註",
        "ai_entities": "AI 實體擷取 (20 筆)",
        "ai_entities_desc": "由 AI 從筆記中擷取 20 個關鍵實體，並以 Markdown 表格呈現。",
        "run_entities_extraction": "產生實體表格",
        "ai_chat": "AI 筆記對話",
        "ai_chat_prompt": "請輸入你的問題或指令（會以目前筆記為上下文）",
        "ai_chat_run": "送出對話",
        "ai_summary": "AI 摘要",
        "ai_summary_prompt": "自訂摘要 Prompt（可使用繁體中文或英文）",
        "ai_summary_run": "產生摘要",
        "ai_magics": "AI Magics",
        "ai_magic_1": "AI 風險雷達",
        "ai_magic_1_desc": "從筆記中找出潛在風險情境與重要警訊。",
        "ai_magic_1_run": "產生風險雷達報告",
        "ai_magic_2": "AI 行動藍圖",
        "ai_magic_2_desc": "根據筆記內容產生分階段行動建議與優先順序。",
        "ai_magic_2_run": "產生行動藍圖",
        "model_select": "選擇模型",
        "tokens_input": "Max Tokens（預設 12000）",
    },
    "en": {
        # 可視需要補齊英文對照
    },
}


def t(key: str) -> str:
    lang = st.session_state.get("language", "zh-TW")
    return TRANSLATIONS.get(lang, TRANSLATIONS["zh-TW"]).get(key, key)


# =========================
# 花卉主題 (20 種 Jackslot 主題，簡化參數)
# =========================

FLOWER_THEMES = [
    {
        "id": "sakura_mist",
        "name_zh": "櫻花薄霧",
        "name_en": "Sakura Mist",
        "emoji": "🌸",
        "bg_light": "#fff7fb",
        "bg_dark": "#2b1b2f",
        "primary": "#f48fb1",
        "accent": "#ff80ab",
    },
    {
        "id": "lotus_serenity",
        "name_zh": "蓮花靜心",
        "name_en": "Lotus Serenity",
        "emoji": "🌺",
        "bg_light": "#f5fbff",
        "bg_dark": "#102027",
        "primary": "#80cbc4",
        "accent": "#26a69a",
    },
    {
        "id": "iris_dusk",
        "name_zh": "鳶尾暮光",
        "name_en": "Iris Dusk",
        "emoji": "🌸",
        "bg_light": "#f3f2ff",
        "bg_dark": "#1c1b2e",
        "primary": "#7e57c2",
        "accent": "#9575cd",
    },
    {
        "id": "rose_gold",
        "name_zh": "玫瑰晨光",
        "name_en": "Rose Gold",
        "emoji": "🌹",
        "bg_light": "#fff4f4",
        "bg_dark": "#32131a",
        "primary": "#ef5350",
        "accent": "#ff8a80",
    },
    {
        "id": "orchid_neon",
        "name_zh": "蘭花霓虹",
        "name_en": "Orchid Neon",
        "emoji": "💮",
        "bg_light": "#faf5ff",
        "bg_dark": "#2a1635",
        "primary": "#ba68c8",
        "accent": "#e1bee7",
    },
    {
        "id": "sunflower_field",
        "name_zh": "向日葵原野",
        "name_en": "Sunflower Field",
        "emoji": "🌻",
        "bg_light": "#fffde7",
        "bg_dark": "#322b0a",
        "primary": "#fbc02d",
        "accent": "#ffeb3b",
    },
    {
        "id": "lavender_breeze",
        "name_zh": "薰衣草微風",
        "name_en": "Lavender Breeze",
        "emoji": "💐",
        "bg_light": "#f8f4ff",
        "bg_dark": "#241b38",
        "primary": "#9575cd",
        "accent": "#b39ddb",
    },
    {
        "id": "camellia_silk",
        "name_zh": "山茶絲綢",
        "name_en": "Camellia Silk",
        "emoji": "🌺",
        "bg_light": "#fff8f6",
        "bg_dark": "#2d1c16",
        "primary": "#ff7043",
        "accent": "#ffab91",
    },
    {
        "id": "peony_glow",
        "name_zh": "牡丹流光",
        "name_en": "Peony Glow",
        "emoji": "🌸",
        "bg_light": "#fff0f6",
        "bg_dark": "#3a1024",
        "primary": "#ec407a",
        "accent": "#f48fb1",
    },
    {
        "id": "cherry_blossom_night",
        "name_zh": "夜櫻微雨",
        "name_en": "Cherry Blossom Night",
        "emoji": "🌸",
        "bg_light": "#fef5ff",
        "bg_dark": "#1e1325",
        "primary": "#f06292",
        "accent": "#ce93d8",
    },
    {
        "id": "magnolia_morning",
        "name_zh": "玉蘭晨露",
        "name_en": "Magnolia Morning",
        "emoji": "🌼",
        "bg_light": "#f8fff9",
        "bg_dark": "#102019",
        "primary": "#aed581",
        "accent": "#c5e1a5",
    },
    {
        "id": "hydrangea_rain",
        "name_zh": "繡球雨靄",
        "name_en": "Hydrangea Rain",
        "emoji": "🌸",
        "bg_light": "#f3f8ff",
        "bg_dark": "#131c2e",
        "primary": "#64b5f6",
        "accent": "#90caf9",
    },
    {
        "id": "poppy_fire",
        "name_zh": "罌粟烈焰",
        "name_en": "Poppy Fire",
        "emoji": "🌺",
        "bg_light": "#fff3e0",
        "bg_dark": "#3b1b0b",
        "primary": "#ff7043",
        "accent": "#ffab91",
    },
    {
        "id": "daisy_cloud",
        "name_zh": "雛菊雲光",
        "name_en": "Daisy Cloud",
        "emoji": "🌼",
        "bg_light": "#f9fff6",
        "bg_dark": "#1b2512",
        "primary": "#c0ca33",
        "accent": "#dce775",
    },
    {
        "id": "lotus_moon",
        "name_zh": "月色荷塘",
        "name_en": "Lotus Moon",
        "emoji": "🌸",
        "bg_light": "#f5fff9",
        "bg_dark": "#101f19",
        "primary": "#4db6ac",
        "accent": "#80cbc4",
    },
    {
        "id": "iris_frost",
        "name_zh": "霜染鳶尾",
        "name_en": "Iris Frost",
        "emoji": "💐",
        "bg_light": "#f4f7ff",
        "bg_dark": "#151c2f",
        "primary": "#5c6bc0",
        "accent": "#7986cb",
    },
    {
        "id": "rose_noir",
        "name_zh": "黑玫瑰序曲",
        "name_en": "Rose Noir",
        "emoji": "🌹",
        "bg_light": "#fdf2f5",
        "bg_dark": "#1f0b12",
        "primary": "#d32f2f",
        "accent": "#e57373",
    },
    {
        "id": "orchid_ice",
        "name_zh": "蘭冰晨曲",
        "name_en": "Orchid Ice",
        "emoji": "💮",
        "bg_light": "#faf3ff",
        "bg_dark": "#231a33",
        "primary": "#ab47bc",
        "accent": "#ce93d8",
    },
    {
        "id": "sunrise_tulip",
        "name_zh": "曙光鬱金香",
        "name_en": "Sunrise Tulip",
        "emoji": "🌷",
        "bg_light": "#fff6e8",
        "bg_dark": "#3a2312",
        "primary": "#ff8f00",
        "accent": "#ffb74d",
    },
    {
        "id": "garden_mint",
        "name_zh": "庭園薄荷",
        "name_en": "Garden Mint",
        "emoji": "🌿",
        "bg_light": "#f3fff9",
        "bg_dark": "#10241b",
        "primary": "#4caf50",
        "accent": "#81c784",
    },
]


def get_theme_by_id(theme_id: str) -> Dict[str, Any]:
    for th in FLOWER_THEMES:
        if th["id"] == theme_id:
            return th
    return FLOWER_THEMES[0]


def get_theme_name(theme: Dict[str, Any]) -> str:
    lang = st.session_state.get("language", "zh-TW")
    return theme["name_zh"] if lang == "zh-TW" else theme["name_en"]


def apply_theme_css():
    theme_id = st.session_state.get("theme_id", FLOWER_THEMES[0]["id"])
    theme = get_theme_by_id(theme_id)
    dark_mode = st.session_state.get("dark_mode", False)

    bg = theme["bg_dark"] if dark_mode else theme["bg_light"]
    primary = theme["primary"]
    accent = theme["accent"]

    css = f"""
    <style>
    body {{
        background-color: {bg} !important;
    }}
    .stApp {{
        background-color: {bg} !important;
    }}
    .css-18e3th9, .css-1d391kg {{
        background-color: {bg} !important;
    }}
    .stButton>button {{
        border-radius: 999px;
        border: 1px solid {accent};
        color: #ffffff;
        background: linear-gradient(90deg, {primary}, {accent});
    }}
    .stTabs [data-baseweb="tab"] {{
        font-weight: 600;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# =========================
# LLM Provider 與模型設定
# =========================

MODEL_OPTIONS = [
    ("openai", "gpt-4o-mini"),
    ("openai", "gpt-4.1-mini"),
    ("gemini", "gemini-2.5-flash"),
    ("gemini", "gemini-2.5-flash-lite"),
    ("anthropic", "claude-3-5-sonnet"),
    ("anthropic", "claude-3-5-haiku"),
    ("grok", "grok-4-fast-reasoning"),
    ("grok", "grok-3-mini"),
]


def get_model_label(provider: str, model: str) -> str:
    return f"{provider}:{model}"


def parse_model_label(label: str):
    provider, model = label.split(":", 1)
    return provider, model


# =========================
# API Key 管理（環境變數優先）
# =========================

ENV_KEYS = {
    "gemini": os.getenv("GEMINI_API_KEY"),
    "openai": os.getenv("OPENAI_API_KEY"),
    "anthropic": os.getenv("ANTHROPIC_API_KEY"),
    "grok": os.getenv("GROK_API_KEY"),
}


def init_session():
    if "language" not in st.session_state:
        st.session_state["language"] = "zh-TW"
    if "dark_mode" not in st.session_state:
        st.session_state["dark_mode"] = False
    if "theme_id" not in st.session_state:
        st.session_state["theme_id"] = FLOWER_THEMES[0]["id"]
    if "user_keys" not in st.session_state:
        st.session_state["user_keys"] = {}
    if "records" not in st.session_state:
        st.session_state["records"] = None
    if "agent_outputs" not in st.session_state:
        st.session_state["agent_outputs"] = {}
    if "note_raw" not in st.session_state:
        st.session_state["note_raw"] = ""
    if "note_md" not in st.session_state:
        st.session_state["note_md"] = ""
    if "note_edit_mode" not in st.session_state:
        st.session_state["note_edit_mode"] = "text"


def get_active_api_key(provider: str) -> str | None:
    if ENV_KEYS.get(provider):
        return ENV_KEYS[provider]
    return st.session_state["user_keys"].get(provider)


# =========================
# LLM 呼叫 (需自行實作具體 API 呼叫)
# =========================

def run_llm(provider: str, model: str, prompt: str, max_tokens: int = 12000) -> str:
    """
    實務中請在這裡接 OpenAI / Gemini / Anthropic / Grok 的 SDK 或 HTTP。
    這裡先用 placeholder，避免部署時出錯。
    """
    api_key = get_active_api_key(provider)
    if not api_key:
        return f"[錯誤] 尚未設定 {provider} 的 API Key，無法呼叫模型 {model}。"

    # TODO: 改為實際 API 呼叫
    fake_response = f"(模擬 {provider}:{model} 回應)\n\n" + prompt[:2000]
    return fake_response


# =========================
# 讀取 agents.yaml
# =========================

def load_agents_config() -> List[Dict[str, Any]]:
    try:
        with open("agents.yaml", "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        return cfg.get("agents", [])
    except Exception as e:
        st.error(f"讀取 agents.yaml 失敗: {e}")
        return []


# =========================
# UI 區塊：頂部列 & Sidebar
# =========================

def render_topbar():
    cols = st.columns([4, 2, 2])
    with cols[0]:
        st.markdown(f"## {t('title')}")
    with cols[1]:
        st.write("")  # 占位
        lang = st.radio(
            t("language"),
            ["zh-TW", "en"],
            horizontal=True,
            index=0 if st.session_state["language"] == "zh-TW" else 1,
            key="lang_radio_top",
        )
        st.session_state["language"] = lang
    with cols[2]:
        st.write("")
        dark = st.checkbox(t("dark_mode"), value=st.session_state["dark_mode"])
        st.session_state["dark_mode"] = dark


def render_theme_jackslot():
    st.subheader(t("theme_selector"))

    current_theme = get_theme_by_id(st.session_state["theme_id"])
    st.markdown(
        f"**{current_theme['emoji']} {get_theme_name(current_theme)}**",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button(t("spin_random_theme")):
            random_theme = random.choice(FLOWER_THEMES)
            st.session_state["theme_candidate"] = random_theme["id"]
    with col2:
        if st.button(t("apply_theme")):
            candidate_id = st.session_state.get("theme_candidate", current_theme["id"])
            st.session_state["theme_id"] = candidate_id

    # 直接選擇主題
    options_labels = [get_theme_name(th) for th in FLOWER_THEMES]
    options_ids = [th["id"] for th in FLOWER_THEMES]
    try:
        idx = options_ids.index(st.session_state["theme_id"])
    except ValueError:
        idx = 0
    selected_label = st.selectbox(t("select_theme"), options_labels, index=idx)
    st.session_state["theme_id"] = options_ids[options_labels.index(selected_label)]


def render_sidebar():
    with st.sidebar:
        # 主題選擇
        render_theme_jackslot()
        st.markdown("---")

        # API Keys
        st.subheader(t("api_keys"))

        for provider, label in [
            ("gemini", "Gemini"),
            ("openai", "OpenAI"),
            ("anthropic", "Anthropic"),
            ("grok", "Grok"),
        ]:
            st.markdown(f"**{label}**")
            if ENV_KEYS.get(provider):
                st.caption(t("ai_key_from_env"))
            else:
                key_val = st.text_input(
                    f"{label} {t('ai_key_input')}",
                    type="password",
                    key=f"{provider}_key_input",
                )
                if key_val:
                    st.session_state["user_keys"][provider] = key_val

        st.markdown("---")

        # 資料集 (簡化版)
        st.subheader(t("dataset"))
        upload = st.file_uploader(t("upload_csv"), type=["csv"], key="csv_uploader")
        if upload:
            import pandas as pd

            df = pd.read_csv(upload)
            st.session_state["records"] = df
            st.success(f"已載入 {len(df)} 筆資料。")
        if st.button(t("or_use_mock")):
            # TODO: 實際讀取 data/mock.csv
            st.session_state["records"] = None
            st.info("Demo 模式：尚未實作實際 mock.csv 載入。")


# =========================
# 各分頁 UI
# =========================

def render_dashboard():
    st.markdown("### 儀表板 (TODO: 實作指標卡與圖表)")
    st.info("此處可放置資料品質、風險分數、AI 執行狀態等 WOW 指標。")


def render_data_studio():
    st.markdown("### 資料工作室")
    import pandas as pd

    df = st.session_state.get("records")
    if df is None:
        st.warning("尚未載入任何資料。請在左側上傳 CSV 或使用示範資料。")
        return

    editable_df = st.data_editor(df, num_rows="dynamic", key="data_editor_df")
    st.session_state["records"] = editable_df

    # 下載
    csv_bytes = editable_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "下載目前資料為 CSV",
        data=csv_bytes,
        file_name="biochain_export.csv",
        mime="text/csv",
    )


def render_network_graph():
    st.markdown("### 供應鏈網路圖")
    st.info("此處可嵌入 D3.js 力導向圖 (使用 st.components.v1.html)。目前為占位。")


def render_time_trends():
    st.markdown("### 時間序列趨勢圖")
    st.info("此處可使用 Plotly/Altair 呈現出貨量隨時間變化。")


# -------------------------
# AI Agents Console
# -------------------------

def render_agents_console():
    st.markdown("### " + t("ai_agents_pipeline"))

    agents_cfg = load_agents_config()
    if not agents_cfg:
        st.warning("找不到 agents.yaml 或內容為空。")
        return

    exec_mode = st.radio(
        t("execution_mode"),
        [t("run_all_enabled"), t("run_single")],
        horizontal=True,
        key="agent_exec_mode",
    )

    run_all = exec_mode == t("run_all_enabled")

    previous_output = None
    for agent in agents_cfg:
        previous_output = render_single_agent_card(agent, previous_output, run_all)


def render_single_agent_card(agent: Dict[str, Any], previous_output: str | None, run_all: bool):
    agent_id = agent["id"]
    with st.expander(f"{agent['name']} ({agent['role']})", expanded=False):
        enabled = st.checkbox(
            t("enable_agent"),
            value=True,
            key=f"enable_{agent_id}",
        )

        if not enabled:
            return previous_output

        default_prompt = agent.get("default_prompt", "")
        prompt = st.text_area(
            t("prompt_template"),
            value=st.session_state.get(f"prompt_{agent_id}", default_prompt),
            key=f"prompt_{agent_id}",
            height=150,
        )

        # 模型選擇
        default_label = get_model_label(
            agent.get("default_provider", "gemini"),
            agent.get("default_model", "gemini-2.5-flash"),
        )
        model_labels = [get_model_label(p, m) for p, m in MODEL_OPTIONS]
        if default_label not in model_labels:
            model_labels.insert(0, default_label)

        model_label = st.selectbox(
            t("model_select"),
            model_labels,
            index=model_labels.index(default_label),
            key=f"model_{agent_id}",
        )
        provider, model_name = parse_model_label(model_label)

        max_tokens = st.number_input(
            t("tokens_input"),
            min_value=512,
            max_value=120000,
            value=agent.get("default_max_tokens", 12000),
            step=512,
            key=f"max_tokens_{agent_id}",
        )

        # 上一個 Agent 輸出
        if previous_output:
            if st.button(t("use_prev_output_as_input"), key=f"use_prev_{agent_id}"):
                st.session_state[f"input_from_prev_{agent_id}"] = previous_output

        input_text = st.text_area(
            t("agent_input"),
            value=st.session_state.get(f"input_from_prev_{agent_id}", ""),
            key=f"agent_input_{agent_id}",
            height=120,
        )

        # 執行
        run_button_pressed = False
        if run_all:
            run_button_pressed = enabled  # pipeline 模式：自動執行已啟用
        else:
            run_button_pressed = st.button(
                t("run_agent"),
                key=f"run_{agent_id}",
            )

        if run_button_pressed:
            full_prompt = f"{prompt}\n\n=== 輸入資料 ===\n{input_text}"
            with st.spinner(f"執行 {agent['name']} 中..."):
                output = run_llm(provider, model_name, full_prompt, max_tokens)
            st.session_state["agent_outputs"][agent_id] = output

        view_mode = st.radio(
            t("view_mode"),
            [t("plain_text"), t("markdown")],
            horizontal=True,
            key=f"view_mode_{agent_id}",
        )

        output = st.session_state["agent_outputs"].get(agent_id, "")
        if output:
            if view_mode == t("markdown"):
                st.markdown(output)
            else:
                st.text_area(
                    t("agent_output"),
                    value=output,
                    height=200,
                    key=f"output_text_{agent_id}",
                )
            st.caption(t("you_can_edit_and_copy_output_for_next_agent"))

        return output if output else previous_output


# -------------------------
# AI Note Keeper
# -------------------------

def render_ai_note_keeper():
    st.markdown(f"### {t('note_keeper_title')}")

    # 原始貼上區
    st.text_area(
        t("note_raw_input"),
        value=st.session_state["note_raw"],
        key="note_raw",
        height=200,
    )

    # 轉 Markdown
    cols = st.columns([1, 2, 2])
    with cols[0]:
        if st.button(t("note_to_markdown")):
            provider, model = "gemini", "gemini-2.5-flash"
            prompt = (
                "請將以下文字轉換為結構良好的 Markdown 筆記，"
                "適度加入標題 (##)、子標題 (###)、條列與表格，"
                "但不要主觀新增事實或刪除關鍵資訊。\n\n"
                "=== 原始文字 ===\n"
                + st.session_state["note_raw"]
            )
            with st.spinner("AI 正在將文字轉為 Markdown ..."):
                md = run_llm(provider, model, prompt, 4000)
            st.session_state["note_md"] = md

    with cols[1]:
        mode = st.radio(
            t("note_edit_mode"),
            [t("note_edit_text"), t("note_preview_md")],
            horizontal=True,
            key="note_edit_mode_radio",
        )
        st.session_state["note_edit_mode"] = (
            "text" if mode == t("note_edit_text") else "markdown"
        )

    with cols[2]:
        st.write("")

    # 編輯 / 預覽
    if st.session_state["note_edit_mode"] == "text":
        st.session_state["note_md"] = st.text_area(
            t("current_note_md"),
            value=st.session_state["note_md"],
            key="note_md_edit",
            height=300,
        )
    else:
        st.markdown(st.session_state["note_md"] or "_目前尚未有 Markdown 內容_")

    st.markdown("---")

    # AI 工具區：四大工具 + 2 個 Magic
    col_fmt, col_kw, col_ent = st.columns(3)

    # --- AI Formatting ---
    with col_fmt:
        st.markdown(f"#### {t('ai_formatting')}")
        st.caption(t("ai_formatting_desc"))
        fmt_model_label = st.selectbox(
            t("model_select") + " (Formatting)",
            [get_model_label(p, m) for p, m in MODEL_OPTIONS],
            key="fmt_model",
        )
        fmt_provider, fmt_model = parse_model_label(fmt_model_label)
        fmt_tokens = st.number_input(
            t("tokens_input") + " (Formatting)",
            min_value=512,
            max_value=120000,
            value=12000,
            step=512,
            key="fmt_tokens",
        )
        if st.button(t("ai_formatting"), key="fmt_run"):
            prompt = (
                "請在不更動事實內容的前提下，將以下 Markdown 筆記重新排版："
                "優化標題層級、條列符號與可讀性，適度拆分段落。\n\n"
                "=== Markdown 筆記 ===\n"
                + st.session_state["note_md"]
            )
            with st.spinner("AI 正在排版優化..."):
                md = run_llm(fmt_provider, fmt_model, prompt, fmt_tokens)
            st.session_state["note_md"] = md
            st.success("已完成 AI 排版優化。")

    # --- AI Keywords ---
    with col_kw:
        st.markdown(f"#### {t('ai_keywords')}")
        st.caption(t("ai_keywords_desc"))
        keywords_str = st.text_area(
            t("keywords_input"),
            key="keywords_input",
            height=80,
        )
        color = st.color_picker(
            t("keywords_color"),
            value="#ffeb3b",
            key="keywords_color_picker",
        )
        if st.button(t("apply_keywords")):
            note_md = st.session_state["note_md"]
            if not note_md:
                st.warning("尚無 Markdown 內容可標註。")
            else:
                keywords = []
                for part in keywords_str.replace("\n", ",").split(","):
                    w = part.strip()
                    if w:
                        keywords.append(w)
                for kw in sorted(set(keywords), key=len, reverse=True):
                    if kw in note_md:
                        note_md = note_md.replace(
                            kw,
                            f"<span style='background-color:{color};"
                            f"padding:0 2px;border-radius:2px'>{kw}</span>",
                        )
                st.session_state["note_md"] = note_md
                st.success("已套用關鍵字高亮。")
                st.markdown(
                    "（注意：關鍵字高亮使用 HTML span，需要 Markdown 頁面允許 HTML）"
                )

    # --- AI Entities ---
    with col_ent:
        st.markdown(f"#### {t('ai_entities')}")
        st.caption(t("ai_entities_desc"))
        ent_model_label = st.selectbox(
            t("model_select") + " (Entities)",
            [get_model_label(p, m) for p, m in MODEL_OPTIONS],
            key="ent_model",
        )
        ent_provider, ent_model = parse_model_label(ent_model_label)
        ent_tokens = st.number_input(
            t("tokens_input") + " (Entities)",
            min_value=512,
            max_value=120000,
            value=12000,
            step=512,
            key="ent_tokens",
        )
        if st.button(t("run_entities_extraction")):
            prompt = (
                "你是一位醫療供應鏈與法規領域的知識圖譜專家。"
                "請從以下 Markdown 筆記中萃取最多 20 個關鍵實體，"
                "並以 Markdown 表格呈現，欄位包含："
                "實體名稱、實體類型（機構/醫材/法規/風險/時間…）、"
                "相關上下文摘要、潛在風險等級（低/中/高）、備註。\n\n"
                "=== Markdown 筆記 ===\n"
                + st.session_state["note_md"]
            )
            with st.spinner("AI 正在擷取實體..."):
                ents_markdown = run_llm(ent_provider, ent_model, prompt, ent_tokens)
            st.markdown("##### 實體表格")
            st.markdown(ents_markdown)

    st.markdown("---")

    # AI Chat + Summary + Magics
    col_chat, col_sum = st.columns(2)

    # --- AI Chat ---
    with col_chat:
        st.markdown(f"#### {t('ai_chat')}")
        chat_prompt = st.text_area(
            t("ai_chat_prompt"),
            key="note_chat_prompt",
            height=120,
        )
        chat_model_label = st.selectbox(
            t("model_select") + " (Chat)",
            [get_model_label(p, m) for p, m in MODEL_OPTIONS],
            key="chat_model",
        )
        chat_provider, chat_model = parse_model_label(chat_model_label)
        chat_tokens = st.number_input(
            t("tokens_input") + " (Chat)",
            min_value=512,
            max_value=120000,
            value=12000,
            step=512,
            key="chat_tokens",
        )
        if st.button(t("ai_chat_run")):
            prompt = (
                "以下是使用者的工作筆記（Markdown 格式）作為上下文，"
                "請根據筆記內容與使用者問題進行專業回答，"
                "回答時可引用關鍵片段，但避免捏造不存在的事實。\n\n"
                "=== 筆記內容 ===\n"
                f"{st.session_state['note_md']}\n\n"
                "=== 使用者問題 ===\n"
                f"{chat_prompt}"
            )
            with st.spinner("AI 正在回應對話..."):
                chat_resp = run_llm(chat_provider, chat_model, prompt, chat_tokens)
            st.markdown("##### 對話回應")
            st.markdown(chat_resp)

    # --- AI Summary ---
    with col_sum:
        st.markdown(f"#### {t('ai_summary')}")
        default_sum_prompt = (
            "請以條列方式撰寫此筆記的重點摘要，包含：\n"
            "1. 核心議題\n"
            "2. 主要利害關係人\n"
            "3. 重要風險或警訊\n"
            "4. 建議後續動作（如有）\n"
        )
        sum_prompt = st.text_area(
            t("ai_summary_prompt"),
            value=default_sum_prompt,
            key="summary_prompt",
            height=150,
        )
        sum_model_label = st.selectbox(
            t("model_select") + " (Summary)",
            [get_model_label(p, m) for p, m in MODEL_OPTIONS],
            key="sum_model",
        )
        sum_provider, sum_model = parse_model_label(sum_model_label)
        sum_tokens = st.number_input(
            t("tokens_input") + " (Summary)",
            min_value=512,
            max_value=120000,
            value=12000,
            step=512,
            key="sum_tokens",
        )
        if st.button(t("ai_summary_run")):
            prompt = (
                sum_prompt
                + "\n\n=== 筆記內容 ===\n"
                + st.session_state["note_md"]
            )
            with st.spinner("AI 正在產生摘要..."):
                summary = run_llm(sum_provider, sum_model, prompt, sum_tokens)
            st.markdown("##### 摘要結果")
            st.markdown(summary)

    st.markdown("---")

    # --- AI Magics ---
    st.markdown(f"#### {t('ai_magics')}")
    col_m1, col_m2 = st.columns(2)

    # Magic 1: 風險雷達
    with col_m1:
        st.markdown(f"##### {t('ai_magic_1')}")
        st.caption(t("ai_magic_1_desc"))
        m1_model_label = st.selectbox(
            t("model_select") + " (Risk Radar)",
            [get_model_label(p, m) for p, m in MODEL_OPTIONS],
            key="m1_model",
        )
        m1_provider, m1_model = parse_model_label(m1_model_label)
        m1_tokens = st.number_input(
            t("tokens_input") + " (Risk Radar)",
            min_value=512,
            max_value=120000,
            value=12000,
            step=512,
            key="m1_tokens",
        )
        if st.button(t("ai_magic_1_run")):
            prompt = (
                "你是一位醫療器材供應鏈與合規風險專家。"
                "請從以下筆記中辨識可能的風險情境與警訊，"
                "並以 Markdown 條列與表格形式輸出："
                "包含風險類型、可能影響、發生機率、風險等級與建議控管措施。\n\n"
                "=== 筆記內容 ===\n"
                + st.session_state["note_md"]
            )
            with st.spinner("AI 正在產生風險雷達..."):
                risk_report = run_llm(m1_provider, m1_model, prompt, m1_tokens)
            st.markdown("##### 風險雷達報告")
            st.markdown(risk_report)

    # Magic 2: 行動藍圖
    with col_m2:
        st.markdown(f"##### {t('ai_magic_2')}")
        st.caption(t("ai_magic_2_desc"))
        m2_model_label = st.selectbox(
            t("model_select") + " (Action Blueprint)",
            [get_model_label(p, m) for p, m in MODEL_OPTIONS],
            key="m2_model",
        )
        m2_provider, m2_model = parse_model_label(m2_model_label)
        m2_tokens = st.number_input(
            t("tokens_input") + " (Action Blueprint)",
            min_value=512,
            max_value=120000,
            value=12000,
            step=512,
            key="m2_tokens",
        )
        if st.button(t("ai_magic_2_run")):
            prompt = (
                "請扮演一位醫療品質與流程改善顧問，"
                "根據以下筆記內容，設計一份『行動藍圖』："
                "分為短期（1-3 個月）、中期（3-12 個月）、長期（超過 1 年），"
                "每個階段以表格列出：行動項目、負責角色、預期成果與風險提醒。\n\n"
                "=== 筆記內容 ===\n"
                + st.session_state["note_md"]
            )
            with st.spinner("AI 正在產生行動藍圖..."):
                plan = run_llm(m2_provider, m2_model, prompt, m2_tokens)
            st.markdown("##### 行動藍圖")
            st.markdown(plan)


def render_system_logs():
    st.markdown("### 系統與紀錄 (TODO)")
    st.info("此處可顯示 AI 執行 log、錯誤訊息、版本資訊等。")


# =========================
# 主程式
# =========================

def main():
    init_session()
    apply_theme_css()

    render_topbar()
    render_sidebar()

    tabs = st.tabs(
        [
            t("dashboard"),
            t("data_studio"),
            t("network_graph"),
            t("time_trends"),
            t("ai_agents"),
            t("ai_note_keeper"),
            t("system_logs"),
        ]
    )

    with tabs[0]:
        render_dashboard()
    with tabs[1]:
        render_data_studio()
    with tabs[2]:
        render_network_graph()
    with tabs[3]:
        render_time_trends()
    with tabs[4]:
        render_agents_console()
    with tabs[5]:
        render_ai_note_keeper()
    with tabs[6]:
        render_system_logs()


if __name__ == "__main__":
    main()
```

---

## 2. `agents.yaml`（31 個進階代理人，繁體中文）

```yaml
agents:
  - id: auditor
    name: "稽核審查員"
    role: "Auditor"
    description: "針對醫療器材交易資料進行異常偵測與稽核建議。"
    default_provider: "gemini"
    default_model: "gemini-2.5-flash"
    default_max_tokens: 12000
    default_prompt: |
      你是一位醫療器材供應鏈的資深稽核專家。
      請以嚴謹但清楚易懂的方式檢視給定的交易資料（已整理為文字或表格摘要），
      針對以下面向提出分析：
      1. 數量異常（例如異常放大、異常縮小、負數、極端值）
      2. 時間分佈異常（集中在特定日期、假日、非工作時段）
      3. 供應商與醫療院所之間的異常關係（交易過度集中、頻率異常）
      4. 可能涉及法規或合約違反的情境
      請以條列方式呈現發現與建議，必要時可附上示意表格。

  - id: logistics_analyst
    name: "物流路徑分析師"
    role: "Logistics"
    description: "分析供應鏈路徑、節點與物流效率瓶頸。"
    default_provider: "openai"
    default_model: "gpt-4o-mini"
    default_max_tokens: 12000
    default_prompt: |
      你是醫療器材物流與供應鏈優化專家。
      根據提供的交易關係與數量資訊，請：
      1. 描述整體供應鏈網路結構（節點類型、主要路徑、樞紐節點）
      2. 找出高流量瓶頸節點與單點故障風險
      3. 提出可行的路徑優化或備援設計建議
      4. 指出任何與冷鏈、時效性或庫存週轉相關的風險

  - id: legal_compliance
    name: "法規合規顧問"
    role: "Legal"
    description: "從法規與合約角度檢視資料與流程是否合規。"
    default_provider: "anthropic"
    default_model: "claude-3-5-sonnet"
    default_max_tokens: 12000
    default_prompt: |
      你是一位熟悉 TFDA 與國際法規（如 EU MDR、FDA）的法規顧問。
      請根據提供的醫療器材交易與物流描述，回答下列問題：
      1. 哪些行為或模式可能違反法規或指引？請說明原因。
      2. 哪些資料欄位目前不足以支援合規稽核？建議補強哪些紀錄？
      3. 若出現產品不良事件或召回，現有供應鏈紀錄是否足以追溯？
      4. 建議的改善措施與文件化需求。

  - id: global_analyst
    name: "整體情境分析師"
    role: "Analyst"
    description: "綜合各面向輸出高階管理層可讀的總結報告。"
    default_provider: "gemini"
    default_model: "gemini-2.5-flash"
    default_max_tokens: 12000
    default_prompt: |
      你是一位為高階管理層撰寫簡報摘要的策略分析師。
      已有其他代理人輸出稽核、物流、法規等分析。
      請整合這些輸出，撰寫一份適合投影片或報告封面的摘要，內容包含：
      1. 核心發現（最多 5 點）
      2. 關鍵風險或機會
      3. 建議的短中長期行動
      4. 如需給 TFDA 或院方簡報，可使用的簡短敘述。

  - id: data_quality_guard
    name: "資料品質守門員"
    role: "Data Quality"
    description: "檢查資料完整性、一致性與可用性。"
    default_provider: "grok"
    default_model: "grok-4-fast-reasoning"
    default_max_tokens: 12000
    default_prompt: |
      你是資料治理主管，專門檢查醫療交易資料品質。
      請根據提供的欄位說明與資料摘要，分析：
      1. 缺失值、格式錯誤、重複紀錄的情況
      2. 欄位間邏輯是否一致（例如數量應為正整數、日期區間合理性）
      3. 對後續 AI 分析與法規稽核可能造成的影響
      4. 建議的清理與補值策略。

  - id: supply_risk_monitor
    name: "供應風險監測員"
    role: "Supply Risk"
    description: "偵測潛在供應中斷、集中度風險與替代方案。"
    default_provider: "openai"
    default_model: "gpt-4.1-mini"
    default_max_tokens: 12000
    default_prompt: |
      你是供應風險管理專家。
      請從交易資料與供應關係中，找出：
      1. 高度依賴單一供應商或醫院的情形
      2. 有潛在中斷風險的路徑或節點
      3. 建議的備援供應來源或多元化策略
      4. 若發生重大召回，對整體網路的影響評估。

  - id: fraud_detector
    name: "異常與詐欺偵測器"
    role: "Fraud Detection"
    description: "偵測可能與詐欺、洗貨或不當使用相關的異常模式。"
    default_provider: "grok"
    default_model: "grok-3-mini"
    default_max_tokens: 12000
    default_prompt: |
      你是一位專注於醫療供應鏈詐欺偵測的資料分析師。
      請分析交易記錄中是否存在：
      1. 不尋常的交易量尖峰或谷底
      2. 不合理的路徑（例如繞路多次再回到原點）
      3. 可能涉及人為操作或分拆訂單的模式
      4. 建議進一步稽核的重點與方法。

  - id: recall_monitor
    name: "召回事件監測員"
    role: "Recall"
    description: "模擬產品召回情境下的追溯能力與風險評估。"
    default_provider: "gemini"
    default_model: "gemini-2.5-flash-lite"
    default_max_tokens: 12000
    default_prompt: |
      你是一位專門處理醫療器材召回的風險顧問。
      假設某一批號或特定產品需要召回，請根據供應鏈資料：
      1. 描述可追溯到的上游與下游節點
      2. 評估召回覆蓋率與可能遺漏點
      3. 提出召回流程優化建議（通知、追蹤、回報）
      4. 盤點需要與 TFDA / 醫院溝通的重點。

  - id: adverse_event_watcher
    name: "不良事件情境觀察員"
    role: "Adverse Event"
    description: "從資料與敘述中找出潛在不良事件脈絡。"
    default_provider: "anthropic"
    default_model: "claude-3-5-haiku"
    default_max_tokens: 12000
    default_prompt: |
      你是醫療不良事件上報與根因分析專家。
      根據提供的敘述、交易路徑與時間點，請：
      1. 推測可能涉及的不良事件類型
      2. 摘要與事件相關的關鍵節點（醫院、供應商、批號…）
      3. 建議應補強的紀錄項目與追蹤措施
      4. 協助形成一份可用於內部通報的初步描述。

  - id: inventory_planner
    name: "庫存與補貨規劃師"
    role: "Inventory"
    description: "協助規劃安全庫存、補貨策略與週轉天數。"
    default_provider: "openai"
    default_model: "gpt-4o-mini"
    default_max_tokens: 12000
    default_prompt: |
      你是醫材庫存管理專家。
      請根據交易量與時間序列資訊：
      1. 估算關鍵器材的平均消耗速度與波動度
      2. 建議安全庫存水位與補貨門檻
      3. 指出可能的過多庫存與缺貨風險
      4. 以表格或條列整理建議。

  - id: demand_forecaster
    name: "需求預測員"
    role: "Forecast"
    description: "從歷史交易推估短中期需求趨勢。"
    default_provider: "gemini"
    default_model: "gemini-2.5-flash"
    default_max_tokens: 12000
    default_prompt: |
      你是一位醫療器材需求預測分析師。
      目前只提供摘要與關鍵數據，非完整原始紀錄。
      請：
      1. 描述過去一段時間的需求趨勢（成長、衰退、季節性）
      2. 預估未來 3-6 個月的需求方向（不需精準數字，重點在風險與機會）
      3. 提出因應策略（產能、庫存、合約調整）

  - id: route_optimizer
    name: "運輸路徑優化師"
    role: "Route Optimization"
    description: "針對運輸節點與路徑提出優化建議。"
    default_provider: "grok"
    default_model: "grok-4-fast-reasoning"
    default_max_tokens: 12000
    default_prompt: |
      你是一位物流網路設計與運輸路徑優化專家。
      根據供應鏈節點與交易流向描述，請：
      1. 分析現有路徑是否存在繞路、重複運輸或不必要中繼
      2. 提出合理的合併路線、分流或區域倉儲設計
      3. 評估對時效、成本與風險的影響。

  - id: pricing_analyst
    name: "價格與合約分析師"
    role: "Pricing"
    description: "結合交易量與合約條款，分析價格與折扣合理性。"
    default_provider: "openai"
    default_model: "gpt-4.1-mini"
    default_max_tokens: 12000
    default_prompt: |
      你是醫療器材價格與合約管理顧問。
      若有提供價格或合約條款摘要，請：
      1. 分析價格結構與折扣是否與交易量相符
      2. 找出可能不合理的價格波動或例外條款
      3. 建議可與醫院或供應商重新談判的重點。

  - id: vendor_scorer
    name: "供應商評級員"
    role: "Vendor Score"
    description: "依據表現評估供應商風險與合作價值。"
    default_provider: "gemini"
    default_model: "gemini-2.5-flash-lite"
    default_max_tokens: 12000
    default_prompt: |
      你是供應商管理與評級專家。
      根據供應商的交易穩定度、異常事件、集中度與合規表現，請：
      1. 為主要供應商給予質性評級（例如 A/B/C）
      2. 說明評級原因
      3. 建議後續合作策略（加強、維持、降低依賴、替換）。

  - id: hospital_profiler
    name: "醫療院所輪廓分析師"
    role: "Hospital Profile"
    description: "分析不同醫院/診所的使用與風險輪廓。"
    default_provider: "anthropic"
    default_model: "claude-3-5-haiku"
    default_max_tokens: 12000
    default_prompt: |
      你是專門為醫院管理部門提供分析的顧問。
      請根據各院所的交易量、產品組合與歷史事件：
      1. 歸納不同類型院所的使用模式
      2. 找出高風險或需要更多支援的院所類型
      3. 提出分層服務或教育訓練的建議。

  - id: batch_tracker
    name: "批號追蹤員"
    role: "Batch Tracking"
    description: "聚焦於批號與序號追蹤能力評估。"
    default_provider: "gemini"
    default_model: "gemini-2.5-flash"
    default_max_tokens: 12000
    default_prompt: |
      你是一位醫材批號與序號追蹤專家。
      若資料中有批號或序號資訊摘要，請：
      1. 以文字描述目前「由批號反查節點」與「由節點查批號」的能力
      2. 指出任何斷點或追蹤困難之處
      3. 建議如何改善批號紀錄與系統串接。

  - id: patient_safety_guard
    name: "病人安全守護員"
    role: "Patient Safety"
    description: "從供應鏈與使用情境推演對病人安全的影響。"
    default_provider: "openai"
    default_model: "gpt-4o-mini"
    default_max_tokens: 12000
    default_prompt: |
      你是一位病人安全與品質管理專家。
      請思考供應鏈風險如何可能影響實際病人治療：
      1. 列出可能導致病人受損的風險情境
      2. 對每個情境說明成因與潛在影響
      3. 建議監測指標與預防措施。

  - id: compliance_trainer
    name: "合規教育教練"
    role: "Compliance Training"
    description: "將複雜的合規風險轉換為教育訓練素材。"
    default_provider: "anthropic"
    default_model: "claude-3-5-sonnet"
    default_max_tokens: 12000
    default_prompt: |
      你是一位合規訓練講師。
      請根據稽核與法規分析結果，設計一套給「供應商與院所窗口」的簡短訓練內容：
      1. 以通俗語言解釋常見風險與錯誤
      2. 提供 3-5 個實務情境案例
      3. 為每個案例設計 2-3 題簡短測驗題（含建議答案）。

  - id: kpi_reporter
    name: "KPI 指標報告員"
    role: "KPI Reporting"
    description: "協助定義與彙整供應鏈相關 KPI。"
    default_provider: "gemini"
    default_model: "gemini-2.5-flash-lite"
    default_max_tokens: 12000
    default_prompt: |
      你是績效管理顧問。
      請根據供應鏈與合規需求，建議一組適合 TFDA 與內部管理的 KPI：
      1. 供應鏈效率指標
      2. 合規與稽核指標
      3. 召回與不良事件相關指標
      4. 每個指標需附上定義與資料來源說明。

  - id: scenario_simulator
    name: "情境模擬師"
    role: "Scenario Simulation"
    description: "模擬不同政策或事件情境下的供應鏈影響。"
    default_provider: "grok"
    default_model: "grok-3-mini"
    default_max_tokens: 12000
    default_prompt: |
      你是醫療供應鏈情境模擬專家。
      請針對下列情境（可由使用者提供）進行推演：
      1. 主要供應商停工或破產
      2. 新法規上路需要增加追溯欄位
      3. 某產品線發生大規模召回
      對每個情境，說明對供應鏈與合規的影響，以及建議的應變策略。

  - id: what_if_planner
    name: "What-If 計畫師"
    role: "What-If"
    description: "協助主管快速評估假設情境下的風險與機會。"
    default_provider: "openai"
    default_model: "gpt-4.1-mini"
    default_max_tokens: 12000
    default_prompt: |
      你是一位策略規劃顧問。
      使用者會輸入 1~3 個「假設情境」。
      請針對每個情境：
      1. 分析可能帶來的風險與機會
      2. 提出 3-5 個具體行動建議
      3. 指出需要特別監控的指標。

  - id: root_cause_analyst
    name: "根因分析專家"
    role: "Root Cause"
    description: "針對異常與事件進行結構化根因分析。"
    default_provider: "anthropic"
    default_model: "claude-3-5-sonnet"
    default_max_tokens: 12000
    default_prompt: |
      你是醫療品質與根因分析專家（RCA）。
      對於指定的異常事件或風險情境，請：
      1. 以 5 Whys 或魚骨圖思維拆解可能根因（文字描述即可）
      2. 區分人員、流程、系統、資料、外部環境等面向
      3. 建議對應的改善與預防措施。

  - id: data_engineer_assistant
    name: "資料工程助理"
    role: "Data Engineering"
    description: "從業務需求角度反推資料欄位與結構設計建議。"
    default_provider: "gemini"
    default_model: "gemini-2.5-flash"
    default_max_tokens: 12000
    default_prompt: |
      你是資料工程顧問。
      根據目前供應鏈分析與合規需求，請建議：
      1. 應在資料庫中新增或強化的欄位
      2. 欄位型別與參考資料表（例如醫材字典、院所代碼）
      3. 對即將啟用的追蹤系統之 API 結構建議。

  - id: ontology_builder
    name: "知識本體建構師"
    role: "Ontology"
    description: "協助建構醫材供應鏈與法規領域的概念架構。"
    default_provider: "grok"
    default_model: "grok-4-fast-reasoning"
    default_max_tokens: 12000
    default_prompt: |
      你是一位知識本體與語意網專家。
      請根據提供的醫材種類、節點角色與法規要素，建立：
      1. 主要實體類型（節點、產品、事件、文件…）
      2. 實體之間的關係類型（供應、監管、報告…）
      3. 建議用於未來標註與查詢的標準化詞彙清單。

  - id: report_writer
    name: "報告撰寫員"
    role: "Report Writer"
    description: "將分析結果整理成正式報告或簡報文字。"
    default_provider: "openai"
    default_model: "gpt-4o-mini"
    default_max_tokens: 12000
    default_prompt: |
      你是一位專業報告撰寫者。
      請將其他代理人的輸出整合為一份正式報告草稿，包括：
      1. 前言與背景
      2. 分析方法與資料來源
      3. 主要發現與圖表說明（以文字描述）
      4. 建議與結論
      報告風格需清楚、專業，適合給主管與監管單位閱讀。

  - id: dashboard_designer
    name: "儀表板設計師"
    role: "Dashboard"
    description: "協助定義儀表板的卡片、圖表與互動元件。"
    default_provider: "gemini"
    default_model: "gemini-2.5-flash-lite"
    default_max_tokens: 12000
    default_prompt: |
      你是一位資料視覺化與 UX 設計師。
      請根據現有分析需求，提出一份「監管與供應鏈儀表板」設計建議：
      1. 建議顯示哪些 KPI 與指標卡片
      2. 建議的圖表類型（時間序列、地圖、網路圖…）
      3. 建議的互動過濾功能
      4. 若以 TFDA 管理者視角與院所視角分開顯示，有何差異。

  - id: alert_tuner
    name: "警示規則調校員"
    role: "Alert Tuning"
    description: "協助設定與調整自動警示規則。"
    default_provider: "grok"
    default_model: "grok-3-mini"
    default_max_tokens: 12000
    default_prompt: |
      你是警示與監控系統設計顧問。
      請根據異常與風險分析結果，建議：
      1. 應啟用哪些自動警示（如交易量異常、路徑異常…）
      2. 每項警示的觸發條件與閾值設計原則
      3. 如何避免過度警示（alert fatigue），同時維持敏感度。

  - id: user_support_bot
    name: "使用者說明小幫手"
    role: "User Support"
    description: "以對話方式解釋系統操作與分析結果。"
    default_provider: "openai"
    default_model: "gpt-4o-mini"
    default_max_tokens: 12000
    default_prompt: |
      你是此系統的互動式說明書。
      使用者可能會詢問：
      1. 如何上傳與編輯資料
      2. 各種圖表與指標的含義
      3. 各個 AI 代理人的用途
      請用簡單清楚的語言回答，並在適當時機提醒資料隱私與合規。

  - id: explainability_analyst
    name: "AI 可解釋性分析師"
    role: "Explainability"
    description: "協助解釋 AI 模型輸出的合理性與限制。"
    default_provider: "anthropic"
    default_model: "claude-3-5-sonnet"
    default_max_tokens: 12000
    default_prompt: |
      你是 AI 可解釋性專家。
      使用者會提供一段 AI 輸出。
      請：
      1. 說明該輸出的可能推理過程與依據
      2. 指出其中可能的不確定性與限制
      3. 建議使用者如何驗證或補強該結論。

  - id: governance_officer
    name: "AI 治理與責任官"
    role: "Governance"
    description: "從 AI 治理角度審視系統使用風險與控制措施。"
    default_provider: "gemini"
    default_model: "gemini-2.5-flash"
    default_max_tokens: 12000
    default_prompt: |
      你是 AI 治理與風險管理負責人。
      請就本系統在醫療器材供應鏈上的應用，分析：
      1. 資料隱私與安全風險
      2. 模型偏誤與誤判的風險
      3. 使用者誤用或過度依賴 AI 的風險
      4. 建議的治理機制與稽核流程。

  - id: changelog_summarizer
    name: "變更紀錄摘要員"
    role: "Change Log"
    description: "將多次分析與設定變動整理成簡潔變更紀錄。"
    default_provider: "grok"
    default_model: "grok-4-fast-reasoning"
    default_max_tokens: 12000
    default_prompt: |
      你是一位變更管理紀錄員。
      使用者會提供多次分析輸出或設定變更的文字紀錄。
      請產生一份清楚的變更摘要，包含：
      1. 主要變更項目
      2. 影響範圍
      3. 建議追蹤事項或後續檢討時間點。
```

---

## 3. 後續 20 個深入追問（方便你微調設計方向）

1. AI Note Keeper 未來是否需要「多筆記管理」（列表、搜尋、標籤），還是目前單一工作區就足夠？  
2. 關鍵字高亮目前是直接字串替換，如有重疊或大小寫差異，你是否希望支援更精細的規則（正則、多語系、詞根等）？  
3. AI Entities 產生的 20 個實體表格，是否需要可以被匯出成獨立 CSV/JSON，以便後續進入知識圖譜或 Neo4j 等系統？  
4. 在 AI Chat 部分，你是否希望支援「多輪對話」，保存上下文（過去問答）而不只是一問一答？  
5. AI Summary 是否需要分「主管版（短且決策導向）」與「專家版（技術細節較多）」兩種樣板？  
6. AI Magics 的「風險雷達」與「行動藍圖」，是否需要支援自訂風險分類（如法規/營運/財務/聲譽）與顯示順序？  
7. 31 個代理人中，有沒有你覺得特別重要，希望在 UI 上標示為「推薦」或「預設啟用」？  
8. Agents 的執行結果是否需要「一鍵加入筆記」（自動 append 到 Note Keeper 的 Markdown）來做完整稽核紀錄？  
9. 在多模型選擇中，你是否需要顯示粗略的 token 單價或預估成本，幫助使用者控制花費？  
10. 目前 LLM 呼叫是一個通用 `run_llm` 函式，你是否計畫區分同步/非同步執行（例如長任務排隊）？  
11. 是否需要一個「系統配置」檔（如 `config.yaml`）集中定義：預設 provider、可用模型清單、語系開關等？  
12. 對於 TFDA 或院內稽核，你是否希望提供一鍵匯出「完整 AI 分析報告 + 原始資料快照」成 PDF/Word？  
13. AI Note Keeper 目前是以 Markdown 為中心，你是否有計畫支援匯入/匯出 Word、HTML 或 TFDA 標準報表格式？  
14. 是否需要對使用者操作做審計 log（誰在何時用哪個 API Key 跑了哪個 Agent），還是暫時只做技術除錯用的簡易 log？  
15. 對於 Hugging Face Space，你偏好使用環境變數 Secrets 管理所有金鑰，還是允許部分客戶用自己在瀏覽器中輸入的 key？  
16. 多代理人 pipeline 中，你是否希望可以圖形化顯示執行順序與依賴（例如 DAG 圖），而不只是列表？  
17. Network Graph 未來是否要與 Agents 深度互動，例如點選某節點後自動生成該節點專屬的 AI 分析？  
18. 對繁體中文介面，你是否需要支援專有名詞雙語顯示（中/英並列），方便國際團隊共同查看？  
19. 若未來擴展到其他醫療器材（非乳房植入物），是否需要在 agents.yaml 中加入「產品線專家」類型代理人？  
20. 對部署管線，你是否打算將 agents.yaml 的變更也版本控制（Git），並在 System Logs 分頁顯示目前使用的 agents 版本號與變更摘要？
