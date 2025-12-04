FDA 510(k) 審查工作室 · 花卉版 V2 - 綜合技術規格文件
文件版本控制
版本	日期	作者	變更說明
1.0	2024-01-XX	系統架構師	初始版本
目錄
執行摘要
系統架構
軟體需求規格 (SRS)
系統需求
環境設定
部署選項
基礎設施即程式碼 (IaC) 與整合
安全性考量
驗證計畫
風險管理
可追溯性矩陣
維護與支援
監管合規性
附錄
1. 執行摘要
1.1 系統概述
FDA 510(k) 審查工作室 · 花卉版 V2 是一個基於人工智慧的多代理協作平台,專為醫療器材監管審查流程設計。本系統整合四大主流 AI 提供商 (Google Gemini, OpenAI, Anthropic Claude, xAI Grok),實現串聯式文件審查、結構化筆記轉換、以及互動式分析儀表板。

1.2 目標用戶
FDA 510(k) 審查人員
醫療器材監管事務專員
法規顧問與品質保證團隊
臨床工程師與技術撰寫人員
1.3 核心價值主張
多模型協作: 同時支援 Gemini, GPT, Claude, Grok,可依任務特性選用最適模型
可編輯鏈式審查: 每個代理步驟的輸入/輸出均可人工編輯,支援混合式人機協作
遊戲化激勵機制: 魔力值 (Mana)、經驗值 (XP)、成就徽章等元素提升使用者參與度
20 種北歐花卉主題: 提供美學化工作環境,降低審查疲勞
AI 筆記助手: 自動將非結構化文本轉換為結構化 Markdown、實體提取、心智圖、測驗題等
1.4 監管定位
本系統為 決策支援工具 (Decision Support Tool),不屬於 FDA 定義之醫療器材。系統輸出結果需由具資格之審查人員驗證,最終決策權歸人類審查員。

2. 系統架構
2.1 高階架構圖
mermaid

Copy
graph TB
    subgraph "使用者層"
        UI[Streamlit Web UI]
    end
    
    subgraph "應用層"
        APP[Python Application Core]
        SESSION[Session State Manager]
        GAMIFY[Gamification Engine]
    end
    
    subgraph "業務邏輯層"
        PIPELINE[Multi-Agent Pipeline Orchestrator]
        NOTE[AI Note Keeper]
        DASH[Analytics Dashboard]
    end
    
    subgraph "AI 服務層"
        GEMINI[Google Gemini API]
        OPENAI[OpenAI API]
        ANTHROPIC[Anthropic Claude API]
        XAI[xAI Grok API]
    end
    
    subgraph "資料層"
        YAML[agents.yaml Config]
        ENV[Environment Variables]
        LOGS[Execution Logs]
    end
    
    UI --> APP
    APP --> SESSION
    APP --> PIPELINE
    APP --> NOTE
    APP --> DASH
    APP --> GAMIFY
    
    PIPELINE --> GEMINI
    PIPELINE --> OPENAI
    PIPELINE --> ANTHROPIC
    PIPELINE --> XAI
    
    NOTE --> GEMINI
    NOTE --> OPENAI
    NOTE --> ANTHROPIC
    NOTE --> XAI
    
    APP --> YAML
    APP --> ENV
    PIPELINE --> LOGS
2.2 技術堆疊
層級	技術/框架	版本要求	用途
前端	Streamlit	≥1.30.0	Web UI 框架
後端	Python	≥3.9	核心應用邏輯
AI SDKs	google-generativeai	latest	Gemini 整合
openai	≥1.0.0	OpenAI 整合
anthropic	latest	Claude 整合
xai-sdk	latest	Grok 整合
配置	PyYAML	≥6.0	agents.yaml 解析
資料結構	dataclasses	stdlib	型別安全配置
2.3 模組架構

Copy
├── app.py (主程式,包含所有功能模組)
├── agents.yaml (代理配置檔)
├── prompts.py (可選,系統提示詞庫)
└── requirements.txt (依賴套件清單)
核心模組說明:

Config/Constants (第 1 節): AI 模型清單、語言標籤、主題定義
Session Management (第 2 節): 狀態初始化、持久化管理
Agent Configuration (第 3 節): YAML 解析、代理物件建構
Theme & Styling (第 4 節): 動態 CSS 注入、主題切換
API Key Handling (第 5 節): 環境變數優先、UI fallback
Provider Calls (第 6 節): 統一 AI 呼叫介面、錯誤處理
Gamification (第 7 節): 魔力值、經驗值、成就系統
Pipeline UI (第 8 節): 多代理串聯、可編輯輸入/輸出
Note Keeper (第 9 節): 結構化轉換、實體提取、心智圖
Dashboard (第 10 節): 指標追蹤、執行日誌視覺化
Settings (第 11 節): 語言、主題模式、API 金鑰設定
2.4 資料流程
mermaid

Copy
sequenceDiagram
    participant U as 使用者
    participant UI as Streamlit UI
    participant P as Pipeline Orchestrator
    participant A1 as Agent 1 (Gemini)
    participant A2 as Agent 2 (OpenAI)
    participant A3 as Agent 3 (Claude)
    participant LOG as Execution Log
    
    U->>UI: 輸入案例描述
    UI->>P: 啟動全流程執行
    P->>A1: 呼叫 Agent 1 (初步審查)
    A1-->>P: 返回結構化輸出
    P->>LOG: 記錄執行狀態
    P->>A2: 將 A1 輸出作為 A2 輸入
    A2-->>P: 返回風險分析
    P->>A3: 將 A2 輸出作為 A3 輸入
    A3-->>P: 返回最終建議
    P->>UI: 更新所有代理結果
    UI->>U: 顯示可編輯輸出
    U->>UI: 編輯 Agent 2 輸出
    UI->>P: 使用編輯後輸出重新執行 Agent 3
    P->>A3: 呼叫 Agent 3 (使用新輸入)
    A3-->>P: 返回更新建議
    P->>UI: 顯示更新結果
