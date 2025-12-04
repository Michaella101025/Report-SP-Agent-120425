Hi please keep all original features and make this system more professinal by create a Awesome UI and optimize the usability.
醫療器材供應鏈追蹤系統 v2.0 技術規格書
(BioChain Analyst Pro Technical Specification)
版本: 2.0
日期: 2023-10-27
語言: 繁體中文 (Traditional Chinese)

專案概述 (Project Overview) 本系統為一款專為 TFDA (食品藥物管理署) 監管需求設計的前端單頁應用程式 (SPA)。主要功能為追蹤醫療器材（特別是乳房植入物）的供應鏈流向。系統結合了多代理人 (Multi-Agent) AI 分析功能、動態網路拓撲視覺化、以及高度可客製化的 UI 主題系統。
核心目標
視覺化追蹤: 透過 D3.js 網路圖呈現經銷商與醫院之間的器材流向與數量。
AI 智能稽核: 利用 Google Gemini API 進行數據異常偵測、法規合規性檢查及物流路徑分析。
使用者體驗: 提供 20 種花卉主題、深色模式及多語言介面。
2. 系統架構 (System Architecture)
本系統採用 Client-Side Rendering (CSR) 架構，所有數據處理、視覺化運算及 AI API 呼叫皆在使用者瀏覽器端執行，確保數據隱私（除非使用者主動執行 AI 分析）並降低伺服器負擔。

2.1 技術堆疊 (Tech Stack)
類別	技術/工具	用途
核心框架	React 19	UI 建構與狀態管理
語言	TypeScript	強型別程式開發，確保代碼品質
樣式系統	Tailwind CSS	Utility-first CSS 框架，支援深色模式與響應式設計
視覺化引擎	D3.js	複雜的供應鏈網絡拓撲圖 (Network Graph)
圖表庫	Recharts	時間序列趨勢圖 (Line Charts)
AI 整合	Google GenAI SDK	串接 Gemini 2.5 Flash 模型進行推論
圖標庫	Lucide React	現代化 UI 圖標
模組載入	ES Modules / Import Map	瀏覽器原生模組載入 (無須複雜 Bundler 即可運行)
2.2 架構圖 (High-Level Architecture)
code
Mermaid
graph TD
User[使用者] -->|上傳 CSV / 互動| UI[React 前端介面]

subgraph Browser_Runtime [瀏覽器執行環境]
    UI -->|狀態管理| State[React State (Context/Hooks)]
    State -->|數據解析| Parser[CSV Parser]
    State -->|渲染指令| Vis[D3 & Recharts 視覺化層]
    State -->|主題切換| Theme[Jackslot 主題引擎]
    
    UI -->|觸發分析| AgentMgr[AI Agent 管理器]
end

subgraph External_Services [外部服務]
    AgentMgr -->|API 請求 (Prompt + Data)| Gemini[Google Gemini API]
    AgentMgr -->|API 請求 (預留)| OpenAI[OpenAI API]
end

Gemini -->|分析結果| AgentMgr
Vis -->|圖表呈現| User
3. 軟體需求規格 (SRS)
3.1 功能需求 (Functional Requirements)
A. 資料管理模組
檔案上傳: 支援 CSV 格式上傳。
必要欄位: trade_date, src_name, dst_name, device_name, quantity。
資料預覽與編輯: 提供表格介面 (Table View) 供使用者直接修改數據並儲存。
資料下載: 將當前（包含修改後）的數據導出為 CSV。
系統預設數據: 提供 Mock Dataset 供演示使用。
B. 視覺化分析模組
供應鏈網路圖 (Network Graph):
節點 (Node): 代表供應商、醫院或診所。
連線 (Link): 代表物流流向，線條粗細代表交易量。
聚合顯示: 相同起訖點的交易需合併計算總量並顯示於連線上。
篩選器: 支援依據「最小數量」與「產品名稱」過濾網路圖。
標籤控制: 可切換顯示/隱藏連線上的數值標籤。
趨勢圖 (Time Trends): 顯示特定時間段內的總出貨量變化。
C. AI 代理人模組 (AI Agents)
多代理人設定: 預設四種角色 (Auditor, Logistics, Legal, Analyst)。
配置介面:
輸入 API Key (Gemini/OpenAI)。
選擇模型 (Gemini 2.5 Flash, GPT-4o 等)。
設定 Max Tokens 與 Prompt Template。
執行流程: 依序執行啟用的 Agent，並在 UI 上即時顯示思考狀態與分析結果。
D. 使用者介面與體驗 (UI/UX)
側邊欄控制: 可收折/展開的側邊欄 (Sidebar)，包含所有設定項。
主題系統: "Jackslot" 拉霸機介面，隨機或手動選取 20 種花卉主題（改變配色、漸層、Emoji）。
深色模式: 支援一鍵切換 Light/Dark Mode。
多語言: 支援 英文 (EN) 與 繁體中文 (zh-TW) 切換。
3.2 非功能需求 (Non-Functional Requirements)
效能: 處理 10,000 筆以內的 CSV 數據時，前端渲染延遲不應超過 2 秒。
相容性: 支援 Chrome, Edge, Safari, Firefox 最新版本。
安全性: API Key 僅存於使用者瀏覽器記憶體中，不傳送至任何後端資料庫。
4. 資料結構定義 (Data Structures)
4.1 追蹤記錄 (TrackingRecord)
code
TypeScript
interface TrackingRecord {
id: string;           // 唯一識別碼
trade_date: string;   // 交易日期 (YYYY-MM-DD)
src_name: string;     // 來源端名稱
dst_name: string;     // 目的端名稱
device_name: string;  // 醫材名稱
quantity: number;     // 數量
}
4.2 代理人設定 (AgentConfig)
code
TypeScript
interface AgentConfig {
id: string;
name: string;        // 代理人名稱
role: string;        // 角色 (如: Auditor)
description: string; // 職責描述
enabled: boolean;    // 是否啟用
}
5. 環境設定 (Environment Settings)
本專案目前的實作方式採用 瀏覽器原生模組 (ES Modules) 搭配 CDN 載入依賴，這意味著它可以在沒有 Node.js 建置步驟的情況下運行（適合快速原型或簡單部署）。

5.1 開發環境需求
雖然可以直接編輯文件，但建議使用以下工具以獲得最佳體驗：

IDE: VS Code (安裝 ESLint, Prettier, Tailwind CSS IntelliSense)。
Runtime: 任意靜態 Web Server (如 Python http.server, VS Code Live Server extension, 或 serve npm 套件)。
API Key: 需準備 Google AI Studio (Gemini) 的 API Key。
5.2 依賴套件 (透過 Import Map 定義)
無需 npm install，依賴直接由瀏覽器從 CDN 下載：

react, react-dom: v19.2.0
@google/genai: v1.30.0
d3: v7.9.0
recharts: v3.5.1
lucide-react: v0.555.0
6. 部署說明 (Deployment Instructions)
由於本應用程式為純靜態網頁 (Static Web App)，部署非常簡單。

方法 A: 靜態 Hosting 服務 (推薦)
適用於 Vercel, Netlify, GitHub Pages, Cloudflare Pages。

將 index.html, index.tsx, App.tsx, types.ts, constants.ts 以及 components/, services/ 資料夾上傳至 Git 儲存庫。
在 Hosting 平台上連接儲存庫。
設定 Build Command 為空 (或 echo "No build needed")。
設定 Output Directory 為根目錄 (.)。
部署完成。
方法 B: 本地端運行 (Localhost)
若要在本地電腦上運行：

確保所有檔案在同一資料夾結構下。
開啟終端機 (Terminal)。
若有安裝 Python，執行：
code
Bash
python3 -m http.server 8000
瀏覽器打開 http://localhost:8000。
方法 C: 企業內網部署 (Docker Nginx)
若需部署於內部伺服器：

建立 Dockerfile:
code
Dockerfile
FROM nginx:alpine
COPY . /usr/share/nginx/html

