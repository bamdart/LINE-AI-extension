import openai
import time
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 從環境變數讀取常數

_API_KEY = os.getenv("OPENAI_API_KEY")
_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")


def setup_openai():
    openai.api_key = _API_KEY


def chat_with_gpt(messages, input_prompt=None):
    """
    使用 OpenAI Assistant API 與 GPT 對話

    Args:
        messages: 訊息列表，每個訊息包含 sender 和 content
        input_prompt: 輸入提示詞

    Returns:
        str: GPT 的回應
    """
    try:
        # 建立一個新的對話執行緒
        thread = openai.beta.threads.create()

        # 添加訊息到執行緒
        content = ""
        for msg in messages:
            content += f"{msg['sender']}: {msg['content']}\n"

        if input_prompt:
            content += f"\n{input_prompt}"

        print(f"content:\n{content}")

        openai.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=content
        )

        # 執行 Assistant
        run = openai.beta.threads.runs.create(
            thread_id=thread.id, assistant_id=_ASSISTANT_ID
        )

        # 等待執行完成
        while True:
            run_status = openai.beta.threads.runs.retrieve(
                thread_id=thread.id, run_id=run.id
            )
            if run_status.status == "completed":
                break
            elif run_status.status in ["failed", "cancelled", "expired"]:
                raise Exception(f"Assistant 執行失敗: {run_status.status}")
            time.sleep(0.1)

        # 獲取回應
        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        latest_message = messages.data[0]

        return latest_message.content[0].text.value

    except Exception as e:
        print(f"與 GPT 對話時發生錯誤: {e}")
        return None


def process_messages_with_gpt(messages_list, input_text=None, reply_message=None):
    """
    處理訊息列表並獲取 GPT 回應

    Args:
        messages_list: 訊息列表
        input_text: 輸入框中的文字

    Returns:
        str: GPT 的回應
    """
    if not messages_list:
        return None

    # 如果輸入框有內容，將其加入到提示詞中
    input_prompt = None
    if input_text:
        input_prompt = f"這是我準備回復上面對話的訊息，幫我修飾並填充內容：{input_text}"

    if reply_message:
        input_prompt = f"這是我主要希望回復的訊息，請針對這個對話來回復：\"{reply_message['username']}: {reply_message['message']}\""

    # 獲取 GPT 回應
    response = chat_with_gpt(messages_list, input_prompt)
    return response
