import requests
headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
            'Referer':"https://bj.lianjia.com/chengjiao/",
            'Host':"bj.lianjia.com",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Connection': "keep-alive",
            'Accept-Encoding': "*"
        }

url = 'https://bj.lianjia.com/chengjiao/'
r = requests.get(url, headers=headers, timeout=5)
html = r.text   #r.的很多内容写入html

# 解析模块
# 导入模块
from lxml import etree    #lxml支持多种方式解析

# 创建一个etree类型的对象
# 把html传入，并选择解析器

result = etree.HTML(html,etree.HTMLParser())   #etree.HTML():构造了一个XPath解析对象并对HTML文本进行自动修正。

xpath = '/html/body/div[5]/div[1]/ul'  #收收收，收到他们属性公共的父节点，就可以了
link1 = result.xpath(xpath+'//@href')
link1 = list(set(link1))

link_list=[]
for link in link1:
    #str(link)
    link='https://bj.lianjia.com'+link
    link_list.extend(link)
print(link_list)