確保 Nginx 設定支援 SPA 或正確的 MIME Types
建置並執行 Container。
7. 限制與注意事項 (Limitations & Notes

以下為在「完全保留原本功能」前提下，針對 UI/UX、AI 代理人與部署架構進行專業升級的 v2.1 規格提案，並整合你先前要求的 1–5 項新功能（WOW UI、Jackslot 花卉主題、API Key 管理、多模型、多代理人串接、Hugging Face Space + Streamlit 部署）。

醫療器材供應鏈追蹤系統 v2.1
BioChain Analyst Pro – WOW UI & HF Space Edition 技術規格書

版本: 2.1
日期: 2025-XX-XX
語言: 繁體中文 (Traditional Chinese) / English (雙語 UI 支援)

0. v2.1 升級重點總覽
在 完全保留 v2.0 功能 的前提下，v2.1 主要新增與優化：

WOW UI + 主題系統重構

Light / Dark 主題切換。
中 / 英雙語 UI（繁體中文 / English）。
20 種花卉主題（色彩與裝飾），透過「Jackslot 拉霸機」介面選擇或隨機。
專業化布局（資料 / 視覺化 / AI 分析 / 設定清楚分區）。
WOW 狀態指示與互動式儀表板

全域系統狀態列：API 連線、資料載入、AI 任務進度。
多代理人 AI 狀態指示（Idle / Preparing / Running / Completed / Error）。
儀表板：關鍵指標、趨勢卡片、異常警示、互動式篩選。
API Key 管理與安全機制

優先讀取環境變數（Hugging Face Secrets）。
若環境無設定，前端顯示 遮蔽式輸入框，讓使用者輸入（僅保存在瀏覽器 / session 中）。
若來自環境變數，UI 不顯示 key 內容也不允許編輯，只顯示「使用系統管理的金鑰」。
AI 代理人進階控制與多模型支援

可設定：
Prompt（可即時修改）。
max_tokens（預設 12000，上限依模型）。
模型選擇：
OpenAI: gpt-4o-mini, gpt-4.1-mini
Google: gemini-2.5-flash, gemini-2.5-flash-lite
Anthropic: （如 claude-3.5-sonnet, claude-3.5-haiku 等）
Grok: grok-4-fast-reasoning, grok-3-mini
代理人逐一執行（可選擇執行順序 / 單獨重跑）。
代理人輸出可編輯，並可選擇 Text / Markdown 檢視模式，再作為下一個代理人輸入。
部署與技術棧調整

部署平台：Hugging Face Spaces。
主框架：Streamlit（Python）為主控 UI + 狀態管理。
AI 後端：Gemini API、OpenAI API、Anthropic API、Grok API。
多代理設定：agents.yaml 外部化設定（角色 / 默認 prompt / 建議模型）。
前端互動式圖形：透過 Streamlit 自訂 Component 包裝 React + D3.js + Recharts。
1. 專案概述 (更新版)
1.1 目標保持不變
視覺化追蹤：使用 D3.js 呈現醫材供應鏈拓樸。
AI 智能稽核：多代理 AI，進行異常偵測 / 合規檢查 / 物流分析。
優質使用者體驗：
20 種花卉主題 + Light/Dark 模式。
EN / zh-TW 雙語。
專業級儀表板與清楚狀態回饋。
1.2 v2.1 新增 UX 流程概觀
首次開啟：

顯示 導覽對話框 (Onboarding)：
第一步：選擇語言（EN / zh-TW）。
第二步：選擇外觀（Light / Dark）。
第三步：透過 Jackslot 選一個花卉主題。
左側「控制側欄」：

分區：
Data（資料檔上傳 / 預覽 / 下載）
Visualization（圖形篩選 / 顯示控制）
AI Agents（代理人設定與執行）
Settings（主題 / 語言 / API Keys）
主工作區分為三個主要區段：

上方：WOW 儀表板（KPI / 異常摘要 / 最近分析結果）。
中間左：供應鏈網路圖 + 篩選條件。
中間右：時間序列趨勢圖 + 分析卡片。
下方：AI 代理人區（多 Panel，逐一檢視 / 編輯 / 串接輸出）。
2. 系統架構 (更新為 HF Space + Streamlit + React Component)
2.1 技術堆疊 (Tech Stack v2.1)
類別	技術 / 工具	用途
Host 平台	Hugging Face Spaces	雲端部署與公開展示
後端 / UI 驅動	Streamlit (Python 3.11+)	UI layout、狀態管理、API 呼叫
AI SDK	- openai / OpenAI client <br> - Google GenAI (google.generativeai 或 HTTP) <br> - Anthropic Python SDK <br> - Grok API (x.ai HTTP)	串接各家大模型
類型設定	pydantic models	請求/回應資料結構、驗證
多代理設定	agents.yaml	定義代理人角色、預設 prompt、模型建議
自訂前端元件	React + TypeScript + D3.js + Recharts + Tailwind CSS（透過 streamlit-component-lib）	供應鏈 Network Graph、時間序列圖、Jackslot 與主題引擎
Icon	Lucide React	現代化 UI icon（嵌入於自訂元件中）
說明：

v2.0 原本「純前端 React + ES Modules」的概念，在 v2.1 轉為 Streamlit + 自訂 React Component。
所有 功能需求 保持一致，僅改變執行環境與整體 UI 風格。
2.2 高階架構圖 (重構版)
graph TD
    User[使用者瀏覽器] -->|瀏覽器互動| StreamlitUI[Streamlit App]

    subgraph HF_Space [Hugging Face Space / Python Runtime]
        StreamlitUI -->|Session State 更新| State[Streamlit Session State]

        StreamlitUI -->|前端交互| ReactComp[Custom React Components]

        subgraph Frontend_Components [React + D3 + Recharts Components]
            ReactComp --> NetworkGraph[D3 Network Graph]
            ReactComp --> TrendCharts[Recharts Time Series]
            ReactComp --> ThemeJackslot[Jackslot 主題引擎]
        end

        State -->|執行指令 + 資料| AgentMgr[AI Agent 管理器]

        AgentMgr -->|API 請求| OpenAI[OpenAI API]
        AgentMgr -->|API 請求| Gemini[Google Gemini API]
        AgentMgr -->|API 請求| Anthropic[Anthropic API]
        AgentMgr -->|API 請求| Grok[Grok API]

        AgentMgr -->|分析結果| State
        State -->|結果渲染| StreamlitUI
    end
3. 功能需求 (Functional Requirements v2.1)
A. 資料管理模組（保持原功能，UX 優化）
維持 v2.0 所有功能，並在 Streamlit 中以更專業的方式呈現。

檔案上傳

st.file_uploader 支援 CSV。
顯示檔名、筆數、欄位檢查（必要欄位：trade_date, src_name, dst_name, device_name, quantity）。
資料預覽與編輯

使用 st.data_editor 或自訂編輯表格：
支援逐列 / 儲存格編輯。
顯示整潔表頭，對應中英翻譯（如「交易日期 (trade_date)」）。
提供「恢復原始資料」按鈕（回到上傳檔或預設 mock dataset）。
資料下載

st.download_button 導出目前資料（含修改結果）為 CSV。
系統預設數據

無上傳檔案時，自動載入 mock dataset，方便 demo。
B. 視覺化分析模組（Network Graph + 時間序列）
B.1 供應鏈網路圖 (Network Graph)
前端：React 自訂 Component（D3.js 為核心）。

功能保持 & 強化：

Node：供應商 / 醫院 / 診所，各用不同顏色 / icon 表示。
Link：線粗表交易數量，並顯示總量（聚合相同起訖）。
滑鼠 hover：
顯示 tooltip（節點類型、累計輸入 / 輸出量、設備種類數）。
點擊節點：
在右側呈現該節點詳細摘要卡片（Top 5 供應設備、最近交易日期等）。
可縮放 / 拖曳 / 聚合。
篩選與控制（由 Streamlit 控制側欄提供）：

最小交易數量 (slider)。
指定醫材名稱 / 關鍵字（multi-select）。
是否顯示連線數量標籤（checkbox）。
著色模式：
按節點類型
按流量大小
按異常風險（若 AI 稽核後有結果）
B.2 趨勢圖 (Time Trends)
使用 Recharts（折線圖 / 面積圖）。
顯示：
總出貨量 vs 時間。
可篩選特定醫材 / 節點。
提供 tooltip / Zoom / 區間選擇。
C. AI 代理人模組 (AI Agents 進階版)
C.1 代理人角色（保留 + 檔案化）
預設四種角色，仍然存在，從 agents.yaml 讀取：

Auditor（稽核員）
Logistics（物流分析）
Legal（法規合規）
Analyst（數據分析）
agents.yaml 範例結構：

agents:
  - id: auditor
    name: 稽核代理人
    role: Auditor
    description: 負責偵測異常交易與可能風險節點。
    default_model: gemini-2.5-flash
    default_max_tokens: 12000
    default_prompt: |
      你是一位醫療器材供應鏈稽核專家，請根據以下 CSV 資料...
  - id: logistics
    name: 物流代理人
    role: Logistics
    ...
C.2 模型與參數選擇（新增）
在「AI Agents」區，每個 Agent 以 Card 呈現，包含：

Agent 基本資訊（名稱、角色、描述）。
啟用開關 (enabled toggle)。
模型下拉選單（模型清單依供應商分組）：
OpenAI:
gpt-4o-mini
gpt-4.1-mini
Google:
gemini-2.5-flash
gemini-2.5-flash-lite
Anthropic:
claude-3.5-sonnet / claude-3.5-haiku（實際名稱依採用）
Grok:
grok-4-fast-reasoning
grok-3-mini
max_tokens 數值輸入（預設 12000，可限制範圍）。
溫度 / top_p 等（可選，視需求）。
C.3 Prompt 管理與輸出編輯（重要新功能）
每個 Agent Card 下方有「Prompt 編輯區」：

可先顯示預設 prompt（來自 agents.yaml）。
使用 st.text_area 提供編輯。
顯示字數統計。
輸出區（Results Panel）：

Tab 1: Markdown View
Tab 2: Text / Raw JSON View
可以內嵌 輕量文字編輯器：
可修改 AI 回覆內容。
支援 Markdown 語法高亮 / 預覽。
串接到下一個代理人：

每個 Agent 結果區提供：
Button：「將本結果設為下一代理人輸入」
Dropdown：選擇要傳給哪個代理人（預設下一位）。
具體行為：
會把「編輯後的文字」寫入下一個 Agent 的 context / additional_input 欄位。
在下一 Agent Card 顯示「已接收來自 [Auditor] 的上游輸出」。
C.4 執行流程與狀態指示（WOW 狀態指標）
在「AI Agents」區域頂部，有執行控制：

「依序執行所有啟用的代理人」
「僅執行選取代理人」
「停止所有執行」（若支援中止）。
每個 Agent Card 上有 狀態徽章：

Idle（灰色）
Preparing（藍色，顯示「準備請求中」）
Calling API（黃色，顯示進度列 / spinner）
Completed（綠色）
Error（紅色，顯示錯誤訊息 tooltip）
Streamlit 內透過 st.status 或自訂狀態列，再搭配 React 動畫 icon，使：

當某 Agent 在跑時，儀表板上方顯示全域進度（已完成 N/4）。
若出錯，顯示特定 Agent 的錯誤位置與原因。
D. WOW 使用者介面與體驗 (UI/UX)
D.1 主題系統與 Jackslot 花卉樣式
核心要求：20 種花卉主題 + Jackslot 選擇機制

主題內容：

每個主題包含：
主色 / 副色 / 強調色（dark/light 各一組）。
對應花卉名稱（如 Sakura、Lotus、Tulip…）。
背景裝飾（花形狀 SVG / 紋理）。
搭配 Emoji（可選）顯示在標題或角落（例如 🌸）。
Jackslot 介面（在 Settings 或首頁 Onboarding 中）：

三軸「拉霸機」：
軸1：花卉名稱。
軸2：色調組合（Pastel / Vibrant / Deep）。
軸3：特效（柔光、玻璃擬態、純色）。
使用者可以：
按「Spin」隨機產生一種主題。
按「鎖定」其中部分軸（只變更未鎖定軸）。
使用「確認主題」按鈕套用至全系統。
Light / Dark Mode

UI 右上角快速切換（太陽 / 月亮 icon）。
每個花卉主題提供 Light / Dark 對應配色。
設定儲存於瀏覽器 localStorage（或 session cookie）中。
多語系 (EN / zh-TW)

使用 i18n 結構（例如 Python 端維護 locales/en.json, locales/zh-TW.json）。
UI 選擇語言後，所有標籤、按鈕、提示文字即時切換。
Agents 描述可同時維護兩語版本，或預設為繁體中文並可自訂。
D.2 儀表板（Dashboard）
上方「WOW 儀表板」區塊包含：

KPI 卡片（cards）：
總交易量（期間可選）。
節點數量（供應商 / 醫院 / 診所）。
異常交易數（來自最新一次 Auditor 分析）。
異常摘要列表：
最近 N 筆「高風險」路徑（若有）。
分析紀錄：
過去 N 次 AI 分析時間 / 執行代理 / 使用模型。
UI 設計風格：

玻璃擬態或卡片式設計，與花卉主題顏色相協調。
點擊 KPI 卡片可在下方視覺化區啟動對應篩選。
D.3 專業化 Layout
左側固定側欄（可收合）：
Logo + 系統名稱
Menu 分區：
Data & Filters
Visualization
AI Agents
Settings
右上角快速設定：
語言切換、主題模式、使用者提示（Help / About）。
底部訊息列：
API 狀態、最後更新時間、目前主題名稱。
E. API Key 管理與安全邏輯
E.1 行為規則
後端先嘗試從環境變數讀取：
OPENAI_API_KEY
GEMINI_API_KEY 或 GOOGLE_API_KEY
ANTHROPIC_API_KEY
GROK_API_KEY
若存在：
UI 中對應廠商區塊顯示：
「使用系統管理的 API Key」（icon: shield）
不顯示 key 字串，也不提供輸入框（只提供「狀態」文字）。
若不存在：
在 Settings → API Keys 頁面中顯示：
密碼型輸入框（type='password'）。
明確標註「僅存在於本次 session，不會儲存至伺服器」。
Streamlit session state 儲存使用者輸入，僅用於呼叫對應 API。
E.2 安全性補充
不在任何 log 中輸出 key。
於 HF Space 中設定環境變數時，建議改用 Secrets 機制，確保不可從前端讀出。
4. 資料結構 (延伸)
保留 v2.0 之 TrackingRecord 與 AgentConfig，並在 Python / Pydantic 中對應。

4.1 TrackingRecord (Python)
from pydantic import BaseModel

class TrackingRecord(BaseModel):
    id: str
    trade_date: str
    src_name: str
    dst_name: str
    device_name: str
    quantity: int
4.2 AgentConfig (Python 對應 agents.yaml)
class AgentConfig(BaseModel):
    id: str
    name: str
    role: str
    description: str
    enabled: bool = True
    default_model: str
    default_max_tokens: int = 12000
    default_prompt: str
5. 非功能需求 (更新後)
效能

10,000 筆 CSV：
Server 端：Pandas / 原生 Python 處理應在 1s 內完成基本聚合。
前端 Network Graph：D3 layout 時間控制在 1–2s 內。
Streamlit 頁面重新渲染時，透過 st.cache_data 或 memo 化減少重計算。
相容性

瀏覽器：Chrome, Edge, Safari, Firefox 最新版。
HF Space 後端：Python 3.11 + pip 套件（openai, google-generativeai, anthropic, requests 等）。
安全性

API Key 僅存在：
HF secrets（環境變數）或
Streamlit session（使用者輸入）。
不寫檔、不回傳給用戶端（除非本地端模式開發才可能）。
6. 部署說明 (Hugging Face Space + Streamlit)
檔案結構建議
.
├─ app.py                   # Streamlit 入口
├─ agents.yaml              # 多代理設定
├─ requirements.txt
├─ components/
│  ├─ network_graph/        # React + D3 元件
│  ├─ trend_charts/
│  └─ theme_jackslot/
├─ data/
│  └─ mock_dataset.csv
├─ locales/
│  ├─ en.json
│  └─ zh-TW.json
└─ utils/
   ├─ ai_clients.py
   ├─ data_loader.py
   ├─ visualization.py
   └─ i18n.py
Space 設定

sdk: streamlit
app_file: app.py
在 HF Space「Settings → Variables and secrets」設定 API Keys（若要由環境管理）。
執行順序

載入 agents.yaml。
初始化多語系資源。
檢查環境變數，更新 session_state API key 狀態。
呈現主 UI（Sidebar + 主頁面 + React components）。
7. WOW 狀態指標與可用性優化 (補充)
狀態列 (Status Bar)

顯示：
資料狀態：未載入 / Mock Data / 使用者檔案。
AI 狀態：Idle / Running (N agents)。
API：每個供應商的可用性（例如 ping 成功與否）。
錯誤回饋

若 AI 請求失敗：
在該 Agent Card 顯示紅色框 + 錯誤訊息。
儀表板也顯示紅色「X」標記，提示使用者可重試 / 更換模型。
引導提示 (Tooltips / Help)

針對供應鏈圖、AI Agents 區域提供 ? 圖示，點擊後顯示簡短教學。
8. 總結
所有 v2.0 功能（資料上傳/編輯/下載、供應鏈網路圖、趨勢圖、四大代理人稽核分析）全部保留。
v2.1 在不改變核心邏輯的前提下：
改採 Hugging Face Space + Streamlit 做為主 UI 與執行平台。
將前端視覺化與主題系統封裝為自訂 React Component。
新增 20 花卉主題 + Jackslot WOW UI、多模型選擇、串接式代理輸出編輯、安全的 API Key 管理。
提供更專業、清晰且可維運的技術架構。
20 個後續深化問題（用來微調設計與實作細節）
花卉主題部分，你是否有特定想要包含的花種或品牌（例如與醫療相關、或象徵「關懷、安全」的風格）？
Light / Dark 模式下，你對對比度的偏好為何（偏高對比以利長時間閱讀，或較柔和以提升美感）？
儀表板上的 KPI 卡片中，除了交易量、節點數、異常交易數，你還有沒有特別想追蹤的指標（例如：平均流通天數、特定加工/倉儲節點的集中度）？
供應鏈網路圖中，你是否需要額外分類節點類型（如：製造商 / 代理商 / 經銷商 / 醫院 / 診所），或現有供應商 vs 醫院即可？
異常偵測結果，你比較想以「列表」方式呈現（逐筆細項）還是「分群 / 熱度圖」方式（顯示高風險路徑群集）？
四個預設 AI 代理人 (Auditor, Logistics, Legal, Analyst) 之外，你是否需要預留自訂代理人 Slot（例如使用者可從 UI 新增第 5、6 個代理人）？
在代理人輸出可編輯的情境中，你是否需要「版本紀錄」功能（例如記錄 AI 原始輸出與使用者修改後版本，方便稽核）？
串接輸出到下一個代理人時，你希望是自動串接（執行順序固定）還是每次由使用者明確選擇要把結果傳給哪一位代理人？
模型選擇清單中，你是否希望預先定義「推薦組合」（例如：Auditor 預設用 Gemini、Legal 預設用 Anthropic），以簡化一般使用者的決策？
max_tokens 預設為 12000，你希望在 UI 中是否顯示對應模型的最大上限（例如阻止使用者輸入超出模型支援的值）？
多語系部分，你更希望：a) 使用者每次自己切換語言；或 b) 初次偵測瀏覽器語言後自動選擇，並記住偏好？
API Key 若由使用者輸入，你是否接受在 session 關閉後即完全遺失（最高安全），還是希望有選項儲存在瀏覽器 localStorage（較方便但安全性稍降）？
在錯誤處理方面，你偏好「詳細技術錯誤訊息」（方便除錯）還是「簡化使用者友善訊息 + 詳細錯誤寫入伺服器 log」？
對供應鏈資料量級的預期是什麼（例如：一般會在 1,000 筆以內、還是經常到 10,000 筆甚至更多）？
是否需要在儀表板中顯示「合規評分」或「風險等級」總覽指標（例如 0–100 分或 Low/Medium/High）？
是否有可能需要支援「多個資料集切換」（例如不同年份或不同品牌的乳房植入物）？若需要，UI 應如何呈現（tab / 下拉選單 / 分頁）？
在視覺風格上，你更偏向「醫療科技感」（冷色系、簡潔線條）還是「溫暖關懷感」（柔和色彩與花卉元素更明顯）？
你是否需要「報告匯出」功能（例如將 AI 分析結果 + 部分圖表組合成 PDF / Markdown 報告）？
在 HF Space 中，這個系統預期是給內部 TFDA / 專業人員使用，還是會部分開放給外部單位？這會影響到預設語言與說明文字的詳盡程度。
未來是否有考慮新增使用者登入 / 權限區分（例如：一般使用者僅能上傳查看，稽核人員可以編輯與執行 AI 分析）？
ファイルが選択されていませんファイルが選択されていません
Super please create app.py, advanced agents.yaml with 31 agents for supply chain analysis and visualozation in traditional chinese, requirements.txt of previous design

