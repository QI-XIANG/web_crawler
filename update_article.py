import requests as req
from bs4 import BeautifulSoup

# 指定要抓取的網頁URL
url = "https://ithelp.ithome.com.tw/users/20135354/articles?"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
# 使用requests.get() 來得到網頁回傳內容
r = req.get(url,headers=headers)
 
# request.get()回傳的是一個物件 
# 若抓成功(即r.status_code==200), 則網頁原始碼會放在物件的text屬性, 我們把它存在一個變數 'web_content'
web_content = r.text
soup = BeautifulSoup(web_content, 'html.parser')
qa_title = soup.find_all('a', class_='qa-list__title-link')
qa_time = soup.find_all('a', class_='qa-list__info-time')
boardNameElements = soup.find('div', class_="profile-pagination").find_all('a')

article_links = []

for article_link in boardNameElements:
    #print(article_link['href'])
    article_links.append(article_link['href'])

article_links = list(article_links[:len(article_links)-1])

article_data = {}
each_art_link = {}

for title,time in zip(qa_title,qa_time):
    #print(title.string.strip())
    #print(time.string.strip())
    each_art_link[title.string.strip()] = str(title['href']).strip()
    article_data[time.string.strip()] = title.string.strip()

for article_link in article_links:
    url = article_link
    r = req.get(url,headers=headers)
    web_content = r.text
    soup = BeautifulSoup(web_content, 'html.parser')
    qa_title = soup.find_all('a', class_='qa-list__title-link')
    qa_time = soup.find_all('a', class_='qa-list__info-time')
    for title,time in zip(qa_title,qa_time):
        #print(title.string.strip())
        #print(time.string.strip())
        each_art_link[title.string.strip()] = str(title['href']).strip()
        article_data[time.string.strip()] = title.string.strip()

#df = pd.DataFrame(list(article_data.items()),
                   #columns=['Time', 'Title'])
#df

f = open("README.md", "a",encoding='UTF-8')
f.write('\n\n')
for key in article_data.keys():
    #print(key)
    f.write('* '+str(key)+" ["+str(article_data[key])+"]("+str(each_art_link[article_data[key]])+")\n")
f.close()

