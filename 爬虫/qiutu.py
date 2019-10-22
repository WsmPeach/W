#-coding:utf-8-*-
import urllib.request
import urllib.parse
import re
import os
import time

def download_image(content):
    pattern=re.compile(r'<div class="thumb">.*?<img src="(.*?)" .*?/>.*?</div>',re.S)
    lt=pattern.findall(content)
    print(lt)
    for image_src in lt:
        image_src='https:'+image_src
        dirname='qiutu'
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        filename=image_src.split('/')[-1]
        filepath=dirname+'/'+filename
        urllib.request.urlretrieve(image_src,filename)
        time.sleep(1)
#根据不同的页码生成不同的请求对象
def handle_request(url,page):
    url=url+str(page)+'/'
    # print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    }
    request = urllib.request.Request(url=url, headers=headers)
    return request

def main():
    url = 'https://www.qiushibaike.com/pic/page/'
    start_page=int(input('请输入起始页码：'))
    end_page=int(input('请输入结束页码：'))
    for page in range(start_page,end_page+1):
        #生成请求对象
        request=handle_request(url,page)
        content=urllib.request.urlopen(request).read().decode()
        # print(content)
        download_image(content)
        time.sleep(2)
if __name__ == '__main__':
        main()
