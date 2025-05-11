# LINE AI 助手

這是一個 LINE 瀏覽器擴充功能的 AI 助手，可以自動回覆 LINE 訊息。

## TODO
- [ ] 自動開啟 LINE 靜音 (fix web_manager.py -> close_alert)
- [ ] 將黑暗模式調整得更好看和完善
- [ ] 整理問答集，讓人格模擬的 assistant 可以更準確的模擬和回答問題
  - [ ] assistant 回答問題都只會重複話語，不會真的回話
- [ ] 建立各 OS 的執行檔

## 功能

- 自動監聽 LINE 訊息
- 使用 OpenAI GPT 生成回覆
- 自動填入回覆內容
- 深色模式支援

## 系統架構
| 檔案             | 功能                   |
| ---------------- | ---------------------- |
| main.py          | 主程式                 |
| web_manager.py   | 負責管理 LINE 擴充功能 |
| ai_functions.py  | 負責處理 AI 的回覆     |
| setup.py         | 負責安裝依賴項         |
| requirements.txt | 負責記錄依賴項         |

## 安裝

1. 安裝 Python，推薦 Python 3.8 以上版本
2. 安裝依賴項：
   ```
   python setup.py
   ```
3. 在 chrome 瀏覽器中安裝 LINE 擴充功能
4. 複製 `.env.example` 檔案為 `.env`，並填入您的設定：
   ```
   cp .env.example .env
   ```
5. 根據 [建立人格步驟](#建立人格步驟) 建立人格模擬 assistant
6. 編輯 `.env` 檔案，填入您的設定：
   - `EXTENSION_ID`：LINE 擴充功能的 ID
   - `EXTENSION_PATH`：LINE 擴充功能的路徑
   - `OPENAI_API_KEY`：OpenAI API 金鑰
   - `OPENAI_ASSISTANT_ID`：OpenAI Assistant ID

## 使用方法

1. 執行主程式：
   ```
   python main.py
   ```
2. 登入 LINE (我通常使用 QRCode 登入)
3. 在聊天室中點擊星星按鈕，AI 助手會自動回覆訊息
   1. 如果有想回復的方向，可以先寫好簡單的回覆在對話窗不要送出，再按下星星按鈕，AI 助手會自動回覆訊息
   2. 如果沒有想回復的方向，可以直接按下星星按鈕，AI 助手會自動回覆訊息

## 注意事項

- 請確保您的 OpenAI API 金鑰有效
- 請確保您的 LINE 擴充功能已正確安裝
- 請不要將 `.env` 檔案上傳到 git


# 建立人格步驟
1. 從 LINE 備份下載需要學習的對話紀錄.txt
   1. 我這邊放到了專案內的 private 資料夾
   2. **千萬注意資訊安全**，不要將此資料夾上傳到公開 git
2. 使用 OpenAI 的 Assistant 建立兩個新的 Assistant
   1. https://platform.openai.com/playground/assistants
   2. 一個作為人格分析，一個做為後面的回覆 assistant
3. 人格分析 assistant 
   1. 上傳所有對話紀錄檔案到 assistant 的 File Search，建立 Vector Database
   2. 將模型調整成 `gpt-4o-mini`
   3. 建立 System Instructions
```
你將扮演一位虛擬助手，專門模擬「沈政一 Dart」這個人。從 File Search 內的檔案能完整瀏覽並理解所有我提供的通訊軟體對話紀錄，目的是整理出他的語氣、說話風格、慣用語與人格特質，進而忠實地再現他在任何情境中的回應方式。

請根據這些紀錄，建構出「沈政一 Dart」的完整人格描述，包括：

1. **語氣特徵**：例如幽默、認真、挑釁、輕鬆、學術、熱情等。
2. **說話風格**：例如喜歡用比喻？習慣用縮寫？講話直接還是委婉？
3. **慣用語**：他經常使用的口頭禪、常見的句型或詞語。
4. **價值觀與反應傾向**：他對事情的看法（如樂觀、悲觀、中立）、處理衝突或表達情緒的方式。
5. **對特定主題的態度**：如工作、朋友、科技、人生等。
6. **文化或語言風格**：如果他有中英夾雜、台語、或其他語言使用習慣，也請標記出來。

最後，請將這些資訊整理成一段可以直接放入 System Instructions 的文字，讓語言模型能夠自然扮演出這個人格。
```
4. 人格模擬 assistant
   1. 將模型調整成 `gpt-4o-mini`
   2. 建立 System Instructions (將人格分析 assistant 產出的 System Instructions 複製過來)
```
你是一位專業技術人員，請以負責、冷靜、友善且誠實的方式協助處理問題。遇到技術或程序障礙時，詳細描述解決步驟並主動溝通需求。對同事或用戶保持親切回應，遇到交期壓力誠實反映，不隱瞞問題。如有需要合作或請教他人時，請主動協調並保持禮貌。鼓勵技術持續改進，對新知有開放態度。
```

# Build Application

## windows pyinstaller
```
pyinstaller --onefile --windowed --icon=icon.ico --name=LINE_AI-windows main.py
```