3. 軟體需求規格 (SRS)
3.1 功能性需求 (Functional Requirements)
FR-001: 多代理流程執行
需求描述: 系統應支援依序執行 N 個 AI 代理,每個代理的輸出自動成為下一個代理的輸入。

驗收標準:

能夠從 agents.yaml 載入任意數量代理配置
全流程執行按鈕可一次性串聯所有代理
每個代理執行狀態即時顯示於 UI (執行中/成功/失敗)
任一代理失敗時,流程中斷並記錄錯誤
優先級: P0 (必須)

追溯性: 需求來源 - FDA 510(k) 審查流程多階段特性

FR-002: 可編輯鏈式審查
需求描述: 使用者可在任意代理步驟編輯輸入或輸出,修改後的內容應成為後續步驟的預設輸入。

驗收標準:

每個代理顯示獨立的「輸入」與「輸出」文字區域
輸出支援「文字編輯」與「Markdown 預覽」雙模式切換
編輯輸出後,下一步代理的預設輸入即時更新
單步執行功能可使用當前編輯狀態執行指定代理
優先級: P0 (必須)

追溯性: 需求來源 - 人機協作審查模式需求

FR-003: 多 AI 提供商整合
需求描述: 系統應整合至少四家主流 AI 提供商,並支援動態模型選擇。

驗收標準:

支援 Google Gemini (≥2 個模型)
支援 OpenAI (≥2 個模型)
支援 Anthropic Claude (≥2 個模型)
支援 xAI Grok (≥2 個模型)
每個代理可獨立配置 provider/model/temperature/max_tokens
API 金鑰支援環境變數與 UI 輸入雙管道
優先級: P0 (必須)

追溯性: 需求來源 - 模型多樣性與容錯需求

FR-004: AI 筆記助手
需求描述: 提供獨立的筆記轉換工具,支援非結構化文本的智慧化處理。

驗收標準:

結構化 Markdown 轉換 (清理、格式化、分段)
監管實體提取 (20 個關鍵實體 → 表格)
Mermaid 心智圖生成 (hierarchical mindmap)
測驗題生成 (5 題 MCQs)
關鍵字高亮 (client-side,無需 AI 呼叫)
優先級: P1 (高度期望)

追溯性: 需求來源 - 會議筆記、測試報告等非結構化資料處理需求

FR-005: 互動式分析儀表板
需求描述: 追蹤並視覺化系統使用指標與執行歷史。

驗收標準:

顯示總執行次數、各提供商呼叫次數、最後執行時長
提供商使用分佈長條圖
執行日誌時間軸 (最近 30 筆)
日誌分類標記 (資訊/成功/錯誤) 以不同顏色區分
優先級: P2 (期望)

追溯性: 需求來源 - 系統可觀測性與使用行為分析

FR-006: 遊戲化激勵系統
需求描述: 透過健康值、魔力值、經驗值、成就徽章等元素提升使用參與度。

驗收標準:

健康值 (Health): 初始 100,固定值 (可擴展為壓力計)
魔力值 (Mana): 初始 100,每次代理執行消耗 20,不足時阻止執行
經驗值 (XP): 每次代理執行 +10,每 100 XP 升 1 級
成就徽章: 50 XP、200 XP、10 次執行等里程碑自動解鎖
魔力球 (Mana Orb): 動畫脈動視覺元件
壓力計 (Stress Meter): 與健康值反向關聯 (Stress = 100 - Health)
優先級: P2 (期望)

追溯性: 需求來源 - 使用者體驗與長時間審查疲勞緩解

FR-007: 多語言與主題支援
需求描述: 支援繁體中文與英文雙語切換,以及 20 種北歐花卉主題。

驗收標準:

語言切換: 英文 (en) / 繁體中文 (zh)
主題模式切換: 亮色 (light) / 暗色 (dark)
20 種花卉主題,每種包含 primary/secondary/accent/bg 四色配置
幸運抽獎按鈕隨機切換主題
主題切換即時套用至全局 CSS
優先級: P2 (期望)

追溯性: 需求來源 - 多地區使用者與審美偏好多樣性

3.2 非功能性需求 (Non-Functional Requirements)
NFR-001: 效能需求
指標	目標值	測量方法
單代理執行回應時間	<30 秒 (95th percentile)	API 呼叫計時器
全流程執行時間 (3 代理)	<90 秒 (95th percentile)	Pipeline orchestrator 計時
UI 載入時間	<3 秒	Streamlit metrics
並發使用者支援	≥10 (單實例)	負載測試
NFR-002: 可用性需求
學習曲線: 新使用者應能在 15 分鐘內完成首次完整流程執行
錯誤訊息: 所有錯誤訊息應為繁體中文/英文雙語,並提供可操作建議
無障礙性: 遵循 WCAG 2.1 AA 級標準 (色彩對比、鍵盤導航)
NFR-003: 可靠性需求
API 失敗容錯: 單一 AI 提供商故障時,使用者可切換至其他提供商繼續執行
會話持久性: 使用者會話資料在瀏覽器 refresh 後保持 (Streamlit session_state)
資料完整性: 所有代理輸出與執行日誌應完整保存於會話內
NFR-004: 安全性需求
詳見 第 8 節: 安全性考量