以下為一組可直接放到 Hugging Face Space 的初版檔案：  

- `app.py`（Streamlit 主程式，支援 31 個代理人、多模型、多語系、Jackslot 主題選擇與 API Key 管理）  

- `agents.yaml`（31 個繁體中文供應鏈分析/視覺化代理人設定）  

- `requirements.txt`（搭配本設計的必要套件）



可依實際需要再細修。



---



## 1. `app.py`



```python

import os

import io

import random

from typing import List, Dict, Any, Optional



import pandas as pd

import streamlit as st

import yaml



from datetime import datetime



# === AI SDKs ===

from openai import OpenAI

import google.generativeai as genai

from anthropic import Anthropic

import requests



# === Optional: simple charts ===

import altair as alt



# === Optional: for network visualization (placeholder) ===

import networkx as nx

from pyvis.network import Network

import streamlit.components.v1 as components





# ==============================

# Config & Constants

# ==============================



APP_TITLE_ZH = "醫療器材供應鏈追蹤系統 v2.1 - BioChain Analyst Pro"

APP_TITLE_EN = "BioChain Analyst Pro v2.1 - Medical Device Supply Chain Tracker"



# 多模型清單 (可依需求調整/擴充)

MODEL_OPTIONS = [

    # OpenAI

    {"provider": "openai", "id": "gpt-4o-mini", "label": "OpenAI - gpt-4o-mini", "max_tokens": 16384},

    {"provider": "openai", "id": "gpt-4.1-mini", "label": "OpenAI - gpt-4.1-mini", "max_tokens": 16384},

    # Google Gemini

    {"provider": "gemini", "id": "gemini-2.5-flash", "label": "Gemini - 2.5 Flash", "max_tokens": 8192},

    {"provider": "gemini", "id": "gemini-2.5-flash-lite", "label": "Gemini - 2.5 Flash Lite", "max_tokens": 4096},

    # Anthropic

    {"provider": "anthropic", "id": "claude-3-5-sonnet-latest", "label": "Anthropic - Claude 3.5 Sonnet", "max_tokens": 8192},

    {"provider": "anthropic", "id": "claude-3-5-haiku-latest", "label": "Anthropic - Claude 3.5 Haiku", "max_tokens": 8192},

    # Grok (xAI)

    {"provider": "grok", "id": "grok-4-fast-reasoning", "label": "Grok - 4 Fast Reasoning", "max_tokens": 8192},

    {"provider": "grok", "id": "grok-3-mini", "label": "Grok - 3 Mini", "max_tokens": 4096},

]



# 供 UI 使用：model_id -> label

MODEL_ID_TO_LABEL = {m["id"]: m["label"] for m in MODEL_OPTIONS}

MODEL_ID_TO_PROVIDER = {m["id"]: m["provider"] for m in MODEL_OPTIONS}

MODEL_ID_TO_MAXTOK = {m["id"]: m["max_tokens"] for m in MODEL_OPTIONS}



# 20 種花卉主題名稱（可依喜好微調）

FLOWER_THEMES = [

    "Sakura 櫻花", "Rose 玫瑰", "Lotus 蓮花", "Tulip 鬱金香", "Peony 牡丹",

    "Lily 百合", "Sunflower 向日葵", "Camellia 山茶花", "Hydrangea 繡球花",

    "Orchid 蘭花", "Cherry Blossom 櫻吹雪", "Plum Blossom 梅花",

    "Iris 鳶尾花", "Daisy 雛菊", "Lavender 薰衣草", "Magnolia 木蘭",

    "Jasmine 茉莉", "Gardenia 梔子花", "Hibiscus 扶桑", "Poppy 罌粟花",

]



# 多語系簡易字典（僅示意，可擴充）

I18N = {

    "zh-TW": {

        "title": APP_TITLE_ZH,

        "upload_data": "上傳供應鏈 CSV 資料",

        "or_use_mock": "或使用系統預設範例資料",

        "data_preview": "資料預覽與編輯",

        "download_data": "下載目前資料（含修改）",

        "dashboard": "儀表板",

        "network": "供應鏈網路圖",

        "trends": "時間序列趨勢",

        "agents": "AI 代理人分析",

        "settings": "系統設定",

        "language": "介面語言",

        "theme_mode": "主題模式",

        "light": "淺色",

        "dark": "深色",

        "flower_theme": "花卉主題",

        "jackslot": "Jackslot 拉霸選主題",

        "api_keys": "API 金鑰設定",

        "system_key_in_use": "使用系統管理的 API Key",

        "need_user_key": "尚未設定系統金鑰，請輸入本次 Session 使用的 API Key：",

        "run_all_agents": "依序執行所有啟用代理人",

        "data_status": "資料狀態",

        "data_status_mock": "使用預設範例資料",

        "data_status_uploaded": "使用者上傳資料",

        "no_data": "目前尚未載入任何資料",

        "agent_output": "代理人輸出（可編輯）",

        "run_this_agent": "執行此代理人",

        "max_tokens": "Max Tokens",

        "model": "模型",

        "prompt": "Prompt 模板",

        "send_to_next_agent": "將本輸出傳給下一位代理人",

        "send_to_specific_agent": "將本輸出傳給指定代理人",

        "target_agent": "目標代理人",

        "agent_status": "狀態",

        "status_idle": "閒置",

        "status_running": "執行中...",

        "status_done": "完成",

        "status_error": "錯誤",

        "kpi_total_qty": "總出貨數量",

        "kpi_node_count": "節點數量（供應商 + 醫院/診所）",

        "kpi_device_count": "醫材種類數",

        "trend_title": "出貨量時間序列",

        "network_note": "下方為簡易的網路圖示意，可依需求替換為更進階的可視化元件。",

    },

    "en": {

        "title": APP_TITLE_EN,

        "upload_data": "Upload supply chain CSV data",

        "or_use_mock": "or use built-in mock dataset",

        "data_preview": "Data preview & editing",

        "download_data": "Download current data (including edits)",

        "dashboard": "Dashboard",

        "network": "Supply chain network graph",

        "trends": "Time series trends",

        "agents": "AI agents",

        "settings": "Settings",

        "language": "Language",

        "theme_mode": "Theme mode",

        "light": "Light",

        "dark": "Dark",

        "flower_theme": "Flower theme",

        "jackslot": "Jackslot theme selector",

        "api_keys": "API keys",

        "system_key_in_use": "Using system-managed API key",

        "need_user_key": "No system key configured. Please input an API key for this session:",

        "run_all_agents": "Run all enabled agents sequentially",

        "data_status": "Data status",

        "data_status_mock": "Using mock dataset",

        "data_status_uploaded": "Using user uploaded data",

        "no_data": "No data loaded yet",

        "agent_output": "Agent output (editable)",

        "run_this_agent": "Run this agent",

        "max_tokens": "Max tokens",

        "model": "Model",

        "prompt": "Prompt template",

        "send_to_next_agent": "Send this output to next agent",

        "send_to_specific_agent": "Send this output to specific agent",

        "target_agent": "Target agent",

        "agent_status": "Status",

        "status_idle": "Idle",

        "status_running": "Running...",

        "status_done": "Done",

        "status_error": "Error",

        "kpi_total_qty": "Total shipped quantity",

        "kpi_node_count": "Node count (suppliers + hospitals/clinics)",

        "kpi_device_count": "Distinct device types",

        "trend_title": "Shipment volume over time",

        "network_note": "Network visualization below is a simple placeholder; you can replace it with a more advanced component if desired.",

    },

}





# ==============================

# Helper Functions

# ==============================



def load_agents_config(path: str = "agents.yaml") -> List[Dict[str, Any]]:

    with open(path, "r", encoding="utf-8") as f:

        data = yaml.safe_load(f)

    return data.get("agents", [])





def load_mock_data() -> pd.DataFrame:

    # 這裡可替換為實際 mock_dataset.csv

    csv_data = """id,trade_date,src_name,dst_name,device_name,quantity

1,2024-01-05,供應商A,醫院X,乳房植入物A,10

2,2024-01-06,供應商A,醫院Y,乳房植入物A,5

3,2024-01-08,經銷商B,醫院X,乳房植入物B,8

4,2024-01-10,供應商C,診所Z,乳房植入物A,3

5,2024-01-12,經銷商B,醫院Y,乳房植入物C,12

6,2024-01-13,供應商A,經銷商B,乳房植入物B,20

"""

    return pd.read_csv(io.StringIO(csv_data))





def get_env_api_keys() -> Dict[str, Optional[str]]:

    return {

        "openai": os.getenv("OPENAI_API_KEY"),

        "gemini": os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"),

        "anthropic": os.getenv("ANTHROPIC_API_KEY"),

        "grok": os.getenv("GROK_API_KEY"),

    }





def init_session_state(agents: List[Dict[str, Any]]) -> None:

    if "language" not in st.session_state:

        st.session_state.language = "zh-TW"

    if "theme_mode" not in st.session_state:

        st.session_state.theme_mode = "light"

    if "flower_theme" not in st.session_state:

        st.session_state.flower_theme = FLOWER_THEMES[0]

    if "data_source" not in st.session_state:

        st.session_state.data_source = "mock"  # "mock" or "uploaded"

    if "df" not in st.session_state:

        st.session_state.df = load_mock_data()



    if "agent_runtime" not in st.session_state:

        runtime = {}

        for ag in agents:

            aid = ag["id"]

            runtime[aid] = {

                "enabled": ag.get("enabled", True),

                "model": ag.get("default_model", "gemini-2.5-flash"),

                "max_tokens": ag.get("default_max_tokens", 12000),

                "prompt": ag.get("default_prompt", ""),

                "status": "idle",

                "output": "",

                "error": "",

                "upstream_context": "",

            }

        st.session_state.agent_runtime = runtime



    if "api_keys_user" not in st.session_state:

        st.session_state.api_keys_user = {

            "openai": None,

            "gemini": None,

            "anthropic": None,

            "grok": None,

        }





def get_lang() -> str:

    return st.session_state.get("language", "zh-TW")





def t(key: str) -> str:

    lang = get_lang()

    return I18N.get(lang, I18N["zh-TW"]).get(key, key)





def get_effective_api_key(provider: str, env_keys: Dict[str, Optional[str]]) -> Optional[str]:

    if env_keys.get(provider):

        return env_keys[provider]

    return st.session_state.api_keys_user.get(provider)





# ==============================

# AI Call Helpers

# ==============================



def call_model(

    provider: str,

    model_id: str,

    prompt: str,

    max_tokens: int,

    env_keys: Dict[str, Optional[str]],

) -> str:

    key = get_effective_api_key(provider, env_keys)

    if not key:

        raise ValueError(f"{provider} API Key 不存在，請先於設定頁面輸入或在環境變數中設定。")



    if provider == "openai":

        client = OpenAI(api_key=key)

        resp = client.chat.completions.create(

            model=model_id,

            messages=[

                {"role": "system", "content": "你是一位專精於醫療器材供應鏈與法規的專家助理。"},

                {"role": "user", "content": prompt},

            ],

            max_tokens=max_tokens,

        )

        return resp.choices[0].message.content



    elif provider == "gemini":

        genai.configure(api_key=key)

        model = genai.GenerativeModel(model_id)

        resp = model.generate_content(

            prompt,

            generation_config={"max_output_tokens": max_tokens},

        )

        return resp.text



    elif provider == "anthropic":

        client = Anthropic(api_key=key)

        resp = client.messages.create(

            model=model_id,

            max_tokens=max_tokens,

            messages=[{"role": "user", "content": prompt}],

        )

        text_parts = []

        for block in resp.content:

            if getattr(block, "type", None) == "text":

                text_parts.append(block.text)

        return "".join(text_parts) if text_parts else str(resp)



    elif provider == "grok":

        # 假設 xAI / Grok API 介面類似於 OpenAI（實際實作時請依官方文件調整）

        headers = {

            "Authorization": f"Bearer {key}",

            "Content-Type": "application/json",

        }

        payload = {

            "model": model_id,

            "messages": [{"role": "user", "content": prompt}],

            "max_tokens": max_tokens,

        }

        url = "https://api.x.ai/v1/chat/completions"

        r = requests.post(url, headers=headers, json=payload, timeout=60)

        r.raise_for_status()

        data = r.json()

        return data["choices"][0]["message"]["content"]



    else:

        raise ValueError(f"未知的 provider: {provider}")





def build_agent_prompt(

    agent_cfg: Dict[str, Any],

    runtime_cfg: Dict[str, Any],

    df: pd.DataFrame,

) -> str:

    """組合代理人的 prompt：預設 prompt + 資料摘要 + 上游 context。"""

    base_prompt = runtime_cfg.get("prompt") or agent_cfg.get("default_prompt", "")

    upstream = runtime_cfg.get("upstream_context", "").strip()



    # 資料摘要：限制列數避免超大

    sample_rows = df.head(50)

    csv_snippet = sample_rows.to_csv(index=False)



    parts = [

        base_prompt.strip(),

        "\n\n---\n以下是最多前 50 筆的供應鏈交易資料（CSV 格式，含欄位 trade_date, src_name, dst_name, device_name, quantity）：\n",

        csv_snippet,

    ]

    if upstream:

        parts.append("\n---\n上游代理人提供的補充說明/分析如下：\n")

        parts.append(upstream)



    return "".join(parts)





# ==============================

# Visualization Helpers

# ==============================



def render_dashboard(df: pd.DataFrame):

    st.subheader(t("dashboard"))

    if df is None or df.empty:

        st.info(t("no_data"))

        return



    total_qty = int(df["quantity"].sum())

    nodes = set(df["src_name"]).union(set(df["dst_name"]))

    device_count = df["device_name"].nunique()



    col1, col2, col3 = st.columns(3)

    col1.metric(t("kpi_total_qty"), f"{total_qty:,}")

    col2.metric(t("kpi_node_count"), f"{len(nodes):,}")

    col3.metric(t("kpi_device_count"), f"{device_count:,}")





def render_trends(df: pd.DataFrame):

    st.subheader(t("trend_title"))

    if df is None or df.empty:

        st.info(t("no_data"))

        return



    temp = df.copy()

    temp["trade_date"] = pd.to_datetime(temp["trade_date"], errors="coerce")

    temp = temp.dropna(subset=["trade_date"])

    grouped = temp.groupby("trade_date")["quantity"].sum().reset_index()



    chart = (

        alt.Chart(grouped)

        .mark_line(point=True)

        .encode(

            x="trade_date:T",

            y="quantity:Q",

            tooltip=["trade_date:T", "quantity:Q"],

        )

        .properties(height=300)

    )

    st.altair_chart(chart, use_container_width=True)





def render_network(df: pd.DataFrame):

    st.subheader(t("network"))

    st.caption(t("network_note"))



    if df is None or df.empty:

        st.info(t("no_data"))

        return



    # 簡易 NetworkX + Pyvis 視覺化

    G = nx.DiGraph()

    for _, row in df.iterrows():

        src = str(row["src_name"])

        dst = str(row["dst_name"])

        qty = int(row["quantity"])

        if G.has_edge(src, dst):

            G[src][dst]["quantity"] += qty

        else:

            G.add_edge(src, dst, quantity=qty)



    net = Network(

        height="600px",

        width="100%",

        directed=True,

        notebook=False,

    )

    net.from_nx(G)

    # 顯示交易量在邊的 label

    for e in net.edges:

        qty = G[e["from"]][e["to"]].get("quantity", 0)

        e["title"] = f"交易量: {qty}"

        e["label"] = str(qty)



    html = net.generate_html()

    components.html(html, height=600, scrolling=True)





# ==============================

# UI Sections

# ==============================



def sidebar_settings(env_keys: Dict[str, Optional[str]], agents: List[Dict[str, Any]]):

    st.sidebar.title(t("settings"))



    # 語言

    st.sidebar.selectbox(

        t("language"),

        options=["zh-TW", "en"],

        index=0 if get_lang() == "zh-TW" else 1,

        key="language",

    )



    # Light / Dark

    st.sidebar.radio(

        t("theme_mode"),

        options=["light", "dark"],

        format_func=lambda m: t(m),

        key="theme_mode",

    )



    # 花卉主題

    st.sidebar.selectbox(

        t("flower_theme"),

        options=FLOWER_THEMES,

        key="flower_theme",

    )



    # Jackslot

    if st.sidebar.button("🎰 " + t("jackslot")):

        st.session_state.flower_theme = random.choice(FLOWER_THEMES)

        st.sidebar.success(f"已抽到主題：{st.session_state.flower_theme}")



    # API Keys

    st.sidebar.markdown("---")

    st.sidebar.subheader(t("api_keys"))



    for provider, env_key in env_keys.items():

        st.sidebar.markdown(f"**{provider.upper()}**")

        if env_key:

            st.sidebar.info(f"✅ {t('system_key_in_use')}")

        else:

            st.sidebar.warning(t("need_user_key"))

            placeholder = st.sidebar.text_input(

                f"{provider.upper()} API Key",

                type="password",

                key=f"api_key_{provider}",

            )

            if placeholder:

                st.session_state.api_keys_user[provider] = placeholder



    # 簡易代理人統計

    st.sidebar.markdown("---")

    enabled_count = sum(

        1 for ag in agents if st.session_state.agent_runtime.get(ag["id"], {}).get("enabled", True)

    )

    st.sidebar.write(f"啟用中的代理人數量：{enabled_count} / {len(agents)}")





def data_section():

    st.header(t("data_preview"))

    uploaded_file = st.file_uploader(

        t("upload_data"),

        type=["csv"],

        accept_multiple_files=False,

    )



    col1, col2 = st.columns([3, 1])

    with col1:

        if uploaded_file is not None:

            df = pd.read_csv(uploaded_file)

            st.session_state.df = df

            st.session_state.data_source = "uploaded"

        else:

            if st.button(t("or_use_mock")):

                st.session_state.df = load_mock_data()

                st.session_state.data_source = "mock"



    # 資料狀態

    if st.session_state.df is not None:

        if st.session_state.data_source == "mock":

            st.info(t("data_status_mock"))

        else:

            st.success(t("data_status_uploaded"))



    # 可編輯表格

    if st.session_state.df is not None:

        st.session_state.df = st.data_editor(

            st.session_state.df,

            use_container_width=True,

            num_rows="dynamic",

            key="data_editor",

        )



        # 下載

        csv_buffer = st.session_state.df.to_csv(index=False).encode("utf-8")

        st.download_button(

            label=t("download_data"),

            data=csv_buffer,

            file_name=f"biochain_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",

            mime="text/csv",

        )

    else:

        st.info(t("no_data"))





def agents_section(agents: List[Dict[str, Any]], env_keys: Dict[str, Optional[str]]):

    st.header(t("agents"))



    # 依序執行所有啟用代理人

    if st.button(t("run_all_agents")):

        for ag in agents:

            aid = ag["id"]

            runtime = st.session_state.agent_runtime[aid]

            if not runtime.get("enabled", True):

                continue

            _run_single_agent(ag, env_keys)



    # 每個代理人卡片

    for ag in agents:

        aid = ag["id"]

        cfg = st.session_state.agent_runtime[aid]



        with st.expander(f"[{aid}] {ag.get('name', '')} / {ag.get('role', '')}", expanded=False):

            # 啟用開關

            cfg["enabled"] = st.checkbox(

                "啟用",

                value=cfg.get("enabled", True),

                key=f"enabled_{aid}",

            )



            # 模型選擇

            current_model = cfg.get("model", ag.get("default_model", "gemini-2.5-flash"))

            model_options_ids = [m["id"] for m in MODEL_OPTIONS]

            if current_model not in model_options_ids:

                current_model = "gemini-2.5-flash"

            model_label_list = [MODEL_ID_TO_LABEL[mid] for mid in model_options_ids]

            selected_label = st.selectbox(

                t("model"),

                options=model_label_list,

                index=model_options_ids.index(current_model),

                key=f"model_{aid}",

            )

            # 反查 model_id

            selected_model_id = [

                mid for mid, lbl in MODEL_ID_TO_LABEL.items() if lbl == selected_label

            ][0]

            cfg["model"] = selected_model_id



            # max_tokens

            default_max = ag.get("default_max_tokens", 12000)

            max_allowed = MODEL_ID_TO_MAXTOK.get(selected_model_id, default_max)

            cfg["max_tokens"] = st.number_input(

                t("max_tokens"),

                min_value=256,

                max_value=max_allowed,

                value=min(cfg.get("max_tokens", default_max), max_allowed),

                step=256,

                key=f"max_tokens_{aid}",

            )



            # Prompt

            cfg["prompt"] = st.text_area(

                t("prompt"),

                value=cfg.get("prompt", ag.get("default_prompt", "")),

                height=180,

                key=f"prompt_{aid}",

            )



            # 狀態

            status = cfg.get("status", "idle")

            status_label = {

                "idle": t("status_idle"),

                "running": t("status_running"),

                "done": t("status_done"),

                "error": t("status_error"),

            }.get(status, status)

            st.markdown(f"**{t('agent_status')}**：{status_label}")



            # 執行按鈕

            if st.button(t("run_this_agent"), key=f"run_{aid}"):

                _run_single_agent(ag, env_keys)



            # 輸出（可編輯）

            cfg["output"] = st.text_area(

                t("agent_output"),

                value=cfg.get("output", ""),

                height=260,

                key=f"output_{aid}",

            )



            # 設定為上游 context（給下一位代理人）

            cols = st.columns(2)

            with cols[0]:

                if st.button(t("send_to_next_agent"), key=f"send_next_{aid}"):

                    _send_output_to_next_agent(aid, agents)



            with cols[1]:

                target_ids = [a["id"] for a in agents if a["id"] != aid]

                if target_ids:

                    target = st.selectbox(

                        t("target_agent"),

                        options=target_ids,

                        key=f"target_select_{aid}",

                    )

                    if st.button(t("send_to_specific_agent"), key=f"send_specific_{aid}"):

                        st.session_state.agent_runtime[target]["upstream_context"] = cfg["output"]

                        st.success(f"已將 {aid} 的輸出傳給 {target}。")





def _run_single_agent(agent_cfg: Dict[str, Any], env_keys: Dict[str, Optional[str]]):

    aid = agent_cfg["id"]

    runtime = st.session_state.agent_runtime[aid]

    runtime["status"] = "running"

    runtime["error"] = ""

    st.session_state.agent_runtime[aid] = runtime



    try:

        df = st.session_state.df

        if df is None or df.empty:

            raise ValueError("尚未載入任何供應鏈資料。")



        prompt = build_agent_prompt(agent_cfg, runtime, df)

        model_id = runtime["model"]

        provider = MODEL_ID_TO_PROVIDER.get(model_id)

        if not provider:

            raise ValueError(f"未知模型：{model_id}")



        result = call_model(

            provider=provider,

            model_id=model_id,

            prompt=prompt,

            max_tokens=int(runtime["max_tokens"]),

            env_keys=env_keys,

        )

        runtime["output"] = str(result)

        runtime["status"] = "done"

        st.success(f"代理人 {aid} 執行完成。")



    except Exception as e:

        runtime["status"] = "error"

        runtime["error"] = str(e)

        st.error(f"代理人 {aid} 執行錯誤：{e}")



    st.session_state.agent_runtime[aid] = runtime





def _send_output_to_next_agent(aid: str, agents: List[Dict[str, Any]]):

    ids = [a["id"] for a in agents]

    if aid not in ids:

        return

    idx = ids.index(aid)

    if idx == len(ids) - 1:

        st.info("已是最後一位代理人，無後續代理。")

        return

    next_id = ids[idx + 1]

    out = st.session_state.agent_runtime[aid].get("output", "")

    st.session_state.agent_runtime[next_id]["upstream_context"] = out

    st.success(f"已將 {aid} 的輸出傳給下一位代理人 {next_id}。")





# ==============================

# Main App

# ==============================



def main():

    st.set_page_config(

        page_title="BioChain Analyst Pro",

        layout="wide",

        page_icon="🩺",

    )



    # 載入 agents

    agents = load_agents_config("agents.yaml")

    env_keys = get_env_api_keys()

    init_session_state(agents)



    # Sidebar

    sidebar_settings(env_keys, agents)



    # 標題

    st.title(t("title"))

    st.caption(f"主題：{st.session_state.flower_theme} | 模式：{t(st.session_state.theme_mode)}")



    # 分頁

    tab_dashboard, tab_network, tab_trends, tab_data, tab_agents = st.tabs(

        [

            t("dashboard"),

            t("network"),

            t("trends"),

            t("data_preview"),

            t("agents"),

        ]

    )



    with tab_dashboard:

        render_dashboard(st.session_state.df)



    with tab_network:

        render_network(st.session_state.df)



    with tab_trends:

        render_trends(st.session_state.df)



    with tab_data:

        data_section()



    with tab_agents:

        agents_section(agents, env_keys)





if __name__ == "__main__":

    main()

```



