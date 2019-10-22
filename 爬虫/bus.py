#-coding:utf-8-*-
import requests
from lxml import etree

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
}
items=[]
def parse_last(content):
    tree=etree.HTML(content)
    #线路名
    bus_name=tree.xpath('//div[@class="bus_i_t1"]/h1/text()')

    bus_name=str(bus_name).replace('&nbsp','')
    #运行时间
    runtime=tree.xpath('//div[@class="bus_i_content"]/p[1]/text()')
    # print(runtime)
    #票价信息
    ticket_price = tree.xpath('//div[@class="bus_i_content"]/p[2]/text()')
    # print(ticket_price)
    #最后更新时间
    last_update_time = tree.xpath('//div[@class="bus_i_content"]/p[4]/text()')
    # print(last_update_time)
    up_route=tree.xpath('//div[@class="bus_line_site "][1]/div/div/a/text()')
    #上行总站数
    total_no=tree.xpath('//span[@class="bus_line_no"]/text()')
    up_total_no = total_no[0].replace('\xa0', '')
    try:
        down_route=tree.xpath('//div[@class="bus_line_site "][2]/div/div/a/text()')
    #下行总站数
        down_total_no = total_no[1].replace('\xa0', '')
    except Exception as e:
        down_route='无下行线路'
        down_total_no=0

    item={
        '线路名': bus_name,
        '运行时间': runtime,
        '票价信息': ticket_price,
        '更新时间': last_update_time,
        '上行站数': up_total_no,
        '上行站点': up_route,
        '下行站数': down_total_no,
        '下行站点': down_route,
    }
    items.append(item)

def parse_route(content):
    tree=etree.HTML(content)
    bus_url_list=tree.xpath('//div[@class="stie_list"]/a/@href')
    bus_name=tree.xpath('//div[@class="stie_list"]/a/@title')
    # print(bus_url_list)
    # print(bus_name)
    i=0
    for route in  bus_url_list:
        route='https://shenzhen.8684.cn'+route
        r=requests.get(url=route,headers=headers)
        parse_last(r.text)
        i=i+1
def parse_navi():
    url = 'https://shenzhen.8684.cn/'
    r = requests.get(url=url, headers=headers)
    tree = etree.HTML(r.text)
    num_href_url=tree.xpath('//div[@class ="bus_kt_r1"]/a/@href')
    char_href_url=tree.xpath('//div[@class ="bus_kt_r2"]/a/@href')
    # print(num_href_url)
    return num_href_url+char_href_url
def main():
    navi_list=parse_navi()
    for first_url in navi_list:
        first_url='https://shenzhen.8684.cn'+first_url
        r=requests.get(url=first_url,headers=headers)
        parse_route(r.text)
        fp=open('深圳公交线路.txt','w',encoding='utf8')
        for item in items:
            fp.write(str(item)+'\n')
        fp.close()
if __name__ == '__main__':
    main()