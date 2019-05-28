# -*- coding: utf-8 -*-
import xlrd
import xlwt
import urllib2
from bs4 import BeautifulSoup
from distutils.filelist import findall
import re
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

def getData(url):
    page = urllib2.urlopen(url)

    contents = page.read()
    # 获得了整个网页的内容也就是源代码

    soup = BeautifulSoup(contents, "html.parser")
    finalList = []
    # print("豆瓣电影TOP250" + "\n" +" 影片名              评分       评价人数     链接 ")
    for tag in soup.find_all('div', class_='info'):
        parent = []
        # print tag.find('span', class_='title').get_text()
        m_name = tag.find('span', class_='title').get_text()
        m_rating_score = float(tag.find('span', class_='rating_num').get_text())
        m_people = tag.find('div', class_="star")
        m_span = m_people.findAll('span')
        m_peoplecount = m_span[3].contents[0]
        m_url = tag.find('a').get('href')
        # print( m_name+"        "  +  str(m_rating_score)   + "           " + m_peoplecount + "    " + m_url )
        parent = [m_name, m_rating_score, m_peoplecount, m_url]
        # subList = getSubPageData(parent[3],1)
        finalList.append(parent)
        # finalList = finalList +subList
        # break
    return finalList

#time:代表是第几代儿子
def getSubPageData(url,time):
    if time >= 3:
        return []
    page = urllib2.urlopen(url)
    contents = page.read()
    # 获得了整个网页的内容也就是源代码

    soup = BeautifulSoup(contents, "html.parser")
    subList = []
    for tag in soup.find_all('dl'):
        item = []
        m_name = tag.find('img').get('alt')
        m_url = tag.find('a').get('href')
        item = [m_name, time, 0, m_url]
        subList.append(item)
        sub_sub_list = getSubPageData(m_url,time+1)
        # print item
        subList = subList + sub_sub_list
    return subList



#[[],[],[],[],[]]
def witeToExcel(data):
    workBook = xlwt.Workbook()
    sheet = workBook.add_sheet('sheet1',cell_overwrite_ok=True)

    sheet.write(0, 0, '001')
    sheet.write(0, 1, '002')
    sheet.write(0, 2, '003')
    sheet.write(0, 3, '004')

    rowNum=0;
    for item in data:
        rowNum= rowNum+1
        colNum=0
        for item_detail in item:
            sheet.write(rowNum,colNum,item_detail)
            colNum = colNum + 1
    workBook.save('''./test.xls''')

if __name__ == '__main__':
    list1 = getData('http://movie.douban.com/top250?format=text')
    witeToExcel(list1)
    # getSubPageData("https://movie.douban.com/subject/1292052/")
    # print(__name__)