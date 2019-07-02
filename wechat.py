import json
import time
import pdfkit

import requests

base_url = 'https://mp.weixin.qq.com/mp/profile_ext'


# 这些信息不能抄我的，要用你自己的才有效
headers = {
    'Connection': 'keep - alive',
    'Accept': '* / *',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 9; MI 6X Build/PKQ1.180904.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/778 MMWEBSDK/190301 Mobile Safari/537.36 MMWEBID/4213 MicroMessenger/7.0.4.1420(0x2700043B) Process/toolsmp NetType/WIFI Language/zh_CN',
    'Referer': 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5MDQ4MzU5NQ==&scene=126&bizpsid=1559652448&devicetype=android-28&version=2700043b&lang=zh_CN&nettype=WIFI&a8scene=3&pass_ticket=ETwbdvgwy0pq9pLxZwe0kD1DpFWCrc07uJZEwFrZ8HS4%2B3bFzMhrD%2FGHAqRtiQMZ&wx_header=1',
    'Accept-Encoding': 'br, gzip, deflate'
}

cookies = {
    'devicetype': 'android-28',
    'lang': 'zh_CN',
    'pass_ticket': 'ETwbdvgwy0pq9pLxZwe0kD1DpFWCrc07uJZEwFrZ8HS4+3bFzMhrD/GHAqRtiQMZ',
    'version': '2700043b',
    'wap_sid2': 'CPH9xfADElxRVndNbnlTNG9JU3pnMlhHemxLd2IxdlZ2LWRGYVFNQ043dVRuM0kzWjRNX2s0ZEdEUktvelNiakljNUJpZnJKbFliNll5QXBIM0g2NHhrakdYRnVkdk1EQUFBfjDfytnnBTgNQJVO',
    'wxuin': '1041334001'
}



def get_params(offset):

    params = {
        'action': 'getmsg',
        '__biz': 'MjM5MDQ4MzU5NQ==',
        'f': 'json',
        'offset': '{}'.format(offset),
        'count': '10',
        'is_ok': '1',
        'scene': '126',
        'uin': '777',
        'key': '777',
        'pass_ticket': 'ETwbdvgwy0pq9pLxZwe0kD1DpFWCrc07uJZEwFrZ8HS4+3bFzMhrD/GHAqRtiQMZ',
        'appmsg_token': '1011_QVGswWOHv%2FcM%2FOLTM3uzT3pd6T18T_oOHMH0sA~~',
        'x5': '0',
        'f': 'json',
    }

    return params


def get_list_data(offset):
    res = requests.get(base_url, headers=headers, params=get_params(offset), cookies=cookies)
    data = json.loads(res.text)
    can_msg_continue = data['can_msg_continue']
    next_offset = data['next_offset']

    general_msg_list = data['general_msg_list']
    list_data = json.loads(general_msg_list)['list']

    for data in list_data:
        # print(data)
        try:
            if data['app_msg_ext_info']['copyright_stat'] == 11:
                msg_info = data['app_msg_ext_info']
                title = msg_info['title']
                content_url = msg_info['content_url']
                # 自己定义存储路径
                options = {
                    'encoding': "UTF-8",
                    'custom-header': [
                        ('Accept-Encoding', 'gzip')
                    ]
                }
                pdfkit.from_url(content_url, 'C:\\Users\\77409\\Desktop\\wechat_pdf\\'+title+'.pdf',options=options)
                print('获取到原创文章：%s ： %s' % (title, content_url))
        except:
            print('跳过')


    if can_msg_continue == 1:
        time.sleep(1)
        get_list_data(next_offset)


if __name__ == '__main__':
    get_list_data(0)