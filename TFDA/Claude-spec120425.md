醫療器材供應鏈追蹤系統 v2.1 - BioChain Analyst Pro
綜合技術規格文件

文件版本控制
版本日期作者變更說明1.02025-01-XX系統架構師初始版本

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
BioChain Analyst Pro v2.1 (醫療器材供應鏈追蹤系統) 是一個基於人工智慧的多代理協作平台,專為醫療器材供應鏈管理與監管追蹤設計。本系統整合四大主流 AI 提供商 (Google Gemini, OpenAI, Anthropic Claude, xAI Grok),實現:

供應鏈資料視覺化: 互動式儀表板、網路圖、時間序列分析
AI 驅動分析: 多代理串聯式資料分析與風險評估
可編輯工作流程: 每個代理步驟的輸入/輸出均可人工編輯
多模型支援: 靈活選擇最適合任務特性的 AI 模型
主題化 UI: 20 種花卉主題提供美學化工作環境

1.2 目標用戶

醫療器材供應鏈管理人員
監管事務專員
品質保證/品質控制團隊
醫療器材製造商與經銷商
醫院/診所採購與庫存管理人員

1.3 核心價值主張
特性價值多模型協作支援 8+ AI 模型,可依任務複雜度、成本、速度需求選擇最佳模型供應鏈透明化即時追蹤從供應商到終端醫療機構的完整路徑風險預警AI 自動識別異常交易模式、斷鏈風險、合規問題可編輯分析人機協作模式,允許專家干預與修正 AI 分析結果多語言支援繁體中文 / 英文雙語切換美學化介面20 種北歐花卉主題降低長時間使用疲勞
1.4 監管定位
本系統為 決策支援工具 (Decision Support Tool),不屬於醫療器材。系統輸出結果需由具資格之管理人員驗證,最終決策權歸人類使用者。

2. 系統架構
2.1 高階架構圖
mermaidCopygraph TB
    subgraph "使用者層"
        UI[Streamlit Web UI]
    end
    
    subgraph "應用層"
        APP[Python Application Core]
        SESSION[Session State Manager]
        DATA[Data Management Module]
    end
    
    subgraph "業務邏輯層"
        PIPELINE[Multi-Agent Pipeline Orchestrator]
        VIZ[Visualization Engine]
        ANALYTICS[Analytics Module]
    end
    
    subgraph "AI 服務層"
        GEMINI[Google Gemini API]
        OPENAI[OpenAI API]
        ANTHROPIC[Anthropic Claude API]
        XAI[xAI Grok API]
    end
    
    subgraph "資料層"
        CSV[CSV Data Files]
        YAML[agents.yaml Config]
        ENV[Environment Variables]
        LOGS[Execution Logs]
    end
    
    UI --> APP
    APP --> SESSION
    APP --> DATA
    APP --> PIPELINE
    APP --> VIZ
    APP --> ANALYTICS
    
    PIPELINE --> GEMINI
    PIPELINE --> OPENAI
    PIPELINE --> ANTHROPIC
    PIPELINE --> XAI
    
    DATA --> CSV
    APP --> YAML
    APP --> ENV
    PIPELINE --> LOGS
    VIZ --> ANALYTICS
2.2 技術堆疊
層級技術/框架版本要求用途前端Streamlit≥1.30.0Web UI 框架後端Python≥3.9核心應用邏輯資料處理pandas≥2.0.0資料操作與分析視覺化Altair≥5.0.0統計圖表pyvis≥0.3.0網路圖視覺化networkx≥3.0圖形分析AI SDKsgoogle-generativeailatestGemini 整合openai≥1.0.0OpenAI 整合anthropiclatestClaude 整合requests≥2.31.0Grok API 呼叫配置PyYAML≥6.0agents.yaml 解析
2.3 模組架構
Copybiochain-analyst-pro/
├── app.py                      # 主應用程式
├── agents.yaml                 # AI 代理配置檔
├── mock_dataset.csv            # 預設範例資料
├── requirements.txt            # Python 依賴清單
├── .env.example                # 環境變數範本
├── tests/                      # 測試套件
│   ├── test_data_processing.py
│   ├── test_agent_execution.py
│   └── test_visualization.py
├── deployment/                 # 部署配置
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── k8s/
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   └── terraform/
│       ├── aws/
│       ├── gcp/
│       └── azure/
└── docs/                       # 文件
    ├── user_manual.md
    ├── api_reference.md
    └── deployment_guide.md
核心模組說明
模組名稱功能描述Config & ConstantsAI 模型清單、花卉主題定義、多語系字典Helper Functions配置載入、Mock 資料生成、API 金鑰管理Session ManagementStreamlit session_state 初始化與持久化AI Call Helpers統一 AI API 呼叫介面、錯誤處理、重試邏輯Visualization Helpers儀表板渲染、網路圖生成、時間序列圖表Data SectionCSV 上傳、資料編輯、匯出功能Agents Section多代理管線編排、輸入/輸出編輯、狀態管理Settings Section語言切換、主題選擇、API 金鑰設定
2.4 資料流程
mermaidCopysequenceDiagram
    participant U as 使用者
    participant UI as Streamlit UI
    participant DM as Data Manager
    participant P as Pipeline Orchestrator
    participant AI as AI Provider
    participant LOG as Execution Log
    
    U->>UI: 上傳 CSV 資料
    UI->>DM: 載入資料至 DataFrame
    DM->>UI: 顯示資料預覽
    
    U->>UI: 配置 Agent 1 (選擇模型/調整參數)
    U->>UI: 執行 Agent 1
    UI->>P: 啟動 Agent 1
    P->>AI: 呼叫 AI API (附帶資料摘要)
    AI-->>P: 返回分析結果
    P->>LOG: 記錄執行狀態
    P->>UI: 更新 Agent 1 輸出
    
    U->>UI: 編輯 Agent 1 輸出
    U->>UI: 執行 Agent 2 (使用編輯後輸入)
    UI->>P: 啟動 Agent 2
    P->>AI: 呼叫 AI API (附帶 Agent 1 輸出)
    AI-->>P: 返回進階分析
    P->>UI: 更新 Agent 2 輸出
    
    U->>UI: 查看儀表板
    UI->>DM: 計算 KPI 指標
    DM-->>UI: 返回統計結果
    UI->>U: 顯示視覺化圖表

3. 軟體需求規格 (SRS)
3.1 功能性需求 (Functional Requirements)
FR-001: 供應鏈資料管理
需求描述: 系統應支援匯入、編輯、匯出供應鏈交易資料。
驗收標準:

支援上傳 CSV 格式檔案 (必要欄位: trade_date, src_name, dst_name, device_name, quantity)
提供內建 Mock 資料集供快速測試
資料表支援即時編輯 (新增/刪除/修改列)
支援匯出當前資料為 CSV (含時間戳)
資料驗證: 自動檢測缺失欄位、資料型別錯誤

優先級: P0 (必須)
追溯性: 基於供應鏈管理核心需求

FR-002: 互動式儀表板
需求描述: 提供 KPI 指標展示與視覺化分析。
驗收標準:

顯示總出貨數量、節點數量、醫材種類數
支援依日期篩選資料
即時更新指標 (資料編輯後)
響應式設計,支援不同螢幕尺寸

優先級: P0 (必須)
追溯性: 需求來源 - 管理層決策支援

FR-003: 供應鏈網路圖視覺化
需求描述: 以節點-邊圖形式展示供應鏈網路結構。
驗收標準:

節點代表供應商/經銷商/醫療機構
邊代表交易關係,粗細反映交易量
支援滑鼠懸停顯示詳細資訊
支援節點拖曳調整佈局
可匯出為 PNG/SVG 格式

優先級: P1 (高度期望)
追溯性: 需求來源 - 供應鏈可視化需求

FR-004: 時間序列趨勢分析
需求描述: 以折線圖展示出貨量隨時間變化趨勢。
驗收標準:

X 軸為日期, Y 軸為出貨數量
支援依醫材種類分組顯示
支援縮放與範圍選擇
自動識別異常值 (選用)

優先級: P1 (高度期望)
追溯性: 需求來源 - 趨勢預測與庫存管理

FR-005: 多 AI 代理分析
需求描述: 支援配置與執行多個 AI 代理進行串聯式分析。
驗收標準:

從 agents.yaml 載入代理配置
每個代理可獨立選擇 provider/model/max_tokens
支援「全流程執行」按鈕依序執行所有代理
支援「單步執行」執行指定代理
代理輸入/輸出支援即時編輯
顯示執行狀態 (閒置/執行中/完成/錯誤)
支援將代理輸出傳遞給下一代理或指定代理

優先級: P0 (必須)
追溯性: 需求來源 - AI 輔助決策需求

FR-006: 多模型支援
需求描述: 整合至少 4 家 AI 提供商,支援 8+ 模型。
驗收標準:

Google Gemini: gemini-2.5-flash, gemini-2.5-flash-lite
OpenAI: gpt-4o-mini, gpt-4.1-mini
Anthropic: claude-3-5-sonnet-latest, claude-3-5-haiku-latest
xAI Grok: grok-4-fast-reasoning, grok-3-mini
API 金鑰支援環境變數與 UI 輸入
模型切換即時生效,無需重啟應用

優先級: P0 (必須)
追溯性: 需求來源 - 模型多樣性與成本優化

FR-007: 多語言與主題支援
需求描述: 支援繁體中文/英文切換與 20 種花卉主題。
驗收標準:

語言切換覆蓋所有 UI 文字
主題模式: 亮色/暗色
20 種花卉主題 (Sakura, Rose, Lotus, Tulip, Peony 等)
Jackslot 按鈕隨機抽取主題
主題切換即時套用,無需頁面刷新

優先級: P2 (期望)
追溯性: 需求來源 - 多地區使用者與使用者體驗

3.2 非功能性需求 (Non-Functional Requirements)
NFR-001: 效能需求
指標目標值測量方法單代理執行回應時間<30 秒 (95th percentile)API 呼叫計時器資料載入時間 (1000 筆)<2 秒pandas read_csv 計時儀表板渲染時間<1 秒Streamlit rerun 計時網路圖渲染 (500 節點)<5 秒pyvis 渲染計時並發使用者支援≥10 (單實例)Locust 負載測試

NFR-002: 可用性需求

學習曲線: 新使用者應能在 10 分鐘內完成首次資料上傳與分析
錯誤訊息: 所有錯誤訊息應為雙語,並提供可操作建議
無障礙性: 遵循 WCAG 2.1 AA 級標準 (色彩對比 ≥4.5, 鍵盤導航)
幫助文件: 提供內建使用手冊與範例影片


NFR-003: 可靠性需求

API 失敗容錯: 單一 AI 提供商故障時,使用者可切換至其他提供商
會話持久性: 資料在瀏覽器 refresh 後保持 (Streamlit session_state)
資料完整性: 所有編輯操作可回溯,支援 Undo 功能 (選用)
自動儲存: 每 5 分鐘自動備份當前資料至瀏覽器 LocalStorage (選用)


NFR-004: 安全性需求
詳見 第 8 節: 安全性考量

NFR-005: 可維護性需求

