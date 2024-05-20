import requests
from lxml import etree
import re
import json
from loguru import logger
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep
import os


#个性化配置的part：
global FavorRoomid
FavorRoomid = '1667826' #3MZ的直播间

cookie = os.environ.get('COOKIES')
pushdeer_key = os.environ.get('PUSHDEERKEY')
Headers = {
    "Content-Type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ""Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81",
            "referer": "https://www.douyu.com",
            'cookie': cookie,
}

def Pushdeer_message(send_message):
    #使用pushdeer推送消息
    key = pushdeer_key
    pushdeer_url = 'https://api2.pushdeer.com/message/push?pushkey='+key+'&text='+send_message
    push = requests.get(pushdeer_url)

def Pushdeer_image(image_url):
    #使用pushdeer推送图片
    key = pushdeer_key
    pushdeer_url = 'https://api2.pushdeer.com/message/push?pushkey='+key+'&text='+image_url+'&type=image'
    push = requests.get(pushdeer_url)

def send_log_to_pushdeer():
    # 打开 log.txt 文件，并读取内容
    with open("log.txt", "r") as file:
        log_content = file.read()
    # 使用 Pushdeer_message 函数发送内容
    Pushdeer_message(log_content)


def Get_FansBadgeDict():
    '''
    获取粉丝牌列表及相关信息
    {'1667826': {'anchor': '一口三明治3Mz', 'level': '11', 'exp_need': 418.3, 'mutiple': 1}, '5684726': {'anchor': '皮特174', 'level': '8', 'exp_need': 426.2, 'mutiple': 1}}        
    '''
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh,zh-CN;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': cookie,
    'referer': 'https://www.douyu.com/member/platform_task/barrage_skin',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}
    badges_url = 'https://www.douyu.com/member/cp/getFansBadgeList'
    badges = requests.get(badges_url, headers=headers)
    #print(badges.text)
    #利用lxml解析网页
    html = etree.HTML(badges.text, etree.HTMLParser())
    #拥有的粉丝牌数
    global badges_num
    badges_num = len(html.xpath('//*[@id="wrap"]/div/div[2]/div[2]/div[3]/table/tbody/tr'))
    re_now = r'(?<= )\d.*\d(?=\/\d)'
    re_up = r'(?<=\/)\d.*\d'
    #创建粉丝牌字典
    global badges_dict #使用badges_dict作为全局变量,修改其值
    for path in range(badges_num):
        path += 1
        #房间号
        room_id = html.xpath('//*[@id="wrap"]/div/div[2]/div[2]/div[3]/table/tbody/tr[%s]/@data-fans-room' % path)[0]
        #煮包名称
        anchor = html.xpath('//*[@id="wrap"]/div/div[2]/div[2]/div[3]/table/tbody/tr[%s]/td[2]/a/text()' % path)[0]
        #当前粉丝牌等级
        level = html.xpath('//*[@id="wrap"]/div/div[2]/div[2]/div[3]/table/tbody/tr[%s]/@data-fans-level' % path)[0]
        #现在的经验值已经这一级所需经验值
        exp = html.xpath('//*[@id="wrap"]/div/div[2]/div[2]/div[3]/table/tbody/tr[%s]/td[3]/text()' % path)[0]
        #计算升级所需经验值
        exp_now = float(re.findall(re_now, exp)[0])
        up_grade = float(re.findall(re_up, exp)[0])
        exp_need = round((up_grade - exp_now), 1)
        if room_id in badges_dict:
            # 如果有，就使用已有的 mutiple 值
            multiple = badges_dict[room_id]['mutiple']
        else:
            # 如果没有，初始化其为 1
            multiple = 1
        badge_info = {
            "anchor": anchor,
            "level":level,
            "exp_need": exp_need,
            "mutiple": multiple
        }
        badges_dict[room_id] = badge_info
    global roomid_list
    roomid_list = list(badges_dict.keys())
    return badges_dict
    #logger.info("成功获取粉丝牌信息：%s"%(badges_dict))
    #print(badges_dict[0]['room_id'])

def Send_glow(propCount,roomid):
    #赠送荧光棒礼物 如果成功返回True，否则返回False
    data = {
    'propId': '268',
    'propCount': propCount, #propCount是荧光棒数目
    'roomId': roomid, #roomid是房间id
    'bizExt': '{"yzxq":{}}',
}
    response = requests.post('https://www.douyu.com/japi/prop/donate/mainsite/v2',  headers=Headers, data=data)
    data = json.loads(response.text)
    if data["msg"] == "success":
        logger.info("成功为房间%s赠送%s个荧光棒" % (roomid,propCount))
        return True
    elif data["msg"] == "请登录":
        logger.error("cookie失效，请重新登录")
        return False
    
def Get_GlowNumber():
    #return荧光棒数量
    GlowNumber_url = 'https://www.douyu.com/japi/prop/backpack/web/v2?rid=1667826'
    response = requests.get(url=GlowNumber_url,headers=Headers)
    GlowData = json.loads(response.text)
    GlowCount = GlowData["data"]["list"][0]["count"]
    return GlowCount

