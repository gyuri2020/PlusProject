import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import MySQLdb

conn = MySQLdb.connect(host = 'localhost', user = 'root', password='1234', database='test', charset='utf8')
sql = "insert into gnuhdoc(name, belong,major, education, career, link) values(%s,%s,%s,%s, %s, %s)"
#sql = "insert into dankookpub(name,belong, pname) values(%s,%s, %s)"
cursor=conn.cursor()
#cursor.execute("CREATE TABLE gnuhdoc(Name text, Belong text, Major text, Education text, Career text, Link text)")
#cursor.execute("CREATE TABLE dankookpub(Name text,Belong text, Pname text)")

chrome_options = webdriver.ChromeOptions()
wd = webdriver.Chrome(r'C:\Users\82109\dataset\chromedriver.exe')

# 기본 설정(관련 과 설정)
department = ['순환기', '심장', '흉부','혈액']
departmentLink = []
doctordepartmentLink = []
doctorLink = []
keyws = ['졸업', '수료','취득','석사','박사','학사','취득']
keyws2 = ['(전)', '교수', '위원', '인턴', '전문의', '레지던트', '조교수' ,'회원']
belong = '창원경상국립대학교병원'
memory = []

gnuhURL = 'https://www.gnuch.co.kr/gnuh/treat/docList.do?rbsIdx=55'

wd.get(gnuhURL)
time.sleep(2)

for i in department:
    try:
        search = wd.find_element_by_id("key")
        search.send_keys(i)
        search.send_keys(Keys.RETURN)
        time.sleep(3)
        datas = wd.find_elements_by_class_name('icoIntro')
        num = len(datas)
        print(wd.current_url)
        print(num)
        for now in range(0,num):
            datas[now].click()
            time.sleep(3)


            name = wd.find_element_by_class_name('doctor_name').text
            name = name.split('[')[0]
            double = False
            try:
                major = wd.find_element_by_css_selector('#contents_area > div.profile.group > div.cont > div.doctor_major > ul > li.title > span').text
            except:
                major = ''
            try:
                temp = wd.find_element_by_css_selector('#contents_area > div.profile.group > div.cont').text
                datas = temp.split('\n')
                career = []
                education = []

                for data in datas:
                    if '[학력]' in data:
                        education.append(data.split('[학력] ')[1])
                    elif '[경력] ' in data:
                        career.append(data.split('[경력] ')[1])

            except:
                career = ''
                education = ''


            print(name)
            print(major)
            career = ', '.join(career)
            print(career)
            education = ', '.join(education)
            print(education)

            for m in memory:
                print(m)
                print(name)
                print(belong)
                print('\n')
                if name == m[0] and major == m[1]:
                    double = True
                    print(m)

            memory.append((name, major))


            if double == False:
                cursor.execute(sql, (name, belong, major, education, career, wd.current_url))




            wd.get(gnuhURL)
            time.sleep(3)
            search = wd.find_element_by_id("key")
            search.send_keys(i)
            search.send_keys(Keys.RETURN)
            time.sleep(3)
            datas = wd.find_elements_by_link_text('상세소개')

    except:
        pass

conn.commit()
conn.close()