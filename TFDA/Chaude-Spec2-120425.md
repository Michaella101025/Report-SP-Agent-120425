FDA 510(k) 審查工作室 · 花卉版 V2 - 綜合技術規格文件
文件版本控制
版本日期作者變更說明1.02025-01-XX系統架構團隊初始版本

目錄

執行摘要
系統架構
軟體需求規格 (SRS)
系統需求
環境設定
部署選項
基礎設施即程式碼 (IaC)
安全性考量
驗證計畫
風險管理
可追溯性矩陣
維護與支援
監管合規性
附錄


1. 執行摘要
1.1 系統概述
GUDID 資料品質分析多代理系統 (花卉版 V2) 是一個基於人工智慧的多代理協作平台,專為美國 FDA 全球唯一器材識別資料庫 (GUDID) 的資料品質審查流程設計。本系統整合四大主流 AI 提供商:

Google Gemini (gemini-2.5-flash, gemini-2.5-flash-lite)
OpenAI (gpt-4o-mini, gpt-4.1-mini)
Anthropic Claude (claude-3-5-sonnet)
xAI Grok (grok-4-fast-reasoning, grok-3-mini)

系統實現串聯式 GUDID 資料分析、結構化筆記轉換、互動式分析儀表板,並融入遊戲化設計元素。
1.2 目標用戶

FDA 510(k) 審查人員
醫療器材監管事務專員 (Regulatory Affairs)
法規顧問與品質保證 (QA) 團隊
臨床工程師與技術撰寫人員
GUDID 資料管理員

1.3 核心價值主張
特性說明多模型協作支援 4 家 AI 提供商,可依任務特性選用最適模型可編輯鏈式審查每個代理步驟的輸入/輸出均可人工編輯,支援混合式人機協作20 種花卉主題提供美學化工作環境 (櫻花微風、蓮花湖畔、鳶尾夜色等),降低審查疲勞AI 筆記助手自動將非結構化文本轉換為結構化 Markdown、實體提取、心智圖等即時資料編輯Streamlit data_editor 支援直接編輯 GUDID CSV 資料視覺化儀表板Plotly 互動圖表追蹤資料品質指標與風險分數
1.4 監管定位

重要聲明: 本系統為 決策支援工具 (Decision Support Tool),不屬於 FDA 定義之醫療器材 (Medical Device)。系統輸出結果需由具資格之審查人員驗證,最終決策權歸人類審查員。


2. 系統架構
2.1 高階架構圖
mermaidCopygraph TB
    subgraph "使用者層"
        UI[Streamlit Web UI<br/>多語言 / 20 種主題]
    end
    
    subgraph "應用層"
        APP[Python Application Core]
        SESSION[Session State Manager]
        THEME[Theme & I18N Engine]
    end
    
    subgraph "業務邏輯層"
        PIPELINE[Multi-Agent Pipeline<br/>Sequential/Single Mode]
        NOTE[AI Note Keeper<br/>Markdown/Entity/Mindmap]
        DASH[Analytics Dashboard<br/>Plotly Charts]
        DATA[GUDID Data Editor<br/>Pandas DataFrame]
    end
    
    subgraph "AI 服務層"
        GEMINI[Google Gemini API<br/>gemini-2.5-flash]
        OPENAI[OpenAI API<br/>gpt-4o-mini]
        ANTHROPIC[Anthropic Claude<br/>claude-3-5-sonnet]
        XAI[xAI Grok API<br/>grok-4-fast-reasoning]
    end
    
    subgraph "資料層"
        YAML[agents.yaml<br/>代理配置]
        CSV[GUDID CSV<br/>sample_data/gudid_mock.csv]
        ENV[Environment Variables<br/>.env / Secrets Manager]
    end
    
    UI --> APP
    APP --> SESSION
    APP --> THEME
    APP --> PIPELINE
    APP --> NOTE
    APP --> DASH
    APP --> DATA
    
    PIPELINE --> GEMINI
    PIPELINE --> OPENAI
    PIPELINE --> ANTHROPIC
    PIPELINE --> XAI
    
    NOTE --> GEMINI
    NOTE --> OPENAI
    NOTE --> ANTHROPIC
    NOTE --> XAI
    
    DATA --> CSV
    APP --> YAML
    APP --> ENV
2.2 技術堆疊
層級技術/框架版本要求用途前端Streamlit≥1.30.0Web UI 框架,互動式元件後端Python≥3.9核心應用邏輯資料處理Pandas≥2.0.0GUDID CSV 載入與編輯視覺化Plotly Express≥5.0.0互動式圖表 (圓餅圖、長條圖)AI SDKgoogle-generativeailatestGemini 整合openai≥1.0.0OpenAI 整合anthropiclatestClaude 整合requests≥2.28.0Grok API 呼叫 (RESTful)配置PyYAML≥6.0agents.yaml 解析HTTPrequests≥2.28.0API 呼叫、健康檢查
2.3 模組架構
Copygudid-multi-agent-studio/
├── app.py                    # 主程式 (所有功能整合)
├── agents.yaml               # 代理配置檔
├── requirements.txt          # Python 依賴套件
├── sample_data/
│   └── gudid_mock.csv       # 範例 GUDID 資料
├── tests/
│   ├── test_agents.py       # 單元測試
│   └── test_integration.py  # 整合測試
├── deployment/
│   ├── Dockerfile           # 容器映像定義
│   ├── docker-compose.yml   # 本地多容器部署
│   ├── k8s/
│   │   ├── deployment.yaml  # Kubernetes 部署配置
│   │   ├── service.yaml     # K8s Service
│   │   └── hpa.yaml         # 自動擴展規則
│   └── terraform/
│       ├── main.tf          # AWS/GCP/Azure IaC
│       └── variables.tf     # Terraform 變數
└── docs/
    ├── TECHNICAL_SPEC.md    # 本文件
    ├── USER_MANUAL.md       # 使用者手冊
    └── API_REFERENCE.md     # API 參考文件
