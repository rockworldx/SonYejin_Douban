import requests
import pandas as pd
from lxml import etree


class SonYejin:

    def __init__(self):
        self.start_url="https://movie.douban.com/celebrity/1014295/movies?start={}&format=pic&sortby=time&"

    def get_url(self,num):
        url = self.start_url.format(num)
        return url

    def get_response_content(self, url):
        header = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Mobile Safari/537.36'}
        response = requests.get(url, headers=header)
        content = response.content.decode()
        return content

    def get_data(self, content):
        html = etree.HTML(content)
        movies = html.xpath("//div[@id='content']//div[@class='grid_view']/ul/li")
        titles=[]
        years=[]
        ratings=[]
        commentscnt=[]
        for movie in movies:
            titles.append(movie.xpath('.//h6/a/text()')[0])
            years.append(movie.xpath(".//h6/span[1]/text()")[0])
            ratings.append(movie.xpath(".//div[@class='star clearfix']//span[2]/text()")[0]
                           if len(movie.xpath(".//div[@class='star clearfix']//span"))>=2
                           else None)

        # get number of pages
        if self.total == 1000:
            self.total = int(html.xpath("//div[@class='paginator']/a[last()]/text()")[0])

        df = pd.DataFrame([titles,years,ratings], index=['title','year','rating'])
        df = df.T
        return df

    def save_data(self,df):
        df.to_csv("SonYejin`s movies_1simple.csv", encoding='utf_8_sig')


    def run(self):
        page=0
        self.total=1000
        datadf = pd.DataFrame()
        while page<self.total:
            # 1 get url
            url = self.get_url(page*10)
            # 2 send request, get response
            content = self.get_response_content(url)
            # 3 extract data
            print(self.get_data(content))
            datadf = datadf.append(self.get_data(content),ignore_index=True)
            page+=1

        # 4 save
        self.save_data(datadf.sort_values('rating'))


if __name__=='__main__':
    sonyejin = SonYejin()
    sonyejin.run()

