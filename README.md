# Agent Workflow

一個基於本地 LLM 的簡易 AI Agent，能自動判斷輸入文字的類型並做出對應處理。

## 功能

- **分類判斷**：自動識別輸入文字是否與資安（cybersecurity）相關
- **摘要生成**：若為資安相關內容，呼叫 LLM 進行摘要
- **一般回應**：非資安內容則直接回傳原始輸入

## 架構

```
輸入文字
   │
   ▼
analyze()  ─── 判斷類型（security / general）
   │
   ├── security ──► summarize() ──► [SECURITY SUMMARY]
   │
   └── general  ──────────────────► [GENERAL RESPONSE]
```

## 環境需求

- Python 3.x
- [Ollama](https://ollama.com/) 在本地運行，並載入 `gemma4` 模型

## 安裝與執行

```bash
# 安裝依賴
pip install requests

# 確保 Ollama 已啟動並載入模型
ollama run gemma4

# 執行 Agent
python agent.py
```

## 範例輸出

```
Input: Cybersecurity systems detect malware and prevent attacks.
Decision + Output: [SECURITY SUMMARY]: ...
```

## 模型設定

預設使用 `gemma4`，可在 `Agent.__init__()` 中修改 `self.model` 切換其他 Ollama 支援的模型。