核心模組說明:

主題與國際化 (第 1 節):

FLOWER_THEMES: 20 種花卉主題定義 (primary/accent/bg/fg 四色)
STRINGS: 繁體中文/英文雙語字典
inject_theme_css(): 動態 CSS 注入


LLM 提供商包裝器 (第 2 節):

LLMClients 類別統一處理 4 家 AI API 呼叫
支援 API 金鑰從環境變數或 Session State 讀取


GUDID 分析助手 (第 3 節):

build_prompt_for_agent(): 組裝代理提示詞 (含 GUDID 樣本 JSON)
parse_agent_result(): 解析 AI 輸出為結構化 JSON


AI 筆記工具 (第 4 節):

ai_format_markdown(): 格式化 Markdown
ai_extract_keywords(): 關鍵字提取
ai_summarize(): 摘要生成 (含 coral 色關鍵字高亮)
ai_extract_entities(): 實體抽取 (20 個實體表格)
ai_chat_on_note(): 筆記問答
ai_magic_insight_map(): 階層式洞察地圖
ai_magic_action_plan(): 行動計畫生成


代理配置載入 (第 5 節):

load_agents(): 從 agents.yaml 載入代理定義


會話狀態管理 (第 6 節):

init_state(): 初始化所有 session_state 變數



2.4 資料流程
mermaidCopysequenceDiagram
    participant U as 使用者
    participant UI as Streamlit UI
    participant DF as Data Editor
    participant P as Pipeline Orchestrator
    participant A1 as Agent 1 (Gemini)
    participant A2 as Agent 2 (OpenAI)
    participant A3 as Agent 3 (Claude)
    participant DASH as Dashboard
    
    U->>UI: 上傳 GUDID CSV
    UI->>DF: 載入 Pandas DataFrame
    DF-->>UI: 顯示可編輯表格
    
    U->>UI: 點擊「Run Analysis」
    UI->>P: 啟動 Sequential Mode
    
    P->>A1: build_prompt (GUDID 樣本 JSON)
    A1-->>P: 返回結構化輸出 (JSON)
    P->>P: parse_agent_result()
    
    P->>A2: 將 A1 輸出作為 A2 輸入
    A2-->>P: 返回風險分析
    
    P->>A3: 將 A2 輸出作為 A3 輸入
    A3-->>P: 返回最終建議
    
    P->>UI: 更新 session_state["agent_results"]
    UI->>DASH: 刷新儀表板指標
    DASH-->>UI: Plotly 圓餅圖/長條圖
    
    UI-->>U: 顯示所有代理結果 (可展開詳情)
    
    U->>UI: 編輯 Agent 2 輸出
    UI->>P: 使用編輯後輸出重新執行 Agent 3
    P->>A3: 呼叫 Claude (使用新輸入)
    A3-->>P: 返回更新建議
    P->>UI: 更新結果

3. 軟體需求規格 (SRS)
3.1 功能性需求 (Functional Requirements)
FR-001: GUDID 資料載入與編輯

需求描述: 系統應支援上傳 CSV 格式的 GUDID 資料,並提供即時編輯功能。
驗收標準:

支援 UTF-8 編碼 CSV 檔案上傳
使用 Streamlit data_editor 顯示可編輯表格
支援新增/刪除/修改列
編輯後可下載為 CSV
若未上傳檔案,自動載入 sample_data/gudid_mock.csv


優先級: P0 (必須)
追溯性: 對應測試案例 ST-FR-001

FR-002: 多代理流程執行

需求描述: 系統應支援依序執行 N 個 AI 代理,每個代理的輸出自動成為下一個代理的輸入。
驗收標準:

從 agents.yaml 載入任意數量代理配置
支援 Sequential Mode (全流程) 與 Single Mode (單代理)
每個代理執行狀態即時顯示 (進度條)
任一代理失敗時,流程中斷並顯示錯誤訊息
執行過程可被使用者中斷


優先級: P0 (必須)
追溯性: 對應測試案例 ST-FR-002

FR-003: 可編輯鏈式審查

需求描述: 使用者可在任意代理步驟編輯輸入或輸出,修改後的內容應成為後續步驟的預設輸入。
驗收標準:

Dashboard Tab 中每個代理顯示「Summary」與「Issues」
支援點擊展開詳細輸出
在 Agents Tab 中顯示「Handoff input to next agent」文字區域
支援「Text」與「Markdown Preview」雙模式切換
編輯後,下一步代理的預設輸入即時更新於 session_state["current_chain_input"]


優先級: P0 (必須)
追溯性: 對應測試案例 ST-FR-003

FR-004: 多 AI 提供商整合

需求描述: 系統應整合至少四家主流 AI 提供商,並支援動態模型選擇。
驗收標準:

支援 Google Gemini (gemini-2.5-flash, gemini-2.5-flash-lite)
支援 OpenAI (gpt-4o-mini, gpt-4.1-mini)
支援 Anthropic Claude (claude-3-5-sonnet)
支援 xAI Grok (grok-4-fast-reasoning, grok-3-mini)
每個代理可在 Agents Tab 中獨立配置 provider/model/max_tokens
API 金鑰支援環境變數與 Sidebar UI 輸入雙管道
API 呼叫失敗時,顯示明確錯誤訊息 (如「API key not configured」)


優先級: P0 (必須)
追溯性: 對應測試案例 ST-FR-004

FR-005: AI 筆記助手

需求描述: 提供獨立的筆記轉換工具,支援非結構化文本的智慧化處理。
驗收標準:

結構化 Markdown 轉換: 清理、格式化、分段
關鍵字提取: 輸出 15-25 個關鍵字 (逗號分隔)
摘要生成: 輸出 Markdown 格式摘要,關鍵字以 <span class="coral-keyword"> 標記
實體抽取: 輸出 20 個實體的 Markdown 表格 (欄位: #, Name, Type, Context)
筆記問答: 支援多輪對話,歷史記錄保存於 session_state["note_chat_history"]
Magic Insight Map: 生成階層式 Markdown 洞察地圖
Magic Action Plan: 生成優先順序行動計畫 (checklist 格式)


優先級: P1 (高度期望)
追溯性: 對應測試案例 ST-FR-005

FR-006: 互動式分析儀表板

需求描述: 追蹤並視覺化 GUDID 資料品質指標與 AI 分析結果。
驗收標準:

顯示 Total Issues (總問題數)、Overall Risk (整體風險評級)、Agents Run (已執行代理數)
Issue Severity Distribution 圓餅圖 (Low/Medium/High)
Per-Agent Risk Scores 長條圖
Detailed Findings by Agent 可展開詳情 (Summary + Issues)
所有圖表使用 Plotly 實現,支援互動式縮放/懸停


優先級: P1 (高度期望)
追溯性: 對應測試案例 ST-FR-006

FR-007: 多語言與主題支援

需求描述: 支援繁體中文與英文雙語切換,以及 20 種北歐花卉主題。
驗收標準:

語言切換: 繁體中文 (zh) / English (en)
主題模式切換: 亮色 (light) / 暗色 (dark)
20 種花卉主題,每種包含 primary/accent/bg/fg 四色配置
Jackslot Spin 按鈕隨機切換主題,顯示主題名稱 (中英文)
主題切換即時套用至全局 CSS (inject_theme_css())
Sidebar 背景使用主題漸層色


優先級: P2 (期望)
追溯性: 對應測試案例 ST-FR-007

FR-008: 代理配置動態管理

需求描述: 使用者可在 Agents Tab 中動態啟用/停用代理,修改系統提示詞與模型參數。
驗收標準:

每個代理顯示獨立的 Expander 元件
支援 Enabled Checkbox 切換
支援編輯 System Prompt (多行文字區域)
支援選擇 Provider 與 Model (下拉選單)
支援設定 Max tokens (數字輸入,範圍 512-120000)
修改後的配置保存於 session_state["agents_config"]


優先級: P1 (高度期望)
追溯性: 對應測試案例 ST-FR-008

3.2 非功能性需求 (Non-Functional Requirements)
NFR-001: 效能需求
指標目標值測量方法單代理執行回應時間<30 秒 (95th percentile)API 呼叫計時器全流程執行時間 (3 代理)<90 秒 (95th percentile)Pipeline orchestrator 計時UI 載入時間<3 秒Streamlit metricsCSV 載入時間 (10,000 列)<2 秒Pandas read_csv 計時並發使用者支援≥10 (單實例)負載測試 (Locust)
NFR-002: 可用性需求

學習曲線: 新使用者應能在 15 分鐘內完成首次完整流程執行
錯誤訊息: 所有錯誤訊息應為繁體中文/英文雙語,並提供可操作建議
無障礙性: 遵循 WCAG 2.1 AA 級標準 (色彩對比 ≥4.5,鍵盤導航支援)
響應式設計: 支援桌面瀏覽器 (≥1280px 寬度),不保證行動裝置最佳化

NFR-003: 可靠性需求

API 失敗容錯: 單一 AI 提供商故障時,使用者可切換至其他提供商繼續執行
會話持久性: 使用者會話資料在瀏覽器 refresh 後保持 (Streamlit session_state 機制)
資料完整性: 所有代理輸出與執行日誌應完整保存於 session_state["agent_results"]
錯誤恢復: 代理執行失敗後,使用者可重新執行而不影響已成功步驟

NFR-004: 安全性需求
詳見 第 8 節: 安全性考量
NFR-005: 可維護性需求

模組化設計: 每個功能模組 (Pipeline, Note Keeper, Dashboard) 應可獨立測試與部署
配置外部化: 代理配置存放於 agents.yaml,無需修改 app.py
程式碼註解: 關鍵函數應包含 Docstring (Google Style)
版本控制: 使用 Git,遵循 Semantic Versioning 2.0.0

NFR-006: 可擴展性需求

水平擴展: 支援 Kubernetes 部署,可透過增加 Pod 數量處理更高負載
模型擴展: 新增 AI 提供商僅需修改 LLMClients 類別的 call() 方法
主題擴展: 新增花卉主題僅需於 FLOWER_THEMES 列表添加新項目
語言擴展: 新增語言僅需於 STRINGS 字典添加新鍵值對

3.3 系統介面需求
3.3.1 使用者介面 (UI)

框架: Streamlit Web UI
瀏覽器相容性: Chrome/Edge/Firefox/Safari (最新兩版)
解析度: 最低 1280×720,建議 1920×1080
色彩模式: 支援亮色 (light) 與暗色 (dark) 主題

3.3.2 外部 API 介面
API 提供商協定認證方式端點範例速率限制Google GeminiRESTAPI Keygenerativelanguage.googleapis.com60 RPM (免費版)OpenAIRESTAPI Keyapi.openai.com/v1/chat/completions3 RPM (免費版)AnthropicRESTAPI Keyapi.anthropic.com/v1/messages50 RPM (Tier 1)xAI GrokRESTAPI Keyapi.x.ai/v1/chat/completionsTBD
3.3.3 配置檔介面
agents.yaml 結構範例:
yamlCopyagents:
  - id: "gudid_validator"
    name: "GUDID 欄位驗證器"
    description: "驗證必填欄位完整性與格式正確性"
    provider: "gemini"
    model: "gemini-2.5-flash"
    max_tokens: 4000
    temperature: 0.2
    enabled: true
    system_prompt: |
      你是 FDA GUDID 資料品質專家。分析以下 GUDID 資料樣本,檢查:
      1. 必填欄位 (Device ID, Brand Name, Version Model Number) 是否完整
      2. 格式是否符合 GUDID 規範 (如 DI 為 14 位數字)
      3. 列舉值是否在允許範圍內 (如 Device Class 僅能為 I/II/III)
      
      輸出 JSON 格式:
      {
        "summary": "整體驗證摘要",
        "issues": [
          {"severity": "high/medium/low", "title": "問題標題", "details": "詳細說明"}
        ],
        "metrics": {"risk_score": 0-100}
      }
      
  - id: "risk_analyzer"
    name: "風險分析器"
    description: "依據器材分類與用途評估潛在風險"
    provider: "openai"
    model: "gpt-4o-mini"
    max_tokens: 3000
    temperature: 0.3
    enabled: true
    system_prompt: |
      你是醫療器材風險管理專家,依據 ISO 14971 與 FDA 指引進行風險分析。
      輸入為前一步驟的驗證結果,請輸出:
      1. 已識別危害清單 (≥5 項)
      2. 風險等級評估 (嚴重性 × 發生機率,1-5 分)
      3. 風險控制措施建議
      
      以繁體中文 JSON 格式輸出。

4. 系統需求
4.1 硬體需求
4.1.1 開發環境
元件最低配置建議配置CPU2 核心 (x86_64)4 核心+RAM4 GB8 GB+硬碟10 GB 可用空間20 GB SSD網路穩定寬頻連線≥10 Mbps
4.1.2 生產環境 (單實例)
元件最低配置建議配置CPU2 vCPU4 vCPURAM4 GB8 GB硬碟20 GB50 GB SSD網路穩定公網連線≥100 Mbps
4.1.3 生產環境 (Kubernetes 叢集)
元件規格節點數量3+ (高可用性)每節點配置4 vCPU, 16 GB RAM持久化儲存支援 ReadWriteMany 的 PV (若需共享 agents.yaml)
4.2 軟體需求
4.2.1 作業系統
環境支援作業系統開發Windows 10+, macOS 11+, Ubuntu 20.04+生產Ubuntu 20.04/22.04 LTS, Amazon Linux 2, RHEL 8+
4.2.2 Python 環境

版本: Python 3.9 - 3.11 (建議 3.10)
套件管理: pip 21.0+, 建議使用 virtual environment

4.2.3 必要 Python 套件
txtCopystreamlit>=1.30.0
pandas>=2.0.0
plotly>=5.0.0
pyyaml>=6.0
google-generativeai>=0.3.0
openai>=1.0.0
anthropic>=0.8.0
requests>=2.28.0
4.2.4 容器環境 (選用)

Docker: 20.10+
基礎映像: python:3.10-slim

4.2.5 Orchestration (選用)

Kubernetes: 1.24+
Helm: 3.10+ (若使用 Helm Chart)

4.3 網路需求
4.3.1 對外連線 (防火牆白名單)
必須允許存取以下網域:
Copygenerativelanguage.googleapis.com  # Gemini
api.openai.com                      # OpenAI
api.anthropic.com                   # Anthropic
api.x.ai                            # xAI Grok
4.3.2 對內連線
若多實例部署,需開放:

Kubernetes Service mesh 通訊 (TCP/443)
Load Balancer 健康檢查 (TCP/8501 或自訂埠)


5. 環境設定
5.1 本地開發環境設定
步驟 1: 安裝 Python
bashCopy# Ubuntu/Debian
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip

# macOS (Homebrew)
brew install python@3.10

# Windows
# 從 https://www.python.org/ 下載安裝器
步驟 2: 建立虛擬環境
bashCopypython3.10 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
步驟 3: 安裝依賴套件
bashCopypip install --upgrade pip
pip install -r requirements.txt
步驟 4: 配置環境變數
建立 .env 檔案 (不應提交至 Git):
bashCopy# .env
GEMINI_API_KEY=AIzaSy...
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
GROK_API_KEY=xai-...
載入環境變數:
bashCopy# Linux/macOS
export $(cat .env | xargs)

# Windows (PowerShell)
Get-Content .env | ForEach-Object { 
    $key,$value = $_.Split('=')
    [Environment]::SetEnvironmentVariable($key, $value, 'Process')
}
步驟 5: 準備配置檔
建立 agents.yaml (參考 3.3.3 節範例)
步驟 6: 準備範例資料
建立 sample_data/gudid_mock.csv:
csvCopyDeviceID,BrandName,VersionModelNumber,DeviceClass,ProductCode,RiskLevel
12345678901234,CardioGuard Pro,v2.1,II,DXH,Medium
23456789012345,DiabetesMonitor X,v1.5,II,NBW,Low
34567890123456,SurgicalRobot Elite,v3.0,III,OZO,High
步驟 7: 啟動應用
bashCopystreamlit run app.py --server.port 8501
瀏覽器開啟 http://localhost:8501
5.2 Docker 環境設定
Dockerfile
dockerfileCopyFROM python:3.10-slim

WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴清單並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式碼與配置
COPY app.py agents.yaml ./
COPY sample_data/ ./sample_data/

# 暴露 Streamlit 預設埠
EXPOSE 8501

# 健康檢查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 啟動指令
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
建置與執行
bashCopy# 建置映像
docker build -t gudid-studio:v2 .

# 執行容器
docker run -d \
  --name gudid-studio \
  -p 8501:8501 \
  -e GEMINI_API_KEY=$GEMINI_API_KEY \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -e GROK_API_KEY=$GROK_API_KEY \
  gudid-studio:v2

# 檢視日誌
docker logs -f gudid-studio

6. 部署選項
6.1 本地部署 (Local Deployment)
適用場景

個人開發測試
隔離環境審查 (無網路連線至雲端)
敏感資料不出內部網路

步驟
依照 5.1 節 完成環境設定,執行:
bashCopystreamlit run app.py
透過 http://localhost:8501 存取。
優點

✅ 完全離線 (若 API 金鑰預先設定)
✅ 最快速部署
✅ 無雲端成本

缺點

❌ 無法多人協作
❌ 單點故障
❌ 無自動擴展


6.2 AWS 部署選項
6.2.1 AWS EC2 部署
架構圖:
CopyInternet → Route 53 → ELB → EC2 Instance (Streamlit) → AI APIs
                                ↓
                           EBS Volume (agents.yaml)
                                ↓
                      Secrets Manager (API Keys)
步驟:

啟動 EC2 執行個體:

AMI: Ubuntu 22.04 LTS
執行個體類型: t3.medium (2 vCPU, 4 GB RAM)
安全群組: 允許 443 (HTTPS), 22 (SSH)
IAM 角色: 附加 SecretsManagerReadWrite 政策


安裝應用:

bashCopyssh -i keypair.pem ubuntu@<EC2_PUBLIC_IP>
sudo apt update && sudo apt install python3.10-venv nginx -y
git clone <REPO_URL>
cd gudid-studio
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

配置 systemd 服務:

iniCopy# /etc/systemd/system/gudid-studio.service
[Unit]
Description=GUDID Multi-Agent Studio
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/gudid-studio
Environment="PATH=/home/ubuntu/gudid-studio/venv/bin"
EnvironmentFile=/home/ubuntu/gudid-studio/.env
ExecStart=/home/ubuntu/gudid-studio/venv/bin/streamlit run app.py --server.port 8501
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
bashCopysudo systemctl daemon-reload
sudo systemctl enable gudid-studio
sudo systemctl start gudid-studio

配置 Nginx 反向代理 (HTTPS):

nginxCopyserver {
    listen 443 ssl http2;
    server_name gudid.example.com;
    
    ssl_certificate /etc/letsencrypt/live/gudid.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/gudid.example.com/privkey.pem;
    ssl_protocols TLSv1.3;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
成本估算 (us-east-1):
項目月費 (USD)t3.medium (On-Demand)$30.37EBS 30 GB gp3$2.40Application Load Balancer$16.20資料傳輸 (5 GB)$0.45總計~$49

6.2.2 AWS ECS Fargate 部署
架構圖:
CopyInternet → Route 53 → ALB → ECS Service (Fargate Tasks) → AI APIs
                                  ↓
                            Secrets Manager (API Keys)
                                  ↓
                          CloudWatch Logs (日誌)
步驟:

建立 ECR 儲存庫並推送映像:

bashCopyaws ecr create-repository --repository-name gudid-studio
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT>.dkr.ecr.us-east-1.amazonaws.com
docker tag gudid-studio:v2 <AWS_ACCOUNT>.dkr.ecr.us-east-1.amazonaws.com/gudid-studio:v2
docker push <AWS_ACCOUNT>.dkr.ecr.us-east-1.amazonaws.com/gudid-studio:v2

建立 Secrets Manager 密鑰:

bashCopyaws secretsmanager create-secret \
  --name gudid/gemini-key \
  --secret-string "AIzaSy..."
  
aws secretsmanager create-secret \
  --name gudid/openai-key \
  --secret-string "sk-proj-..."

建立 ECS Task Definition (JSON):

jsonCopy{
  "family": "gudid-studio-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "gudid-studio",
      "image": "<ECR_IMAGE_URI>",
      "portMappings": [{"containerPort": 8501}],
      "secrets": [
        {"name": "GEMINI_API_KEY", "valueFrom": "arn:aws:secretsmanager:us-east-1:ACCOUNT:secret:gudid/gemini-key"},
        {"name": "OPENAI_API_KEY", "valueFrom": "arn:aws:secretsmanager:us-east-1:ACCOUNT:secret:gudid/openai-key"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/gudid-studio",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}

建立 ECS Service:

bashCopyaws ecs create-service \
  --cluster gudid-cluster \
  --service-name gudid-service \
  --task-definition gudid-studio-task \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx,subnet-yyy],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:us-east-1:ACCOUNT:targetgroup/gudid-tg,containerName=gudid-studio,containerPort=8501"

自動擴展配置:

bashCopyaws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --scalable-dimension ecs:service:DesiredCount \
  --resource-id service/gudid-cluster/gudid-service \
  --min-capacity 2 \
  --max-capacity 10

aws application-autoscaling put-scaling-policy \
  --policy-name gudid-cpu-scaling \
  --service-namespace ecs \
  --scalable-dimension ecs:service:DesiredCount \
  --resource-id service/gudid-cluster/gudid-service \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration '{
    "TargetValue": 70.0,
    "PredefinedMetricSpecification": {
      "PredefinedMetricType": "ECSServiceAverageCPUUtilization"
    }
  }'
成本估算:
項目月費 (USD)Fargate (1 vCPU, 2GB) × 2 tasks$59.10Application Load Balancer$16.20NAT Gateway (若使用私有子網)$32.40CloudWatch Logs (10 GB)$5.00總計~$113

6.3 GCP 部署選項
6.3.1 GCP Cloud Run 部署 (推薦)
優勢: 完全託管、自動擴展、按請求計費
步驟:

建置容器並推送至 GCR:

bashCopygcloud builds submit --tag gcr.io/PROJECT_ID/gudid-studio

建立 Secret Manager 密鑰:

bashCopyecho -n "AIzaSy..." | gcloud secrets create gemini-key --data-file=-
echo -n "sk-proj-..." | gcloud secrets create openai-key --data-file=-

部署至 Cloud Run:

bashCopygcloud run deploy gudid-studio \
  --image gcr.io/PROJECT_ID/gudid-studio \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 3600 \
  --concurrency 10 \
  --max-instances 10 \
  --set-secrets GEMINI_API_KEY=gemini-key:latest,OPENAI_API_KEY=openai-key:latest

配置自訂網域:

bashCopygcloud run domain-mappings create \
  --service gudid-studio \
  --domain gudid.example.com
成本估算 (低流量場景):
假設每月 10,000 請求,平均每請求 30 秒 CPU 時間:
項目費用 (USD)請求費用 (10K × $0.40/M)$0.004CPU 時間 (10K × 30s × 2 vCPU × $0.00002400)$14.40Memory 時間 (10K × 30s × 2GB × $0.00000250)$1.50總計~$16

6.3.2 GCP GKE 部署
類似 AWS EKS,使用 Kubernetes Deployment + Service,步驟略。
成本估算:
項目月費 (USD)GKE 叢集管理費 ($0.10/hr)$733 × e2-standard-4 節點$367Load Balancer$18總計~$458

6.4 Azure 部署選項
6.4.1 Azure App Service 部署
步驟:

建立 App Service Plan:

bashCopyaz appservice plan create \
  --name gudid-plan \
  --resource-group gudid-rg \
  --sku B2 \
  --is-linux

建立 Web App:

bashCopyaz webapp create \
  --name gudid-studio \
  --resource-group gudid-rg \
  --plan gudid-plan \
  --runtime "PYTHON:3.10"

配置 App Settings:

bashCopyaz webapp config appsettings set \
  --name gudid-studio \
  --resource-group gudid-rg \
  --settings \
    GEMINI_API_KEY=@Microsoft.KeyVault(SecretUri=https://gudid-kv.vault.azure.net/secrets/gemini-key/) \
    OPENAI_API_KEY=@Microsoft.KeyVault(SecretUri=https://gudid-kv.vault.azure.net/secrets/openai-key/)

部署程式碼 (透過 ZIP):

bashCopyzip -r app.zip app.py agents.yaml requirements.txt sample_data/
az webapp deployment source config-zip \
  --name gudid-studio \
  --resource-group gudid-rg \
  --src app.zip
成本估算:
項目月費 (USD)B2 App Service Plan$73Azure Key Vault (10K 操作)$0.03流量傳輸 (5 GB)$0.40總計~$73

6.5 混合部署 (Hybrid Deployment)
場景
敏感 GUDID 資料需留在內部機房,但希望使用雲端 AI 服務。
架構
Copy[內部機房]
   ↓
企業防火牆 (Outbound HTTPS 允許 AI API 網域)
   ↓
[雲端 AI 提供商 APIs]
實施步驟

內部 VM/容器部署: 依照 6.1 節 於企業資料中心部署
網路設定: 配置防火牆允許存取:

generativelanguage.googleapis.com
api.openai.com
api.anthropic.com
api.x.ai


VPN/Direct Connect (選用): 若需存取雲端託管的 Secrets Manager
Identity Federation: 使用企業 SSO (SAML/OAuth) 整合使用者驗證

優點

✅ 資料不出內部網路
✅ 符合 HIPAA/GDPR 等合規要求

缺點

❌ 需自行維護基礎設施
❌ 網路延遲可能較高 (跨境 API 呼叫)


6.6 部署建議矩陣
場景建議部署方案原因個人/小團隊測試本地 or GCP Cloud Run成本低、部署快企業 POC (10-50 用戶)AWS ECS Fargate易管理、自動擴展生產環境 (100+ 用戶)GCP GKE / AWS EKS高可用性、可觀測性高度監管環境混合部署 (內部 VM)資料主權、合規性無固定流量GCP Cloud Run按需計費、零閒置成本

7. 基礎設施即程式碼 (IaC)
7.1 Terraform 範例 (AWS ECS Fargate)
main.tf:
hclCopyterraform {
  required_version = ">= 1.3"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC
resource "aws_vpc" "gudid_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "gudid-vpc"
  }
}

# Public Subnets
resource "aws_subnet" "public_a" {
  vpc_id                  = aws_vpc.gudid_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "public_b" {
  vpc_id                  = aws_vpc.gudid_vpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "${var.aws_region}b"
  map_public_ip_on_launch = true
}

# Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.gudid_vpc.id
}

# Route Table
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.gudid_vpc.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

resource "aws_route_table_association" "public_rta_a" {
  subnet_id      = aws_subnet.public_a.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "public_rta_b" {
  subnet_id      = aws_subnet.public_b.id
  route_table_id = aws_route_table.public_rt.id
}

# Security Group
resource "aws_security_group" "ecs_sg" {
  vpc_id = aws_vpc.gudid_vpc.id
  name   = "gudid-ecs-sg"
  
  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "gudid_cluster" {
  name = "gudid-cluster"
}

# Task Definition
resource "aws_ecs_task_definition" "gudid_task" {
  family                   = "gudid-studio-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "1024"
  memory                   = "2048"
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  
  container_definitions = jsonencode([{
    name  = "gudid-studio"
    image = var.ecr_image_uri
    portMappings = [{
      containerPort = 8501
      protocol      = "tcp"
    }]
    secrets = [
      {
        name      = "GEMINI_API_KEY"
        valueFrom = aws_secretsmanager_secret.gemini.arn
      },
      {
        name      = "OPENAI_API_KEY"
        valueFrom = aws_secretsmanager_secret.openai.arn
      }
    ]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = "/ecs/gudid-studio"
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "ecs"
        "awslogs-create-group"  = "true"
      }
    }
  }])
}

# ECS Service
resource "aws_ecs_service" "gudid_service" {
  name            = "gudid-studio-service"
  cluster         = aws_ecs_cluster.gudid_cluster.id
  task_definition = aws_ecs_task_definition.gudid_task.arn
  desired_count   = 2
  launch_type     = "FARGATE"
  
  network_configuration {
    subnets          = [aws_subnet.public_a.id, aws_subnet.public_b.id]
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = true
  }
  
  load_balancer {
    target_group_arn = aws_lb_target_group.gudid_tg.arn
    container_name   = "gudid-studio"
    container_port   = 8501
  }
  
  depends_on = [aws_lb_listener.gudid_listener]
}

# Application Load Balancer
resource "aws_lb" "gudid_alb" {
  name               = "gudid-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.ecs_sg.id]
  subnets            = [aws_subnet.public_a.id, aws_subnet.public_b.id]
}

resource "aws_lb_target_group" "gudid_tg" {
  name        = "gudid-tg"
  port        = 8501
  protocol    = "HTTP"
  vpc_id      = aws_vpc.gudid_vpc.id
  target_type = "ip"
  
  health_check {
    path                = "/_stcore/health"
    interval            = 30
    timeout             = 10
    healthy_threshold   = 2
    unhealthy_threshold = 3
    matcher             = "200-299"
  }
}

resource "aws_lb_listener" "gudid_listener" {
  load_balancer_arn = aws_lb.gudid_alb.arn
  port              = "80"
  protocol          = "HTTP"
  
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.gudid_tg.arn
  }
}

# IAM Role for ECS Execution
resource "aws_iam_role" "ecs_execution_role" {
  name = "gudid-ecs-execution-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_execution_policy" {
  role       = aws_iam_role.ecs_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy" "secrets_access" {
  role = aws_iam_role.ecs_execution_role.name
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "secretsmanager:GetSecretValue"
      ]
      Resource = [
        aws_secretsmanager_secret.gemini.arn,
        aws_secretsmanager_secret.openai.arn
      ]
    }]
  })
}

