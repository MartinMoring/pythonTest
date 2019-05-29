# -*- coding: utf-8 -*-
import xlwt
import urllib2
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('UTF-8')


# 获取该url中的电影数据
# url：豆瓣电影TOP250连接 ，
# 返回    [["电影名"，评分数，评价人数，"电影地址"],["电影名"，评分数，评价人数，"电影地址"]]
def getData(url):

    # 获得了整个网页的内容也就是源代码
    page = urllib2.urlopen(url)
    contents = page.read()
    soup = BeautifulSoup(contents, "html.parser")

    finalList = []
    for tag in soup.find_all('div', class_='info'):
        parent = []
        m_name = tag.find('span', class_='title').get_text()
        m_rating_score = float(tag.find('span', class_='rating_num').get_text())
        m_people = tag.find('div', class_="star")
        m_span = m_people.findAll('span')
        m_peoplecount = m_span[3].contents[0]
        m_url = tag.find('a').get('href')
        # print( m_name+"        "  +  str(m_rating_score)   + "           " + m_peoplecount + "    " + m_url )
        parent = [m_name, m_rating_score, m_peoplecount, m_url]
        finalList.append(parent)
        # 获得了一个电影关联的其他电影
        # subList = getSubPageData(parent[3],1)
        # finalList = finalList +subList
    return finalList

#获得了一个电影关联的其他电影
# url ： 要爬取的页面
# time ：:代表是第几代儿子 ，如：2表示子页面的子页面
def getSubPageData(url, time):
    if time >= 3:#限制第三代和三代以上就终止，防止无限爬取
        return []
    # 获得了整个网页的内容也就是源代码
    page = urllib2.urlopen(url)
    contents = page.read()
    soup = BeautifulSoup(contents, "html.parser")
    subList = []
    for tag in soup.find_all('dl'):
        item = []
        m_name = tag.find('img').get('alt')
        m_url = tag.find('a').get('href')
        item = [m_name, time, 0, m_url]
        subList.append(item)
        sub_sub_list = getSubPageData(m_url, time + 1)
        subList = subList + sub_sub_list
    return subList


# 将格式为[[],[],[],[],[]]的数据写到excle中
def witeToExcel(data):
    workBook = xlwt.Workbook()
    sheet = workBook.add_sheet('sheet1', cell_overwrite_ok=True)
    # 标题
    sheet.write(0, 0, '001')
    sheet.write(0, 1, '002')
    sheet.write(0, 2, '003')
    sheet.write(0, 3, '004')

    rowNum = 0;
    for item in data:
        rowNum = rowNum + 1
        colNum = 0
        for item_detail in item:
            sheet.write(rowNum, colNum, item_detail)
            colNum = colNum + 1
    workBook.save('''./test.xls''')


if __name__ == '__main__':
    #获取数据
    list = getData('http://movie.douban.com/top250?format=text')
    # 写入数据
    witeToExcel(list)