NFR-005: 可維護性需求
模組化設計: 每個功能模組 (Pipeline, Note Keeper, Dashboard) 應可獨立測試與部署
配置外部化: 代理配置、系統提示詞應存放於 agents.yaml 與 prompts.py,無需修改主程式
日誌記錄: 所有代理執行應記錄於 execution_log,包含時間戳、類型、訊息
NFR-006: 可擴展性需求
水平擴展: 支援 Kubernetes 部署,可透過增加 Pod 數量處理更高負載
模型擴展: 新增 AI 提供商僅需修改 AI_MODELS 字典與對應 call_* 函數
主題擴展: 新增花卉主題僅需於 FLOWER_THEMES 列表添加新項目
3.3 系統介面需求
3.3.1 使用者介面 (UI)
框架: Streamlit Web UI
瀏覽器相容性: Chrome/Edge/Firefox/Safari (最新兩版)
RWD: 支援桌面瀏覽器,不保證行動裝置最佳化 (FDA 審查通常於桌面環境進行)
3.3.2 外部 API 介面
API 提供商	協定	認證方式	端點範例
Google Gemini	REST	API Key	generativelanguage.googleapis.com
OpenAI	REST	API Key	api.openai.com/v1/chat/completions
Anthropic	REST	API Key	api.anthropic.com/v1/messages
xAI Grok	REST	API Key	api.x.ai/v1/chat (假設)
3.3.3 配置檔介面
agents.yaml 結構範例:

yaml

Copy
agents:
  - id: "initial_review"
    name: "Initial 510(k) Reviewer"
    description: "Performs preliminary device classification and predicate identification"
    provider: "gemini"
    model: "gemini-2.5-flash"
    max_tokens: 4000
    temperature: 0.2
    system_prompt: |
      You are an FDA 510(k) pre-market reviewer specializing in initial device assessment.
      Analyze the provided device description and output:
      1. Device classification (Class I/II/III)
      2. Product code and regulation number
      3. Potential predicate devices
      4. Key regulatory concerns
      Output in structured Markdown.
      
  - id: "risk_analysis"
    name: "Risk Analyzer"
    description: "Evaluates biocompatibility, electrical safety, and software risks"
    provider: "openai"
    model: "gpt-4o-mini"
    max_tokens: 3000
    temperature: 0.3
    system_prompt: |
      你是醫療器材風險管理專家,依據 ISO 14971 與 FDA 指引進行風險分析。
      輸入為前一步驟的裝置描述,請輸出:
      1. 已識別危害清單 (≥10 項)
      2. 風險等級評估 (嚴重性 × 發生機率)
      3. 風險控制措施建議
      4. 殘餘風險評估
      以繁體中文 Markdown 表格與條列式呈現。
4. 系統需求
4.1 硬體需求
4.1.1 開發環境
元件	最低配置	建議配置
CPU	2 核心	4 核心+
RAM	4 GB	8 GB+
硬碟	10 GB 可用空間	20 GB SSD
網路	穩定寬頻連線	≥10 Mbps
4.1.2 生產環境 (單實例)
元件	最低配置	建議配置
CPU	2 vCPU	4 vCPU
RAM	4 GB	8 GB
硬碟	20 GB	50 GB SSD
網路	穩定公網連線	≥100 Mbps
4.1.3 生產環境 (Kubernetes 叢集)
節點數量: 3+ (高可用性)
每節點配置: 4 vCPU, 16 GB RAM
持久化儲存: 支援 ReadWriteMany 的 PV (若需共享配置檔)
4.2 軟體需求
4.2.1 作業系統
開發: Windows 10+, macOS 11+, Ubuntu 20.04+
生產: Ubuntu 20.04/22.04 LTS, Amazon Linux 2, RHEL 8+
4.2.2 Python 環境
版本: Python 3.9 - 3.11 (建議 3.10)
套件管理: pip 21.0+, 建議使用 virtual environment
4.2.3 必要 Python 套件
txt

Copy
streamlit>=1.30.0
pyyaml>=6.0
google-generativeai>=0.3.0
openai>=1.0.0
anthropic>=0.8.0
xai-sdk>=0.1.0  # 假設版本
4.2.4 容器環境 (選用)
Docker: 20.10+
基礎映像: python:3.10-slim
4.2.5 Orchestration (選用)
Kubernetes: 1.24+
Helm: 3.10+ (若使用 Helm Chart)
4.3 網路需求
對外連線: 需存取以下網域 (防火牆白名單)
generativelanguage.googleapis.com (Gemini)
api.openai.com (OpenAI)
api.anthropic.com (Anthropic)
api.x.ai (xAI)
對內連線: 若多實例部署,需開放容器間通訊 (K8s Service mesh)
5. 環境設定
5.1 本地開發環境設定
步驟 1: 安裝 Python
bash

Copy
# Ubuntu/Debian
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip

# macOS (Homebrew)
brew install python@3.10

# Windows (透過 python.org 下載安裝器)
步驟 2: 建立虛擬環境
bash

Copy
python3.10 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
步驟 3: 安裝依賴套件
bash

Copy
pip install --upgrade pip
pip install -r requirements.txt
步驟 4: 配置環境變數
建立 .env 檔案 (不應提交至 Git):

bash

Copy
# .env
GEMINI_API_KEY=AIzaSy...
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
XAI_API_KEY=xai-...
載入環境變數:

bash

Copy
# Linux/macOS
export $(cat .env | xargs)

# Windows (PowerShell)
Get-Content .env | ForEach-Object { $_.Split('=') | Set-Variable }
步驟 5: 準備配置檔
建立 agents.yaml (參考 3.3.3 節)

步驟 6: 啟動應用
bash

Copy
streamlit run app.py --server.port 8501
瀏覽器開啟 http://localhost:8501

5.2 Docker 環境設定
Dockerfile
dockerfile

Copy
FROM python:3.10-slim

WORKDIR /app

# 安裝系統依賴 (若需要)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴清單並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式碼
COPY app.py prompts.py agents.yaml ./

# 暴露 Streamlit 預設埠
EXPOSE 8501

# 健康檢查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 啟動指令
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
建置與執行
bash

Copy
# 建置映像
docker build -t fda-review-studio:v2 .

# 執行容器
docker run -d \
  --name fda-studio \
  -p 8501:8501 \
  -e GEMINI_API_KEY=$GEMINI_API_KEY \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -e XAI_API_KEY=$XAI_API_KEY \
  fda-review-studio:v2