模組化設計: 視覺化、代理執行、資料處理模組應可獨立測試
配置外部化: 代理配置存放於 agents.yaml,無需修改程式碼
日誌記錄: 所有 AI 呼叫記錄於執行日誌,包含時間戳、模型、輸入/輸出摘要
程式碼品質: 遵循 PEP 8 規範,函數平均複雜度 <10


NFR-006: 可擴展性需求

水平擴展: 支援 Kubernetes 部署,可透過增加 Pod 數量處理更高負載
模型擴展: 新增 AI 提供商僅需修改 MODEL_OPTIONS 字典與新增呼叫函數
主題擴展: 新增花卉主題僅需於 FLOWER_THEMES 列表添加
資料來源擴展: 未來可支援 Excel, JSON, SQL 資料庫


3.3 系統介面需求
3.3.1 使用者介面 (UI)

框架: Streamlit Web UI
瀏覽器相容性: Chrome/Edge/Firefox/Safari (最新兩版)
解析度: 最佳化為 1920×1080,最低支援 1366×768
RWD: 支援桌面瀏覽器 (平板與手機不保證完整功能)


3.3.2 外部 API 介面
API 提供商協定認證方式端點範例文件連結Google GeminiRESTAPI Keygenerativelanguage.googleapis.comhttps://ai.google.dev/docsOpenAIRESTAPI Keyapi.openai.com/v1/chat/completionshttps://platform.openai.com/docsAnthropicRESTAPI Keyapi.anthropic.com/v1/messageshttps://docs.anthropic.comxAI GrokRESTAPI Keyapi.x.ai/v1/chat/completionshttps://docs.x.ai

3.3.3 資料檔案格式
CSV 格式 (supply_chain_data.csv):
csvCopyid,trade_date,src_name,dst_name,device_name,quantity
1,2024-01-05,供應商A,醫院X,乳房植入物A,10
2,2024-01-06,供應商A,醫院Y,乳房植入物A,5
必要欄位:

id: 交易唯一識別碼 (整數)
trade_date: 交易日期 (YYYY-MM-DD 格式)
src_name: 來源節點名稱 (字串)
dst_name: 目標節點名稱 (字串)
device_name: 醫療器材名稱 (字串)
quantity: 交易數量 (整數,>0)


3.3.4 配置檔格式
agents.yaml 結構範例:
yamlCopyagents:
  - id: "supply_chain_analyst"
    name: "供應鏈分析師"
    role: "分析交易模式並識別異常"
    enabled: true
    default_model: "gemini-2.5-flash"
    default_max_tokens: 4000
    default_prompt: |
      你是一位專精於醫療器材供應鏈的資料分析師。
      請分析以下供應鏈資料,並輸出:
      1. 交易量前 5 名的供應商
      2. 潛在的供應鏈瓶頸
      3. 異常交易模式 (如突然大量出貨、長期未交易等)
      請以繁體中文 Markdown 格式輸出。

4. 系統需求
4.1 硬體需求
4.1.1 開發環境
元件最低配置建議配置CPU2 核心 (Intel i3 / AMD Ryzen 3)4 核心+ (Intel i5 / AMD Ryzen 5)RAM4 GB8 GB+硬碟10 GB 可用空間20 GB SSD網路穩定寬頻連線≥10 Mbps顯示器1366×7681920×1080

4.1.2 生產環境 (單實例)
元件最低配置建議配置CPU2 vCPU4 vCPURAM4 GB8 GB硬碟20 GB50 GB SSD網路穩定公網連線≥100 Mbps頻寬500 GB/月1 TB/月

4.1.3 生產環境 (Kubernetes 叢集)

節點數量: 3+ (高可用性)
每節點配置: 4 vCPU, 16 GB RAM
持久化儲存: 支援 ReadWriteMany 的 PV (若需共享配置檔)
負載平衡器: L7 Load Balancer (HTTP/HTTPS)


4.2 軟體需求
4.2.1 作業系統
環境支援系統開發Windows 10+, macOS 11+, Ubuntu 20.04+生產Ubuntu 20.04/22.04 LTS, Amazon Linux 2, RHEL 8+, CentOS Stream 8+容器Docker 20.10+, Kubernetes 1.24+

4.2.2 Python 環境

版本: Python 3.9 - 3.11 (建議 3.10)
套件管理: pip 21.0+, 建議使用 virtual environment 或 conda


4.2.3 必要 Python 套件
txtCopystreamlit>=1.30.0
pandas>=2.0.0
pyyaml>=6.0
google-generativeai>=0.3.0
openai>=1.0.0
anthropic>=0.8.0
requests>=2.31.0
altair>=5.0.0
networkx>=3.0
pyvis>=0.3.0

4.2.4 選用套件 (增強功能)
txtCopyplotly>=5.14.0          # 進階互動圖表
streamlit-aggrid>=0.3.0 # 進階表格編輯
python-dotenv>=1.0.0    # .env 檔案載入

4.2.5 容器環境 (選用)

Docker: 20.10+
基礎映像: python:3.10-slim 或 python:3.10-alpine


4.3 網路需求
4.3.1 對外連線 (防火牆白名單)
需允許存取以下網域:

generativelanguage.googleapis.com (Gemini)
api.openai.com (OpenAI)
api.anthropic.com (Anthropic)
api.x.ai (xAI)
pypi.org (Python 套件下載)


4.3.2 對內連線

若多實例部署,需開放容器間通訊 (Kubernetes Service mesh)
預設應用埠: 8501 (Streamlit)


4.3.3 SSL/TLS 需求

生產環境必須啟用 HTTPS (TLS 1.2+, 建議 TLS 1.3)
建議使用 Let's Encrypt 免費憑證或企業 CA 簽發憑證


5. 環境設定
5.1 本地開發環境設定
步驟 1: 安裝 Python
Ubuntu/Debian:
bashCopysudo apt update
sudo apt install python3.10 python3.10-venv python3-pip git
macOS (Homebrew):
bashCopybrew install python@3.10 git
Windows:

從 python.org 下載 Python 3.10 安裝器
安裝時勾選「Add Python to PATH」


步驟 2: 建立專案目錄與虛擬環境
bashCopy# 克隆或建立專案目錄
mkdir biochain-analyst-pro
cd biochain-analyst-pro

# 建立虛擬環境
python3.10 -m venv venv

# 啟動虛擬環境
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

步驟 3: 安裝依賴套件
bashCopy# 升級 pip
pip install --upgrade pip

# 建立 requirements.txt
cat > requirements.txt << EOF
streamlit>=1.30.0
pandas>=2.0.0
pyyaml>=6.0
google-generativeai>=0.3.0
openai>=1.0.0
anthropic>=0.8.0
requests>=2.31.0
altair>=5.0.0
networkx>=3.0
pyvis>=0.3.0
EOF

# 安裝套件
pip install -r requirements.txt

步驟 4: 配置環境變數
建立 .env 檔案 (不應提交至 Git):
bashCopy# .env
GEMINI_API_KEY=AIzaSy...
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-api03-...
GROK_API_KEY=xai-...
載入環境變數:
bashCopy# Linux/macOS
export $(cat .env | xargs)

# Windows (PowerShell)
Get-Content .env | ForEach-Object {
    $key, $value = $_ -split '=', 2
    [Environment]::SetEnvironmentVariable($key, $value, 'Process')
}

步驟 5: 準備配置檔與程式碼

將提供的 app.py 複製到專案目錄
建立 agents.yaml (參考 3.3.4 節)
建立 mock_dataset.csv (或使用程式內建 mock 資料)


步驟 6: 啟動應用
bashCopystreamlit run app.py --server.port 8501
瀏覽器自動開啟 http://localhost:8501

5.2 Docker 環境設定
Dockerfile
dockerfileCopyFROM python:3.10-slim

WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴清單並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式碼
COPY app.py agents.yaml mock_dataset.csv ./

# 建立非 root 使用者
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 暴露 Streamlit 預設埠
EXPOSE 8501

# 健康檢查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 啟動指令
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]

建置與執行
bashCopy# 建置映像
docker build -t biochain-analyst:v2.1 .

# 執行容器
docker run -d \
  --name biochain-app \
  -p 8501:8501 \
  -e GEMINI_API_KEY=$GEMINI_API_KEY \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -e GROK_API_KEY=$GROK_API_KEY \
  biochain-analyst:v2.1

# 檢視日誌
docker logs -f biochain-app

# 停止與刪除容器
docker stop biochain-app
docker rm biochain-app

docker-compose.yml (選用)
yamlCopyversion: '3.8'

services:
  biochain-app:
    build: .
    image: biochain-analyst:v2.1
    container_name: biochain-app
    ports:
      - "8501:8501"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - GROK_API_KEY=${GROK_API_KEY}
    volumes:
      - ./agents.yaml:/app/agents.yaml:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
執行:
bashCopydocker-compose up -d

6. 部署選項
6.1 本地部署 (Local Deployment)
適用場景

個人開發測試
隔離環境審查 (離線或內部網路)
POC 展示

部署步驟
依照 5.1 節 完成環境設定並執行 streamlit run app.py
優點

完全離線 (若 API 金鑰預先設定)
最快速部署 (<5 分鐘)
無雲端成本
完整資料控制權

缺點

無法多人協作
單點故障
無自動擴展
依賴本機效能


6.2 AWS 部署選項
6.2.1 AWS EC2 部署
架構圖:
CopyInternet → Route 53 → ALB (HTTPS) → EC2 Instance → AI APIs
                                         ↓
                                    EBS Volume
                                         ↓
                                  CloudWatch Logs
部署步驟:

啟動 EC2 執行個體:

AMI: Ubuntu 22.04 LTS
執行個體類型: t3.medium (2 vCPU, 4 GB RAM)
安全群組:

Inbound: 443 (HTTPS), 22 (SSH from your IP)
Outbound: All


IAM 角色: 附加 SecretsManagerReadWrite 政策


SSH 連線並安裝依賴:

bashCopyssh -i keypair.pem ubuntu@<EC2_PUBLIC_IP>
sudo apt update && sudo apt upgrade -y
sudo apt install python3.10-venv nginx certbot python3-certbot-nginx -y

部署應用:

bashCopygit clone https://github.com/yourorg/biochain-analyst-pro.git
cd biochain-analyst-pro
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

配置 systemd 服務:

bashCopysudo tee /etc/systemd/system/biochain.service > /dev/null <<EOF
[Unit]
Description=BioChain Analyst Pro
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/biochain-analyst-pro
Environment="PATH=/home/ubuntu/biochain-analyst-pro/venv/bin"
EnvironmentFile=/home/ubuntu/biochain-analyst-pro/.env
ExecStart=/home/ubuntu/biochain-analyst-pro/venv/bin/streamlit run app.py --server.port 8501 --server.address 127.0.0.1
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable biochain
sudo systemctl start biochain

配置 Nginx 反向代理:

bashCopysudo tee /etc/nginx/sites-available/biochain > /dev/null <<'EOF'
server {
    listen 80;
    server_name biochain.yourdomain.com;
    
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name biochain.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/biochain.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/biochain.yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
    
    location /_stcore/stream {
        proxy_pass http://127.0.0.1:8501/_stcore/stream;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/biochain /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

取得 SSL 憑證:

bashCopysudo certbot --nginx -d biochain.yourdomain.com
成本估算 (us-east-1, 按需執行 730 小時/月):

t3.medium: $0.0416/hr × 730 = $30.37/月
EBS gp3 (30 GB): $2.40/月
Application Load Balancer (選用): $16.20/月
資料傳輸 (10 GB): $0.90/月
總計: ~$50/月 (不含 ALB) 或 ~$66/月 (含 ALB)


6.2.2 AWS ECS Fargate 部署
架構圖:
CopyInternet → Route 53 → ALB → ECS Service (Fargate) → AI APIs
                                    ↓
                           Secrets Manager (API Keys)
                                    ↓
                           CloudWatch Logs
部署步驟:

建立 ECR 儲存庫並推送映像:

bashCopyaws ecr create-repository --repository-name biochain-analyst
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT>.dkr.ecr.us-east-1.amazonaws.com
docker tag biochain-analyst:v2.1 <AWS_ACCOUNT>.dkr.ecr.us-east-1.amazonaws.com/biochain-analyst:v2.1
docker push <AWS_ACCOUNT>.dkr.ecr.us-east-1.amazonaws.com/biochain-analyst:v2.1

建立 Secrets Manager 密鑰:

bashCopyaws secretsmanager create-secret \
  --name biochain/gemini-key \
  --secret-string "AIzaSy..."

aws secretsmanager create-secret \
  --name biochain/openai-key \
  --secret-string "sk-proj-..."

建立 ECS Task Definition (task-definition.json):

jsonCopy{
  "family": "biochain-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::<ACCOUNT>:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "biochain-app",
      "image": "<AWS_ACCOUNT>.dkr.ecr.us-east-1.amazonaws.com/biochain-analyst:v2.1",
      "portMappings": [{"containerPort": 8501, "protocol": "tcp"}],
      "secrets": [
        {"name": "GEMINI_API_KEY", "valueFrom": "arn:aws:secretsmanager:us-east-1:<ACCOUNT>:secret:biochain/gemini-key"},
        {"name": "OPENAI_API_KEY", "valueFrom": "arn:aws:secretsmanager:us-east-1:<ACCOUNT>:secret:biochain/openai-key"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/biochain",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8501/_stcore/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}

註冊 Task Definition:

bashCopyaws ecs register-task-definition --cli-input-json file://task-definition.json

建立 ECS 叢集:

bashCopyaws ecs create-cluster --cluster-name biochain-cluster

建立 ALB 與 Target Group (透過 AWS Console 或 CLI)
建立 ECS Service:

bashCopyaws ecs create-service \
  --cluster biochain-cluster \
  --service-name biochain-service \
  --task-definition biochain-task \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx,subnet-yyy],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:us-east-1:xxx:targetgroup/biochain-tg,containerName=biochain-app,containerPort=8501"

配置 Auto Scaling:

bashCopyaws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --scalable-dimension ecs:service:DesiredCount \
  --resource-id service/biochain-cluster/biochain-service \
  --min-capacity 2 \
  --max-capacity 10

aws application-autoscaling put-scaling-policy \
  --policy-name biochain-cpu-scaling \
  --service-namespace ecs \
  --scalable-dimension ecs:service:DesiredCount \
  --resource-id service/biochain-cluster/biochain-service \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration file://scaling-policy.json
成本估算 (us-east-1, 2 tasks 持續執行):

Fargate (1 vCPU, 2GB) × 2: $0.04048/hr × 2 × 730 = $59.10/月
ALB: $16.20/月
NAT Gateway (若私有子網): $32.40/月
CloudWatch Logs (5 GB): $2.50/月
總計: ~$110/月 (含 NAT Gateway)


6.2.3 AWS Lambda + API Gateway (不建議)
限制:

Streamlit 依賴長連線 WebSocket,不適合 Lambda
Lambda 15 分鐘執行時限可能不足
冷啟動延遲影響使用者體驗

替代方案: 將核心分析邏輯包裝成 Lambda 函數,前端改用靜態 S3 + React/Vue.js

6.3 GCP 部署選項
6.3.1 GCP Compute Engine 部署
類似 AWS EC2,使用 e2-medium 執行個體,步驟略。
成本估算 (us-central1):

e2-medium: $24.27/月
Persistent Disk (30 GB): $2.04/月
Load Balancer: $18/月
總計: ~$45/月


6.3.2 GCP Cloud Run 部署 (推薦)
優勢:

完全託管,自動擴展
按請求計費 (無流量時成本接近 $0)
內建 HTTPS 與自訂網域

部署步驟:

建置並推送映像至 GCR:

bashCopygcloud builds submit --tag gcr.io/PROJECT_ID/biochain-analyst

部署至 Cloud Run:

bashCopygcloud run deploy biochain-service \
  --image gcr.io/PROJECT_ID/biochain-analyst \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 3600 \
  --concurrency 10 \
  --max-instances 10 \
  --set-env-vars GEMINI_API_KEY=xxx,OPENAI_API_KEY=xxx \
  --port 8501

配置自訂網域:

bashCopygcloud run domain-mappings create \
  --service biochain-service \
  --domain biochain.yourdomain.com \
  --region us-central1
成本估算 (假設每月 10,000 請求,平均 30 秒執行):

請求費用: $0.40 / 1M requests × 0.01M = $0.004/月
CPU: $0.00002400 / vCPU-sec × 2 vCPU × 30 sec × 10,000 = $14.40/月
Memory: $0.00000250 / GiB-sec × 2 GiB × 30 sec × 10,000 = $1.50/月
總計: ~$16/月 (低流量場景)


6.3.3 GCP GKE 部署
類似 AWS EKS,使用 Kubernetes Deployment,步驟略。
成本估算:

GKE 叢集管理費: $0.10/hr × 730 = $73/月
3 × e2-standard-4 節點: $122.18/月 × 3 = $366.54/月
總計: ~$440/月 (適合企業級高流量)


6.4 Azure 部署選項
6.4.1 Azure App Service 部署
部署步驟:

建立 App Service Plan:

bashCopyaz appservice plan create \
  --name biochain-plan \
  --resource-group biochain-rg \
  --sku B2 \
  --is-linux

建立 Web App:

bashCopyaz webapp create \
  --name biochain-app \
  --resource-group biochain-rg \
  --plan biochain-plan \
  --runtime "PYTHON:3.10"

配置環境變數:

bashCopyaz webapp config appsettings set \
  --name biochain-app \
  --resource-group biochain-rg \
  --settings GEMINI_API_KEY=xxx OPENAI_API_KEY=xxx

部署程式碼 (透過 ZIP):

bashCopyzip -r app.zip app.py agents.yaml requirements.txt
az webapp deployment source config-zip \
  --name biochain-app \
  --resource-group biochain-rg \
  --src app.zip
成本估算:

B2 (2 核心, 3.5 GB RAM): $73/月
流量傳輸 (10 GB): $0.87/月
總計: ~$74/月


6.4.2 Azure Container Instances (ACI)
快速部署 (適合測試):
bashCopyaz container create \
  --name biochain-container \
  --resource-group biochain-rg \
  --image <ACR_IMAGE_URI> \
  --cpu 2 \
  --memory 4 \
  --ports 8501 \
  --environment-variables GEMINI_API_KEY=xxx OPENAI_API_KEY=xxx \
  --dns-name-label biochain
成本: ~$45/月 (2 vCPU, 4 GB RAM, 持續執行)

6.4.3 Azure Kubernetes Service (AKS)
類似 AWS EKS / GCP GKE,步驟略。
成本估算:

3 × Standard_D2s_v3 節點: $96.36/月 × 3 = $289.08/月
Load Balancer: $18.25/月
總計: ~$307/月


6.5 混合部署 (Hybrid Deployment)
場景

敏感資料需留在內部機房
企業安全政策禁止資料外傳
需符合 HIPAA/GDPR 等嚴格合規要求

架構
Copy[內部機房]
   ↓ (VM/Docker)
企業防火牆 (Outbound HTTPS 允許 AI API 網域)
   ↓
[雲端 AI 提供商]
實施步驟

內部 VM/容器部署: 依照 6.1 節 於企業資料中心部署
網路設定: 配置防火牆允許存取:

api.openai.com
generativelanguage.googleapis.com
api.anthropic.com
api.x.ai


VPN/Direct Connect (選用): 若需存取雲端託管的配置檔或日誌儲存
Identity Federation: 使用企業 SSO (SAML/OAuth) 整合使用者驗證

優點

資料不出內部網路
符合嚴格合規要求
完整控制權

缺點

需自行維護基礎設施
網路延遲可能較高
高可用性需額外配置


6.6 部署建議矩陣
場景建議方案原因預估成本個人/小團隊測試本地 or GCP Cloud Run成本低、部署快$0-20/月企業 POC (10-50 人)AWS ECS Fargate易管理、自動擴展$110/月生產環境 (100+ 人)AWS/GCP/Azure Kubernetes高可用性、可觀測性$300-500/月高度監管環境混合部署 (內部 VM)資料主權、合規性依內部成本無固定流量GCP Cloud Run按需計費、零閒置成本$15-30/月

7. 基礎設施即程式碼 (IaC)
7.1 Terraform 範例 (AWS ECS Fargate)
完整 Terraform 配置檔案範例 (省略部分重複內容,詳見前述範本):
目錄結構:
Copyterraform/aws/
├── main.tf
├── variables.tf
├── outputs.tf
├── vpc.tf
├── ecs.tf
├── alb.tf
├── secrets.tf
└── iam.tf
variables.tf:
hclCopyvariable "aws_region" {
  description = "AWS 區域"
  default     = "us-east-1"
}

variable "project_name" {
  description = "專案名稱"
  default     = "biochain"
}

variable "ecr_image_uri" {
  description = "ECR 映像 URI"
  type        = string
}

variable "gemini_api_key" {
  description = "Gemini API Key"
  type        = string
  sensitive   = true
}

variable "openai_api_key" {
  description = "OpenAI API Key"
  type        = string
  sensitive   = true
}
部署指令:
bashCopycd terraform/aws
terraform init
terraform plan -var="ecr_image_uri=xxx" -var="gemini_api_key=xxx" -var="openai_api_key=xxx"
terraform apply -auto-approve

7.2 Kubernetes Deployment YAML
完整 Kubernetes 配置範例 (詳見前述範本),關鍵要點:

Namespace 隔離: 建立獨立 biochain namespace
Secrets 管理: 使用 Kubernetes Secret 儲存 API 金鑰
ConfigMap: 將 agents.yaml 掛載為 ConfigMap
HPA: 配置 Horizontal Pod Autoscaler (CPU 70%)
Service: LoadBalancer 類型,自動配置外部 IP

部署指令:
bashCopykubectl apply -f k8s/namespace.yaml
kubectl create secret generic ai-api-keys \
  --from-literal=gemini-key=$GEMINI_API_KEY \
  --from-literal=openai-key=$OPENAI_API_KEY \
  -n biochain
kubectl apply -f k8s/deployment.yaml
kubectl get svc -n biochain  # 取得 Load Balancer IP

7.3 CI/CD 整合 (GitHub Actions)
.github/workflows/deploy.yml:
yamlCopyname: Build and Deploy to GCP Cloud Run

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  GCP_PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
  GCP_REGION: us-central1
  SERVICE_NAME: biochain-service

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ --cov=app --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Authenticate to Google Cloud
      uses: google-github-actions/auth@v1
      with:
        credentials_json: ${{ secrets.GCP_SA_KEY }}
    
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
          --max-instances 10 \
          --set-secrets GEMINI_API_KEY=gemini-key:latest,OPENAI_API_KEY=openai-key:latest
    
    - name: Run smoke tests
      run: |
        SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $GCP_REGION --format 'value(status.url)')
        curl -f $SERVICE_URL/_stcore/health || exit 1
        
    - name: Notify Slack
      if: always()
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        text: 'Deployment to Cloud Run: ${{ job.status }}'
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}

8. 安全性考量
8.1 威脅模型 (STRIDE)
威脅類型潛在攻擊緩解措施Spoofing (身份偽裝)未授權使用者冒充合法管理員OAuth 2.0 / SAML SSO,整合企業 ADTampering (資料竄改)惡意修改上傳資料或代理輸出檔案完整性檢查 (SHA-256),唯讀配置檔Repudiation (否認性)使用者否認執行過某操作完整審計日誌 (使用者 ID、時間戳、操作)Information Disclosure (資訊洩漏)API 金鑰外洩、敏感資料洩漏Secrets Manager,TLS 1.3,資料遮罩Denial of Service (阻斷服務)惡意大量請求耗盡資源Rate limiting (每使用者 10 req/min),Auto-scalingElevation of Privilege (權限提升)一般使用者取得管理員權限RBAC,最小權限原則,定期權限審查

8.2 API 金鑰管理最佳實踐
8.2.1 環境變數 (開發/測試)
bashCopy# .env (絕不提交至 Git)
GEMINI_API_KEY=AIzaSy...
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-api03-...
GROK_API_KEY=xai-...
.gitignore:
Copy.env
*.env
secrets/
__pycache__/
*.pyc

8.2.2 雲端 Secrets Manager (生產環境)
AWS Secrets Manager:
bashCopy# 建立密鑰
aws secretsmanager create-secret \
  --name biochain/gemini-key \
  --secret-string "AIzaSy..."

# ECS Task Definition 引用
"secrets": [
  {
    "name": "GEMINI_API_KEY",
    "valueFrom": "arn:aws:secretsmanager:us-east-1:xxx:secret:biochain/gemini-key"
  }
]
GCP Secret Manager:
bashCopyecho -n "AIzaSy..." | gcloud secrets create gemini-key --data-file=-

# Cloud Run 引用
gcloud run deploy biochain-service \
  --set-secrets GEMINI_API_KEY=gemini-key:latest
Azure Key Vault:
bashCopyaz keyvault secret set \
  --vault-name biochain-vault \
  --name gemini-key \
  --value "AIzaSy..."

# App Service 引用
@Microsoft.KeyVault(SecretUri=https://biochain-vault.vault.azure.net/secrets/gemini-key/)

8.2.3 金鑰輪替策略

輪替週期: 每 90 天
自動化: 使用 AWS Secrets Manager Rotation Lambda
多版本: 保留前一版本金鑰 24 小時,確保無服務中斷
監控: CloudWatch Alarms 監控金鑰存取失敗


8.3 資料隱私保護
8.3.1 PII (個人身份資訊) 處理
匿名化函數:
pythonCopyimport re

def anonymize_text(text: str) -> str:
    """移除或遮罩個人身份資訊"""
    # 人名 (中文/英文)
    text = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[PATIENT_NAME]', text)
    text = re.sub(r'[\u4e00-\u9fff]{2,4}', '[姓名]', text)
    
    # 醫療記錄號碼
    text = re.sub(r'\b\d{6,10}\b', '[MRN]', text)
    
    # 電話號碼
    text = re.sub(r'\b\d{2,4}-\d{3,4}-\d{4}\b', '[PHONE]', text)
    
    # Email
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
    
    return text
資料留存政策:

不儲存任何案例資料於後端伺服器
僅保存於使用者瀏覽器 Session (Streamlit session_state)
Session 過期時間: 24 小時

合規性:

符合 HIPAA Privacy Rule (若處理美國健康資料)
符合 GDPR Article 32 (若處理歐盟居民資料)


8.3.2 傳輸層安全

TLS 版本: 強制 TLS 1.2+,建議 TLS 1.3
憑證管理: Let's Encrypt 自動更新 (Certbot) 或企業 CA
HSTS: 啟用 HTTP Strict Transport Security

Nginx 配置:
nginxCopyadd_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;

8.4 應用程式安全
8.4.1 輸入驗證
pythonCopydef validate_csv_upload(df: pd.DataFrame) -> bool:
    """驗證上傳的 CSV 資料"""
    required_columns = ['trade_date', 'src_name', 'dst_name', 'device_name', 'quantity']
    
    # 檢查必要欄位
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"缺少必要欄位: {required_columns}")
    
    # 檢查資料型別
    if not pd.api.types.is_numeric_dtype(df['quantity']):
        raise ValueError("quantity 欄位必須為數值")
    
    # 檢查數量範圍
    if (df['quantity'] <= 0).any():
        raise ValueError("quantity 必須 > 0")
    
    # 檢查日期格式
    try:
        pd.to_datetime(df['trade_date'])
    except:
        raise ValueError("trade_date 格式錯誤,應為 YYYY-MM-DD")
    
    # 檢查檔案大小 (防止 DoS)
    if len(df) > 100000:
        raise ValueError("資料筆數超過 100,000 筆上限")
    
    return True

8.4.2 輸出編碼

Markdown 渲染: Streamlit 預設會 sanitize HTML,但需防範 Markdown injection
日誌輸出: 避免記錄未編碼的使用者輸入


8.4.3 依賴套件掃描
bashCopy# 安裝掃描工具
pip install pip-audit safety

# 掃描已知漏洞
pip-audit
safety check --file requirements.txt

# 自動化 (GitHub Actions)
- name: Security scan
  run: |
    pip install pip-audit
    pip-audit --require-hashes --disable-pip

8.5 存取控制
8.5.1 驗證機制 (Authentication)
選項 1: Streamlit Authenticator (簡易)
pythonCopyimport streamlit_authenticator as stauth
import yaml

# 載入使用者配置
with open('users.yaml') as file:
    config = yaml.safe_load(file)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    st.write(f'歡迎 *{name}*')
    # 主應用程式
elif authentication_status == False:
    st.error('使用者名稱或密碼錯誤')
elif authentication_status == None:
    st.warning('請輸入使用者名稱與密碼')
選項 2: OAuth 2.0 (Google Workspace)
使用 streamlit-oauth 或自訂 OAuth 流程整合 Google/Azure AD

8.5.2 授權機制 (Authorization) - RBAC
角色定義:
角色權限Viewer (檢視者)查看儀表板、網路圖、趨勢分析 (唯讀)Analyst (分析師)Viewer 權限 + 上傳資料、執行 AI 代理Admin (管理員)Analyst 權限 + 編輯 agents.yaml、查看所有使用者日誌
實作範例:
pythonCopy# 於 session_state 儲存角色
if 'user_role' not in st.session_state:
    st.session_state.user_role = 'viewer'

# 權限檢查裝飾器
def require_role(allowed_roles):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if st.session_state.user_role not in allowed_roles:
                st.error(f"此功能需要 {allowed_roles} 權限")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 使用範例
@require_role(['analyst', 'admin'])
def upload_data_section():
    uploaded_file = st.file_uploader("上傳 CSV")
    # ...

8.6 審計日誌
8.6.1 日誌欄位
欄位說明範例timestampISO 8601 時間戳2024-01-15T14:23.123Zuser_id使用者唯一識別碼analyst@company.comaction操作類型data_upload / agent_run / config_editagent_id涉及代理 ID (若適用)supply_chain_analystproviderAI 提供商geminimodel模型名稱gemini-2.5-flashinput_hash輸入資料 SHA-256a3b2c1d4e5f6...output_hash輸出資料 SHA-256d4e5f6a3b2c1...status執行狀態success / errorerror_msg錯誤訊息 (若失敗)API rate limit exceededduration_ms執行時長 (毫秒)12345ip_address使用者 IP203.0.113.42

8.6.2 日誌實作
pythonCopyimport logging
import hashlib
from datetime import datetime

# 配置日誌
logging.basicConfig(
    filename='audit.log',
    level=logging.INFO,
    format='%(message)s'
)

def log_audit_event(
    user_id: str,
    action: str,
    status: str,
    details: dict = None
):
    """記錄審計事件"""
    event = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'user_id': user_id,
        'action': action,
        'status': status,
        'ip_address': st.session_state.get('user_ip', 'unknown'),
    }
    if details:
        event.update(details)
    
    logging.info(json.dumps(event, ensure_ascii=False))

# 使用範例
log_audit_event(
    user_id=st.session_state.username,
    action='agent_run',
    status='success',
    details={
        'agent_id': 'supply_chain_analyst',
        'provider': 'gemini',
        'model': 'gemini-2.5-flash',
        'duration_ms': 15420
    }
)

8.6.3 日誌儲存與保留
本地檔案 (開發):

路徑: ./logs/audit.log
輪替: 每 10 MB 或每月輪替
保留: 最近 12 個月

雲端日誌服務 (生產):

AWS: CloudWatch Logs (保留 90 天,之後歸檔至 S3 Glacier)
GCP: Cloud Logging (保留 30 天,長期儲存至 BigQuery)
Azure: Monitor Logs (保留 90 天,匯出至 Storage Account)

SIEM 整合 (企業):

透過 Fluentd/Logstash 轉發至 Splunk/ELK/Azure Sentinel


8.7 安全開發生命週期 (SDL)
mermaidCopygraph LR
    A[需求階段] --> B[設計階段]
    B --> C[開發階段]
    C --> D[測試階段]
    D --> E[部署階段]
    E --> F[維運階段]
    
    A -->|威脅模型| TM[STRIDE 分析]
    B -->|安全架構審查| SAR[Security Review]
    C -->|靜態程式碼掃描| SAST[Bandit / Semgrep]
    D -->|滲透測試| PT[OWASP ZAP / Burp Suite]
    E -->|配置掃描| CS[Trivy / Checkov]
    F -->|漏洞監控| VM[Snyk / Dependabot]

9. 驗證計畫
9.1 驗證目標
依據 ISO 13485 (醫療器材品質管理系統) 與 IEC 62304 (醫療器材軟體生命週期) 精神,本驗證計畫確保:

功能性: 系統符合 SRS 所有功能需求
可重現性: 相同輸入產生相同輸出 (AI 溫度=0 時)
資料完整性: 資料不丟失、不損壞
安全性: 安全控制有效運作
可追溯性: 所有需求可追溯至測試案例


9.2 驗證層級 (V 模型)
Copy需求 (SRS) ←─────────→ 驗收測試 (UAT)
    ↓                        ↑
  設計 ←─────────→ 系統整合測試 (SIT)
    ↓                        ↑
  編碼 ←─────────→ 單元測試 (UT)

9.3 單元測試 (Unit Testing)
9.3.1 測試框架
bashCopypip install pytest pytest-cov pytest-mock

9.3.2 測試案例範例
tests/test_data_processing.py:
醫療器材供應鏈追蹤系統 v2.1 - BioChain Analyst Pro
綜合技術規格文件 (續)
9.3.2 測試案例範例 (續)
tests/test_data_processing.py:
pythonCopyimport pytest
import pandas as pd
from app import validate_csv_upload, anonymize_text, generate_mock_data

class TestDataProcessing:
    """資料處理模組測試"""
    
    def test_validate_csv_upload_success(self):
        """測試有效 CSV 資料驗證通過"""
        df = pd.DataFrame({
            'trade_date': ['2024-01-01', '2024-01-02'],
            'src_name': ['供應商A', '供應商B'],
            'dst_name': ['醫院X', '醫院Y'],
            'device_name': ['植入物A', '植入物B'],
            'quantity': [10, 20]
        })
        assert validate_csv_upload(df) == True
    
    def test_validate_csv_upload_missing_columns(self):
        """測試缺少必要欄位時拋出異常"""
        df = pd.DataFrame({
            'trade_date': ['2024-01-01'],
            'src_name': ['供應商A']
        })
        with pytest.raises(ValueError, match="缺少必要欄位"):
            validate_csv_upload(df)
    
    def test_validate_csv_upload_invalid_quantity(self):
        """測試負數或零數量時拋出異常"""
        df = pd.DataFrame({
            'trade_date': ['2024-01-01'],
            'src_name': ['供應商A'],
            'dst_name': ['醫院X'],
            'device_name': ['植入物A'],
            'quantity': [0]
        })
        with pytest.raises(ValueError, match="quantity 必須 > 0"):
            validate_csv_upload(df)
    
    def test_validate_csv_upload_invalid_date(self):
        """測試無效日期格式時拋出異常"""
        df = pd.DataFrame({
            'trade_date': ['2024-13-45'],
            'src_name': ['供應商A'],
            'dst_name': ['醫院X'],
            'device_name': ['植入物A'],
            'quantity': [10]
        })
        with pytest.raises(ValueError, match="trade_date 格式錯誤"):
            validate_csv_upload(df)
    
    def test_validate_csv_upload_oversized(self):
        """測試超過大小限制時拋出異常"""
        df = pd.DataFrame({
            'trade_date': ['2024-01-01'] * 100001,
            'src_name': ['供應商A'] * 100001,
            'dst_name': ['醫院X'] * 100001,
            'device_name': ['植入物A'] * 100001,
            'quantity': [10] * 100001
        })
        with pytest.raises(ValueError, match="資料筆數超過 100,000 筆上限"):
            validate_csv_upload(df)
    
    def test_anonymize_text(self):
        """測試 PII 匿名化功能"""
        input_text = "患者張三 (MRN: 1234567) 電話 02-2345-6789"
        expected = "患者[姓名] (MRN: [MRN]) 電話 [PHONE]"
        assert anonymize_text(input_text) == expected
    
    def test_generate_mock_data(self):
        """測試 Mock 資料生成"""
        df = generate_mock_data(num_records=100)
        assert len(df) == 100
        assert all(col in df.columns for col in ['trade_date', 'src_name', 'dst_name', 'device_name', 'quantity'])
        assert df['quantity'].min() >= 1
        assert df['quantity'].max() <= 50
tests/test_agent_execution.py:
pythonCopyimport pytest
from unittest.mock import Mock, patch
from app import call_gemini_api, call_openai_api, execute_agent_pipeline

class TestAgentExecution:
    """AI 代理執行模組測試"""
    
    @patch('app.genai.GenerativeModel')
    def test_call_gemini_api_success(self, mock_model):
        """測試 Gemini API 呼叫成功"""
        mock_response = Mock()
        mock_response.text = "分析結果: 供應鏈正常"
        mock_model.return_value.generate_content.return_value = mock_response
        
        result = call_gemini_api(
            api_key="test_key",
            model="gemini-2.5-flash",
            prompt="分析供應鏈",
            max_tokens=1000
        )
        assert "供應鏈正常" in result
    
    @patch('app.genai.GenerativeModel')
    def test_call_gemini_api_error(self, mock_model):
        """測試 Gemini API 呼叫失敗時的錯誤處理"""
        mock_model.return_value.generate_content.side_effect = Exception("API Error")
        
        result = call_gemini_api(
            api_key="test_key",
            model="gemini-2.5-flash",
            prompt="分析供應鏈",
            max_tokens=1000
        )
        assert "錯誤" in result or "Error" in result
    
    @patch('app.openai.ChatCompletion.create')
    def test_call_openai_api_success(self, mock_create):
        """測試 OpenAI API 呼叫成功"""
        mock_create.return_value = {
            'choices': [{
                'message': {'content': '風險評估: 低風險'}
            }]
        }
        
        result = call_openai_api(
            api_key="test_key",
            model="gpt-4o-mini",
            prompt="評估風險",
            max_tokens=1000
        )
        assert "低風險" in result
    
    def test_execute_agent_pipeline(self):
        """測試多代理串聯執行"""
        agents_config = [
            {
                'id': 'agent1',
                'name': '分析師',
                'prompt': '分析資料',
                'default_model': 'gemini-2.5-flash'
            },
            {
                'id': 'agent2',
                'name': '審查員',
                'prompt': '審查分析結果',
                'default_model': 'gpt-4o-mini'
            }
        ]
        
        with patch('app.call_gemini_api') as mock_gemini, \
             patch('app.call_openai_api') as mock_openai:
            mock_gemini.return_value = "分析完成"
            mock_openai.return_value = "審查通過"
            
            results = execute_agent_pipeline(agents_config, "測試資料")
            assert len(results) == 2
            assert results['agent1'] == "分析完成"
            assert results['agent2'] == "審查通過"
tests/test_visualization.py:
pythonCopyimport pytest
import pandas as pd
import networkx as nx
from app import create_supply_chain_network, calculate_kpis, generate_time_series_chart

class TestVisualization:
    """視覺化模組測試"""
    
    def test_create_supply_chain_network(self):
        """測試供應鏈網路圖生成"""
        df = pd.DataFrame({
            'src_name': ['供應商A', '供應商A', '供應商B'],
            'dst_name': ['醫院X', '醫院Y', '醫院X'],
            'quantity': [10, 20, 15]
        })
        
        G = create_supply_chain_network(df)
        assert isinstance(G, nx.Graph)
        assert G.number_of_nodes() == 4  # 2 供應商 + 2 醫院
        assert G.number_of_edges() == 3
        assert G['供應商A']['醫院X']['weight'] == 10
    
    def test_calculate_kpis(self):
        """測試 KPI 計算"""
        df = pd.DataFrame({
            'src_name': ['供應商A', '供應商B'],
            'dst_name': ['醫院X', '醫院Y'],
            'device_name': ['植入物A', '植入物B'],
            'quantity': [100, 200]
        })
        
        kpis = calculate_kpis(df)
        assert kpis['total_quantity'] == 300
        assert kpis['num_nodes'] == 4
        assert kpis['num_device_types'] == 2
    
    def test_generate_time_series_chart(self):
        """測試時間序列圖表生成"""
        df = pd.DataFrame({
            'trade_date': pd.date_range('2024-01-01', periods=5),
            'quantity': [10, 15, 12, 18, 20]
        })
        
        chart = generate_time_series_chart(df)
        assert chart is not None
        assert hasattr(chart, 'to_json')  # Altair Chart 物件
9.3.3 測試執行與覆蓋率
bashCopy# 執行所有測試
pytest tests/ -v

# 執行特定測試檔案
pytest tests/test_data_processing.py -v

# 生成覆蓋率報告
pytest tests/ --cov=app --cov-report=html --cov-report=term

# 覆蓋率目標
# - 語句覆蓋率 (Statement Coverage): ≥ 85%
# - 分支覆蓋率 (Branch Coverage): ≥ 75%
# - 函數覆蓋率 (Function Coverage): ≥ 90%
9.4 整合測試 (Integration Testing)
9.4.1 測試場景
測試案例 ID測試描述前置條件測試步驟預期結果IT-001完整資料分析流程已上傳有效 CSV1. 上傳資料<br>2. 執行 Agent 1<br>3. 執行 Agent 2<br>4. 檢視儀表板所有代理成功執行,儀表板正確顯示IT-002API 金鑰錯誤處理設定無效 API 金鑰1. 執行任一代理顯示明確錯誤訊息,不中斷系統IT-003大型資料集處理準備 10,000 筆資料1. 上傳大型 CSV<br>2. 生成網路圖<br>3. 計算 KPI30 秒內完成,無錯誤IT-004並發使用者測試啟動 10 個並發 Session同時執行資料上傳與分析所有 Session 獨立運作,無資料混淆IT-005主題與語言切換系統正常運行1. 切換主題<br>2. 切換語言即時生效,無頁面錯誤
9.4.2 整合測試自動化 (Selenium)
pythonCopy# tests/integration/test_ui_flow.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.get("http://localhost:8501")
    yield driver
    driver.quit()

def test_data_upload_and_analysis(browser):
    """測試完整資料上傳與分析流程"""
    # 等待頁面載入
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    
    # 上傳 CSV
    upload_input = browser.find_element(By.CSS_SELECTOR, "input[type='file']")
    upload_input.send_keys("/path/to/test_data.csv")
    
    # 等待資料載入完成
    WebDriverWait(browser, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "資料預覽")
    )
    
    # 執行 Agent
    run_button = browser.find_element(By.XPATH, "//button[contains(text(), '執行')]")
    run_button.click()
    
    # 等待執行完成
    WebDriverWait(browser, 60).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "完成")
    )
    
    # 驗證結果
    assert "分析結果" in browser.page_source
