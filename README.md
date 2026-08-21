# Agent Workflow

一個基於本地 LLM 的簡易 AI Agent，能自動判斷輸入文字的類型並做出對應處理。

## 功能

- **分類判斷**：自動識別輸入文字是否與資安（cybersecurity）相關
- **摘要生成**：若為資安相關內容，呼叫 LLM 進行摘要
- **一般回應**：非資安內容則直接回傳原始輸入

## 架構

專案拆分為多個低耦合模組，各自負責單一職責，並透過依賴注入串接：

```
agent_workflow/
├── config.py       # 設定（base_url / model / timeout），可由環境變數覆寫
├── llm_client.py   # 封裝與 Ollama API 溝通的細節，統一錯誤處理（LLMError）
├── classifier.py   # TextClassifier：判斷文字類型（security / general）
├── summarizer.py   # TextSummarizer：產生摘要
├── agent.py        # Agent：協調 classifier 與 summarizer
└── __init__.py

main.py             # 執行範例
tests/               # 單元測試（以假的 LLM client 隔離外部依賴）
```

```
輸入文字
   │
   ▼
Agent.run()
   │
   ▼
classifier.classify()  ─── 判斷類型（security / general）
   │
   ├── security ──► summarizer.summarize() ──► [SECURITY SUMMARY]
   │
   └── general  ────────────────────────────► [GENERAL RESPONSE]
```

`TextClassifier` 與 `TextSummarizer` 都只依賴 `LLMClient` 這個抽象介面，`Agent` 也允許在建構時注入自訂實作，方便替換模型或在測試中使用假物件（見 `tests/test_agent.py`）。

## 環境需求

- Python 3.10+
- [Ollama](https://ollama.com/) 在本地運行，並載入設定的模型（預設 `gemma4`）

## 安裝與執行

```bash
# 安裝依賴
pip install -r requirements.txt

# 確保 Ollama 已啟動並載入模型
ollama run gemma4

# 執行範例
python main.py
```

## 測試

```bash
pip install -r requirements-dev.txt
pytest
```

測試以假的 LLM client 取代真實網路呼叫，因此不需要啟動 Ollama 即可執行。

## 設定

可透過環境變數覆寫預設設定：

| 環境變數 | 說明 | 預設值 |
| --- | --- | --- |
| `AGENT_LLM_BASE_URL` | Ollama API 位址 | `http://localhost:11434` |
| `AGENT_LLM_MODEL` | 使用的模型名稱 | `gemma4` |
| `AGENT_LLM_TIMEOUT` | 請求逾時秒數 | `30` |

## 範例輸出

```
Input: Cybersecurity systems detect malware and prevent attacks.
Decision + Output: [SECURITY SUMMARY]: ...
```