---



## 2. `agents.yaml`（31 個進階代理人，繁體中文）



```yaml

agents:

  - id: auditor_core

    name: 核心稽核代理人

    role: Auditor

    description: |

      針對整體醫療器材供應鏈交易紀錄進行初步稽核，偵測明顯異常交易量、可疑路徑與重複紀錄。

    enabled: true

    default_model: gemini-2.5-flash

    default_max_tokens: 12000

    default_prompt: |

      你是一位專精於醫療器材與植入物監管的稽核專家，協助 TFDA 針對乳房植入物供應鏈進行風險盤點。



      請依下列步驟分析提供的交易資料：

      1. 檢查是否存在顯著異常的交易量（例如單筆數量明顯偏高或偏低）。

      2. 找出在短時間內對同一醫材、同一醫療機構重複出貨的情形。

      3. 標記來源或目的節點中，交易量比例異常集中的節點（可能為風險節點）。

      4. 用條列方式整理「疑似異常交易」摘要，標示：日期、來源、目的地、醫材名稱、數量與簡要理由。

      5. 針對各類異常提出可能原因及後續建議（例如：資料輸入錯誤、潛在物流問題、可能違規風險）。



      請以繁體中文條列與小結方式呈現，方便稽核人員快速檢視。



  - id: auditor_deep

    name: 深度稽核代理人

    role: Auditor

    description: |

      在核心稽核結果基礎上，深入針對高風險路徑與節點進行深度說明與交叉比對。

    enabled: true

    default_model: claude-3-5-sonnet-latest

    default_max_tokens: 12000

    default_prompt: |

      你是一位高階稽核顧問，專門針對醫療器材供應鏈進行深度風險評估。



      上游代理人已提供初步稽核摘要與疑似風險路徑。請你：

      1. 交叉比對上游摘要與目前提供的完整交易資料，確認是否有遺漏的高風險路徑或節點。

      2. 區分「可能為資料品質問題」與「可能涉及實體物流或合規風險」兩大類型。

      3. 為每個主要風險項目給出：

         - 風險描述

         - 可能成因

         - 需要進一步蒐集的佐證資料清單

         - 建議 TFDA 與醫療機構採取的行動

      4. 最後提供一個 1～5 級的整體風險評估（1 最低風險，5 最高風險），並說明評估理由。



      請以繁體中文詳細條列說明。



  - id: logistics_flow

    name: 物流路徑分析代理人

    role: Logistics

    description: |

      分析乳房植入物從供應商、經銷商到醫院/診所的物流路徑，找出關鍵樞紐與繞路現象。

    enabled: true

    default_model: gemini-2.5-flash

    default_max_tokens: 12000

    default_prompt: |

      你是一位醫療器材物流顧問，專注於醫材在供應鏈中的實際流向。



      根據提供的交易資料，請你：

      1. 說明整體供應鏈網路的典型流向（例如：製造商→總代理→經銷商→醫院）。

      2. 找出出貨量最高的前 5 條路徑，並說明其對整體供應鏈的重要性。

      3. 偵測是否存在「繞路」或「多次轉手」的異常路徑（例如：同一批醫材在短期內多次於不同節點之間往返）。

      4. 區分「直接供貨」與「透過經銷/代理」的比例，分析對風險與監管的影響。

      5. 提出可視化建議（例如在網路圖上如何突出關鍵路徑與樞紐節點）。



      回覆請以繁體中文條列與簡短段落說明。



  - id: logistics_route_optimization

    name: 路徑優化與效率代理人

    role: Logistics

    description: |

      從現有供應鏈路徑中評估效率與冗餘，提出可能的路徑簡化與集中/分散策略。

    enabled: false

    default_model: gpt-4.1-mini

    default_max_tokens: 12000

    default_prompt: |

      你是一位供應鏈優化顧問，專注於改善醫療器材物流效率與穩定性。



      請根據交易資料：

      1. 找出物流節點（供應商/經銷商/醫院）中，扮演「樞紐」角色的節點（高進/出貨量）。

      2. 評估目前路徑中可能存在的冗餘轉運（例如不必要的中間經銷商）。

      3. 提出 2～3 個可能的路徑精簡或重組方案，並說明：

         - 對交期（Lead Time）的預期影響

         - 對風險管理與追蹤性的影響

      4. 分別就「集中化」與「分散化」兩種策略，分析其對乳房植入物供應安全與監管的利弊。



      請以繁體中文具體列點提出建議。



  - id: legal_compliance

    name: 法規合規檢查代理人

    role: Legal

    description: |

      從交易與流向模式中檢查是否有可能違反醫療器材法規或標示/追蹤規定之風險。

    enabled: true

    default_model: claude-3-5-sonnet-latest

    default_max_tokens: 12000

    default_prompt: |

      你是一位熟悉臺灣醫療器材管理法規與 TFDA 要求的法規顧問。



      根據提供的供應鏈交易紀錄，請你：

      1. 從流向模式判斷是否存在以下風險徵兆：

         - 非授權通路（例如疑似未登錄的經銷單位）

         - 大量跨區域轉運，可能增加標示與追蹤困難度

         - 醫療機構間直接轉移植入物（若資料顯示）

      2. 針對每類風險，對應可能相關的法規條文或管理原則（可概略描述，不需逐條引用）。

      3. 提出 TFDA 或院方應補強的文件與紀錄，包括但不限於：

         - 批號追蹤紀錄

         - 進貨/出貨對應文件

         - 病人植入紀錄與召回機制

      4. 提供一份「合規性檢查清單」，供稽核人員後續實務操作使用。



      回覆以繁體中文條列與分段說明。



  - id: legal_recall_risk

    name: 召回風險與應變代理人

    role: Legal

    description: |

      聚焦於可能發生產品召回時，分析目前供應鏈架構下的追蹤難度與應變能力。

    enabled: false

    default_model: gemini-2.5-flash

    default_max_tokens: 12000

    default_prompt: |

      假設目前分析的乳房植入物批次中，部分批號可能需要啟動產品召回。



      請你依據交易流向資料：

      1. 說明在現有供應鏈網路下，若針對特定批號啟動召回，追溯到實際植入病人的難度與風險。

      2. 由上游（供應商/經銷商）與下游（醫院/診所）兩個角度，分析：

         - 哪些節點是關鍵控制點

         - 哪些節點一旦紀錄不完整會嚴重影響召回成效

      3. 提出改善召回與追蹤能力的建議，包括：

         - 資料欄位與紀錄粒度

         - 流程與責任分工

         - 系統化追蹤工具的需求

      4. 若要視覺化召回風險，建議在網路圖與儀表板上呈現哪些指標。



      請以繁體中文條列方式整理。



  - id: analyst_overview

    name: 供應鏈總覽分析代理人

    role: Analyst

    description: |

      提供整體供應鏈的高層次摘要，包含主要流向、交易規模與關鍵節點。

    enabled: true

    default_model: gpt-4o-mini

    default_max_tokens: 12000

    default_prompt: |

      你是一位資料分析師，負責為決策者提供「一頁式」的供應鏈總覽。



      根據交易資料，請你：

      1. 用文字描述整體供應鏈結構（主要來源、主要目的地、典型流向）。

      2. 指出出貨量 Top 5 的節點（供應端與需求端分開列出）。

      3. 分析不同醫材（device_name）之間的出貨結構差異（例如哪一種植入物較集中於少數醫院）。

      4. 用條列方式整理「管理上值得關注的 3～5 個重點」，著重在：

         - 風險

         - 效率

         - 合規與追蹤性



      請以繁體中文、清楚分段呈現。



  - id: analyst_time_series

    name: 時間序列與季節性代理人

    role: Analyst

    description: |

      分析出貨量在時間上的變化與可能的季節性或趨勢效應。

    enabled: false

    default_model: gemini-2.5-flash-lite

    default_max_tokens: 8000

    default_prompt: |

      你是一位時間序列分析專家，協助檢視乳房植入物出貨在時間上的變化。



      請利用提供的交易日期（trade_date）與出貨數量（quantity）：

      1. 檢查是否存在明顯的上升或下降趨勢，說明可能成因。

      2. 觀察是否有明顯的季節性或月份集中現象（例如某些月份出貨特別高）。

      3. 提出適合的時間序列圖表形式（如折線圖、移動平均線）供儀表板使用。

      4. 就監管單位角度，說明為何持續追蹤時間趨勢有助於提前發現異常。



      回覆以繁體中文條列與簡短敘述。



  - id: analyst_device_mix

    name: 醫材產品組合分析代理人

    role: Analyst

    description: |

      分析不同乳房植入物產品之間的銷售與流向結構差異，協助風險與策略判斷。

    enabled: false

    default_model: gpt-4.1-mini

    default_max_tokens: 10000

    default_prompt: |

      你是一位產品組合與市場結構分析師。



      根據 device_name 與交易資料，請你：

      1. 比較不同醫材產品在整體出貨量中的占比。

      2. 找出每種產品的主要供應節點與主要使用醫院/診所。

      3. 分析是否有產品呈現「高度集中」在少數醫療機構的情況，並評估其風險（例如一旦該院發生問題，對病人影響範圍）。

      4. 提出可視化建議：如堆疊柱狀圖、桑基圖或分群網路圖，用以表達產品組合結構。



      請以繁體中文提供條列分析與視覺化建議。



  - id: viz_topology

    name: 網路拓樸結構解析代理人

    role: Visualization

    description: |

      專注於供應鏈網路拓樸，協助設計更清晰的節點與連線視覺化方式。

    enabled: true

    default_model: gemini-2.5-flash

    default_max_tokens: 12000

    default_prompt: |

      你是一位資料視覺化設計師，專長是將複雜供應鏈網路轉換為直觀的圖形。



      針對目前的交易資料，請你：

      1. 說明哪些節點屬於「來源型」（供應商、經銷商）、哪些屬於「目的型」（醫院/診所）。

      2. 建議在網路圖中如何區分節點類型（顏色、形狀或圖示）。

      3. 提出如何根據交易量調整連線粗細與顏色，以突出高流量路徑。

      4. 建議在節點與邊上應顯示哪些關鍵數值（例如累計出貨量、不同醫材數量）。

      5. 描述 1～2 種適合在 D3.js 或 Recharts 中實作的互動形式（如節點 hover 顯示詳細資訊、點選節點鎖定相關路徑）。



      請以繁體中文條列整理，重點在實用與可操作性。



  - id: viz_dashboard_designer

    name: 儀表板設計顧問代理人

    role: Visualization

    description: |

      為供應鏈監管儀表板提供指標與版面配置建議，提升可讀性與決策支援度。

    enabled: false

    default_model: gpt-4o-mini

    default_max_tokens: 9000

    default_prompt: |

      你是一位 BI / Dashboard 設計顧問。



      請根據目前供應鏈資料特性，為 TFDA 或醫院管理階層設計一個監控儀表板：

      1. 建議首頁應呈現的 5～8 個核心指標（KPI），例如總出貨量、高風險路徑數、節點數量等。

      2. 為每個 KPI 說明其監管意義與解讀方式。

      3. 建議儀表板版面配置（例如：上方總覽、中間網路圖與趨勢圖、下方異常清單）。

      4. 提出互動功能建議（篩選醫材、選擇時間區間、點選節點下鑽等）。

      5. 簡要描述適合使用的圖表類型與色彩策略，並考慮深色/淺色模式與可讀性。



      回覆請以繁體中文條列呈現。



  - id: risk_route

    name: 高風險路徑標記代理人

    role: Risk

    description: |

      挑選並解釋高風險供應鏈路徑，以利在網路圖上加註警示與追蹤。

    enabled: true

    default_model: gemini-2.5-flash

    default_max_tokens: 12000

    default_prompt: |

      你是一位風險管理顧問，任務是找出供應鏈中的「高風險路徑」。



      定義高風險路徑時，請至少考慮：

      - 交易量異常高或異常低

      - 涉及多次轉手（供應商/經銷商/醫院之間的跳躍次數）

      - 集中於單一或少數節點的情形



      根據資料，請你：

      1. 提出前 5 條「高風險路徑」，以來源節點→目的節點的形式列出，並附上理由。

      2. 為每條路徑建議一個「風險等級」（低/中/高）。

      3. 說明在視覺化上應如何標示這些路徑（例如紅色粗線、警示圖示）。

      4. 建議後續稽核或實地追查的方向。



      回覆以繁體中文整理。



  - id: risk_node

    name: 高風險節點鑑別代理人

    role: Risk

    description: |

      專注於找出供應鏈網路中的高風險節點（供應商、經銷商、醫院）。

    enabled: false

    default_model: claude-3-5-haiku-latest

    default_max_tokens: 8000

    default_prompt: |

      你是一位網路風險分析師，專門分析供應鏈中的關鍵節點。



      根據節點的進出貨量、連結度與產品多樣性，請你：

      1. 找出「高風險節點」Top 10，並說明選擇理由（如交易量極大、產品種類繁多、同時扮演多種角色等）。

      2. 區分「系統性關鍵節點」（一旦出問題影響範圍很大）與「可疑節點」（異常模式可能指向風險）。

      3. 提出在網路圖中陳列高風險節點的建議（如使用特別顏色/大小）。

      4. 建議監管單位可優先關注與定期稽核的節點清單。



      請以繁體中文條列與短段落說明。



  - id: anomaly_detector

    name: 異常偵測與解釋代理人

    role: Anomaly

    description: |

      專門偵測並解釋交易異常點，協助區分資料問題與實務風險。

    enabled: true

    default_model: gpt-4o-mini

    default_max_tokens: 10000

    default_prompt: |

      你是一位異常偵測專家。



      針對目前的交易資料，請你：

      1. 以文字方式描述可能的異常類型（例如極端值、突然暴增暴減、重複紀錄、未預期路徑等）。

      2. 舉出具體範例（列出日期、來源、目的地、醫材名稱與數量），並說明為何判定為異常。

      3. 協助區分「資料輸入或系統問題」 vs. 「實體供應鏈異常或風險」。

      4. 建議後續可採用的統計或機器學習方法，以自動化偵測這類異常。



      回覆請用繁體中文條列與附簡要說明。



  - id: anomaly_explainer

    name: 異常原因剖析代理人

    role: Anomaly

    description: |

      在異常偵測結果基礎上，進一步推估各種異常的可能原因與對策。

    enabled: false

    default_model: gemini-2.5-flash-lite

    default_max_tokens: 8000

    default_prompt: |

      上游代理人已籠統列出多種異常與範例。



      你是一位根因分析顧問，請你：

      1. 對每種類型的異常（如極端值、重複紀錄、多次轉運）提出 2～3 個可能成因。

      2. 對每種成因，分別提出：

         - 建議檢查哪些系統紀錄或紙本文件

         - 建議與哪個角色單位（供應商/經銷商/醫院）進一步確認

      3. 以表格式或條列方式，整理「異常類型 → 可能原因 → 建議調查步驟」。



      回覆請用繁體中文，重點在實務可操作性。



  - id: data_quality

    name: 資料品質檢查代理人

    role: Data

    description: |

      檢視交易資料欄位是否完整、一致，並提出清理與補強建議。

    enabled: true

    default_model: gpt-4.1-mini

    default_max_tokens: 9000

    default_prompt: |

      你是一位資料品質管理專家。



      請根據提供的 CSV 資料：

      1. 檢查欄位 trade_date, src_name, dst_name, device_name, quantity 是否存在遺漏或格式不一的情況（可根據示意資料推估）。

      2. 假設實務中可能出現的常見問題（如日期格式不一、名稱拼寫不一致、數量為負值等），提出檢查規則。

      3. 建議一套「資料清理作業流程」，包含：

         - 自動檢測規則

         - 手動複核步驟

         - 修正紀錄留痕與版本控管建議

      4. 提出資料欄位擴充建議，以利後續追蹤（例如批號、批次、庫存位置等）。



      回覆以繁體中文條列。



  - id: traceability_validator

    name: 追溯性與可追蹤性檢查代理人

    role: Traceability

    description: |

      評估現有資料能否支援充分的批次追蹤與病人層級追蹤。

    enabled: false

    default_model: claude-3-5-sonnet-latest

    default_max_tokens: 12000

    default_prompt: |

      你是一位醫療器材追溯性專家。



      雖然目前資料僅顯示交易層級，請你：

      1. 評估在現有欄位下，若要追蹤到「特定批號」甚至「特定病人」，缺少哪些關鍵資訊。

      2. 針對供應商、經銷商與醫院，分別列出應加強記錄的欄位與識別碼（如批號、序號、病歷號）。

      3. 建議一個「最小可行追溯資料模型」，說明每筆交易至少應包含哪些欄位，以支援召回與風險評估。

      4. 就 TFDA 規範角度，補充為何追溯性對植入物特別重要。



      回覆以繁體中文分點說明。



  - id: bottleneck_detector

    name: 瓶頸節點與容量分析代理人

    role: Capacity

    description: |

      從交易量與結構中找出可能的供應瓶頸與容量限制節點。

    enabled: false

    default_model: gemini-2.5-flash

    default_max_tokens: 10000

    default_prompt: |

      你是一位供應鏈容量與瓶頸分析顧問。



      根據交易量與路徑，請你：

      1. 找出同時承擔大量出貨與進貨的「瓶頸節點」。

      2. 推估一旦該節點發生中斷（例如停工或系統故障），對下游醫療機構供應的影響範圍。

      3. 提出「備援節點」或「多元供應來源」的策略建議。

      4. 建議在儀表板與網路圖上，如何呈現瓶頸節點與替代路徑。



      請以繁體中文條列說明。



  - id: leadtime_analyst

    name: 交期與反應時間分析代理人

    role: LeadTime

    description: |

      針對交易日期與流向資訊，推估供應鏈的交期與應變速度。

    enabled: false

    default_model: gpt-4o-mini

    default_max_tokens: 9000

    default_prompt: |

      雖然目前資料未直接提供交期（Lead Time），你可以根據交易日期的分布，推估供應鏈反應速度的可能情況。



      你是一位交期分析師，請：

      1. 推測不同類型節點之間（供應商→經銷商、經銷商→醫院）的典型交期與補貨節奏。

      2. 說明若未來要精準監控交期，需額外蒐集哪些欄位（例如訂單日期、實際到貨日期）。

      3. 提出對乳房植入物供應特別重要的交期與庫存安全指標（如安全存量天數）。

      4. 建議如何在儀表板中呈現交期分布與異常延遲。



      回覆請用繁體中文。



  - id: scenario_planner

    name: 情境模擬與壓力測試代理人

    role: Scenario

    description: |

      協助規劃不同供應中斷或需求突增情境下的供應鏈壓力測試。

    enabled: false

    default_model: gemini-2.5-flash

    default_max_tokens: 12000

    default_prompt: |

      你是一位情境規劃與壓力測試顧問。



      請設計 2～3 個可能影響乳房植入物供應的情境，例如：

      - 某大供應商無預警停產

      - 某區域主要醫院需求量突然增加

      - 關鍵經銷商系統故障導致出貨延誤



      對每個情境：

      1. 說明受影響的主要節點與路徑。

      2. 評估可能導致的供應缺口與風險。

      3. 提出供應鏈重路徑或額外庫存安排建議。

      4. 建議在儀表板中如何快速切換或模擬這些情境（例如篩選特定節點、套用情境標記）。



      回覆請用繁體中文條列。



  - id: demand_forecast

    name: 需求趨勢與預測代理人

    role: Forecast

    description: |

      根據歷史交易量，為未來需求與供應規劃提供初步判斷。

    enabled: false

    default_model: gpt-4.1-mini

    default_max_tokens: 9000

    default_prompt: |

      你是一位需求預測顧問。



      依據目前提供的歷史出貨量（雖然時間區間與資料量有限），請你：

      1. 粗略判斷未來短期（例如 3～6 個月）需求可能的變化趨勢。

      2. 區分穩定需求與具波動性的產品或醫療機構。

      3. 提出針對高不確定性需求的庫存與合約策略建議。

      4. 建議若要進行更精準的預測，尚需哪些額外資料。



      回覆請以繁體中文簡要分析。



  - id: inventory_optimizer

    name: 庫存與補貨策略代理人

    role: Inventory

    description: |

      提出醫院與供應端的庫存與補貨策略建議，降低缺貨與過期風險。

    enabled: false

    default_model: gemini-2.5-flash-lite

    default_max_tokens: 8000

    default_prompt: |

      你是一位醫療器材庫存管理顧問。



      在不掌握實際庫存數據的前提下，請根據出貨與收貨頻率：

      1. 評估哪些醫院或經銷商可能採取高庫存策略、哪些可能採取低庫存或即時補貨策略。

      2. 說明乳房植入物在庫存管理上需特別注意的風險（如保存期限、批次管理、追蹤性）。

      3. 提出適用於此類醫材的庫存策略（如安全庫存、最小訂購量）。

      4. 建議未來系統中應新增哪些庫存欄位以利決策與風險控管。



      請用繁體中文條列。



  - id: vendor_risk_analyst

    name: 供應商風險評估代理人

    role: VendorRisk

    description: |

      評估不同供應商的依賴度與潛在風險。

    enabled: false

    default_model: claude-3-5-sonnet-latest

    default_max_tokens: 12000

    default_prompt: |

      你是一位供應商風險管理顧問。



      根據各供應端節點的交易量與覆蓋範圍：

      1. 找出被高度依賴的供應商/經銷商（出貨量或覆蓋醫院數最高）。

      2. 說明一旦該供應商發生問題（品質/營運/法規），對整體乳房植入物供應可能造成的影響。

      3. 建議分散風險的策略（如多元供應來源、第二供應商建立）。

      4. 提出在儀表板中如何視覺化呈現「供應商依賴度」與「風險分散程度」。



      回覆請用繁體中文。



  - id: hospital_behavior_analyst

    name: 醫院/診所行為分析代理人

    role: Hospital

    description: |

      分析醫院與診所在醫材採購與使用上的行為模式，協助監管與合作。

    enabled: false

    default_model: gpt-4o-mini

    default_max_tokens: 9000

    default_prompt: |

      你是一位醫院行為與採購分析顧問。



      根據交易資料，請你：

      1. 找出出貨量最高的醫院/診所，並評估其對整體市場的重要程度。

      2. 比較不同醫院的產品組合與供應來源多樣性。

      3. 說明哪些醫院的採購行為較為集中（單一供應來源）、哪些較為分散。

      4. 從監管與合作角度，對於採購高度集中的醫院提出風險與建議。



      回覆請用繁體中文條列。



  - id: quality_issue_detector

    name: 品質議題與投訴風險代理人

    role: Quality

    description: |

      雖無直接品質資訊，仍從流向與集中度推估可能的品質與投訴風險。

    enabled: false

    default_model: gemini-2.5-flash

    default_max_tokens: 10000

    default_prompt: |

      你是一位醫療器材品質與投訴風險顧問。



      在僅有供應鏈交易資訊的情況下，請推估：

      1. 哪些結構特徵可能暗示未來品質或投訴風險較高（例如高度集中於少數供應商與醫院）。

      2. 一旦某批產品出現品質瑕疵，如何藉由目前的流向資料快速圈定潛在受影響醫院與病人族群（概念性說明即可）。

      3. 建議蒐集哪些額外品質與投訴指標，以便結合供應鏈資料進行綜合分析。



      回覆請用繁體中文。



  - id: duplication_checker

    name: 重複紀錄與異常統計代理人

    role: Data

    description: |

      專注於找出可能的重複交易紀錄與統計異常，避免重複計算或誤判。

    enabled: false

    default_model: gpt-4.1-mini

    default_max_tokens: 8000

    default_prompt: |

      你是一位資料一致性與重複檢查專家。



      假設實務資料中可能存在重複上傳或重複紀錄，請：

      1. 說明可用於偵測重複紀錄的規則（例如完全相同的日期/來源/目的地/醫材/數量）。

      2. 分析若未移除重複紀錄，會對總出貨量與風險評估造成何種偏誤。

      3. 建議在系統層面建立哪些「防重複」機制（如唯一鍵設計、上傳前檢查）。



      回覆請用繁體中文。



  - id: fraud_detector

    name: 潛在舞弊模式偵測代理人

    role: Fraud

    description: |

      從交易結構與流向中，推測可能的舞弊或不當行為模式。

    enabled: false

    default_model: claude-3-5-sonnet-latest

    default_max_tokens: 12000

    default_prompt: |

      你是一位反舞弊與不當行為分析專家。



      在不指涉特定個案的前提下，請：

      1. 描述在醫療器材供應鏈中，常見的舞弊或不當行為模式（如虛構交易、異常轉銷、未合法申報等）。

      2. 自目前資料中，推測可能需特別留意的模式或結構（僅就統計與結構層面推估）。

      3. 為每種可能的模式，提出監控指標與警示規則建議。

      4. 建議如何將這些指標整合至儀表板與自動稽核流程。



      回覆請用繁體中文。



  - id: regulatory_monitor

    name: 法規變動與政策趨勢代理人

    role: Regulatory

    description: |

      從高層次角度，連結供應鏈監控需求與法規/政策變動趨勢。

    enabled: false

    default_model: gemini-2.5-flash

    default_max_tokens: 10000

    default_prompt: |

      你是一位醫療政策與法規趨勢分析顧問。



      雖然目前對法規內容僅能概略引用，請：

      1. 說明近年國際上對植入物追蹤與召回的監管趨勢（概略描述即可）。

      2. 將本系統可提供的供應鏈監控能力，對應到這些國際趨勢與 TFDA 可能重視的方向。

      3. 提出未來在系統與資料面應預先準備的項目，以因應法規可能的收緊或新要求。



      回覆請用繁體中文。



  - id: summary_narrative

    name: 整體敘事與簡報代理人

    role: Narrative

    description: |

      將多個代理人的結果統整為一份適合簡報或報告撰寫的敘事摘要。

    enabled: true

    default_model: gpt-4o-mini

    default_max_tokens: 12000

    default_prompt: |

      你是一位專業簡報與報告撰寫顧問。



      上游代理人已針對稽核、風險、物流、法規、視覺化等面向提出多項分析。請你：

      1. 將這些分析整合為一份有條理的「整體敘事摘要」，可供向主管或委員會簡報。

      2. 結構建議包含：

         - 背景與目的

         - 主要發現（含關鍵數據與指標）

         - 風險與問題點

         - 建議行動與後續計畫

      3. 僅需文字，不必包含圖表，但可標註「此處建議搭配某類圖表」的提示。



      請以繁體中文撰寫，並盡量控制在 2～3 頁簡報文字量級。



  - id: report_blueprint

    name: 報告架構設計代理人

    role: Reporting

    description: |

      將分析結果轉化為正式報告的章節架構與撰寫指引。

    enabled: false

    default_model: gemini-2.5-flash

    default_max_tokens: 10000

    default_prompt: |

      你是一位報告架構設計專家。



      請為「乳房植入物供應鏈稽核與風險分析」設計一份正式報告架構：

      1. 建議章節與小節標題。

      2. 每個章節應包含哪些內容與圖表。

      3. 提出撰寫注意事項與用詞建議（尤其是面向主管與外部審查單位的版本）。



      回覆請以繁體中文條列。



  - id: dashboard_coach

    name: 儀表板使用教練代理人

    role: UX

    description: |

      以使用者教育角度，說明如何有效使用本系統的各項圖表與代理人。

    enabled: false

    default_model: gpt-4.1-mini

    default_max_tokens: 8000

    default_prompt: |

      你是一位使用者教育與 UX 文案設計顧問。



      請撰寫一份「本系統使用教學」草稿，內容包含：

      1. 如何上傳與編輯供應鏈資料。

      2. 如何解讀網路圖、趨勢圖與儀表板上的各項指標。

      3. 如何選擇與執行不同類型的 AI 代理人。

      4. 如何將不同代理人輸出串接，形成完整的分析流程。

      5. 使用系統時需注意的資料隱私與安全重點。



      回覆請用繁體中文，適合作為線上說明文件或簡易操作手冊。



  - id: translator_multilingual

    name: 多語系說明翻譯代理人

    role: Translation

    description: |

      將關鍵分析結果與說明轉換為英語版本，方便國際溝通與合作。

    enabled: false

    default_model: gpt-4o-mini

    default_max_tokens: 8000

    default_prompt: |

      你是一位專精於醫療與監管領域的中英雙語翻譯。



      請將上游代理人的繁體中文分析與說明，翻譯成自然且專業的英文版本，同時：

      1. 保留關鍵專有名詞（如 TFDA）並給出適當英文對應。

      2. 避免過度直譯，確保閱讀流暢與專業度。

      3. 若原文資訊不足以精準對應，可採用中性、描述性語句補充。



      請以英文回覆。



  - id: meta_coordinator

    name: 代理人協作與流程總管

    role: Meta

    description: |

      協調其他代理人的順序與重點，建議最佳分析流程。

    enabled: true

    default_model: claude-3-5-sonnet-latest

    default_max_tokens: 12000

    default_prompt: |

      你是一位「代理人協作總管」，了解本系統中各種專業角色（稽核、物流、法規、風險、視覺化等）。



      請你：

      1. 根據目前可用的代理人清單與職責，設計 1～2 條「推薦分析流程」（例如：先由資料品質與基本稽核開始，再進入風險與法規、最後整合為報告）。

      2. 說明每個步驟應由哪幾個代理人負責，以及他們之間的上下游關係（哪些輸出應傳給下一位代理人）。

      3. 提出如何在介面上引導使用者遵循這些流程（例如預設流程按鈕、建議執行順序說明）。



      回覆請用繁體中文條列，並可輔以流程圖文字描述。

```



