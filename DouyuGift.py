# 待测试 
#3.获取荧光棒模块（好像是不到直播间，不会获得荧光棒）



# ADD 
#1.判断谁开启了双倍 
#2.精简mod 到三个
#
#4.如何自动更新cookie值


import requests
from lxml import etree
import re
import json
from loguru import logger


global FavorRoomid
FavorRoomid = '1667826' #3MZ的直播间

#待完善:
global multiple_list 
multiple_list= [1]*2


Headers = {
    "Content-Type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ""Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81",
            "referer": "https://www.douyu.com",
            'cookie': 'dy_did=045960b05c4fd451ebfc15d900091701; acf_did=045960b05c4fd451ebfc15d900091701; _ga=GA1.1.7498322.1711971748; dy_did=045960b05c4fd451ebfc15d900091701; acf_uid=156747034; acf_username=156747034; acf_nickname=%E5%B0%8F%E9%BB%91%E4%B8%87%E4%BA%BA%E8%BF%B7; acf_own_room=0; acf_groupid=1; acf_phonestatus=1; dy_teen_mode=%7B%22uid%22%3A%22156747034%22%2C%22status%22%3A0%2C%22birthday%22%3A%22%22%2C%22password%22%3A%22%22%7D; acf_ssid=1729388853985710099; acf_web_id=7352862669335976974; acf_abval=webnewhome%253DD; loginrefer=pt_kj414lcie41b; _ga_5JKQ7DTEXC=GS1.1.1712503947.23.1.1712505351.60.0.0; PHPSESSID=q4i8o3p7oad3vi61m6maogom10; acf_auth=3b89E5W2I%2Ft7%2FOGI11%2BddGp89%2Fd7Zh23D3MF7uABB8V9O3SzwOnMs%2FiF6LSbP6G5OgbiUNNmCVn7CkUFN0xRa8NtogIWO8Gy8Oaa%2BT2UUJmM%2FAWRVssmFfg; dy_auth=af20M%2BZQbHQzvNGAyDWd8C7T4NLv25ImxemnX5eZI%2B1GZXro%2BY8L8jAvuvp8GUwXdgBfwhcDUzXlC53wg9QUFV2MMZtDWssMgU5y3rjMqhvHX0HTURFpmXo; wan_auth37wan=5495e3ddbf367Z0rAcPqWUsdEN1Ok6CM2qA%2F9uNlHPYOrFhk9S0EGrYNOp8kUyUrbrt8Er11D9G2vY%2Bs2LdFAQ86dgr8GCynkN5aPDzey2EqN5HJBsY; acf_avatar=https%3A%2F%2Fapic.douyucdn.cn%2Fupload%2Favanew%2Fface%2F201708%2F12%2F22%2F68ab181a733b2b7c46ed0461c2fd5416_; acf_ct=0; acf_ltkid=37482509; acf_biz=1; acf_stk=3be8a95545e04133; acf_ccn=0cfe497e9e2d15d3566d0db90eba7beb; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1712408034,1712496497,1712505334,1712748746; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1712748746',
}

def Pushdeer_message(send_message):
    #使用pushdeer推送消息
    key = 'PDU16893TbNIY80fUGyeo7DOVwyWmXUSqCG6btUjx'
    pushdeer_url = 'https://api2.pushdeer.com/message/push?pushkey='+key+'&text='+send_message
    push = requests.get(pushdeer_url)

def Pushdeer_image(image_url):
    #使用pushdeer推送图片
    key = 'PDU16893TbNIY80fUGyeo7DOVwyWmXUSqCG6btUjx'
    pushdeer_url = 'https://api2.pushdeer.com/message/push?pushkey='+key+'&text='+image_url+'&type=image'
    push = requests.get(pushdeer_url)

def Get_FansBadgeList():
    '''
    获取粉丝牌列表及相关信息
    [{'room_id': '5684726', 'anchor': '皮特174', 'level': '8', 'exp_need': 520.2}, {'room_id': '1667826', 'anchor': '一口三明治3Mz', 'level': '11', 'exp_need': 1156.1}]        
    '''
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh,zh-CN;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': 'dy_did=045960b05c4fd451ebfc15d900091701; acf_did=045960b05c4fd451ebfc15d900091701; _ga=GA1.1.7498322.1711971748; dy_did=045960b05c4fd451ebfc15d900091701; acf_uid=156747034; acf_username=156747034; acf_nickname=%E5%B0%8F%E9%BB%91%E4%B8%87%E4%BA%BA%E8%BF%B7; acf_own_room=0; acf_groupid=1; acf_phonestatus=1; dy_teen_mode=%7B%22uid%22%3A%22156747034%22%2C%22status%22%3A0%2C%22birthday%22%3A%22%22%2C%22password%22%3A%22%22%7D; acf_ssid=1729388853985710099; acf_web_id=7352862669335976974; acf_abval=webnewhome%253DD; loginrefer=pt_kj414lcie41b; _ga_5JKQ7DTEXC=GS1.1.1712503947.23.1.1712505351.60.0.0; PHPSESSID=q4i8o3p7oad3vi61m6maogom10; acf_auth=3b89E5W2I%2Ft7%2FOGI11%2BddGp89%2Fd7Zh23D3MF7uABB8V9O3SzwOnMs%2FiF6LSbP6G5OgbiUNNmCVn7CkUFN0xRa8NtogIWO8Gy8Oaa%2BT2UUJmM%2FAWRVssmFfg; dy_auth=af20M%2BZQbHQzvNGAyDWd8C7T4NLv25ImxemnX5eZI%2B1GZXro%2BY8L8jAvuvp8GUwXdgBfwhcDUzXlC53wg9QUFV2MMZtDWssMgU5y3rjMqhvHX0HTURFpmXo; wan_auth37wan=5495e3ddbf367Z0rAcPqWUsdEN1Ok6CM2qA%2F9uNlHPYOrFhk9S0EGrYNOp8kUyUrbrt8Er11D9G2vY%2Bs2LdFAQ86dgr8GCynkN5aPDzey2EqN5HJBsY; acf_avatar=https%3A%2F%2Fapic.douyucdn.cn%2Fupload%2Favanew%2Fface%2F201708%2F12%2F22%2F68ab181a733b2b7c46ed0461c2fd5416_; acf_ct=0; acf_ltkid=37482509; acf_biz=1; acf_stk=3be8a95545e04133; acf_ccn=0cfe497e9e2d15d3566d0db90eba7beb; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1712408034,1712496497,1712505334,1712748746; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1712748746',
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
    #创建粉丝牌列表
    global badges_list 
    badges_list = []
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
        multiple = multiple_list[path - 1] 
        badge_info = {
            "room_id": room_id,
            "anchor": anchor,
            "level":level,
            "exp_need": exp_need,
            "mutiple": multiple
        }
        badges_list.append(badge_info)
    return badges_list
    #logger.info("成功获取粉丝牌信息：%s"%(badges_list))
    #print(badges_list[0]['room_id'])
    