# 檢視日誌
docker logs -f fda-studio
6. 部署選項
6.1 本地部署 (Local Deployment)
適用場景: 個人開發測試、隔離環境審查

步驟:

依照 5.1 節 完成環境設定
執行 streamlit run app.py
透過 http://localhost:8501 存取
優點:

完全離線 (若 API 金鑰預先設定)
最快速部署
無雲端成本
缺點:

無法多人協作
單點故障
無自動擴展
6.2 AWS 部署選項
6.2.1 AWS EC2 部署
架構圖:


Copy
Internet → ELB → EC2 Instance (Streamlit) → AI APIs
                    ↓
                 EBS Volume (配置檔)
步驟:

啟動 EC2 執行個體:
AMI: Ubuntu 22.04 LTS
執行個體類型: t3.medium (2 vCPU, 4 GB RAM)
安全群組: 允許 443 (HTTPS), 22 (SSH)
IAM 角色: 若需存取 Secrets Manager 儲存 API 金鑰
安裝應用:
bash

Copy
ssh -i keypair.pem ubuntu@<EC2_PUBLIC_IP>
sudo apt update && sudo apt install python3.10-venv nginx -y
git clone <REPO_URL>
cd fda-review-studio
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
配置 systemd 服務:
ini

Copy
# /etc/systemd/system/fda-studio.service
[Unit]
Description=FDA Review Studio
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/fda-review-studio
Environment="PATH=/home/ubuntu/fda-review-studio/venv/bin"
EnvironmentFile=/home/ubuntu/fda-review-studio/.env
ExecStart=/home/ubuntu/fda-review-studio/venv/bin/streamlit run app.py --server.port 8501
Restart=always

[Install]
WantedBy=multi-user.target
啟動服務:
bash

Copy
sudo systemctl daemon-reload
sudo systemctl enable fda-studio
sudo systemctl start fda-studio
配置 Nginx 反向代理 (HTTPS):
nginx