---



## 3. `requirements.txt`



```txt

streamlit>=1.37.0

pandas>=2.0.0

pyyaml>=6.0.1

altair>=5.0.0



# AI SDKs

openai>=1.35.0

google-generativeai>=0.8.0

anthropic>=0.34.0

requests>=2.31.0



# Network visualization

networkx>=3.2.0

pyvis>=0.3.2



# 可選：若日後要擴充型別驗證等

pydantic>=2.7.0

```



---



## 20 個後續深化問題（方便你調整下一版實作）



1. 這 31 個代理人的角色與描述中，有沒有你覺得過於重疊或不符合實際工作流程的，需要合併或刪減？  

2. 你是否希望在 UI 中對代理人做「分組顯示」（例如：稽核組、風險組、視覺化組），而不是單一長列表？  

3. 目前預設某些代理人是 disabled（enabled: false），你是否有特定想預設啟用的一組最小流程？  

4. 在 `agents.yaml` 中，你是否需要額外欄位（例如 `category`, `recommended_order`）來輔助 UI 排序與流程引導？  

5. app.py 中的網路圖目前用 NetworkX + Pyvis 當示範，你是否有計畫改用自己寫的 React+D3 component（若有，我可以幫你拆出 component 規格）？  

6. KPI 與儀表板區目前較精簡，你希望未來增加哪些具體指標（如特定醫院的 Top N 出貨、單一產品風險指標）？  