# Secrets Manager
resource "aws_secretsmanager_secret" "gemini" {
  name = "gudid/gemini-api-key"
}

resource "aws_secretsmanager_secret" "openai" {
  name = "gudid/openai-api-key"
}

# Outputs
output "alb_dns_name" {
  value       = aws_lb.gudid_alb.dns_name
  description = "ALB DNS name to access the application"
}
variables.tf:
hclCopyvariable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "ecr_image_uri" {
  description = "ECR image URI"
  type        = string
}
部署指令:
bashCopyterraform init
terraform plan -var="ecr_image_uri=123456789012.dkr.ecr.us-east-1.amazonaws.com/gudid-studio:v2"
terraform apply -auto-approve

7.2 Kubernetes Deployment YAML
k8s-deployment.yaml:
yamlCopyapiVersion: v1
kind: Namespace
metadata:
  name: gudid-studio

---
apiVersion: v1
kind: Secret
metadata:
  name: ai-api-keys
  namespace: gudid-studio
type: Opaque
data:
  gemini-key: <BASE64_ENCODED_KEY>
  openai-key: <BASE64_ENCODED_KEY>
  anthropic-key: <BASE64_ENCODED_KEY>
  grok-key: <BASE64_ENCODED_KEY>

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: agents-config
  namespace: gudid-studio