9.5 系統測試 (System Testing)
9.5.1 功能測試矩陣
需求 ID測試案例 ID測試方法狀態FR-001ST-001 ~ ST-005手動測試✅ 通過FR-002ST-006 ~ ST-010自動化測試✅ 通過FR-003ST-011 ~ ST-015手動測試✅ 通過FR-004ST-016 ~ ST-020自動化測試✅ 通過FR-005ST-021 ~ ST-030手動 + 自動⚠️ 部分通過FR-006ST-031 ~ ST-040自動化測試✅ 通過FR-007ST-041 ~ ST-050手動測試✅ 通過
9.5.2 非功能性測試
效能測試 (Performance Testing)
pythonCopy# tests/performance/locust_load_test.py
from locust import HttpUser, task, between
import random

class BiochainUser(HttpUser):
    wait_time = between(1, 5)
    
    @task(3)
    def view_dashboard(self):
        """模擬查看儀表板"""
        self.client.get("/?page=dashboard")
    
    @task(2)
    def run_agent(self):
        """模擬執行代理"""
        self.client.post("/api/agents/run", json={
            "agent_id": "supply_chain_analyst",
            "provider": "gemini",
            "model": "gemini-2.5-flash"
        })
    
    @task(1)
    def upload_data(self):
        """模擬上傳資料"""
        files = {'file': ('test.csv', open('test_data.csv', 'rb'), 'text/csv')}
        self.client.post("/api/data/upload", files=files)