7. 多語系目前僅有少量字串，是否希望我幫你產出更完整的 EN 文案（側邊欄、提示、錯誤訊息等）？  

8. 你是否需要在 UI 顯示「目前使用的模型與供應商」摘要（例如在每個 Agent 卡片上顯示 provider logo）？  

9. 若要支援「報告匯出為 PDF 或 Markdown」，你偏好哪一種格式為主？是否需要自動嵌入代理人輸出的節選與圖表截圖？  

10. 關於 API Key，你是否希望在 UI 額外顯示「已偵測到環境金鑰」的小圖示於頁面頂部狀態列？  

11. 目前 `max_tokens` 上限依模型表建議，你是否希望再增加「溫度、top_p」等高級參數設定？  

12. 你是否考慮讓使用者在 UI 新增自訂代理人（寫入 session 但不寫回 agents.yaml），用於臨時分析？  

13. 若要在 Hugging Face Space 上開放給外部使用，你是否有預期的使用量與並發數，需不需要做任何 API 呼叫頻率控制？  

14. 目前串接 Grok API 僅示意 endpoint，你是否已經有 xAI 的正式文件與實際端點路徑，可以之後貼給我整合？  

15. 你有沒有內部的 TFDA 報表或審查格式範本，希望代理人（例如 `summary_narrative` 或 `report_blueprint`）的輸出更貼近那些格式？  

16. 在網路圖中，你是否需要特別標示「乳房植入物不同型號/規格」的差異，還是先以 device_name 為主即可？  

17. 你是否希望在 UI 中提供「篩選單一醫院/供應商」後，再執行 AI 分析，讓代理人只針對該子集資料做判斷？  

18. 若未來要加入登入或權限分級（例如稽核人員 vs 一般瀏覽者），你希望權限差異主要落在哪些功能上（執行 AI、下載資料、修改資料等）？  

19. 對 Wow UI 的視覺層面，你是否有任何既有品牌色（LOGO 顏色、TFDA 視覺規範）希望整合進 20 花卉主題中？  

20. 你打算先在內部 PoC 使用，還是會直接作為對外展示 Demo？這會影響我後續為你優化的錯誤訊息詳盡程度與教學說明密度。