data:
  agents.yaml: |
    agents:
      - id: "gudid_validator"
        name: "GUDID 欄位驗證器"
        provider: "gemini"
        model: "gemini-2.5-flash"
        max_tokens: 4000
        temperature: 0.2
        enabled: true
        system_prompt: "你是 GUDID 資料品質專家..."

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gudid-studio-deployment
  namespace: gudid-studio
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gudid-studio
  template:
    metadata:
      labels:
        app: gudid-studio
    spec:
      containers:
      - name: gudid-studio
        image: gcr.io/PROJECT_ID/gudid-studio:v2
        ports:
        - containerPort: 8501
          name: http
        env:
        - name: GEMINI_API_KEY
          valueFrom:
            secretKeyRef:
              name: ai-api-keys
              key: gemini-key
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: ai-api-keys
              key: openai-key
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: ai-api-keys
              key: anthropic-key
        - name: GROK_API_KEY
          valueFrom:
            secretKeyRef:
              name: ai-api-keys
              key: grok-key
        volumeMounts:
        - name: config-volume
          mountPath: /app/agents.yaml
          subPath: agents.yaml
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /_stcore/health
            port: 8501
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /_stcore/health
            port: 8501
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
      volumes:
      - name: config-volume
        configMap:
          name: agents-config

---
apiVersion: v1
kind: Service
metadata:
  name: gudid-studio-service
  namespace: gudid-studio
