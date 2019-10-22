#-coding:utf-8-*-
import urllib.request
import urllib.parse
import os

url='http://tieba.baidu.com/f?&ie=utf-8&'

baname=input('请输入贴吧名：')
startpage=int(input('请输入起始页码：'))
endpage=int(input('请输入结束页码：'))

if not os.path.exists(baname):
    os.mkdir(baname)
for page in range(startpage,endpage+1):
    data={
        'kw':baname,
        'pn':(startpage-1)*50
    }
    data=urllib.parse.urlencode(data)
    url_t=url+data
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    request=urllib.request.Request(url=url_t,headers=headers)
    print('第%s页开始下载......'%page)
    response=urllib.request.urlopen(request)
    filename=baname+'-'+str(page)+'.html'
    filpath=baname+'/'+filename

    with open(filpath,'wb')as fp:
        fp.write(response.read())
        print('第%s页下载结束'%page)





