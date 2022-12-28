import requests as req
from bs4 import BeautifulSoup
import datetime 
import pytz
import pickle

#create Taipei timezone
tw = pytz.timezone('Asia/Taipei')

# 指定要抓取的網頁URL
url = "https://ithelp.ithome.com.tw/users/20135354/articles?"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
# 使用requests.get() 來得到網頁回傳內容
r = req.get(url,headers=headers)
 
# request.get()回傳的是一個物件 
# 若抓成功(即r.status_code==200), 則網頁原始碼會放在物件的text屬性, 我們把它存在一個變數 'web_content'
web_content = r.text
soup = BeautifulSoup(web_content, 'html.parser')
qa_count = soup.find_all('span', class_='qa-condition__count')[2::3]
boardNameElements = soup.find('div', class_="profile-pagination").find_all('a')

article_links = []
article_views = []

for article_link in boardNameElements:
    #print(article_link['href'])
    article_links.append(article_link['href'])

for article_view in qa_count:
    #print(article_view.string)
    article_views.append(int(article_view.string))


article_links = list(set(article_links))
#print(article_links)

for article_link in article_links:
    url = article_link
    r = req.get(url,headers=headers)
    web_content = r.text
    soup = BeautifulSoup(web_content, 'html.parser')
    qa_count = soup.find_all('span', class_='qa-condition__count')[2::3]
    for article_view in qa_count:
        #print(article_view.string)
        article_views.append(int(article_view.string))

total_views = sum(article_views)
#print("累計發布文章篇數"+str(len(article_views))+"篇文章")
#print("累計文章觀看次數: "+str(total_views))
#print("平均文章觀看次數: "+str(round((total_views/len(article_views)),0)))
#print("資料更新時間:",datetime.datetime.now())

with open('lastRecord.txt', 'rb') as f:
    lastRecord = pickle.load(f)

lastRecord['lastView'] = int(lastRecord['lastView'])
add_view = total_views - lastRecord['lastView'] 

f = open("README.md", "w",encoding='UTF-8')
f.write("# iT邦幫忙 個人統計\n")
f.write("### 累計發布文章篇數: "+str(len(article_views))+"\n")
f.write("### 累計文章觀看次數: "+str(total_views)+" ("+str(add_view)+"\u2191)"+"\n")
f.write("### 平均文章觀看次數: "+str(round((total_views/len(article_views)),0))+"\n")
f.write("###### 資料更新時間: "+str(datetime.datetime.now(tw).strftime("%Y-%m-%d %H:%M:%S")))
f.close()

dict1 = {'lastView' : total_views}
file1 = open("lastRecord.txt", "wb") 
pickle.dump(dict1, file1)
file1.close()