# 執行負載測試
# locust -f locust_load_test.py --host=http://localhost:8501 --users 50 --spawn-rate 5
效能測試結果範例:
指標目標實測結果狀態50 並發用戶下平均回應時間< 2 秒1.8 秒✅95th 百分位回應時間< 5 秒4.2 秒✅系統吞吐量> 100 req/sec125 req/sec✅CPU 使用率 (峰值)< 80%72%✅記憶體使用率 (峰值)< 85%78%✅錯誤率< 1%0.3%✅
壓力測試 (Stress Testing)
bashCopy# 使用 Apache Bench 進行壓力測試
ab -n 10000 -c 100 -t 60 http://localhost:8501/

# 結果分析:
# - Requests per second: 150 [#/sec]
# - Time per request (mean): 666 [ms]
# - Failed requests: 0
# 結論: 系統在 100 並發下可穩定運行
安全性測試 (Security Testing)
bashCopy# 使用 OWASP ZAP 進行漏洞掃描
docker run -v $(pwd):/zap/wrk/:rw -t owasp/zap2docker-stable zap-baseline.py \
  -t http://localhost:8501 -r zap_report.html

# 主要檢查項目:
# - SQL Injection
# - XSS (Cross-Site Scripting)
# - CSRF (Cross-Site Request Forgery)
# - 敏感資訊洩漏
# - 不安全的 HTTP Headers
安全測試結果:
漏洞類型風險等級發現數量狀態SQL Injection高0✅XSS高0✅CSRF中0✅敏感資訊洩漏中1⚠️ 修復中不安全的 HTTP Headers低2✅ 已修復
9.6 使用者驗收測試 (UAT)
9.6.1 UAT 測試場景
UAT ID測試場景測試人員角色驗收標準UAT-001新使用者首次使用供應鏈管理員10 分鐘內完成資料上傳與首次分析UAT-002異常交易識別品質保證專員AI 正確識別預設的 3 個異常交易模式UAT-003多語言使用國際業務人員中英文切換無遺漏,術語翻譯準確UAT-004報告生成與匯出監管事務專員匯出的 CSV 與 PDF 包含所有必要資訊UAT-005多模型比較資料分析師能並行測試 4 種模型並比較結果
9.6.2 UAT 執行記錄範本
CopyUAT 測試記錄表

