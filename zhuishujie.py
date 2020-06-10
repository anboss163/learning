# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
import time
import re
import csv
import codecs
# import logging

HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3346.9 Safari/537.36'
}

# 完本小说
BASEURL = 'http://www.zhuishujie.com/all/order/recommend%2Bdesc/serialize/1.html'

books = []
try:
    # 状态（1：连载， 2：完本）
    book = {'status': '2'}
    basePage = requests.get(BASEURL, headers=HEADER, timeout=10)
    html = basePage.text
    obj = BeautifulSoup(html, 'html.parser')
    listDiv = obj.find('div', 'listboxw')
    summaryDivs = listDiv.findAll('dl')
    for  summary in summaryDivs:
        # 封面图片url
        book['imgUrl'] = summary.find('img', 'lazyimg')['data-original']
        # 书名
        book['name'] = summary.find('a', 'bigpic-book-name').text
        # 书籍详细链接
        book['detailLink'] = summary.find('a', 'bigpic-book-name')['href']

        pTags = summary.findAll('p')
        for p in pTags:
            isAuthorP = False
            isSummaryP = False
            aTags = p.findAll('a')
            if len(aTags) == 2:
                isAuthorP = True
                # 作者
                book['author'] = aTags[0].text
                # 类型
                book['type'] = aTags[1].text

            spanTags = p.findAll('span')
            if len(spanTags) == 2:
                isSummaryP = True
                book['totalWords'] = spanTags[0].text.strip(' |')


        print(book)

except RequestException as err:
    print('Failed to access url: ' + BASEURL)
