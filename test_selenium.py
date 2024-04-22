from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def Go_roomforglow():
    driver_path = ChromeDriverManager().install()  # 使用webdriver manager自动安装新版本
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(driver_path, options=chrome_options)
    print("打开直播间获取荧光棒")
    #配置chrome请求网站时的cookie信息
    driver.get("https://www.douyu.com/1667826")

