import requests
from bs4 import BeautifulSoup
import time
import sqlite3

base_url = "https://report.ge/politics/"

connection = sqlite3.connect("news.db")
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS latest_news(
                    id INTEGER,
                    title TEXT,
                    date TEXT)
                    """)

id = 1
for i in range(1, 6):
    r = requests.get(base_url + str(i))
    c = r.text

    soup = BeautifulSoup(c, "html.parser")
    tbody = soup.find("ul", {'class': 'category-news-blocks'})

    rows = tbody.find_all("li")

    for item in rows:
        title = item.find('h3').text
        date = item.find('span').text

        cursor.execute("Insert into latest_news values(?,?,?)", (id, title, date[:-2]))
        id += 1

    time.sleep('20')

cursor.execute("select * from latest_news")

for data in cursor.fetchall():
    print(data)

connection.commit()
connection.close()