專案名稱: BioChain Analyst Pro v2.1
測試日期: 2024-01-20
測試人員: 張經理 (供應鏈部門)

UAT-001: 新使用者首次使用
步驟:
1. 開啟系統 URL - ✅ 成功
2. 選擇語言(繁體中文) - ✅ 成功
3. 點擊「使用 Mock 資料」 - ✅ 成功,載入 50 筆資料
4. 查看儀表板 - ✅ KPI 正確顯示
5. 執行「供應鏈分析師」代理 - ✅ 45 秒內完成
6. 檢視分析結果 - ✅ 結果清晰易懂

總耗時: 8 分鐘
結論: ✅ 通過
建議: 可增加引導式教學 (Tutorial)

簽名: __________ 日期: __________
9.7 回歸測試 (Regression Testing)
9.7.1 回歸測試策略
每次程式碼變更後執行:
bashCopy# 自動化回歸測試套件
pytest tests/ --regression -v

# 包含以下測試:
# 1. 所有單元測試
# 2. 核心功能整合測試
# 3. 關鍵使用者路徑測試
# 4. 效能基準測試 (Performance Baseline)
9.7.2 回歸測試自動化 (CI/CD)
yamlCopy# .github/workflows/regression.yml
name: Regression Tests

on:
  pull_request:
    branches: [main, develop]
  schedule:
    - cron: '0 2 * * *'  # 每日凌晨 2 點執行

jobs:
  regression:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-benchmark
    
    - name: Run regression tests
      run: |
        pytest tests/ --regression --benchmark-only --benchmark-compare
    
    - name: Check performance degradation
      run: |
        # 若效能退化超過 10%,則測試失敗
        python scripts/check_performance.py --threshold 0.1
    
    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: regression-results
        path: test-results/
9.8 驗證報告範本
markdownCopy# 系統驗證報告
**BioChain Analyst Pro v2.1**

## 1. 驗證摘要
- **驗證日期**: 2024-01-15 ~ 2024-01-25
- **驗證環境**: AWS ECS Fargate (Staging)
- **測試範圍**: 所有 SRS 功能與非功能性需求
- **測試人員**: QA 團隊 (3 人) + 終端使用者 (5 人)

## 2. 測試結果統計
| 測試類型 | 總計 | 通過 | 失敗 | 阻擋 | 通過率 |
|---------|------|------|------|------|--------|
| 單元測試 | 120 | 118 | 2 | 0 | 98.3% |
| 整合測試 | 45 | 43 | 2 | 0 | 95.6% |
| 系統測試 | 50 | 48 | 1 | 1 | 96.0% |
| UAT | 25 | 24 | 0 | 1 | 96.0% |
| **總計** | **240** | **233** | **5** | **2** | **97.1%** |

## 3. 關鍵缺陷

### 缺陷 #001 (中等優先級)
- **描述**: 當資料集超過 50,000 筆時,網路圖渲染超過 10 秒
- **影響範圍**: FR-003 供應鏈網路圖視覺化
- **解決方案**: 實作資料分頁與延遲載入
- **預計修復版本**: v2.1.1
- **狀態**: 修復中

### 缺陷 #002 (低優先級)
- **描述**: 某些花卉主題下,文字對比度不足 (WCAG AA 不通過)
- **影響範圍**: NFR-002 無障礙性
- **解決方案**: 調整主題色彩配置
- **預計修復版本**: v2.2.0
- **狀態**: 已排程

## 4. 效能驗證結果
| 指標 | 目標 | 實測 | 狀態 |
|-----|------|------|------|
| 單代理執行時間 | <30s | 28s | ✅ |
| 儀表板渲染 | <1s | 0.8s | ✅ |
| 並發用戶支援 | ≥10 | 15 | ✅ |

## 5. 驗證結論
系統整體達到發布標準,建議:
1. 修復缺陷 #001 後發布至生產環境
2. 缺陷 #002 可於下一版本修復
3. 增加監控告警機制

**批准簽名**:
- QA 主管: __________ 日期: __________
- 專案經理: __________ 日期: __________

10. 風險管理
10.1 風險識別與評估
風險 ID風險描述可能性影響風險等級緩解措施負責人R-001API 提供商服務中斷中高高1. 多提供商冗餘<br>2. 本地快取機制<br>3. 離線模式技術主管R-002API 金鑰洩漏低極高高1. Secrets Manager<br>2. 金鑰輪替<br>3. 存取日誌監控安全工程師R-003資料隱私違規低極高高1. 資料匿名化<br>2. 合規審計<br>3. 員工培訓合規專員R-004大規模並發導致系統崩潰中中中1. 自動擴展<br>2. Rate Limiting<br>3. 負載測試DevOps 工程師R-005AI 模型輸出錯誤導致決策失誤中高高1. 人工審核機制<br>2. 免責聲明<br>3. 輸出驗證產品經理R-006依賴套件漏洞中中中1. 自動漏洞掃描<br>2. 定期更新<br>3. 虛擬環境隔離開發團隊R-007使用者誤操作刪除重要資料中中中1. 操作確認對話框<br>2. 資料備份<br>3. Undo 功能UX 設計師R-008雲端成本超支低中低1. 成本告警<br>2. 資源配額<br>3. 定期審查財務主管
風險等級計算:

可能性: 低 (1), 中 (2), 高 (3)
影響: 低 (1), 中 (2), 高 (3), 極高 (4)
風險等級 = 可能性 × 影響

1-2: 低風險 (綠色)
3-4: 中風險 (黃色)
6-9: 高風險 (橙色)
10-12: 極高風險 (紅色)



10.2 風險監控與回應
R-001: API 提供商服務中斷
監控指標:
pythonCopy# CloudWatch Alarm (AWS)
{
  "MetricName": "APIErrorRate",
  "Threshold": 5,  # 5% 錯誤率
  "EvaluationPeriods": 2,
  "Period": 300,
  "Statistic": "Average",
  "ComparisonOperator": "GreaterThanThreshold"
}
應急預案:

自動容錯轉移: 若 Provider A 失敗率 > 10%,自動切換至 Provider B
使用者通知: 顯示橫幅提示當前使用備用提供商
降級服務: 若所有提供商失敗,啟用離線模式 (僅提供視覺化功能)

實作範例:
pythonCopydef call_ai_with_fallback(prompt, providers=['gemini', 'openai', 'claude']):
    """多提供商容錯呼叫"""
    for provider in providers:
        try:
            if provider == 'gemini':
                return call_gemini_api(prompt)
            elif provider == 'openai':
                return call_openai_api(prompt)
            elif provider == 'claude':
                return call_claude_api(prompt)
        except Exception as e:
            log_error(f"{provider} 失敗: {e}")
            continue
    
    return "所有 AI 提供商暫時無法使用,請稍後再試"
R-002: API 金鑰洩漏
監控指標:

AWS CloudTrail: 監控 Secrets Manager 存取異常
異常 IP 位址存取告警
API 使用量突增 (>200% 平時平均值)

應急預案:

立即撤銷: 透過 Secrets Manager 自動輪替金鑰
通知團隊: Slack/Email 緊急通知
事件調查: 啟動安全事件回應流程
防範措施: 加強存取控制與 MFA

R-005: AI 模型輸出錯誤
緩解措施實作:
pythonCopydef validate_ai_output(output: str, expected_format: str) -> bool:
    """驗證 AI 輸出格式與內容"""
    # 檢查基本格式
    if expected_format == 'markdown':
        if not ('##' in output or '###' in output):
            log_warning("AI 輸出格式異常")
            return False
    
    # 檢查敏感詞彙 (避免不當建議)
    forbidden_words = ['保證', '100%', '絕對']
    if any(word in output for word in forbidden_words):
        log_warning("AI 輸出包含不當用詞")
        return False
    
    return True

# 使用範例
output = call_ai_api(prompt)
if not validate_ai_output(output, 'markdown'):
    output = "⚠️ AI 輸出未通過驗證,請人工審查:\n\n" + output
10.3 風險儀表板
使用 Streamlit 建立即時風險監控儀表板:
pythonCopydef render_risk_dashboard():
    st.header("🚨 系統風險監控")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        api_error_rate = get_api_error_rate()  # 從日誌獲取
        st.metric(
            "API 錯誤率",
            f"{api_error_rate:.2%}",
            delta=f"{api_error_rate - 0.01:.2%}",
            delta_color="inverse"
        )
        if api_error_rate > 0.05:
            st.error("⚠️ API 錯誤率超過閾值!")
    
    with col2:
        api_cost_today = get_daily_api_cost()
        st.metric(
            "今日 API 成本",
            f"${api_cost_today:.2f}",
            delta=f"${api_cost_today - 10:.2f}"
        )
        if api_cost_today > 50:
            st.warning("💰 API 成本接近預算上限")
    
    with col3:
        last_security_scan = get_last_security_scan_time()
        st.metric(
            "上次安全掃描",
            f"{last_security_scan} 天前"
        )
        if last_security_scan > 7:
            st.warning("🔒 建議執行安全掃描")

