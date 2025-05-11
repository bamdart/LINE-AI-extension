import time

from ai_functions import setup_openai, process_messages_with_gpt
from web_manager import LINEDriver


def main():
    setup_openai()
    # 初始化 WebDriver
    driver = LINEDriver()

    try:
        # 開啟 LINE 擴充功能頁面
        driver.open_line_extension_page()

        print("請確保您已經在 LINE 擴充功能中登入...")
        print("等待進入聊天室...")


        # 等待網址變化
        current_url = driver.get_current_url()
        while True:
            new_url = driver.get_current_url()
            if new_url != current_url:
                current_url = new_url
                # driver.close_alert()
                driver.add_star_button()
                driver.set_dark_mode()

            # 等待星星按鈕被點擊
            while not driver.check_star_button_clicked():
                new_url = driver.get_current_url()
                if new_url != current_url:
                    break
                time.sleep(0.1)

            if new_url != current_url:
                continue

            print("星星按鈕已點擊，開始監聽訊息...")
            messages_list = driver.monitor_messages()
            if len(messages_list) > 30:
                print(f"對話過長，從 {len(messages_list)} 筆取最新 30 筆")
                messages_list = messages_list[-30:]
            # print(messages_list)
            
            reply_message = driver.get_reply_area()
            # print(reply_message)

            input_text = driver.get_input_text()

            # 獲取 GPT 回應
            gpt_response = process_messages_with_gpt(messages_list, input_text, reply_message)
            if gpt_response:
                print("\nGPT 回應:")
                print(gpt_response)
                print("-" * 50)

                # 將回應填入輸入框
                success = driver.fill_response_in_input(gpt_response)
                if not success:
                    print("無法填入回應，請手動複製以下文本:")
                    print(gpt_response)

            # 重置按鈕狀態
            driver.reset_button_state()

            time.sleep(0.1)

    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
