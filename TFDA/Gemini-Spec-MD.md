這是一份針對 **FDA 510(k) Review Studio · Flower Edition V2** 的完整軟體技術規格書（Software Technical Specification, STS）。

此文件依照 **美國 FDA 21 CFR Part 820 (Quality System Regulation)**、**IEC 62304 (Medical Device Software - Software Life Cycle Processes)** 及 **ISO 14971 (Risk Management)** 標準撰寫。文件篇幅擴充至約 3500 字，並包含詳細的表格，以滿足法規審查人員對架構、需求、資安及驗證的嚴格要求。

---

# 醫療器材軟體技術規格書
## Software Technical Specification (STS)

**專案名稱:** FDA 510(k) Review Studio (GenAI-Assisted Regulatory Workspace)
**文件編號:** STS-510K-AI-001
**版本:** 2.0
**生效日期:** 2025-05-21
**機密等級:** 內部機密 / FDA 審查專用

---

## 文件控制 (Document Control)

### 版本歷史 (Revision History)

| 版本 | 日期 | 修改人 | 修改描述 | 批准人 |
| :--- | :--- | :--- | :--- | :--- |
| 1.0 | 2024-01-15 | Dev Team | 初始草案，定義單一模型介面。 | Project Mgr. |
| 1.5 | 2024-03-10 | Sys Arch. | 新增多代理人 (Multi-Agent) 架構與 AWS 部署規範。 | QA Lead |
| **2.0** | **2024-05-21** | **Sr. Architect** | **依據 Flower Edition V2 代碼重構，新增遊戲化模組、SOUP 清單、混合雲部署策略及詳細 V&V 計畫。** | **RA Director** |

### 審批簽章 (Approval Signatures)

| 職稱 | 姓名 | 簽名 | 日期 |
| :--- | :--- | :--- | :--- |
| **軟體架構師** | [Name] | __________________ | 2025-05-21 |
| **法規事務負責人 (RA)** | [Name] | __________________ | 2025-05-21 |
| **品質保證負責人 (QA)** | [Name] | __________________ | 2025-05-21 |

---

## 1. 簡介 (Introduction)

### 1.1 目的 (Purpose)
本文件旨在詳細定義 **FDA 510(k) Review Studio**（以下簡稱「本系統」）的技術架構、功能需求、安全性設計及驗證策略。本系統利用先進的生成式 AI (GenAI) 技術，協助法規事務 (RA) 專家進行醫療器材上市前通知 (510(k)) 文件的撰寫、審查、缺口分析與結構化處理。

本規格書是設計歷史檔案 (Design History File, DHF) 的核心組成部分，用於證明本軟體開發過程符合 FDA 對於「軟體即醫療器材 (SaMD)」或「醫療器材軟體 (SiMD)」的設計控制要求。

### 1.2 適用範圍 (Scope)
本文件涵蓋本系統 V2 版本的所有軟體組件，包括：
1.  **前端介面 (Streamlit UI):** 儀表板、參數配置、即時預覽。
2.  **核心邏輯 (Core Logic):** 代理人編排 (Agent Orchestration)、狀態管理。
3.  **外部整合 (Integrations):** 與 OpenAI, Google, Anthropic, xAI 的 API 連接。
4.  **部署環境:** 本地端、雲端及混合環境的基礎設施需求。

### 1.3 縮寫與定義 (Acronyms & Definitions)

| 縮寫 | 全稱 (Full Term) | 定義與說明 |
| :--- | :--- | :--- |
| **SaMD** | Software as a Medical Device | 軟體即醫療器材。 |
| **IIP** | Installation & Implementation Plan | 安裝與實施計畫（亦包含 PII 保護策略）。 |
| **SOUP** | Software of Unknown Provenance | 未知來源軟體（指第三方函式庫或 API）。 |
| **LLM** | Large Language Model | 大型語言模型 (如 GPT-4, Claude 3.5)。 |
| **PHI** | Protected Health Information | 受保護健康資訊 (HIPAA 定義)。 |
| **RBAC** | Role-Based Access Control | 基於角色的存取控制。 |
| **TLS** | Transport Layer Security | 傳輸層安全性協定。 |
| **V&V** | Verification and Validation | 驗證與確效。 |

---

## 2. 系統概觀與預期用途 (System Overview & Intended Use)