def Send_glow(propCount,roomid):
    #赠送荧光棒礼物 ，
    data = {
    'propId': '268',
    'propCount': propCount, #propCount是荧光棒数目
    'roomId': roomid, #roomid是房间id
    'bizExt': '{"yzxq":{}}',
}
    response = requests.post('https://www.douyu.com/japi/prop/donate/mainsite/v2',  headers=Headers, data=data)
    #print(response)

def Get_GlowNumber():
    GlowNumber_url = 'https://www.douyu.com/japi/prop/backpack/web/v2?rid=1667826'
    response = requests.get(url=GlowNumber_url,headers=Headers)
    GlowData = json.loads(response.text)
    GlowCount = GlowData["data"]["list"][0]["count"]
    print(GlowCount)
    #return GlowCount

def Get_LeastExpRoomid():
    FasterRoomid = 1667826
    #计算升级最快的房间（也就是缺少最少经验值的房间）
    Temp_LeastExp = 99999999
    for x in range(badges_num):
        if badges_list[x]["exp_need"] < Temp_LeastExp:
            Temp_LeastExp = badges_list[x]["exp_need"]
            FasterRoomid = badges_list[x]["room_id"]
    return FasterRoomid
        
def Get_MutiplestRoomid():
    #return MutiplestRoomid 
    #希望返回开启多倍的直播间，并计算倍数，并返回最高倍数的直播间id
    for x in range(badges_num):
        Get_FansBadgeList()
        expNeed_before = badges_list[x]['exp_need']
        Send_glow(1,badges_list[x]['room_id'])
        Get_FansBadgeList()
        expNeed_after = badges_list[x]['exp_need']
        multiple_list[x] = expNeed_before -  expNeed_after
    #print(multiple_list)
    MaxMultiple = max(multiple_list)
    MaxPath = multiple_list.index(MaxMultiple)
    MutiplestRoomid = badges_list[MaxPath]['room_id']
    #print(MutiplestRoomid)
    return MutiplestRoomid,MaxMultiple
    

def Donate_Mod(mod):
    Max_GlowNum = 6
    FasterRoomid = Get_LeastExpRoomid()
    Mutiplestinfo = Get_MutiplestRoomid()
    MutiplestRoomid = Mutiplestinfo[0]
    Mutiple = Mutiplestinfo[1]
    if mod == 1:#偏爱虎子（除了偏爱的主播，其余的都只送一个荧光棒保等级）
        logger.info("当前为 1. 偏爱模式，正在为你最喜欢的主播:%s赠送%s个荧光棒,其余的都只送1个荧光棒保等级" % (room_id_to_anchor[FavorRoomid],Max_GlowNum-badges_num+1))
        for x in range(badges_num):
            Send_glow(1,badges_list[x]['room_id'])
        Send_glow(Max_GlowNum-badges_num,FavorRoomid)# BUG 这好像没执行 
    if mod == 2:#雨露均沾
        logger.info("当前为 2. 雨露均沾模式，正在为你喜欢的主播平均赠送%s个荧光棒" % (Max_GlowNum//badges_num))
        for x in range(badges_num):
            Send_glow(Max_GlowNum//badges_num,badges_list[x]['room_id'])
    if mod == 3:#升级优先
        logger.info("当前为 3. 升级优先模式,升级最快的房间是%s,为其赠送%s个荧光棒" % (room_id_to_anchor[FasterRoomid],Max_GlowNum))
        Send_glow(Max_GlowNum,FasterRoomid)
    if mod == 4:#性价比模式
        logger.info("当前为 4. 性价比模式,开启经验最高倍的房间是%s,倍数为%s,为其赠送%s个荧光棒" % (room_id_to_anchor[MutiplestRoomid],Mutiple,Max_GlowNum))
        Send_glow(Max_GlowNum,MutiplestRoomid)



if __name__ == '__main__':
    room_id_to_anchor = {
    '5684726': '皮特174',
    '1667826': '一口三明治3Mz'
}
    
    Get_FansBadgeList()
    print(Get_FansBadgeList())
    Donate_Mod(4)
    print(Get_FansBadgeList())
    #Get_GlowNumber()
    #Get_FansBadgeList()

