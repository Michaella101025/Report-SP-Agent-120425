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