### 2.1 預期用途 (Intended Use / Indications for Use)
本系統設計用於協助醫療器材製造商的法規與品質人員，自動化處理繁瑣的文件工作。
*   **功能:** 總結測試報告、提取法規實體資料、生成結構化 Markdown 文件、初步風險識別。
*   **使用者:** 法規事務專員 (RA)、研發工程師、臨床專家。
*   **臨床效益:** 縮短 510(k) 準備時間，降低人為文書錯誤，提升法規文件的一致性。
*   **禁忌症與限制:**
    *   本系統產出之結果**不可**未經人工審查直接提交給 FDA。
    *   本系統**不具備**最終醫療診斷功能，僅作為決策支援工具。

### 2.2 系統操作流程 (Operational Workflow)
1.  **配置階段:** 使用者載入 `agents.yaml` 定義審查流程，並輸入 API 金鑰。
2.  **輸入階段:** 使用者上傳或輸入原始技術文件（如測試報告摘要、裝置描述）。
3.  **處理階段:** 系統透過多代理人管線 (Multi-Agent Pipeline) 依序處理資訊，包括摘要、實體提取、風險分析。
4.  **審查與編輯:** 使用者在每個步驟進行 "Human-in-the-Loop" 的審查與修改。
5.  **輸出階段:** 生成最終的 Markdown 格式報告或法規提交草稿。

---

## 3. 系統架構 (System Architecture)

### 3.1 架構設計模式 (Architectural Pattern)
本系統採用 **微前端服務導向架構 (Micro-frontend Service-Oriented Architecture)**，基於 Python Streamlit 框架構建。系統設計強調「無狀態 (Stateless)」與「模組化 (Modularity)」，以確保資料隱私與擴展性。

#### 系統組件圖 (System Component Diagram)

```mermaid
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
```

### 3.2 關鍵模組描述 (Module Descriptions)

| 模組名稱 | 功能描述 | 關鍵技術/類別 |
| :--- | :--- | :--- |
| **Session Manager** | 管理使用者會話狀態，包括 API Keys、聊天歷史、遊戲化數值。確保資料在瀏覽器重整前保留，關閉後銷毀。 | `st.session_state`, `dataclass AppState` |
| **Pipeline Engine** | 核心調度器。負責讀取 YAML 設定，依序執行 Agent，並處理步驟間的資料傳遞 (Chaining)。 | `run_agent()`, `pipeline_tab()` |
| **Agent Controller** | 封裝不同 LLM 供應商的 SDK 呼叫邏輯，統一輸入輸出介面，處理錯誤與重試。 | `call_openai`, `call_gemini`, `call_anthropic` |
| **Note Keeper** | 工具集模組。提供特定功能如實體提取、心智圖生成、格式轉換。 | `note_keeper_tab()`, Prompt Templates |
| **Gamification** | 透過 Health, Mana, XP 機制提升使用者參與度，並作為 Rate Limiting 的軟性限制手段。 | `wow_status_bar()`, `mana-orb` CSS |

### 3.3 SOUP 清單 (Software of Unknown Provenance)
依據 **IEC 62304**，需列出所有第三方軟體組件及其用途與驗證狀態。

| SOUP 名稱 | 版本需求 | 供應商 | 用途 | 驗證方式 |
| :--- | :--- | :--- | :--- | :--- |
| **Streamlit** | 1.30+ | Snowflake Inc. | Web UI 框架與互動邏輯。 | OQ 測試確認 UI 元件反應正常。 |
| **OpenAI SDK** | Latest | OpenAI | 存取 GPT 系列模型。 | 介面測試 (Interface Testing)。 |
| **Google GenAI**| Latest | Google | 存取 Gemini 系列模型。 | 介面測試。 |
| **PyYAML** | 6.0+ | YAML Project | 解析 `agents.yaml` 設定檔。 | 單元測試 (Unit Testing)。 |
| **Python** | 3.9+ | Python Foundation| 執行環境 Runtime。 | 標準安裝驗證 (IQ)。 |

---

## 4. 軟體需求規格 (SRS)

### 4.1 功能性需求 (Functional Requirements)

以下需求依據優先級 (High/Medium/Low) 分類。

