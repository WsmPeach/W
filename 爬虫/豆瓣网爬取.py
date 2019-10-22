#-coding:utf-8-*-
import requests
from lxml.html import fromstring
import json

class SpiderDouban():
    def __init__(self,url):
        self.url=url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }
    def getdata(self):
        r=requests.get(url=self.url,headers=self.headers)

        data=fromstring(r.text)
        selector=data.xpath('//div[@id="nowplaying"] /div[@class="mod-bd"]/ul/li')
        print(selector)
        movie_data=[]
        for i in selector:
            title=i.xpath('@data-title')[0]
            score=i.xpath('@data-score')[0]
            region=i.xpath('@data-region')[0]
            actors=i.xpath('@data-actors')[0]
            director=i.xpath('@data-director')[0]

            movie_data.append({
                'title':title if title else'',
                'score': score if  score else'',
                'region': region if region else '',
                'actors': actors if actors else '',
                'director': director if director else '',


            })
            with open('movie_data.json','w',encoding='utf-8')as f:
                json.dump(movie_data,f,indent=1,ensure_ascii=False)
        pass

if __name__=='__main__':
    s=SpiderDouban('https://movie.douban.com/cinema/nowplaying/nanchang/')
    s.getdata()