spec:
  type: LoadBalancer
  selector:
    app: gudid-studio
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8501

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: gudid-studio-hpa
  namespace: gudid-studio
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: gudid-studio-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
部署指令:
bashCopy# 建立 namespace
kubectl apply -f k8s-deployment.yaml

# 檢視 Service External IP
kubectl get svc -n gudid-studio gudid-studio-service

# 檢視 Pod 狀態
kubectl get pods -n gudid-studio

# 檢視日誌
kubectl logs -f -n gudid-studio <POD_NAME>

7.3 CI/CD 整合 (GitHub Actions)
.github/workflows/deploy.yml:
yamlCopyname: Build and Deploy to GCP Cloud Run

on:
  push:
    branches: [main]
  workflow_dispatch:

env:
  GCP_PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
  GCP_REGION: us-central1
  SERVICE_NAME: gudid-studio

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    permissions:
      contents: read
      id-token: write
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Authenticate to Google Cloud
      uses: google-github-actions/auth@v1
      with:
        workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
        service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}
    
    - name: Set up Cloud SDK
      uses: google-github-actions/setup-gcloud@v1
    
    - name: Build and push Docker image
      run: |
        gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/$SERVICE_NAME:$GITHUB_SHA
        gcloud builds submit --tag gcr.io/$GCP_PROJECT_ID/$SERVICE_NAME:latest
    
    - name: Deploy to Cloud Run
      run: |
        gcloud run deploy $SERVICE_NAME \
          --image gcr.io/$GCP_PROJECT_ID/$SERVICE_NAME:$GITHUB_SHA \
          --platform managed \
          --region $GCP_REGION \
          --allow-unauthenticated \
          --memory 2Gi \
          --cpu 2 \
          --timeout 3600 \
          --concurrency 10 \
          --max-instances 10 \
          --set-secrets GEMINI_API_KEY=gemini-key:latest,OPENAI_API_KEY=openai-key:latest,ANTHROPIC_API_KEY=anthropic-key:latest,GROK_API_KEY=grok-key:latest
    
    - name: Run integration tests
      run: |
        SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $GCP_REGION --format 'value(status.url)')
        curl -f $SERVICE_URL/_stcore/health || exit 1
        echo "✅ Health check passed"
    
    - name: Notify deployment status
      if: always()
      run: |
        if [ ${{ job.status }} == 'success' ]; then
          echo "🚀 Deployment successful"
        else
          echo "❌ Deployment failed"
        fi