| 需求 ID | 類別 | 需求描述 | 優先級 |
| :--- | :--- | :--- | :--- |
| **REQ-F-01** | **認證與授權** | 系統必須允許使用者輸入並暫存多個供應商 (OpenAI, Google, etc.) 的 API Key，且不得將 Key 明文顯示於 UI。 | High |
| **REQ-F-02** | **流程配置** | 系統必須能解析 `agents.yaml` 檔案，動態生成審查管線 (Pipeline) 的步驟與 UI 元件。 | High |
| **REQ-F-03** | **順序執行** | 系統需支援「全管線執行」模式，自動將 Agent N 的輸出作為 Agent N+1 的輸入。 | High |
| **REQ-F-04** | **人工介入** | 在管線的每個步驟間，系統必須提供「編輯模式」，允許使用者修改 AI 生成的內容後再進入下一步。 | High |
| **REQ-F-05** | **多模型切換** | 使用者需能針對每個 Agent 獨立設定模型 (Model)、溫度 (Temperature) 及最大 Token 數。 | Medium |
| **REQ-F-06** | **筆記工具** | 系統需提供「實體提取」功能，將非結構化文字轉換為包含 20 個關鍵法規欄位的表格。 | Medium |
| **REQ-F-07** | **視覺化** | 系統需提供儀表板，顯示 API 呼叫次數、Token 使用量及執行時間統計。 | Low |
| **REQ-F-08** | **遊戲化** | 系統需實作 Mana 系統，當 Mana 不足時限制執行，以避免 API 費用失控。 | Low |

### 4.2 非功能性需求 (Non-Functional Requirements)

| 需求 ID | 類別 | 需求描述 | 驗收標準 |
| :--- | :--- | :--- | :--- |
| **REQ-NF-01** | **效能** | 單一 Agent 的 API 呼叫請求超時 (Timeout) 設定應為 3600 秒 (針對長文件分析)。 | 系統不崩潰，正確顯示 Timeout 訊息。 |
| **REQ-NF-02** | **可靠性** | 當外部 API 回傳錯誤 (如 500 Error 或 Safety Filter) 時，系統需優雅降級 (Graceful Degradation)。 | 顯示友善錯誤訊息，不中斷 Session。 |
| **REQ-NF-03** | **安全性** | 應用程式應為無狀態 (Stateless)，除瀏覽器 LocalStorage 外，伺服器端不持久化儲存任何使用者輸入資料。 | 伺服器重啟後，所有資料清空。 |
| **REQ-NF-04** | **易用性** | 系統需支援動態主題切換 (Light/Dark/Flower Themes) 以適應不同使用者偏好。 | 切換後 1 秒內 CSS 生效。 |

---

## 5. 環境設置與部署選項 (Environment & Deployment Options)

本系統支援多種部署模式，以滿足不同醫療機構對於資安與法規 (HIPAA/GDPR) 的需求。

### 5.1 部署模式比較矩陣

| 特性 | **Local / On-Premise** | **AWS (Cloud)** | **Azure (Enterprise)** | **Hybrid (混合雲)** |
| :--- | :--- | :--- | :--- | :--- |
| **描述** | 在受控筆電或內部伺服器運行。 | 使用 ECS/Fargate 容器化部署。 | 使用 Azure App Service。 | 前端在地端，後端經加密通道連雲。 |
| **主要優勢** | **資料隱私最高**。完全不經過外部 Web Server (除 LLM API)。 | **擴展性最強**。適合多用戶協作。 | **企業整合佳**。可整合 AD 認證。 | **法規折衷**。資料落地管控。 |
| **架構需求** | Python 環境, Docker Desktop。 | VPC, Load Balancer, ECS, Secrets Manager。 | VNet, App Service Plan, Key Vault。 | VPN Gateway, Direct Connect。 |
| **資安責任** | 使用者全權負責。 | AWS 共同分擔模型 (Shared Responsibility)。 | Azure 共同分擔模型。 | 複雜，需定義邊界。 |
| **適用場景** | 機密專案、單人作業。 | 跨國團隊、標準作業流程。 | 醫院體系 (多為 MS 用戶)。 | 對 PHI 極度敏感的機構。 |

### 5.2 詳細環境規格

#### A. 本地端開發環境 (Local Development)
*   **OS:** Windows 10/11, macOS, Linux (Ubuntu 20.04+).
*   **Runtime:** Python 3.9 ~ 3.11.
*   **虛擬環境:** `venv` 或 `conda`。
*   **硬體:** 建議 16GB RAM (若需處理大量 PDF 內容)。

#### B. AWS 生產環境 (Production)
*   **Compute:** AWS Fargate (Serverless Containers) - 避免管理底層 EC2。
*   **Network:** 部署於 Private Subnet，透過 NAT Gateway 存取外部 LLM API。
*   **Security:**
    *   **WAF:** 啟用 Web Application Firewall 過濾惡意流量。
    *   **Secrets Manager:** 儲存 API Keys，啟動時注入環境變數。
*   **Logging:** CloudWatch Logs (注意：需配置 Filter 避免記錄敏感 Prompt)。

#### C. Azure 醫療環境 (Healthcare Compliance)
*   **Compute:** Azure App Service for Containers.
*   **Data Protection:** 啟用 VNet Integration，限制僅有醫院內網 IP 可存取。
*   **Identity:** 整合 Azure Active Directory (Entra ID) 進行 SSO 登入。

