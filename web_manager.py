from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

load_dotenv()

_EXTENSION_ID = os.getenv("EXTENSION_ID")
_EXTENSION_PATH = os.getenv("EXTENSION_PATH")


class LINEDriver:
    def __init__(self):
        """設置並返回 WebDriver 實例"""
        # 設定 Chrome 選項
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")

        # 添加 LINE 擴充功能
        chrome_options.add_argument(f"--load-extension={_EXTENSION_PATH}")

        # 初始化 WebDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        # 設置深色模式
        self.set_dark_mode()

    def set_dark_mode(self):
        """
        設置瀏覽器的深色模式，將背景改為黑色，文字改為白色
        """
        try:
            # 使用 JavaScript 注入 CSS 樣式
            self.driver.execute_script(
                """
                // 定義顏色變數
                const COLORS = {
                    BLACK: '#1E1E1E',      // 深灰色背景
                    GRAY: '#2D2D2D',       // 次要背景色
                    WHITE: '#E0E0E0',      // 柔和的白色文字
                    LIGHT_GRAY: '#3D3D3D', // 較淺的灰色
                    ACCENT: '#4A9EFF'      // 強調色
                };
                
                // 創建樣式元素
                var style = document.createElement('style');
                style.type = 'text/css';
                style.innerHTML = `                 
                    .positive_button_first {
                        background-color: ${COLORS.BLACK} !important;
                    }
                    
                    .chatroomEditor-module__textarea__yKTlH {
                        background-color: ${COLORS.BLACK} !important;
                        color: ${COLORS.WHITE} !important;
                        border: 1px solid ${COLORS.LIGHT_GRAY} !important;
                    }
                    
                    .searchInput-module__input_box__vp6NF {
                        background-color: ${COLORS.BLACK} !important;
                    }
                    
                    .searchInput-module__label__40CWI {
                        background-color: ${COLORS.GRAY} !important;
                    }
                    
                    /* 已讀訊息數 */
                    .metaInfo-module__read_count__8-U6j {
                        color: ${COLORS.LIGHT_GRAY} !important;
                    }
                    
                    /* 訊息時間 */
                    .metaInfo-module__send_time__-3Q6- {
                        color: ${COLORS.LIGHT_GRAY} !important;
                    }
                    
                    .chatroomHeader-module__name__t-K11 {
                        color: ${COLORS.WHITE} !important;
                    }
                    
                    .chatlistItem-module__title_box__aDNJD {
                        color: ${COLORS.WHITE} !important;
                    }
                    
                    .categoryLayout-module__category_wrap__31191 {
                        background-color: ${COLORS.BLACK} !important;
                    }
                    
                    .friendlistItem-module__text__YxSko {
                        color: ${COLORS.WHITE} !important;
                    }
                    
                    .folderTab-module__tab_item__7dbuI[aria-selected="true"] {
                        color: ${COLORS.LIGHT_GRAY} !important;
                    }

                    /* AI 助手按鈕樣式 */
                    #ai-assistant-star-btn svg path {
                        stroke: ${COLORS.WHITE} !important;
                    }

                    #ai-assistant-star-btn[data-activated="true"] {
                        pointer-events: none !important;
                        /* 不斷旋轉的動畫 */
                        animation: spin 1s linear infinite;
                    }

                    #ai-assistant-star-btn[data-activated="true"] svg path {
                        stroke: ${COLORS.GRAY} !important;
                    }

                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                `;
                
                // 將樣式添加到文檔頭部
                document.head.appendChild(style);
            """
            )

            return True
        except Exception as e:
            print(f"設置深色模式時發生錯誤: {e}")
            return False

    def open_line_extension_page(self):
        # 開啟 LINE 擴充功能頁面
        self.driver.get(f"chrome-extension://{_EXTENSION_ID}/index.html")

    def get_current_url(self):
        """獲取當前頁面 URL"""
        return self.driver.current_url

    def get_input_text(self):
        """
        獲取輸入框中的文字內容

        Args:
            driver: WebDriver 實例

        Returns:
            str: 輸入框中的文字，如果為空則返回空字符串
        """
        try:
            # 找到textarea-ex元素
            textarea_ex = self.driver.find_element(
                By.CSS_SELECTOR, "textarea-ex.chatroomEditor-module__textarea__yKTlH"
            )

            # 使用JavaScript獲取Shadow DOM中的textarea內容
            input_text = self.driver.execute_script(
                """
                var textareaEx = arguments[0];
                var shadowRoot = textareaEx.shadowRoot;
                if (!shadowRoot) return '';
                
                var textarea = shadowRoot.querySelector('textarea');
                if (!textarea) return '';
                
                return textarea.value || '';
                """,
                textarea_ex,
            )

            return input_text.strip()
        except Exception as e:
            print(f"獲取輸入框內容時發生錯誤: {e}")
            return ""

    def fill_response_in_input(self, response_text):
        """
        將 GPT 回應填入指定的輸入框

        Args:
            driver: WebDriver 實例
            response_text: 要填入的文本
        """
        try:
            print("嘗試填入回應...")

            # 找到textarea-ex元素
            textarea_ex = self.driver.find_element(
                By.CSS_SELECTOR, "textarea-ex.chatroomEditor-module__textarea__yKTlH"
            )

            # 使用JavaScript處理Shadow DOM
            self.driver.execute_script(
                """
                var textareaEx = arguments[0];
                var text = arguments[1];
                
                // 獲取Shadow DOM
                var shadowRoot = textareaEx.shadowRoot;
                if (!shadowRoot) {
                    console.error('無法獲取Shadow DOM');
                    return false;
                }
                
                // 在Shadow DOM中查找textarea
                var textarea = shadowRoot.querySelector('textarea');
                if (!textarea) {
                    console.error('無法在Shadow DOM中找到textarea');
                    return false;
                }
                
                // 設置值
                textarea.value = text;
                
                // 觸發必要的事件
                var inputEvent = new Event('input', { bubbles: true, composed: true });
                textarea.dispatchEvent(inputEvent);
                
                var changeEvent = new Event('change', { bubbles: true, composed: true });
                textarea.dispatchEvent(changeEvent);
                
                // 更新父元素的data-is-empty屬性
                textareaEx.setAttribute('data-is-empty', 'false');
                
                return true;
            """,
                textarea_ex,
                response_text,
            )

            print("已將回應填入輸入框")
            return True

        except Exception as e:
            print(f"填入回應時發生錯誤: {e}")

            # 嘗試備用方法
            try:
                # 使用JavaScript直接操作Shadow DOM
                result = self.driver.execute_script(
                    """
                    var textareaEx = document.querySelector('textarea-ex.chatroomEditor-module__textarea__yKTlH');
                    if (!textareaEx) return false;
                    
                    var shadowRoot = textareaEx.shadowRoot;
                    if (!shadowRoot) return false;
                    
                    var textarea = shadowRoot.querySelector('textarea');
                    if (!textarea) return false;
                    
                    textarea.value = arguments[0];
                    
                    var inputEvent = new Event('input', { bubbles: true, composed: true });
                    textarea.dispatchEvent(inputEvent);
                    
                    return true;
                """,
                    response_text,
                )

                if result:
                    print("使用備用方法已將回應填入輸入框")
                    return True
                else:
                    print("備用方法失敗: 無法找到元素")
                    return False

            except Exception as e2:
                print(f"備用方法也失敗: {e2}")
                return False

    def add_star_button(self):
        """
        在截取畫面按鈕旁邊添加星星按鈕

        Args:
            driver: WebDriver 實例
        """
        try:
            # 使用JavaScript添加星星按鈕
            self.driver.execute_script(
                """
                // 檢查按鈕是否已存在
                if (document.getElementById('ai-assistant-star-btn')) {
                    return;
                }
                
                // 找到編輯區域
                const editorArea = document.querySelector('.chatroomEditor-module__editor_area__1UsgR');
                if (!editorArea) {
                    console.error('無法找到編輯區域');
                    return;
                }
                
                // 找到按鈕容器
                const actionBox = editorArea.querySelector('.actionGroup-module__action_box__-HA8N');
                if (!actionBox) {
                    console.error('無法找到按鈕容器');
                    return;
                }
                
                // 找到截取畫面按鈕
                const captureButton = actionBox.querySelector('button[data-type="capture"]');
                if (!captureButton) {
                    console.error('無法找到截取畫面按鈕');
                    return;
                }
                
                // 創建星星按鈕
                const starButton = document.createElement('button');
                starButton.type = 'button';
                starButton.id = 'ai-assistant-star-btn';
                starButton.className = 'actionGroup-module__button_action__VwNgx';
                starButton.setAttribute('aria-label', 'AI Assistant');
                starButton.setAttribute('data-type', 'ai-assistant');
                starButton.setAttribute('data-tooltip', 'AI助手');
                starButton.setAttribute('data-tooltip-placement', 'top-start');
                
                // 創建星星圖標
                const icon = document.createElement('i');
                icon.className = 'icon';
                icon.innerHTML = `
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 2L14 10L22 12L14 14L12 22L10 14L2 12L10 10L12 2Z" stroke="#303030" stroke-width="1.5" fill="none"/>
                    </svg>
                `;
                
                // 添加按鈕到頁面
                starButton.appendChild(icon);
                actionBox.insertBefore(starButton, captureButton.nextSibling);
                
                // 添加點擊事件
                starButton.addEventListener('click', function() {
                    // 設置全局標記，表示已點擊
                    window.aiAssistantActivated = true;
                    
                    starButton.setAttribute('data-activated', 'true');
                });
                
                console.log('已添加星星按鈕');
                """
            )

            return True
        except Exception as e:
            print(f"添加星星按鈕時發生錯誤: {e}")
            return False

    def check_star_button_clicked(self):
        """
        檢查星星按鈕是否被點擊

        Args:
            driver: WebDriver 實例

        Returns:
            bool: 按鈕是否被點擊
        """
        try:
            result = self.driver.execute_script(
                """
                return window.aiAssistantActivated === true;
            """
            )
            return result
        except:
            return False

    def extract_message_info(self, message_element):
        """從訊息元素中提取資訊"""
        try:
            # 從 data-message-content-prefix 獲取時間和人名
            prefix = message_element.get_attribute("data-message-content-prefix")
            if not prefix:
                return None

            # 分割時間和人名 (格式: "HH:MM 名字 ")
            parts = prefix.strip().split(" ", 1)
            if len(parts) != 2:
                return None

            send_time = parts[0]
            sender = parts[1].strip()

            # 嘗試獲取訊息內容（文字、圖片或連結）
            content = None

            # 檢查是否為文字訊息
            try:
                text_element = message_element.find_element(
                    By.CLASS_NAME, "textMessageContent-module__text__EFwEN"
                )

                content = text_element.text.strip()

                if content == "":
                    text_element = text_element.find_element(
                        By.CLASS_NAME, "textMessageContent-module__content_wrap__238E1"
                    )
                    content = text_element.text.strip()
            except:
                pass

            # 如果內容為空，返回 None
            if not content:
                return None

            return {"sender": sender, "content": content, "time": send_time}
        except Exception as e:
            print(f"提取訊息時發生錯誤: {e}")
            return None

    def monitor_messages(self):
        """監聽新訊息"""
        processed_messages = set()
        messages_list = []

        try_count = 10
        while try_count > 0:
            try:
                # 找到所有訊息元素
                message_elements = self.driver.find_elements(
                    By.CLASS_NAME, "message-module__message__7odk3"
                )

                for message in message_elements:
                    # 使用訊息 ID 作為唯一標識
                    message_id = message.get_attribute("data-message-select-id")

                    if message_id and message_id not in processed_messages:
                        message_info = self.extract_message_info(message)
                        if message_info:
                            messages_list.insert(0, message_info)
                            processed_messages.add(message_id)

                if len(messages_list) > 0:
                    break

                time.sleep(1)  # 每秒檢查一次

            except Exception as e:
                print(f"監聽訊息時發生錯誤: {e}")
                time.sleep(1)

            try_count -= 1

        return messages_list

    def get_reply_area(self):
        """獲取回復區域"""
        try:
            reply_area = self.driver.find_element(
                By.CLASS_NAME, "replyTargetMessage-module__reply_target_message__Sw1D8"
            )

            if not reply_area:
                print("無指定回復訊息")
                return None

            username = reply_area.find_element(
                By.CLASS_NAME, "username-module__username__vGQGj"
            )

            username_text = username.find_element(By.TAG_NAME, "span").text.strip()

            message = reply_area.find_element(
                By.CLASS_NAME, "replyMessageContent-module__text__0T50-"
            )

            # text in message span element
            message_text = message.find_element(By.TAG_NAME, "span").text.strip()

            return {"username": username_text, "message": message_text}

        except Exception as e:
            print(f"獲取回復區域時發生錯誤: {e}")
            return None

        return None

    def close_alert(self):
        """
        找到 button class gnb-module__button_action__aTdj7
        如果 button class 的 data-tooltip="開啟所有提醒" 代表已靜音
        點擊 button class actionPopoverListItem-module__button_action__mHl56
        """
        try:
            check_button = self.driver.find_element(
                By.CLASS_NAME, "gnb-module__button_action__aTdj7"
            )
            if not check_button:
                raise Exception("找不到靜音按鈕")

            tooltip = check_button.get_attribute("data-tooltip")
            if tooltip == "開啟所有提醒":
                print("已靜音")
                return True

            check_button.click()

            # driver wait 0.3 second
            time.sleep(0.3)

            action_button = self.driver.find_element(
                By.CLASS_NAME, "actionPopoverListItem-module__button_action__mHl56"
            )

            action_button.click()
            print("已靜音")
            return True

        except Exception as e:
            print(f"關閉 alert 時發生錯誤: {e}")
            return False

    def reset_button_state(self):
        """重置按鈕狀態"""
        self.driver.execute_script("window.aiAssistantActivated = false;")
        self.driver.execute_script(
            "document.getElementById('ai-assistant-star-btn').setAttribute('data-activated', 'false');"
        )

    def quit(self):
        """關閉瀏覽器"""
        self.driver.quit()
