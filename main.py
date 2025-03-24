from PIL import Image
import io
from ocr import recognize_captcha
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json

# 登录函数
def login(driver, username, password):
    login_url = "https://www.v2ex.com/signin"

    # 打开网站
    driver.get(login_url)

    # 获取所有 class="sl" 的 input 元素
    sl_inputs = driver.find_elements(by=By.CLASS_NAME, value='sl')

    # 假设页面中只有三个 class="sl" 的 input 元素，且顺序为账号、密码、验证码
    username_input = sl_inputs[0]  # 第一个是账号输入框
    password_input = sl_inputs[1]  # 第二个是密码输入框
    captcha_input = sl_inputs[2]   # 第三个是验证码输入框

    # 获取验证码图片
    captcha_element = driver.find_element(by=By.ID, value='captcha-image')  # 定位验证码图片
    captcha_image_data = captcha_element.screenshot_as_png  # 使用 WebDriver 截图功能获取验证码图片数据
    captcha_image = Image.open(io.BytesIO(captcha_image_data))  # 打开验证码图片
    captcha_image.save("captcha.png")  # 保存图片到本地
    # 识别验证码
    captcha_text = recognize_captcha()
    print(f"识别的验证码: {captcha_text}")  # 调试信息

    username_input.send_keys(username)  # 替换为你的用户名
    password_input.send_keys(password)  # 替换为你的密码
    captcha_input.send_keys(captcha_text)

    # 提交登录表单
    login_button = driver.find_element(by=By.CLASS_NAME, value='super.normal.button')
    login_button.click()

    # 检查是否登录成功
    time.sleep(5)  # 等待页面加载
    if "signin" in driver.current_url:  # 如果仍然停留在登录页面，说明登录失败
        print("登录失败，请检查用户名、密码或验证码")
        return False
    print("登录成功")
    return True

def sign_in(driver):
    # 执行签到操作
    driver.get('https://www.v2ex.com')
    # 通过 link_text 定位签到按钮
    signin_button = driver.find_element(by=By.LINK_TEXT, value='领取今日的登录奖励')
    # 如果没有该按钮，则说明已经签到过了
    if len(signin_button) <= 0:
        print("已签到过了")
        return

    signin_button.click()

    # 点击领取X铜币
    get_coin_button = driver.find_element(by=By.CLASS_NAME, value='super.normal.button')
    get_coin_button.click()

# 主函数
def main():
    with open('config.json', 'r') as file:
        config = json.load(file)
        username = config['username']
        password = config['password']

    # 设置 WebDriver 路径
    ser = Service()
    ser.executable_path = '/usr/local/bin/chromedriver'

    chrome_options = webdriver.ChromeOptions()
    # headless mode
    chrome_options.add_argument("--headless=new")

    # # 设置代理
    # PROXY = "127.0.0.1:7890"
    # chrome_options.add_argument('--proxy-server=http://%s' % PROXY)
    chrome_options.ignore_local_proxy_environment_variables()

    driver = webdriver.Chrome(service=ser, options=chrome_options)

    try:
        for attempt in range(3):  # 最多尝试3次
            if login(driver, username, password):
                break
            print(f"登录失败，重试第 {attempt + 1} 次")
            time.sleep(2)  # 等待2秒后重试
        else:
            print("多次尝试登录失败，程序退出")
            return
        sign_in(driver)
    finally:
        # 确保浏览器在程序结束时关闭
        driver.quit()
    
if __name__ == "__main__":
    main()