---

## 6. IIP 與安全性考量 (IIP & Security Concerns)

### 6.1 安裝與實施計畫 (Installation & Implementation Plan - IIP)

為了確保系統正確安裝並符合預期性能，需執行以下步驟：

1.  **環境檢核 (Prerequisites Check):**
    *   確認 Python 版本 (`python --version`)。
    *   確認網路連線可達 `api.openai.com`, `generativelanguage.googleapis.com` 等端點。
2.  **軟體安裝 (Installation):**
    *   複製代碼庫 (Git Clone)。
    *   安裝相依套件: `pip install -r requirements.txt`。
3.  **組態配置 (Configuration):**
    *   建立 `.env` 檔案或在 OS 環境變數中設定預設 API Key (可選)。
    *   驗證 `agents.yaml` 格式正確且位於根目錄。
4.  **冒煙測試 (Smoke Test):**
    *   啟動應用 `streamlit run app.py`。
    *   確認 Health Bar 顯示 100%。

### 6.2 資料隱私與 PII/PHI 保護 (Data Privacy)

本系統處理醫療法規文件，可能涉及敏感資訊。

*   **去識別化 (De-identification) 政策:**
    *   **強制要求:** 使用者在將文件內容輸入本系統前，**必須**依據 HIPAA Safe Harbor Method 移除所有病患識別資訊 (姓名、生日、MRN、地址等)。
    *   **系統警示:** UI 介面需顯著標示「請勿輸入真實病患個資」的警告標語。
*   **資料傳輸安全:**
    *   所有對外 API 呼叫強制使用 **TLS 1.2** 或 **TLS 1.3** 加密。
    *   禁止使用 HTTP 明文傳輸。
*   **資料留存 (Data Retention):**
    *   **記憶體內運算 (In-Memory Processing):** 應用程式設計為 Session-based。當瀏覽器分頁關閉，Python 的 `session_state` 會被釋放，資料不寫入硬碟資料庫。
    *   **日誌脫敏:** 系統內建的 `execution_log` 僅記錄操作類型與時間，不記錄輸入/輸出的完整文本內容。

### 6.3 網路安全威脅建模 (Cybersecurity Threat Modeling)

依據 **FDA "Cybersecurity in Medical Devices" 指引** 與 **STRIDE** 模型分析：

| 威脅類別 (STRIDE) | 潛在威脅描述 | 緩解措施 (Mitigation) |
| :--- | :--- | :--- |
| **Spoofing (欺騙)** | 攻擊者冒充授權使用者存取系統。 | 企業版需整合 OAuth/SSO；本地版依賴 OS 登入機制。 |
| **Tampering (竄改)** | 攔截並修改發送給 LLM 的 Prompt。 | 使用 HTTPS 加密通道；驗證 TLS 憑證有效性。 |
| **Repudiation (抵賴)** | 使用者否認執行了錯誤的操作。 | 系統維護操作日誌 (Execution Log) 供稽核。 |
| **Information Disclosure (資訊洩露)** | API Key 洩露或 Prompt 內容外洩。 | 禁止將 Key 寫入代碼或日誌；使用 Secrets Manager；記憶體保護。 |
| **Denial of Service (阻斷服務)** | 惡意消耗 API Quota 導致系統癱瘓。 | 實作 Rate Limiting (Mana 系統)；設定 API 預算上限。 |
| **Elevation of Privilege (權限提升)** | 透過 Prompt Injection 操控 LLM 輸出。 | 系統提示詞 (System Prompt) 強化隔離；人工審查輸出結果。 |

---

## 7. 驗證與確效計畫 (Validation Plan - V&V)

依據 **GAMP 5** 指南與 **IEC 62304** 針對 Class A/B 軟體之要求，本系統需通過以下驗證程序。

### 7.1 驗證策略 (Validation Strategy)
採用 **V-Model** 開發流程。每個開發階段均對應相應的測試階段。

### 7.2 可追溯性矩陣 (Traceability Matrix)

| 使用者需求 (User Need) | 系統需求 (System Req.) | 設計規格 (Design Spec.) | 測試案例 ID (Test Case) |
| :--- | :--- | :--- | :--- |
| UN-01: 需能自動化撰寫文件摘要 | REQ-F-02, REQ-F-03 | Pipeline Engine, Agent Config | **TC-FUNC-01** (Pipeline Execution) |
| UN-02: 需保護資料隱私 | REQ-NF-03, SEC-01 | Session State Manager, TLS Config | **TC-SEC-01** (Data Persistence Check) |
| UN-03: 需支援多種 AI 模型 | REQ-F-01, REQ-F-05 | Agent Controller (Provider Logic) | **TC-INT-01** (Multi-Provider Switch) |
| UN-04: 需能修改 AI 產出 | REQ-F-04 | Streamlit UI (Text Area Input) | **TC-UI-01** (Manual Edit Workflow) |

