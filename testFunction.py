import pandas as pd
import numpy as np
import requests
from lxml import etree
import time
url = "https://movie.douban.com/subject/27040853/"
url1 = "https://movie.douban.com/celebrity/1014295/movies?start=0&format=pic&sortby=time&"
header = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Mobile Safari/537.36',
          'Referer': 'https://movie.douban.com/celebrity/1014295/movies?start=0&format=pic&sortby=time&'}
header1 = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Mobile Safari/537.36'}
response = requests.get(url1, headers=header1)
time.sleep(2)
response = requests.get(url, headers=header)
print(response.status_code)
content = response.content.decode()
html = etree.HTML(content)
path = '//h2/i'
element = html.xpath(path)
# element = html.xpath('//span[@property="v:summary"]/text()')[0]
print(str(element).strip('\n').strip(' '))
