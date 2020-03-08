import requests
import pandas as pd
from lxml import etree
import time


class SonYejin:

    def __init__(self):
        self.start_url="https://movie.douban.com/celebrity/1014295/movies?start={}&format=pic&sortby=time&"
        self.header_suffix = ""
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}


    def get_url(self,num):
        url = self.start_url.format(num)
        return url

    def get_response_content(self, url):
        response = requests.get(url, headers=self.header)
        content = response.content.decode()
        time.sleep(1)
        return content


    def get_node(self, content, path):
        html = etree.HTML(content)
        element = html.xpath(path) if len(html.xpath(path))>=1 else None
        return element


    def get_data(self, content, path):
        titles = self.get_node(content, path + '//h6/a/text()')
        years = self.get_node(content, path + "//h6/span[1]/text()")
        casting = self.get_node(content, path + "/dl/dd/dl/dd[last()]/text()")

        movies = self.get_node(content, path)
        ratings = []
        totalcomments = []
        storylines = []
        for movie in movies:
            # get ratings and comments for each movie
            ratings.append(movie.xpath(".//div[@class='star clearfix']//span[2]/text()")[0] if len(
                movie.xpath(".//div[@class='star clearfix']//span")) >= 2 else None)
            totalcomments.append(movie.xpath(".//div[@class='star clearfix']//span[3]/text()")[0]
                                 if len(movie.xpath(".//div[@class='star clearfix']//span")) >= 3
                                 else None)
            # get storyline for each movie
            story_link = str(movie.xpath('.//h6/a/@href')[0])
            story_content = self.get_response_content(story_link)
            story = self.get_node(story_content, "//span[@property='v:summary']/text()")[0] \
                if self.get_node(story_content, "//span[@property='v:summary']/text()") \
                else None
            storylines.append(str(story).strip('\n').strip(' '))

        # get number of pages
        if self.total == 1000:
            self.total = int(self.get_node(content, "//div[@class='paginator']/a[last()]/text()")[0])

        df = pd.DataFrame([titles, years, ratings, totalcomments, casting, storylines],
                          index=['title', 'year', 'rating', 'total_comments', 'acted_by', "story"])
        df = df.T
        print(df.story)
        return df


    def save_data(self,df):
        df.to_csv("SonYejin`s movies_3withStoryline.csv", encoding='utf-8-sig')


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
            if self.header_suffix != "": self.header['Referer'] = url
            movie_path ="//div[@id='content']//div[@class='grid_view']/ul/li"
            datadf = datadf.append(self.get_data(content, movie_path), ignore_index=True)
            page+=1

        # 4 save
        self.save_data(datadf.sort_values('rating'))


if __name__=='__main__':
    sonyejin = SonYejin()
    sonyejin.run()