11. 可追溯性矩陣 (Traceability Matrix)
11.1 需求 → 測試追溯
需求 ID需求描述測試案例驗證方法狀態FR-001供應鏈資料管理UT-001 ~ UT-005<br>IT-001, ST-001 ~ ST-005自動化 + 手動✅FR-002互動式儀表板UT-010 ~ UT-015<br>ST-006 ~ ST-010自動化✅FR-003供應鏈網路圖UT-020, IT-003<br>ST-011 ~ ST-015手動⚠️FR-004時間序列趨勢分析UT-025, ST-016 ~ ST-020自動化✅FR-005多 AI 代理分析UT-030 ~ UT-040<br>IT-002, ST-021 ~ ST-030自動化 + 手動✅FR-006多模型支援UT-045 ~ UT-060<br>ST-031 ~ ST-040自動化✅FR-007多語言與主題ST-041 ~ ST-050<br>UAT-003手動✅NFR-001效能需求PT-001 ~ PT-010負載測試✅NFR-002可用性需求UAT-001, UAT-003使用者測試✅NFR-003可靠性需求IT-002, IT-004<br>Chaos Engineering故障注入測試✅NFR-004安全性需求SEC-001 ~ SEC-020滲透測試 + 掃描⚠️
11.2 設計 → 實作追溯
設計文件章節實作檔案程式碼行數審查狀態系統架構圖2.1app.py (主架構)150-250✅ 已審查資料流程圖2.4app.py (資料處理)400-600✅ 已審查AI 呼叫介面3.3.2app.py (call_*_api 函數)800-1200✅ 已審查視覺化模組FR-002/003/004app.py (可視化函數)1200-1500⚠️ 待審查安全控制8.2 ~ 8.4app.py (安全函數)600-800✅ 已審查
11.3 缺陷 → 修復追溯
缺陷 ID發現階段關聯需求修復 PR驗證測試關閉日期BUG-001整合測試FR-003#PR-125IT-003-retest2024-01-18BUG-002UATNFR-002#PR-138UAT-003-retest2024-01-22BUG-003安全測試NFR-004#PR-142SEC-005-retest進行中

12. 維護與支援
12.1 維護策略
12.1.1 預防性維護
每日自動任務:
bashCopy#!/bin/bash
# scripts/daily_maintenance.sh

# 1. 清理暫存檔案 (超過 7 天)
find /tmp/streamlit-* -mtime +7 -delete

# 2. 輪替日誌檔案
logrotate /etc/logrotate.d/biochain

# 3. 檢查磁碟空間
DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "警告: 磁碟使用率 ${DISK_USAGE}%" | mail -s "磁碟告警" admin@company.com
fi

# 4. 健康檢查
curl -f http://localhost:8501/_stcore/health || systemctl restart biochain

# 5. 備份配置檔
cp /app/agents.yaml /backup/agents_$(date +%Y%m%d).yaml
每週維護任務:

更新 Python 依賴套件 (安全性更新)
審查系統日誌與錯誤模式
效能指標趨勢分析
API 成本審查

每月維護任務:

完整系統備份 (配置 + 資料)
安全性掃描與漏洞修補
容量規劃評估
災難復原演練

12.1.2 修正性維護
錯誤分類與 SLA:
嚴重性描述回應時間解決時間範例P0 (緊急)系統完全無法使用15 分鐘4 小時生產環境崩潰、資料遺失P1 (高)核心功能失效1 小時24 小時AI 代理全部失敗、無法上傳資料P2 (中)部分功能異常4 小時3 工作日特定主題顯示錯誤、圖表渲染緩慢P3 (低)小問題或改進建議1 工作日下次發布UI 文字錯誤、效能優化建議
問題追蹤流程:
mermaidCopygraph LR
    A[使用者回報] --> B{嚴重性評估}
    B -->|P0/P1| C[立即指派工程師]
    B -->|P2/P3| D[加入待辦清單]
    C --> E[根本原因分析]
    D --> E
    E --> F[修復開發]
    F --> G[Code Review]
    G --> H[測試驗證]
    H --> I{通過?}
    I -->|是| J[部署至生產]
    I -->|否| F
    J --> K[通知使用者 & 關閉工單]
12.2 支援層級
12.2.1 一級支援 (L1 Support)
職責:

接收與記錄使用者問題
提供基本操作指導
處理常見問題 (FAQ)
升級至 L2 (無法解決時)

工具:

工單系統 (Jira Service Desk / Zendesk)
知識庫 (Confluence / Notion)
即時通訊 (Slack #support 頻道)

常見問題範例:
問題解決方案無法登入1. 檢查網路連線<br>2. 清除瀏覽器快取<br>3. 重設密碼上傳失敗1. 檢查檔案格式 (必須是 CSV)<br>2. 確認檔案大小 < 10 MB<br>3. 驗證必要欄位代理執行緩慢1. 檢查網路延遲<br>2. 選擇較快的模型 (如 grok-3-mini)<br>3. 減少輸入資料量
12.2.2 二級支援 (L2 Support)
職責:

深入技術問題排查
系統配置調整
資料庫查詢與修復
升級至開發團隊 (L3)

工具:

日誌分析平台 (ELK / Splunk)
監控系統 (Grafana / Datadog)
SSH 遠端存取
資料庫管理工具

升級標準:

需要修改原始碼
涉及安全性漏洞
系統架構變更
無法在 4 小時內解決

12.2.3 三級支援 (L3 Support)
職責:

程式碼除錯與修復
新功能開發
架構優化
安全性修補

團隊組成:

後端工程師 (2 人)
前端工程師 (1 人)
DevOps 工程師 (1 人)
安全工程師 (0.5 人,兼職)

12.3 文件維護
12.3.1 技術文件清單
文件名稱版本更新頻率負責人位置綜合技術規格文件2.1每季系統架構師/docs/technical_spec.md使用者操作手冊2.1每次發布技術寫作師/docs/user_manual.mdAPI 參考文件2.1隨程式碼更新開發團隊/docs/api_reference.md部署指南2.1每季DevOps 工程師/docs/deployment_guide.md疑難排解指南1.3每月L2 支援團隊/docs/troubleshooting.md變更日誌 (CHANGELOG)-每次發布產品經理/CHANGELOG.md
12.3.2 文件版本控制
bashCopy# 文件儲存於 Git 倉庫
docs/
├── technical_spec.md
├── user_manual.md
├── api_reference.md
├── deployment_guide.md
├── troubleshooting.md
└── archive/
    ├── technical_spec_v2.0.md
    └── user_manual_v2.0.md

# 使用語意化版本號
# 格式: [主版本].[次版本].[修訂版本]
# 範例: 2.1.3
# - 主版本: 架構重大變更
# - 次版本: 新增功能
# - 修訂版本: Bug 修復與小改進
12.3.3 自動文件生成
pythonCopy# scripts/generate_api_docs.py
"""從程式碼註解自動生成 API 文件"""

import ast
import inspect
from app import *

def extract_docstrings(module):
    """提取模組中所有函數的 docstring"""
    docs = []
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and obj.__doc__:
            docs.append({
                'function': name,
                'signature': str(inspect.signature(obj)),
                'docstring': inspect.getdoc(obj)
            })
    return docs

# 生成 Markdown 格式文件
docs = extract_docstrings(sys.modules['app'])
with open('docs/api_reference.md', 'w', encoding='utf-8') as f:
    f.write("# API 參考文件\n\n")
    for doc in docs:
        f.write(f"## `{doc['function']}{doc['signature']}`\n\n")
        f.write(f"{doc['docstring']}\n\n")
        f.write("---\n\n")
12.4 備份與災難復原
12.4.1 備份策略
資料分類:
資料類型備份頻率保留期限備份方法系統配置 (agents.yaml)每日30 天Git + S3使用者上傳資料即時 (若啟用)90 天S3 Versioning執行日誌每小時180 天CloudWatch Logs系統快照每週4 週EBS Snapshot資料庫 (若有)每日 + 每週完整1 年RDS Automated Backup
3-2-1 備份原則:

3 份資料副本 (1 正本 + 2 備份)
2 種不同媒體 (本地磁碟 + 雲端儲存)
1 份異地備份 (不同 AWS Region)

12.4.2 災難復原計畫 (DRP)
災難場景定義:
場景描述RTORPO復原策略單一 EC2 執行個體失敗硬體故障或軟體崩潰15 分鐘5 分鐘Auto Scaling 自動啟動新執行個體整個 Availability Zone 失敗AWS AZ 級別故障1 小時15 分鐘Multi-AZ 部署,Load Balancer 自動切換Region 級別災難整個 AWS Region 不可用4 小時1 小時跨 Region 複寫,手動切換 DNS資料損壞/刪除惡意刪除或程式錯誤2 小時24 小時從 S3 Versioning 或快照還原安全性入侵系統被入侵或勒索軟體8 小時4 小時隔離受感染系統,從乾淨備份復原
RTO (Recovery Time Objective): 系統可接受的最長停機時間
RPO (Recovery Point Objective): 可接受的最大資料遺失時間
災難復原演練計畫:
markdownCopy## DR 演練 Runbook

### 演練日期: 2024-03-15
### 演練場景: EC2 執行個體失敗

#### 步驟:
1. **T+0 min**: 模擬失敗 - 手動停止生產環境 EC2
2. **T+1 min**: 驗證監控告警觸發 (PagerDuty/CloudWatch)
3. **T+5 min**: Auto Scaling 啟動替換執行個體
4. **T+10 min**: 驗證新執行個體健康狀態
5. **T+15 min**: 驗證應用程式可用性 (執行煙霧測試)
6. **T+20 min**: 檢查資料一致性
7. **T+30 min**: 演練結束,記錄改進事項

#### 成功標準:
- RTO < 15 分鐘 ✅
- RPO < 5 分鐘 ✅
- 無資料遺失 ✅
- 所有監控正常 ✅

#### 改進事項:
- [ ] 優化 EC2 啟動時間 (當前 8 分鐘,目標 5 分鐘)
- [ ] 增加更詳細的健康檢查

13. 監管合規性
13.1 適用監管框架
法規/標準適用性關鍵要求合規狀態FDA 21 CFR Part 11❌ 不適用電子記錄與電子簽章N/A (非醫療器材)EU MDR 2017/745❌ 不適用醫療器材上市要求N/A (決策支援工具)ISO 13485⚠️ 參考品質管理系統部分符合IEC 62304⚠️ 參考醫療器材軟體生命週期部分符合GDPR (EU)✅ 適用 (若服務歐盟使用者)個人資料保護✅ 符合HIPAA (US)✅ 適用 (若處理 PHI)健康資訊隱私✅ 符合ISO 27001⚠️ 建議資訊安全管理部分符合
13.2 監管定位聲明
Copy重要聲明:

BioChain Analyst Pro v2.1 為「決策支援工具」(Decision Support Tool),
非醫療器材 (Medical Device)。

依據:
- FDA Guidance "Clinical Decision Support Software" (2022)
- EU MDR Annex VIII Rule 11

本系統符合以下條件,不屬於醫療器材:
1. 僅用於供應鏈管理與資料分析,不直接涉及診斷或治療
2. 不處理患者個人健康資訊 (PHI)
3. 最終決策權完全由人類使用者掌握
4. 系統輸出需經專業人員驗證後方可採取行動

使用者責任:
- 使用者應具備供應鏈管理相關專業知識
- 不得將 AI 輸出作為唯一決策依據
- 應遵循組織內部審批流程

若未來產品用途變更,可能需重新評估監管定位。
13.3 GDPR 合規措施
13.3.1 個人資料處理原則
GDPR 原則實作措施合法性、公平性、透明性提供隱私權政策,明確告知資料處理目的目的限制僅用於供應鏈分析,不作其他用途資料最小化不收集不必要的個人資訊,支援匿名化準確性提供資料編輯功能,確保資料正確性儲存限制Session 資料於 24 小時後自動清除完整性與保密性TLS 加密傳輸,Secrets Manager 保護金鑰問責制維護處理活動記錄,定期審計
13.3.2 資料主體權利
權利實作方法存取權 (Right to Access)提供資料匯出功能 (CSV 下載)更正權 (Right to Rectification)內建資料編輯功能刪除權 (Right to Erasure)提供「清除所有資料」按鈕 + Session 自動過期限制處理權 (Right to Restriction)允許使用者暫停特定代理執行資料可攜權 (Right to Portability)支援 CSV 格式匯出反對權 (Right to Object)允許使用者選擇不使用 AI 功能自動化決策相關權利免責聲明
13.3.3 隱私權政策範本
markdownCopy# 隱私權政策
**BioChain Analyst Pro v2.1**

最後更新: 2024-01-15

## 1. 資料控制者
[公司名稱]
[地址]
聯絡方式: privacy@company.com

## 2. 收集的資料
- **使用者輸入資料**: 您上傳的供應鏈 CSV 檔案
- **日誌資料**: IP 位址、瀏覽器類型、操作時間戳
- **不收集**: 姓名、Email、電話等個人身份資訊 (除非您主動輸入於資料中)

## 3. 資料用途
- 執行 AI 輔助分析
- 系統效能優化
- 安全性監控

## 4. 資料分享
- **AI 提供商**: 您的輸入資料會傳送至 Google/OpenAI/Anthropic/xAI 進行處理
  (請參考各提供商隱私政策)
- **不分享**: 我們不會將您的資料出售或分享給其他第三方

## 5. 資料保留
- Session 資料: 24 小時後自動刪除
- 日誌資料: 保留 90 天

## 6. 您的權利
您有權要求:
- 存取您的資料
- 更正或刪除資料
- 限制處理
- 資料可攜

請聯繫: privacy@company.com

## 7. Cookie 使用
我們使用 Streamlit Session Cookie 維持您的工作階段,不使用追蹤 Cookie。

## 8. 變更通知
本政策變更時,我們會在系統中顯示通知。
13.4 HIPAA 合規措施 (若適用)
13.4.1 技術保護措施 (Technical Safeguards)
要求實作存取控制 (§164.312(a)(1))OAuth 2.0 認證 + RBAC 授權審計控制 (§164.312(b))完整審計日誌 (見 8.6 節)完整性控制 (§164.312(c)(1))SHA-256 資料雜湊傳輸安全 (§164.312(e)(1))TLS 1.3 加密加密 (可選) (§164.312(a)(2)(iv))API 金鑰加密存放於 Secrets Manager
13.4.2 管理保護措施 (Administrative Safeguards)

安全管理流程: 定期風險評估 (每季)
人員培訓: 年度 HIPAA 合規培訓 (若處理 PHI)
事件回應計畫: 見 12.4.2 節災難復原計畫

13.4.3 物理保護措施 (Physical Safeguards)
若自建機房:

門禁控制 (刷卡記錄)
監視攝影機
防火與防水措施

若使用雲端 (AWS/GCP/Azure):

依賴雲端提供商的 HIPAA 合規認證 (BAA - Business Associate Agreement)

13.5 稽核準備
13.5.1 稽核文件清單
markdownCopy## 稽核文件包 (Audit Documentation Package)

### 1. 系統文件
- [ ] 綜合技術規格文件 (本文件)
- [ ] 系統架構圖
- [ ] 資料流程圖
- [ ] 網路拓撲圖

### 2. 風險管理
- [ ] 風險評估報告
- [ ] 威脅模型 (STRIDE 分析)
- [ ] 災難復原計畫

### 3. 驗證文件
- [ ] 測試計畫
- [ ] 測試案例與結果
- [ ] 驗證報告
- [ ] 可追溯性矩陣

### 4. 安全性文件
- [ ] 安全性測試報告 (OWASP ZAP / Burp Suite)
- [ ] 漏洞掃描報告 (Snyk / Trivy)
- [ ] 滲透測試報告 (若有)
- [ ] 安全事件日誌

### 5. 變更管理
- [ ] CHANGELOG (版本歷史)
- [ ] Git Commit 記錄
- [ ] Code Review 記錄
- [ ] 發布審批記錄

### 6. 合規證明
- [ ] GDPR 資料處理活動記錄 (ROPA)
- [ ] HIPAA BAA (若適用)
- [ ] ISO 27001 證書 (若有)
- [ ] 雲端提供商合規證書 (AWS/GCP SOC 2)

### 7. 訓練記錄
- [ ] 開發團隊安全培訓記錄
- [ ] 使用者操作培訓記錄
13.5.2 定期合規審查
審查項目頻率負責人最後審查日期存取控制審查每季安全主管2024-01-10日誌完整性檢查每月DevOps2024-01-15API 金鑰輪替每 90 天開發團隊2024-01-05依賴套件更新每月開發團隊2024-01-12災難復原演練每半年全體團隊2023-12-20隱私權政策更新每年法務2024-01-01

14. 附錄
14.1 詞彙表 (Glossary)
術語定義AI 代理 (AI Agent)執行特定分析任務的 AI 模型實例,配置於 agents.yaml供應鏈節點 (Supply Chain Node)供應商、經銷商或醫療機構多代理管線 (Multi-Agent Pipeline)依序執行多個 AI 代理,前一代理輸出作為下一代理輸入溫度 (Temperature)AI 模型隨機性參數,0=確定性,1=高創意性TokenAI 模型處理的最小文字單位 (~4 字元)Streamlit Session State瀏覽器會話期間保持資料狀態的機制Mock 資料 (Mock Data)模擬測試資料,用於展示與開發KPI (Key Performance Indicator)關鍵績效指標RTO (Recovery Time Objective)目標復原時間RPO (Recovery Point Objective)目標復原點 (資料遺失容忍度)PHI (Protected Health Information)受保護健康資訊 (HIPAA)PII (Personally Identifiable Information)個人身份資訊BAA (Business Associate Agreement)HIPAA 商業夥伴協議
14.2 縮寫對照表
縮寫全名AIArtificial Intelligence (人工智慧)APIApplication Programming Interface (應用程式介面)AWSAmazon Web ServicesCI/CDContinuous Integration / Continuous Deployment (持續整合/部署)CSVComma-Separated Values (逗號分隔值)DRPDisaster Recovery Plan (災難復原計畫)ECSElastic Container Service (AWS)GDPRGeneral Data Protection Regulation (通用資料保護規範)GCPGoogle Cloud PlatformHIPAAHealth Insurance Portability and Accountability Act (美國)IaCInfrastructure as Code (基礎設施即程式碼)IAMIdentity and Access Management (身分與存取管理)JSONJavaScript Object NotationKPIKey Performance Indicator (關鍵績效指標)L1/L2/L3Support Level 1/2/3 (支援層級)MDRMedical Device Regulation (EU)OAuthOpen Authorization (開放授權)RBACRole-Based Access Control (角色式存取控制)RESTRepresentational State TransferRPORecovery Point Objective (目標復原點)RTORecovery Time Objective (目標復原時間)SAMLSecurity Assertion Markup LanguageSDKSoftware Development Kit (軟體開發套件)SLAService Level Agreement (服務等級協議)SQLStructured Query LanguageSRSSoftware Requirements Specification (軟體需求規格)SSL/TLSSecure Sockets Layer / Transport Layer SecurityUATUser Acceptance Testing (使用者驗收測試)UIUser Interface (使用者介面)UXUser Experience (使用者體驗)YAMLYAML Ain't Markup Language
14.3 參考文獻

Streamlit 官方文件
https://docs.streamlit.io/
版本: 1.30.0, 存取日期: 2024-01-15
Google Gemini API 文件
https://ai.google.dev/docs
版本: 2025-01, 存取日期: 2024-01-15
OpenAI API 參考
https://platform.openai.com/docs/api-reference
版本: v1, 存取日期: 2024-01-15
Anthropic Claude API 文件
https://docs.anthropic.com/claude/reference
版本: 2024-01, 存取日期: 2024-01-15
xAI Grok API 文件
https://docs.x.ai/
版本: Beta, 存取日期: 2024-01-15
ISO 13485 - Medical devices — Quality management systems
International Organization for Standardization
IEC 62304+AMD1 - Medical device software — Software life cycle processes
International Electrotechnical Commission
FDA Guidance: Clinical Decision Support Software (2022)
https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software
GDPR Official Text (Regulation EU 2016/679)
https://gdpr-info.eu/
HIPAA Security Rule (45 CFR Part 164 Subpart C)
https://www.hhs.gov/hipaa/for-professionals/security/index.html
OWASP Top 10 - 2021
https://owasp.org/Top10/
NIST Cybersecurity Framework v1.1 (2018)
https://www.nist.gov/cyberframework

14.4 變更歷史 (Change History)
版本日期作者變更摘要0.12024-01-05系統架構師初始草稿 (架構設計)0.52024-01-10系統架構師新增 SRS 與部署章節0.92024-01-18系統架構師 + QA 主管新增驗證計畫與風險管理1.02024-01-25全體團隊正式發布版本1.12024-02-10安全工程師強化安全性章節 (8.2~8.4)2.02024-03-01系統架構師重構架構 (支援多提供商)2.12024-03-15系統架構師新增 Kubernetes 部署選項與監管合規章節
14.5 審查簽核
Copy文件審查與批准

技術審查:
姓名: ________________  職位: 系統架構師      日期: __________
姓名: ________________  職位: 資深開發工程師   日期: __________

品質審查:
姓名: ________________  職位: QA 主管         日期: __________

安全審查:
姓名: ________________  職位: 資訊安全主管     日期: __________

監管審查:
姓名: ________________  職位: 監管事務專員     日期: __________

最終批准:
姓名: ________________  職位: 專案經理        日期: __________
姓名: ________________  職位: 技術總監        日期: __________
14.6 聯絡資訊
技術支援:

Email: support@company.com
Slack: #biochain-support
工單系統: https://support.company.com

安全問題回報:

Email: security@company.com (PGP 公鑰: https://company.com/pgp)
Bug Bounty: https://company.com/security/bug-bounty

商業合作:

Email: sales@company.com
網站: https://www.company.com/biochain

監管與合規:

Email: compliance@company.com
隱私權問題: privacy@company.com


文件結尾
BioChain Analyst Pro v2.1 - 綜合技術規格文件
總頁數: [本文件約 80-100 頁 A4]
文件版本: 2.1
最後更新: 2024-03-15
文件 ID: BIOCHAIN-SPEC-2024-001

附加資源
線上文件庫: https://docs.company.com/biochain/v2.1/
GitHub 倉庫: https://github.com/company/biochain-analyst-pro
Docker Hub: https://hub.docker.com/r/company/biochain-analyst
示範影片: https://www.youtube.com/watch?v=xxxxx
社群論壇: https://community.company.com/biochain

版權聲明
© 2024 [公司名稱]. All rights reserved.
本文件包含專有資訊,未經授權不得複製或分發。
