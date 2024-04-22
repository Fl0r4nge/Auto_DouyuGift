# 待测试 
#3.获取荧光棒模块（好像是不到直播间，不会获得荧光棒）
# ADD 
#4.如何自动更新cookie值

import requests
from lxml import etree
import re
import json
from loguru import logger

#个性化配置的part：
global FavorRoomid
FavorRoomid = '1667826' #3MZ的直播间

Headers = {
    "Content-Type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ""Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81",
            "referer": "https://www.douyu.com",
            'cookie': 'dy_did=045960b05c4fd451ebfc15d900091701; acf_did=045960b05c4fd451ebfc15d900091701; _ga=GA1.1.7498322.1711971748; dy_did=045960b05c4fd451ebfc15d900091701; dy_teen_mode=%7B%22uid%22%3A%22156747034%22%2C%22status%22%3A0%2C%22birthday%22%3A%22%22%2C%22password%22%3A%22%22%7D; acf_ssid=1729388853985710099; acf_web_id=7352862669335976974; acf_abval=webnewhome%253DD; loginrefer=pt_kj414lcie41b; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1713525330,1713538559,1713705640,1713711097; PHPSESSID=pel1to47qk73cftn2ld60iufb4; acf_auth=762cxp5fjABevRp%2FaUDxLZnhBfoT1kuMT26dRHQl28Cd4I4z20BqTKzXODszHcbVNdYZivdes8MbwpYOLs%2F9AbeyHwSnU9wtQaKYq%2BvZ8v4Z%2BCGK7jrjzZs; dy_auth=25847DvUAC1n5ClCZ8HAQh7uj6kYLURnJaW3fl9SaWH%2FxPE7ZNlj%2BI4ORWUtMigzQjtFdxzXgQDQPcYej8COtHbezQyAowgX2nVpX34UNEEfss9vIVn7SQw; wan_auth37wan=94472183c764ngaq4GWEopB%2FtaLgMg0xoz6qt6UFs4JBaFQqaciI18Ykm9zM1tq3BZSm2%2BUzmH8xxOEAqq1UZttXIzUZTeuEMakWaRTjuv9d5dtPHn4; acf_uid=156747034; acf_username=156747034; acf_nickname=%E5%B0%8F%E9%BB%91%E4%B8%87%E4%BA%BA%E8%BF%B7; acf_own_room=0; acf_groupid=1; acf_phonestatus=1; acf_avatar=https%3A%2F%2Fapic.douyucdn.cn%2Fupload%2Favanew%2Fface%2F201708%2F12%2F22%2F68ab181a733b2b7c46ed0461c2fd5416_; acf_ct=0; acf_ltkid=37482519; acf_biz=1; acf_stk=0abc31f876abb526; _ga_5JKQ7DTEXC=GS1.1.1713711099.42.1.1713711551.54.0.720510930; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1713711552',
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

def Get_FansBadgeDict():
    '''
    获取粉丝牌列表及相关信息
    {'1667826': {'anchor': '一口三明治3Mz', 'level': '11', 'exp_need': 418.3, 'mutiple': 1}, '5684726': {'anchor': '皮特174', 'level': '8', 'exp_need': 426.2, 'mutiple': 1}}        
    '''
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh,zh-CN;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': 'dy_did=045960b05c4fd451ebfc15d900091701; acf_did=045960b05c4fd451ebfc15d900091701; _ga=GA1.1.7498322.1711971748; dy_did=045960b05c4fd451ebfc15d900091701; dy_teen_mode=%7B%22uid%22%3A%22156747034%22%2C%22status%22%3A0%2C%22birthday%22%3A%22%22%2C%22password%22%3A%22%22%7D; acf_ssid=1729388853985710099; acf_web_id=7352862669335976974; acf_abval=webnewhome%253DD; loginrefer=pt_kj414lcie41b; acf_uid=156747034; acf_username=156747034; acf_nickname=%E5%B0%8F%E9%BB%91%E4%B8%87%E4%BA%BA%E8%BF%B7; acf_own_room=0; acf_groupid=1; acf_phonestatus=1; acf_ct=0; acf_ltkid=37482509; acf_biz=1; acf_auth=2c5cfsXKGckQNgBO9n32LnwPsxzaUz6WXx5VwlGD4Ae0W4W6WrN24xgFFV3dK22%2FUPlZDG5DDFENm7xeYuqL8m6aLdWvVFEFyejrMiEbaLAT7VrvF3CwL1s; dy_auth=f4027tusahkWLK4OMrrUjsc2ZYZgsr2nx0WBb4pLgzATLvhUxCED5cqQGcI6w1l7c3p5YtT3jKN0LMwDwcYn0k23q8fjqIdc6aMHNzCQpE5AQ8MgPG0YmLI; wan_auth37wan=4be441b387bd11576%2Fgw%2BKqDsjNyCkyomBIb1SamSmduO7yEe8r2T2aI7ovoaGgHtFwEGP%2F4jtIAm8nAl3PnuecINx3CG%2FfH3QdgnIl9%2BZTWumbIrLs; acf_stk=e85bb63ef0662cc4; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1713193263,1713445046,1713499747,1713525330; PHPSESSID=k0r70pc5ghmb2u8mvc0tpqml35; acf_ccn=61d73cba586b32798555c19a86af9ef9; acf_avatar=https%3A%2F%2Fapic.douyucdn.cn%2Fupload%2Favanew%2Fface%2F201708%2F12%2F22%2F68ab181a733b2b7c46ed0461c2fd5416_; _ga_5JKQ7DTEXC=GS1.1.1713525330.37.1.1713527236.54.0.1532942086; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1713527240',
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
    

def Donate_Mod(mod):
    #调试时调整，Max_GlowNum的数量
    #Max_GlowNum = Get_GlowNumber()
    Max_GlowNum = 6

    if mod == 1:#偏爱虎子（除了偏爱的主播，其余的都只送一个荧光棒保等级）
        logger.info("当前为 1. 偏爱模式，正在为你最喜欢的主播:%s赠送%s个荧光棒,其余的都只送1个荧光棒保等级" % (badges_dict[FavorRoomid]['anchor'],Max_GlowNum-badges_num+1))
        for roomid in roomid_list:
            Send_glow(1,roomid)
        Send_glow(Max_GlowNum-badges_num,FavorRoomid)# BUG 这好像没执行 
    if mod == 2:#雨露均沾
        logger.info("当前为 2. 雨露均沾模式，正在为你喜欢的主播平均赠送%s个荧光棒" % (Max_GlowNum//badges_num))
        for roomid in roomid_list:
            Send_glow(Max_GlowNum//badges_num,roomid)
    if mod == 3:#升级优先
        FasterRoomid = Get_LeastExpRoomid()
        logger.info("当前为 3. 升级优先模式,升级最快的房间是%s,为其赠送%s个荧光棒" % (badges_dict[FasterRoomid]['anchor'],Max_GlowNum))
        Send_glow(Max_GlowNum,FasterRoomid)
    if mod == 4:#性价比模式
        MutiplestRoomid = Get_MutiplestRoomid()
        Mutiple = badges_dict[MutiplestRoomid]['mutiple']
        logger.info("当前为 4. 性价比模式,开启经验最高倍的房间是%s,倍数为%s,为其赠送%s个荧光棒" % (badges_dict[MutiplestRoomid]['anchor'],Mutiple,Max_GlowNum))
        Send_glow(Max_GlowNum,MutiplestRoomid)



if __name__ == '__main__':
    #创建一个badges_dict用于存储粉丝牌信息
    badges_dict = {}
    Fans_info = Get_FansBadgeDict()
    print("Before: %s" % (Fans_info))
    glowNumber = Get_GlowNumber()
    print("当前荧光棒数量为：%s" % (glowNumber))
    #Donate_Mod(4)
    #Fans_info_after = Get_FansBadgeDict()
    #print("After: %s" % (Fans_info_after))


