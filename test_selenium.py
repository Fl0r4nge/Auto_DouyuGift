from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from loguru import logger
from time import sleep

cookie = 'dy_did=045960b05c4fd451ebfc15d900091701; acf_did=045960b05c4fd451ebfc15d900091701; _ga=GA1.1.7498322.1711971748; dy_did=045960b05c4fd451ebfc15d900091701; dy_teen_mode=%7B%22uid%22%3A%22156747034%22%2C%22status%22%3A0%2C%22birthday%22%3A%22%22%2C%22password%22%3A%22%22%7D; acf_ssid=1729388853985710099; acf_web_id=7352862669335976974; acf_abval=webnewhome%253DD; loginrefer=pt_kj414lcie41b; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1713525330,1713538559,1713705640,1713711097; PHPSESSID=pel1to47qk73cftn2ld60iufb4; acf_auth=762cxp5fjABevRp%2FaUDxLZnhBfoT1kuMT26dRHQl28Cd4I4z20BqTKzXODszHcbVNdYZivdes8MbwpYOLs%2F9AbeyHwSnU9wtQaKYq%2BvZ8v4Z%2BCGK7jrjzZs; dy_auth=25847DvUAC1n5ClCZ8HAQh7uj6kYLURnJaW3fl9SaWH%2FxPE7ZNlj%2BI4ORWUtMigzQjtFdxzXgQDQPcYej8COtHbezQyAowgX2nVpX34UNEEfss9vIVn7SQw; wan_auth37wan=94472183c764ngaq4GWEopB%2FtaLgMg0xoz6qt6UFs4JBaFQqaciI18Ykm9zM1tq3BZSm2%2BUzmH8xxOEAqq1UZttXIzUZTeuEMakWaRTjuv9d5dtPHn4; acf_uid=156747034; acf_username=156747034; acf_nickname=%E5%B0%8F%E9%BB%91%E4%B8%87%E4%BA%BA%E8%BF%B7; acf_own_room=0; acf_groupid=1; acf_phonestatus=1; acf_avatar=https%3A%2F%2Fapic.douyucdn.cn%2Fupload%2Favanew%2Fface%2F201708%2F12%2F22%2F68ab181a733b2b7c46ed0461c2fd5416_; acf_ct=0; acf_ltkid=37482519; acf_biz=1; acf_stk=0abc31f876abb526; _ga_5JKQ7DTEXC=GS1.1.1713711099.42.1.1713711551.54.0.720510930; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1713711552'

#设置cookie为webdriver需要的格式
def set_cookie(cookie):
    cookies = {}
    for line in cookie.split(';'):
        # 其设置为1就会把字符串拆分成2份
        name, value = line.strip().split('=', 1)
        cookies[name] = value
    return cookies

def Go_roomforglow():
    driver_path = ChromeDriverManager().install()  # 使用webdriver manager自动安装新版本
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在报错问题
    chrome_options.add_argument('--disable-gpu')  # 禁用GPU硬件加速，如果软件渲染器没有就位，则GPU进程将不会启动
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')  # 无界面
    driver = webdriver.Chrome(options=chrome_options)
    logger.info("打开直播间")
    driver.get('https://www.douyu.com/1667826')
    dy_cookie = set_cookie(cookie)
    for i in dy_cookie.keys():
        mycookie = {
            'domain': '.douyu.com',
            'name': i,
            'value': dy_cookie[i],
            'expires': '',
            'path': '/',
            'httpOnly': False,
            'HostOnly': False,
            'Secure': False,
        }
        driver.add_cookie(mycookie)
    logger.info("刷新页面以完成登录")
    driver.refresh()
    sleep(10)
    driver.quit()
    logger.info("关闭直播间")


if __name__ == '__main__':
    Go_roomforglow()
