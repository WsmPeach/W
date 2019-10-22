# 爬虫框架
# 链家案例
import requests
from lxml import etree
import xlwt   #xlwt模块实现对excel文件的写入

class crawler():

    # 配置信息
    def __init__(self):
        self.headers = {
            # 伪造浏览器
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Accept-Encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }

    # 请求模块
    def get_response(self,url):
        r = requests.get(url,headers=self.headers,timeout=5)
        html = r.text
        return html

    # 一个爬虫可能会多个解析模块
    # 解析模块
    def parse_list_data(self,html):
        result = etree.HTML(html)

        # 提取数据部分，替换xpath
        xpath = '/html/body/div[5]/div[1]/ul'
        link = result.xpath(xpath+'//@href')
        print(link)
        print(2)

        return link

    def parse_detail_data(self,html):
        data_list = []
        result = etree.HTML(html)

        # 提取数据部分，替换xpath
        xpath = '/html/body/div[4]/div/h1' #重要！！详细信息点进去，提取：察慈小区 3室1厅 79.4平米
        name = result.xpath(xpath + '/text()')
        # print(name)

        xpath = '/html/body/section[1]/div[2]/div[2]/div[1]/span/i'   #重要！！详细信息点进去，提取：价格
        price = result.xpath(xpath+'/text()')
        # print(price)

        data = [name[0],price[0]]
        data_list.append(data)
        return data_list

    # 存储模块
    def save_data(self,data_list):
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('data', cell_overwrite_ok=True)
        i = 1
        for data in data_list:
            for j in range(len(data)):
                worksheet.write(i, j, data[j])  # 写入excel；参数对应 行, 列, 值
            i = i + 1
        workbook.save('data.xls')


if __name__ == '__main__':
    # 声明一个爬虫类
    crawler = crawler()


    # 翻页逻辑---列表页的翻页，列表页获取全部链接，遍历全部链接爬取内容。

    # 列表页的翻页
    url_list = []
    for i in range(3):
        url = 'https://bj.lianjia.com/chengjiao/pg'+str(i)
        print('正在爬取列表页'+str(i),url)
        # 请求列表页
        html = crawler.get_response(url)
        # 解析，列表页获取全部链接
        data = crawler.parse_list_data(html)
        url_list.extend(data)
        print(url_list)
        print(1)

    # 遍历全部链接爬取内容
    data_list = []
    url_list = list(set(url_list))
    for url in url_list:
        if 'chengjiao' in url:      #别把所有有链接的地方都爬取出来了
            html = crawler.get_response(url)
            data = crawler.parse_detail_data(html)
            data_list.extend(data)
            # print(data)
            print(data_list)

    # 存储数据
    crawler.save_data(data_list)