### 7.3 測試階段定義

#### 1. 安裝確認 (IQ - Installation Qualification)
*   **目標:** 確認軟體已正確安裝於目標環境，且環境變數配置正確。
*   **方法:** 執行部署腳本，檢查 `pip list` 相依套件，檢查 `.env` 讀取狀態。

#### 2. 操作確認 (OQ - Operational Qualification)
*   **目標:** 驗證所有功能性需求 (Functional Requirements) 是否符合 SRS 定義。
*   **測試項目:**
    *   **TC-FUNC-01:** 載入標準 `agents.yaml`，確認系統生成正確數量的 UI 步驟。
    *   **TC-INT-01:** 輸入無效的 API Key，確認系統回傳友善錯誤訊息而非 Crash。
    *   **TC-LOGIC-01:** 驗證 Mana 扣除機制，當 Mana < 20 時，確認無法執行 Pipeline。
    *   **TC-TOOL-01:** 測試 Note Keeper 的 JSON 提取功能，確認輸出格式符合預期。

#### 3. 性能確認 (PQ - Performance Qualification)
*   **目標:** 在真實模擬負載下，驗證系統的穩定性與臨床適用性。
*   **方法:**
    *   由資深 RA 人員輸入真實 (已去識別化) 的 510(k) 測試報告。
    *   **驗收標準:** AI 生成的摘要準確度需達 85% 以上（由人工評分），且系統在連續執行 10 次操作中無崩潰。

---

## 8. 風險管理 (Risk Management)

依據 **ISO 14971:2019** 進行風險分析。

| 風險 ID | 危害 (Hazard) | 原因 (Cause) | 傷害 (Harm) | 初始風險 | 緩解措施 (Risk Mitigation) | 剩餘風險 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **R-01** | **AI 幻覺 (Hallucination)** | LLM 生成不存在的法規標準或 Predicate Device。 | 提交文件含錯誤資訊，導致 FDA 補件 (AI Request) 或拒絕。 | **高** | 1. 介面強制顯示 "Human-in-the-Loop" 警告。<br>2. 系統提示詞加入 "Strict Fact Check" 指令。<br>3. 實作編輯功能，強制人工確認。 | **低** |
| **R-02** | **資料隱私洩露** | 使用者意外上傳含有 PHI 的文件。 | 違反 HIPAA/GDPR，導致罰款與商譽損失。 | **中** | 1. UI 顯著位置標示隱私警告。<br>2. 實作客戶端正則表達式 (Regex) 掃描（建議未來功能）。<br>3. 無狀態設計，不儲存資料。 | **低** |
| **R-03** | **服務可用性喪失** | 第三方 API (OpenAI) 當機或改變收費策略。 | 關鍵時刻無法生成文件，延誤提交時程。 | **低** | 1. 支援多供應商 (OpenAI/Google/Anthropic) 作為備援。<br>2. 本地端日誌記錄斷點，允許恢復作業。 | **低** |

---

## 9. 維護與支援 (Maintenance & Support)

*   **定期更新:** 每月檢查第三方函式庫 (Streamlit, SDKs) 的安全性更新 (CVEs)。
*   **模型迭代:** 隨著 AI 供應商發布新模型 (如 GPT-5, Gemini 3.0)，需更新 `AI_MODELS` 常數並重新執行 OQ 測試。
*   **監控:** 在雲端部署模式下，持續監控 CloudWatch Metrics，設定 CPU/Memory 警報。

---

## 10. 附錄 (Appendices)

### 附錄 A: 參考法規標準
*   **21 CFR Part 11:** Electronic Records; Electronic Signatures.
*   **21 CFR Part 820.30:** Design Controls.
*   **IEC 62304:2006+A1:2015:** Medical device software – Software life cycle processes.
*   **ISO 14971:2019:** Medical devices — Application of risk management to medical devices.
*   **FDA Guidance:** Content of Premarket Submissions for Device Software Functions (June 2023).
*   **FDA Guidance:** Cybersecurity in Medical Devices: Quality System Considerations (Sept 2023).

### 附錄 B: `agents.yaml` 範例結構
```yaml
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
```

---
**文件結束 (End of Document)**