def Get_LeastExpRoomid():
    #return升级最快的房间号
    FasterRoomid = 1667826
    #计算升级最快的房间（也就是缺少最少经验值的房间）
    Temp_LeastExp = 99999999
    for roomid in roomid_list:
        if badges_dict[roomid]["exp_need"] < Temp_LeastExp:
            Temp_LeastExp = badges_dict[roomid]["exp_need"]
            FasterRoomid = roomid
    return FasterRoomid
        
def update_mutiple(roomid):
    expNeed_before = badges_dict[roomid]['exp_need']
    Send_glow(1,roomid)
    Get_FansBadgeDict()
    expNeed_after = badges_dict[roomid]['exp_need']
    exp_change = round(expNeed_before - expNeed_after,2)
    logger.info("房间%s的经验值变化为%s倍"%(roomid,exp_change))
    badges_dict[roomid]['mutiple']= exp_change

def Get_MutiplestRoomid():
    #return MutiplestRoomid 
    #希望返回开启多倍的直播间，并计算倍数，并返回最高倍数的直播间id
    for roomid in roomid_list:
        update_mutiple(roomid)
    #找到倍数最多的房间的id号
    multiple_list = []
    for roomid in roomid_list:
        multiple_list.append(badges_dict[roomid]['mutiple'])
    MutiplestRoomid = roomid_list[multiple_list.index(max(multiple_list))]
    print(badges_dict)
    return MutiplestRoomid


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


def Donate_Mod(mod):
    #调试时调整，Max_GlowNum的数量
    Max_GlowNum = Get_GlowNumber()
    #Max_GlowNum = 6

    if mod == 1:#偏爱虎子（除了偏爱的主播，其余的都只送一个荧光棒保等级）
        logger.info("当前为 1. 偏爱模式，正在为你最喜欢的主播:%s赠送%s个荧光棒,其余的都只送1个荧光棒保等级" % (badges_dict[FavorRoomid]['anchor'],Max_GlowNum-badges_num+1))
        Pushdeer_message("当前为 1. 偏爱模式，正在为你最喜欢的主播:%s赠送%s个荧光棒,其余的都只送1个荧光棒保等级" % (badges_dict[FavorRoomid]['anchor'],Max_GlowNum-badges_num+1))
        for roomid in roomid_list:
            Send_glow(1,roomid)
        Send_glow(Max_GlowNum-badges_num,FavorRoomid)# BUG 这好像没执行 
    if mod == 2:#雨露均沾
        logger.info("当前为 2. 雨露均沾模式，正在为你喜欢的主播平均赠送%s个荧光棒" % (Max_GlowNum//badges_num))
        Pushdeer_message("当前为 2. 雨露均沾模式，正在为你喜欢的主播平均赠送%s个荧光棒" % (Max_GlowNum//badges_num))
        for roomid in roomid_list:
            Send_glow(Max_GlowNum//badges_num,roomid)
    if mod == 3:#升级优先
        FasterRoomid = Get_LeastExpRoomid()
        logger.info("当前为 3. 升级优先模式,升级最快的房间是%s,为其赠送%s个荧光棒" % (badges_dict[FasterRoomid]['anchor'],Max_GlowNum))
        Pushdeer_message("当前为 3. 升级优先模式,升级最快的房间是%s,为其赠送%s个荧光棒" % (badges_dict[FasterRoomid]['anchor'],Max_GlowNum))
        Send_glow(Max_GlowNum,FasterRoomid)
    if mod == 4:#性价比模式
        MutiplestRoomid = Get_MutiplestRoomid()
        Mutiple = badges_dict[MutiplestRoomid]['mutiple']
        logger.info("当前为 4. 性价比模式,开启经验最高倍的房间是%s,倍数为%s,为其赠送%s个荧光棒" % (badges_dict[MutiplestRoomid]['anchor'],Mutiple,Max_GlowNum))
        Pushdeer_message("当前为 4. 性价比模式,开启经验最高倍的房间是%s,倍数为%s,为其赠送%s个荧光棒" % (badges_dict[MutiplestRoomid]['anchor'],Mutiple,Max_GlowNum))
        Send_glow(Max_GlowNum,MutiplestRoomid)


if __name__ == '__main__':
    #配置赠送模式为： 
    Mod = 1 

    #创建一个badges_dict用于存储粉丝牌信息
    badges_dict = {}

    logger.add("log.txt")
    Fans_info = Get_FansBadgeDict()
    logger.info("成功获取粉丝牌信息：%s"%(badges_dict))
    Pushdeer_message("成功获取粉丝牌信息：%s"%(badges_dict))
    logger.info("前往直播间获取荧光棒")
    Pushdeer_message("前往直播间获取荧光棒")
    Go_roomforglow()
    glowNumber = Get_GlowNumber()
    logger.info("当前荧光棒数量为：%s" % (glowNumber))
    Pushdeer_message("当前荧光棒数量为：%s" % (glowNumber))
    Donate_Mod(Mod)