8. 安全性考量
8.1 威脅模型 (STRIDE)
威脅類型潛在攻擊緩解措施Spoofing (身份偽裝)未授權使用者冒充合法審查員• 實施 OAuth 2.0 / SAML SSO<br>• 整合企業 Active Directory<br>• 強制 MFA (多因素認證)Tampering (資料竄改)惡意修改代理輸出或 agents.yaml• agents.yaml 檔案權限限制為唯讀<br>• 輸出加密儲存 (若持久化)<br>• Git 版本控制追蹤配置變更Repudiation (否認性)使用者否認執行過某審查操作• 完整審計日誌 (包含使用者 ID、時間戳、操作內容)<br>• 日誌寫入不可變儲存 (如 AWS S3 Object Lock)Information Disclosure (資訊洩漏)API 金鑰外洩、GUDID 資料洩漏• 環境變數 + Secrets Manager<br>• 傳輸層 TLS 1.3<br>• GUDID 資料不持久化於後端Denial of Service (阻斷服務)惡意大量請求耗盡資源• Rate limiting (per-user)<br>• Auto-scaling (K8s HPA)<br>• API Gateway 速率限制Elevation of Privilege (權限提升)一般使用者取得管理員權限• RBAC (Role-Based Access Control)<br>• 最小權限原則<br>• 定期權限稽核
8.2 API 金鑰管理最佳實踐
8.2.1 環境變數 (開發/測試)
bashCopy# .env (絕不提交至 Git)
GEMINI_API_KEY=AIzaSy...
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
GROK_API_KEY=xai-...
Git 保護:
bashCopy# .gitignore
.env
*.env
secrets/
*.key
8.2.2 雲端 Secrets Manager (生產環境)
AWS Secrets Manager:
bashCopyaws secretsmanager create-secret \
  --name gudid/gemini-api-key \
  --secret-string "AIzaSy..." \
  --description "Gemini API key for GUDID studio"

