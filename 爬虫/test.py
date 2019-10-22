#-coding:utf-8-*-
import requests
import urllib.request
import urllib.parse
import re
import time
import csv
import codecs


# def data_write_csv(file_name, datas):#file_name为写入CSV文件的路径，datas为要写入数据列表
#     file_csv = codecs.open(file_name,'w+','utf-8')#追加
#     writer = csv.writer(file_csv, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
#     for data in datas:
#         writer.writerow(data)
#     print("保存文件成功，处理结束")


f=open('上市公司列表.csv','r',encoding='utf-8')
mystr = f.readline().strip()
company = open('company','w',encoding='utf-8')
company_news = open('company_news','w',encoding='utf-8')
company_time = open('company_time','w',encoding='utf-8')

# url='http://app.finance.ifeng.com/data/stock/tab_gaxw.php?code=sz000004'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}
while mystr:
    mystr1=mystr
    mystr=mystr.split(',')[0]
    url='http://app.finance.ifeng.com/data/stock/tab_gaxw.php?code=sz'+str(mystr)
    print(url)
    request=urllib.request.Request(url=url,headers=headers)
    content=urllib.request.urlopen(request).read().decode()
    pattern = re.compile(r'<a name=(.*?)></a>.*?<a href="http://finance.ifeng.com/a/\d+/\w+.shtml" target="_blank">(.*?)</a>')
    pattern1=re.compile(r'<span id="time">(.*?)</span>')
    #   pattern = re.compile(r'<a name=.*?></a>.*?<a href="http://finance.ifeng.com/a/\d+/\w+.shtml" target="_blank">(.*?)</a>')

    lt = pattern.findall(content)
    lt1=pattern1.findall(content)
    print(lt)
    # print(lt1)
    print(mystr)
    print(mystr1)
    company_news.write(str(mystr) + '\n')
    company_news.write(str(lt) + '\n'+'\n')
    company_time.write(str(lt1) + '\n')

    mystr = f.readline().strip()

# print(mystr)


f.close()
company.close()
company_news.close()
# company_time.close()