Copy
server {
    listen 443 ssl;
    server_name fda-review.example.com;
    
    ssl_certificate /etc/letsencrypt/live/fda-review.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/fda-review.example.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
成本估算 (us-east-1):

t3.medium: $0.0416/hr × 730 hrs = $30.37/月
EBS (30 GB): $3/月
ELB (Application): $16.20/月
資料傳輸: ~$5/月
總計: ~$55/月
6.2.2 AWS ECS Fargate 部署
架構圖:


Copy
Internet → ALB → ECS Service (Fargate Tasks) → AI APIs
                        ↓
                    EFS (共享配置檔)
                        ↓
                 Secrets Manager (API Keys)
步驟:

建立 ECR 儲存庫:
bash

Copy
aws ecr create-repository --repository-name fda-review-studio
docker tag fda-review-studio:v2 <AWS_ACCOUNT>.dkr.ecr.us-east-1.amazonaws.com/fda-review-studio:v2
docker push <AWS_ACCOUNT>.dkr.ecr.us-east-1.amazonaws.com/fda-review-studio:v2
建立 ECS Task Definition (JSON):
json

Copy
{
  "family": "fda-studio-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "fda-studio",
      "image": "<ECR_IMAGE_URI>",
      "portMappings": [{"containerPort": 8501}],
      "secrets": [
        {"name": "GEMINI_API_KEY", "valueFrom": "arn:aws:secretsmanager:us-east-1:xxx:secret:fda/gemini"},
        {"name": "OPENAI_API_KEY", "valueFrom": "arn:aws:secretsmanager:us-east-1:xxx:secret:fda/openai"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/fda-studio",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
建立 ECS Service:
bash

Copy
aws ecs create-service \
  --cluster fda-cluster \
  --service-name fda-studio-service \
  --task-definition fda-studio-task \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:us-east-1:xxx:targetgroup/fda-tg,containerName=fda-studio,containerPort=8501"
自動擴展配置:

bash

Copy
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --scalable-dimension ecs:service:DesiredCount \
  --resource-id service/fda-cluster/fda-studio-service \
  --min-capacity 2 \
  --max-capacity 10

aws application-autoscaling put-scaling-policy \
  --policy-name fda-cpu-scaling \
  --service-namespace ecs \
  --scalable-dimension ecs:service:DesiredCount \
  --resource-id service/fda-cluster/fda-studio-service \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration file://scaling-policy.json
成本估算:

Fargate (1 vCPU, 2GB) × 2 tasks: $0.04048/hr × 2 × 730 = $59.10/月
ALB: $16.20/月
NAT Gateway (若使用私有子網): $32.40/月
總計: ~$108/月
6.2.3 AWS Lambda + API Gateway 部署 (實驗性)
限制: Streamlit 本身不適合 Lambda,但可將核心邏輯 (run_agent) 包裝成 Lambda 函數,前端改用靜態 S3 + API Gateway。

不建議原因:

Streamlit 狀態管理依賴長連線 WebSocket
Lambda 15 分鐘執行時限可能不足 (多代理流程)
冷啟動延遲影響使用者體驗
6.3 GCP 部署選項
6.3.1 GCP Compute Engine 部署
類似 AWS EC2,使用 e2-medium 執行個體,步驟略。

成本估算:

e2-medium (us-central1): $24.27/月
Persistent Disk (30 GB): $2.04/月
Load Balancer: $18/月
總計: ~$45/月
6.3.2 GCP Cloud Run 部署
優勢: 完全託管、自動擴展、按請求計費

步驟:

建置容器並推送至 GCR:
bash

Copy
gcloud builds submit --tag gcr.io/PROJECT_ID/fda-review-studio
部署至 Cloud Run:
bash

Copy
gcloud run deploy fda-studio \
  --image gcr.io/PROJECT_ID/fda-review-studio \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 3600 \
  --set-env-vars GEMINI_API_KEY=xxx,OPENAI_API_KEY=xxx \
  --max-instances 10
配置自訂網域:
bash

Copy
gcloud run domain-mappings create --service fda-studio --domain fda-review.example.com
成本估算 (低流量場景):

請求費用: $0.40 per million requests
CPU: $0.00002400 per vCPU-second
Memory: $0.00000250 per GiB-second
假設每月 10,000 請求,平均 30 秒執行: ~$15/月
6.3.3 GCP GKE 部署
類似 AWS EKS,使用 Kubernetes Deployment + Service,步驟略。

成本估算:

GKE 叢集管理費: $0.10/hr × 730 = $73/月
3 × e2-standard-4 節點: $122.18/月 × 3 = $366.54/月
總計: ~$440/月 (適合企業級高流量場景)
6.4 Azure 部署選項
6.4.1 Azure App Service 部署
步驟:

建立 App Service Plan:
bash

Copy
az appservice plan create \
  --name fda-plan \
  --resource-group fda-rg \
  --sku B2 \
  --is-linux
建立 Web App:
bash

Copy
az webapp create \
  --name fda-review-studio \
  --resource-group fda-rg \
  --plan fda-plan \
  --runtime "PYTHON:3.10"
配置環境變數:
bash

Copy
az webapp config appsettings set \
  --name fda-review-studio \
  --resource-group fda-rg \
  --settings GEMINI_API_KEY=xxx OPENAI_API_KEY=xxx
部署程式碼 (透過 ZIP):
bash

Copy
zip -r app.zip app.py agents.yaml prompts.py requirements.txt
az webapp deployment source config-zip \
  --name fda-review-studio \
  --resource-group fda-rg \
  --src app.zip
成本估算:

B2 (2 核心, 3.5 GB RAM): $73/月
流量傳輸: ~$5/月
總計: ~$78/月
6.4.2 Azure Container Instances (ACI)
快速部署 (適合測試):

bash

Copy
az container create \
  --name fda-studio \
  --resource-group fda-rg \
  --image <ACR_IMAGE_URI> \
  --cpu 2 \
  --memory 4 \
  --ports 8501 \
  --environment-variables GEMINI_API_KEY=xxx OPENAI_API_KEY=xxx \
  --dns-name-label fda-review
成本: ~$45/月 (2 vCPU, 4 GB RAM, 持續執行)

6.4.3 Azure Kubernetes Service (AKS)
類似 AWS EKS / GCP GKE,步驟略。

成本估算:

3 × Standard_D2s_v3 節點: $96.36/月 × 3 = $289.08/月
Load Balancer: $18.25/月
總計: ~$307/月
6.5 混合部署 (Hybrid Deployment)
場景: 敏感資料需留在內部機房,但希望使用雲端 AI 服務

架構:


Copy
[內部機房]
   ↓
企業防火牆 (Outbound HTTPS 允許 AI API 網域)
   ↓
[雲端 AI 提供商]
實施步驟:

內部 VM/容器部署: 依照 6.1 節 於企業資料中心部署
網路設定: 配置防火牆允許存取 api.openai.com, generativelanguage.googleapis.com 等
VPN/Direct Connect (選用): 若需存取雲端託管的配置檔或日誌儲存 (如 S3)
Identity Federation: 使用企業 SSO (SAML/OAuth) 整合使用者驗證
優點:

資料不出內部網路
符合 HIPAA/GDPR 等合規要求
缺點:

需自行維護基礎設施
網路延遲可能較高
6.6 部署建議矩陣
場景	建議部署方案	原因
個人/小團隊測試	本地 or GCP Cloud Run	成本低、部署快
企業 POC (10-50 用戶)	AWS ECS Fargate	易管理、自動擴展
生產環境 (100+ 用戶)	AWS/GCP/Azure Kubernetes	高可用性、可觀測性
高度監管環境	混合部署 (內部 VM)	資料主權、合規性
無固定流量	GCP Cloud Run	按需計費、零閒置成本
7. 基礎設施即程式碼 (IaC) 與整合
7.1 Terraform 範例 (AWS ECS Fargate)
hcl

Copy
# main.tf
terraform {
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
resource "aws_vpc" "fda_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "fda-vpc"
  }
}

# Subnets (公有 × 2)
resource "aws_subnet" "public_subnet_a" {
  vpc_id                  = aws_vpc.fda_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "public_subnet_b" {
  vpc_id                  = aws_vpc.fda_vpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "${var.aws_region}b"
  map_public_ip_on_launch = true
}

# Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.fda_vpc.id
}

# Route Table
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.fda_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

resource "aws_route_table_association" "public_rta_a" {
  subnet_id      = aws_subnet.public_subnet_a.id
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "public_rta_b" {
  subnet_id      = aws_subnet.public_subnet_b.id
  route_table_id = aws_route_table.public_rt.id
}

# Security Group
resource "aws_security_group" "ecs_sg" {
  vpc_id = aws_vpc.fda_vpc.id
  
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
resource "aws_ecs_cluster" "fda_cluster" {
  name = "fda-cluster"
}

# Task Definition
resource "aws_ecs_task_definition" "fda_task" {
  family                   = "fda-studio-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "1024"
  memory                   = "2048"
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  
  container_definitions = jsonencode([{
    name  = "fda-studio"
    image = var.ecr_image_uri
    portMappings = [{
      containerPort = 8501
      protocol      = "tcp"
    }]
    secrets = [
      { name = "GEMINI_API_KEY", valueFrom = aws_secretsmanager_secret.gemini.arn },
      { name = "OPENAI_API_KEY", valueFrom = aws_secretsmanager_secret.openai.arn }
    ]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = "/ecs/fda-studio"
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "ecs"
      }
    }
  }])
}

# ECS Service
resource "aws_ecs_service" "fda_service" {
  name            = "fda-studio-service"
  cluster         = aws_ecs_cluster.fda_cluster.id
  task_definition = aws_ecs_task_definition.fda_task.arn
  desired_count   = 2
  launch_type     = "FARGATE"
  
  network_configuration {
    subnets          = [aws_subnet.public_subnet_a.id, aws_subnet.public_subnet_b.id]
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = true
  }
  
  load_balancer {
    target_group_arn = aws_lb_target_group.fda_tg.arn
    container_name   = "fda-studio"
    container_port   = 8501
  }
}

# Application Load Balancer
resource "aws_lb" "fda_alb" {
  name               = "fda-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.ecs_sg.id]
  subnets            = [aws_subnet.public_subnet_a.id, aws_subnet.public_subnet_b.id]
}

resource "aws_lb_target_group" "fda_tg" {
  name        = "fda-tg"
  port        = 8501
  protocol    = "HTTP"
  vpc_id      = aws_vpc.fda_vpc.id
  target_type = "ip"
  
  health_check {
    path                = "/_stcore/health"
    interval            = 30
    timeout             = 10
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }
}

resource "aws_lb_listener" "fda_listener" {
  load_balancer_arn = aws_lb.fda_alb.arn
  port              = "80"
  protocol          = "HTTP"
  
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.fda_tg.arn
  }
}

# IAM Role for ECS Execution
resource "aws_iam_role" "ecs_execution_role" {
  name = "fda-ecs-execution-role"
  
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

# Secrets Manager
resource "aws_secretsmanager_secret" "gemini" {
  name = "fda/gemini-api-key"
}

resource "aws_secretsmanager_secret" "openai" {
  name = "fda/openai-api-key"
}

# 輸出
output "alb_dns_name" {
  value = aws_lb.fda_alb.dns_name
}
部署指令:

bash

Copy
terraform init
terraform plan -var="aws_region=us-east-1" -var="ecr_image_uri=xxx"
terraform apply
7.2 Kubernetes Deployment YAML
yaml

Copy
# k8s-deployment.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: fda-studio

---
apiVersion: v1
kind: Secret
metadata:
  name: ai-api-keys
  namespace: fda-studio
type: Opaque
data:
  gemini-key: <BASE64_ENCODED>
  openai-key: <BASE64_ENCODED>
  anthropic-key: <BASE64_ENCODED>
  xai-key: <BASE64_ENCODED>

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: agents-config
  namespace: fda-studio
data:
  agents.yaml: |
    agents:
      - id: "initial_review"
        name: "Initial Reviewer"
        provider: "gemini"
        model: "gemini-2.5-flash"
        max_tokens: 4000
        temperature: 0.2
        system_prompt: "..."

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fda-studio-deployment
  namespace: fda-studio
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fda-studio
  template:
    metadata:
      labels:
        app: fda-studio
    spec:
      containers:
      - name: fda-studio
        image: gcr.io/PROJECT_ID/fda-review-studio:v2
        ports:
        - containerPort: 8501
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
        readinessProbe:
          httpGet:
            path: /_stcore/health
            port: 8501
          initialDelaySeconds: 10
          periodSeconds: 5
      volumes:
      - name: config-volume
        configMap:
          name: agents-config

---
apiVersion: v1
kind: Service
metadata:
  name: fda-studio-service
  namespace: fda-studio
spec:
  type: LoadBalancer
  selector:
    app: fda-studio
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8501

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: fda-studio-hpa
  namespace: fda-studio
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fda-studio-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
部署指令:

bash

Copy
kubectl apply -f k8s-deployment.yaml
kubectl get svc -n fda-studio  # 取得 Load Balancer IP
7.3 CI/CD 整合 (GitHub Actions)
yaml

Copy
# .github/workflows/deploy.yml
name: Build and Deploy

on:
  push:
    branches: [main]

env:
  GCP_PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
  GCP_REGION: us-central1
  SERVICE_NAME: fda-studio

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
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
          --set-secrets GEMINI_API_KEY=gemini-key:latest,OPENAI_API_KEY=openai-key:latest
    
    - name: Run integration tests
      run: |
        SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $GCP_REGION --format 'value(status.url)')
        curl -f $SERVICE_URL/_stcore/health || exit 1
8. 安全性考量
8.1 威脅模型 (STRIDE)
威脅類型	潛在攻擊	緩解措施
Spoofing (身份偽裝)	未授權使用者冒充合法審查員	實施 OAuth 2.0 / SAML SSO,整合企業 AD
Tampering (資料竄改)	惡意修改代理輸出或配置檔	agents.yaml 檔案權限限制為唯讀,輸出加密儲存
Repudiation (否認性)	使用者否認執行過某審查操作	完整審計日誌 (包含使用者 ID、時間戳、操作內容)
Information Disclosure (資訊洩漏)	API 金鑰外洩、敏感案例資料洩漏	環境變數 + Secrets Manager,傳輸層 TLS 1.3
Denial of Service (阻斷服務)	惡意大量請求耗盡 Mana/資源	Rate limiting (per-user),Auto-scaling
Elevation of Privilege (權限提升)	一般使用者取得管理員權限	RBAC,最小權限原則
8.2 API 金鑰管理最佳實踐
8.2.1 環境變數 (開發/測試)
bash

Copy
# .env (絕不提交至 Git)
GEMINI_API_KEY=AIzaSy...
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-api03-...
XAI_API_KEY=xai-...
Git 保護:

bash

Copy
# .gitignore
.env
*.env
secrets/
8.2.2 雲端 Secrets Manager (生產環境)
AWS Secrets Manager:

bash

Copy
aws secretsmanager create-secret \
  --name fda/gemini-api-key \
  --secret-string "AIzaSy..."

# ECS Task Definition 引用
"secrets": [
  {
    "name": "GEMINI_API_KEY",
    "valueFrom": "arn:aws:secretsmanager:us-east-1:xxx:secret:fda/gemini-api-key"
  }
]
GCP Secret Manager:

bash

Copy
echo -n "AIzaSy..." | gcloud secrets create gemini-key --data-file=-

# Cloud Run 部署時引用
gcloud run deploy fda-studio \
  --set-secrets GEMINI_API_KEY=gemini-key:latest
Azure Key Vault:

bash

Copy
az keyvault secret set \
  --vault-name fda-keyvault \
  --name gemini-api-key \
  --value "AIzaSy..."

# App Service 引用
az webapp config appsettings set \
  --name fda-studio \
  --settings GEMINI_API_KEY=@Microsoft.KeyVault(SecretUri=https://fda-keyvault.vault.azure.net/secrets/gemini-api-key/)
8.2.3 金鑰輪替策略
輪替週期: 每 90 天
自動化: 使用 AWS Secrets Manager Rotation Lambda
多版本: 保留前一版本金鑰 24 小時,確保無服務中斷
8.3 資料隱私保護
8.3.1 PII (個人身份資訊) 處理
匿名化: 所有案例描述在發送至 AI 前,自動替換患者姓名、醫療記錄號碼等 PII
python

Copy
import re
def anonymize_text(text):
    text = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[PATIENT_NAME]', text)
    text = re.sub(r'\b\d{6,10}\b', '[MRN]', text)
    return text
資料留存: 不儲存任何案例資料於後端,僅保存於使用者瀏覽器 Session (Streamlit session_state)
合規性: 符合 HIPAA Privacy Rule (若處理美國健康資料)
8.3.2 傳輸層安全
TLS 1.3: 所有對外通訊 (瀏覽器 ↔ 伺服器、伺服器 ↔ AI APIs) 強制使用 TLS 1.3
憑證管理: 使用 Let's Encrypt 自動更新 SSL 憑證 (Certbot)
HSTS: 啟用 HTTP Strict Transport Security header
nginx

Copy
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
8.4 應用程式安全
8.4.1 輸入驗證
python

Copy
def validate_input(text: str) -> bool:
    if len(text) > 100000:  # 防止超大輸入導致 DoS
        raise ValueError("輸入文字超過 100,000 字元限制")
    if re.search(r'<script|javascript:|onerror=', text, re.IGNORECASE):
        raise ValueError("偵測到潛在 XSS 攻擊向量")
    return True
8.4.2 輸出編碼
Markdown 渲染: Streamlit 預設會 sanitize HTML,但需防範 Markdown injection
日誌輸出: 避免記錄未編碼的使用者輸入,防止 Log Injection
8.4.3 依賴套件掃描
bash

Copy
# 使用 pip-audit 掃描已知漏洞
pip install pip-audit
pip-audit

# 使用 Safety 檢查
safety check --file requirements.txt
自動化: 於 CI/CD pipeline 整合 Snyk 或 Dependabot

8.5 存取控制
8.5.1 驗證機制 (Authentication)
選項 1: OAuth 2.0 (Google Workspace)

python

Copy
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(
    names=['審查員A', '審查員B'],
    usernames=['reviewer_a', 'reviewer_b'],
    passwords=[...],  # 雜湊後密碼
    cookie_name='fda_studio_auth',
    key='random_signature_key',
    cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    st.write(f'歡迎 {name}')
    # 主應用程式邏輯
elif authentication_status == False:
    st.error('使用者名稱或密碼錯誤')
選項 2: SAML SSO (企業級)

使用 AWS Cognito / Azure AD / Okta 作為 Identity Provider
Streamlit 前方部署 Nginx + auth_request 模組,轉發至 IDP
8.5.2 授權機制 (Authorization)
角色定義:

角色	權限
Reviewer (審查員)	執行 Pipeline、Note Keeper,查看 Dashboard
Admin (管理員)	所有審查員權限 + 編輯 agents.yaml、查看所有使用者日誌
Auditor (稽核員)	唯讀存取 Dashboard 與執行日誌
實作範例:

python

Copy
if st.session_state.user_role == 'admin':
    st.sidebar.button("編輯代理配置")
elif st.session_state.user_role == 'auditor':
    st.info("您的角色僅可查看資料,無法執行審查")
8.6 審計日誌
8.6.1 日誌欄位
欄位	說明	範例
timestamp	ISO 8601 時間戳	2024-01-15T14:23
.123Z
user_id	使用者唯一識別碼	reviewer_a@fda.gov
action	操作類型	pipeline_run / note_transform / config_edit
agent_id	涉及代理 ID	initial_review
provider	AI 提供商	gemini
model	模型名稱	gemini-2.5-flash
input_hash	輸入文字 SHA-256	a3b2c1...
output_hash	輸出文字 SHA-256	d4e5f6...
status	執行狀態	success / error
error_msg	錯誤訊息 (若失敗)	API key invalid
duration_ms	執行時長 (毫秒)	12345
8.6.2 日誌儲存
本地檔案 (開發):

python

Copy
import logging

logging.basicConfig(
    filename='fda_audit.log',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

logging.info(f"user={user_id} | action=pipeline_run | agent={agent.id} | status=success")
雲端日誌服務 (生產):

AWS CloudWatch Logs: ECS Task 自動轉發至 /ecs/fda-studio log group
GCP Cloud Logging: Cloud Run 自動整合
Azure Monitor Logs: App Service 診斷設定啟用
SIEM 整合: 透過 Fluentd/Logstash 轉發至 Splunk/ELK

8.7 安全開發生命週期 (SDL)
mermaid

Copy
graph LR
    A[需求階段] --> B[設計階段]
    B --> C[開發階段]
    C --> D[測試階段]
    D --> E[部署階段]
    E --> F[維運階段]
    
    A -->|威脅模型| TM[STRIDE 分析]
    B -->|安全架構審查| SAR[Security Architecture Review]
    C -->|靜態程式碼掃描| SAST[Bandit / SonarQube]
    D -->|滲透測試| PT[OWASP ZAP]
    E -->|配置掃描| CS[Trivy / Checkov]
    F -->|漏洞監控| VM[Snyk / Dependabot]
9. 驗證計畫
9.1 驗證目標
依據 FDA 21 CFR Part 11 (電子記錄/電子簽章) 與 ISO 13485 (醫療器材品質管理系統) 精神,本驗證計畫確保系統:

功能符合 SRS 規格
輸出結果可重現
資料完整性與可追溯性
安全性控制有效運作
9.2 驗證層級

Copy
V 模型:
  需求 (SRS) ←→ 驗收測試 (UAT)
      ↓              ↑
    設計 ←→ 系統整合測試 (SIT)
      ↓              ↑
   編碼 ←→ 單元測試 (UT)
9.3 單元測試 (Unit Testing)
9.3.1 測試框架
bash

Copy
pip install pytest pytest-cov
9.3.2 測試案例範例
python

Copy
# tests/test_agent_execution.py
import pytest
from unittest.mock import patch, MagicMock
from app import run_agent, AgentConfig

def test_run_agent_gemini_success():
    """測試 Gemini 代理正常執行"""
    agent = AgentConfig(
        id="test_agent",
        name="Test Agent",
        description="",
        model="gemini-2.5-flash",
        max_tokens=1000,
        temperature=0.2,
        system_prompt="You are a test assistant.",
        provider="gemini"
    )
    
    with patch('app.call_gemini', return_value="Test output"):
        result = run_agent(agent, "Test input")
    
    assert result == "Test output"
    assert agent.provider == "gemini"

def test_run_agent_api_key_missing():
    """測試缺少 API 金鑰時拋出異常"""
    agent = AgentConfig(
        id="test_agent",
        name="Test Agent",
        description="",
        model="gpt-4o-mini",
        max_tokens=1000,
        temperature=0.2,
        system_prompt="",
        provider="openai"
    )
    
    with patch('app.get_api_key', return_value=None):
        with pytest.raises(RuntimeError, match="No API key configured"):
            run_agent(agent, "Test input")

def test_anonymize_pii():
    """測試 PII 匿名化功能"""
    from app import anonymize_text  # 假設已實作
    
    input_text = "Patient John Doe with MRN 123456789 underwent surgery."
    expected = "Patient [PATIENT_NAME] with MRN [MRN] underwent surgery."
    
    result = anonymize_text(input_text)
    assert result == expected
9.3.3 覆蓋率要求
目標: 程式碼覆蓋率 ≥80%
執行:
bash

Copy
pytest --cov=app --cov-report=html
open htmlcov/index.html
9.4 整合測試 (Integration Testing)
9.4.1 測試情境
測試案例 ID	情境描述	預期結果	優先級
IT-001	完整 3 代理流程執行	所有代理成功執行,輸出連續傳遞	P0
IT-002	代理 2 失敗時流程中斷	Pipeline 停止,錯誤訊息記錄	P0
IT-003	編輯代理 1 輸出後重新執行代理 2	代理 2 使用新輸入,輸出更新	P0
IT-004	Note Keeper Markdown 轉換	非結構化文字轉為標準 Markdown	P1
IT-005	Dashboard 指標更新	執行後 total_runs +1, provider_calls 正確增量	P2
9.4.2 測試腳本範例 (IT-001)
python

Copy
# tests/test_integration.py
import streamlit as st
from app import init_session_state, run_agent, AgentConfig

def test_full_pipeline_execution():
    """測試完整 3 代理流程"""
    init_session_state()
    
    # 模擬 3 個代理
    agents = [
        AgentConfig("a1", "Agent 1", "", "gemini-2.5-flash", 1000, 0.2, "Prompt 1", "gemini"),
        AgentConfig("a2", "Agent 2", "", "gpt-4o-mini", 1000, 0.3, "Prompt 2", "openai"),
        AgentConfig("a3", "Agent 3", "", "claude-3-5-haiku-20241022", 1000, 0.2, "Prompt 3", "anthropic"),
    ]
    
    # 模擬 API 呼叫
    with patch('app.call_gemini', return_value="A1 Output"), \
         patch('app.call_openai', return_value="A2 Output"), \
         patch('app.call_anthropic', return_value="A3 Output"):
        
        input_text = "Initial case description"
        
        # 執行 Agent 1
        result1 = run_agent(agents[0], input_text)
        assert result1 == "A1 Output"
        
        # 執行 Agent 2 (使用 A1 輸出)
        result2 = run_agent(agents[1], result1)
        assert result2 == "A2 Output"
        
        # 執行 Agent 3 (使用 A2 輸出)
        result3 = run_agent(agents[2], result2)
        assert result3 == "A3 Output"
    
    # 驗證指標
    assert st.session_state.metrics["total_runs"] == 3
    assert st.session_state.metrics["provider_calls"]["gemini"] == 1
    assert st.session_state.metrics["provider_calls"]["openai"] == 1
    assert st.session_state.metrics["provider_calls"]["anthropic"] == 1
9.5 系統測試 (System Testing)
9.5.1 功能性測試
測試案例 ID	需求 ID	測試步驟	預期結果
ST-FR-001	FR-001	1. 載入 agents.yaml<br>2. 點擊「Run Full Pipeline」	所有代理依序執行,狀態燈顯示「成功」
ST-FR-002	FR-002	1. 執行代理 1<br>2. 編輯輸出<br>3. 點擊「Run only step 2」	代理 2 使用編輯後輸入,輸出更新
ST-FR-003	FR-003	1. 於代理 1 配置選擇 provider=OpenAI<br>2. 執行	成功呼叫 OpenAI API,返回有效輸出
ST-FR-004	FR-004	1. 於 Note Keeper 輸入非結構化文字<br>2. 選擇「實體提取」<br>3. 執行	輸出包含 20 個實體的 Markdown 表格
Max tokens to sample reached
