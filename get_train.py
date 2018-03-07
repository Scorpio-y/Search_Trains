from get_stations import stations
from prettytable import PrettyTable
from colorama import Fore
import warnings
import requests

from_s = input('请输入起始城市：\n')
f = stations[from_s]     # 通过字典转化为车站对应的缩写字母
to_s = input('请输入目的城市：\n')
t = stations[to_s]       # 通过字典转化为车站对应的缩写字母
date = input('请输入出发时间：格式如：2018-01-01 \n')
d = str(date)
print('正在查询' + from_s + '至' + to_s + '的列车...')
# 合成完整的url
url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=' + d + '&leftTicketDTO.from_station=' + f + '&leftTicketDTO.to_station=' + t +'&purpose_codes=ADULT'
# print(url)
warnings.filterwarnings("ignore")  # 这个网站是有安全警告的，这段代码可以忽略警告
r = requests.get(url, verify=False)
# print(r.json())
raw_trains = r.json()['data']['result']     # 获取车次信息
num = len(raw_trains)       # 获取车次数目
print('共查询到%d个车次信息'%num)
# print(raw_trains)
pt = PrettyTable(["车次", "车站", "时间", "历时", "商务座", "一等座", "二等座", "高级软卧", "软卧", "动卧", "硬卧", "软座", "硬座", "无座", "其他"])
for raw_train in raw_trains:
    # split分割之后得到的是一个列表
    data_list = raw_train.split("|")
    # print(data_list)
    checi = data_list[3]     # 车次
    fctime = data_list[8]    # 发车时间
    ddtime = data_list[9]    # 到达时间
    lishi = data_list[10]    # 历时
    shangwuzuo = data_list[20] or "--"    # 商务座/特等座
    yidengzuo = data_list[21] or "--"     # 一等座
    erdengzuo = data_list[22] or "--"     # 二等座
    gjruanwo = data_list[23] or "--"      # 高级软卧
    ruanwo = data_list[24] or "--"        # 软卧
    dongwo = data_list[25] or "--"        # 动卧
    yingwo = data_list[26] or "--"        # 硬卧
    ruanzuo = data_list[27] or "--"       # 软座
    yingzuo = data_list[28] or "--"       # 硬座
    wuzuo = data_list[29] or "--"         # 无座
    others = data_list[30] or "--"        # 其他

    pt.add_row([
        # 对特定文字添加颜色
        checi,
        '\n'.join([Fore.GREEN + from_s + Fore.RESET, Fore.RED + to_s + Fore.RESET]),
        '\n'.join([Fore.GREEN + fctime + Fore.RESET, Fore.RED + ddtime + Fore.RESET]),
        lishi,
        shangwuzuo,
        yidengzuo,
        erdengzuo,
        gjruanwo,
        ruanwo,
        dongwo,
        yingwo,
        ruanzuo,
        yingzuo,
        wuzuo,
        others
    ])
print(pt)       # 打印表格