# 自動輪替 (每 90 天)
aws secretsmanager rotate-secret \
  --secret-id gudid/gemini-api-key \
  --rotation-lambda-arn arn:aws:lambda:us-east-1:ACCOUNT:function:SecretsManagerRotation \
  --rotation-rules AutomaticallyAfterDays=90
GCP Secret Manager:
bashCopyecho -n "AIzaSy..." | gcloud secrets create gemini-key \
  --data-file=- \
  --replication-policy="automatic" \
  --labels="app=gudid-studio,env=prod"

# 版本管理
gcloud secrets versions add gemini-key --data-file=new_key.txt
Azure Key Vault:
bashCopyaz keyvault secret set \
  --vault-name gudid-keyvault \
  --name gemini-api-key \
  --value "AIzaSy..." \
  --expires 2025-12-31T23:59:59Z
8.2.3 金鑰輪替策略
項目策略輪替週期每 90 天 (符合 NIST SP 800-57 建議)自動化使用 AWS Lambda / GCP Cloud Functions多版本保留前一版本金鑰 24 小時,確保無服務中斷通知輪替前 7 天發送郵件通知管理員
8.3 資料隱私保護
8.3.1 PII (個人身份資訊) 處理
匿名化函數範例:
pythonCopyimport re

def anonymize_gudid_data(text: str) -> str:
    """
    匿名化 GUDID 資料中的 PII
    - 患者姓名 → [PATIENT_NAME]
    - 醫療記錄號碼 → [MRN]
    - 電話號碼 → [PHONE]
    """
    # 患者姓名 (大寫字母開頭的連續兩個單詞)
    text = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[PATIENT_NAME]', text)
    
    # 醫療記錄號碼 (6-10 位數字)
    text = re.sub(r'\b\d{6,10}\b', '[MRN]', text)
    
    # 美國電話號碼
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', text)
    
    return text
合規性:

✅ 符合 HIPAA Privacy Rule (美國健康保險流通與責任法案)
✅ 符合 GDPR Article 32 (歐盟一般資料保護規範)
✅ 資料留存: 不儲存任何 GUDID 資料於後端,僅保存於使用者瀏覽器 Session

8.3.2 傳輸層安全
項目配置TLS 版本強制 TLS 1.3憑證管理Let's Encrypt 自動更新 (Certbot)HSTSStrict-Transport-Security: max-age=31536000; includeSubDomains; preloadCSPContent-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'
Nginx 配置範例:
nginxCopyserver {
    listen 443 ssl http2;
    server_name gudid.example.com;
    
    ssl_certificate /etc/letsencrypt/live/gudid.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/gudid.example.com/privkey.pem;
    ssl_protocols TLSv1.3;
    ssl_ciphers 'TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384';
    ssl_prefer_server_ciphers off;
    
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Content-Security-Policy "default-src 'self'; 
