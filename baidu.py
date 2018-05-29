# 百度文章分类
# 输出至new.json
import json
import re
import sqlite3

from aip import AipNlp

APP_ID = '11310741'
API_KEY = 'UzTdSOi7kKgVSu1dWU9hRigT'
SECRET_KEY = 'XPBPjAkunpYrkyk5S1nD0Wm5q0FrCKQP'

databasename = 'data.db'


def getdata(databasename):
    conn = sqlite3.connect(databasename)
    conn.text_factory = str
    cursor = conn.cursor()
    cursor.execute('select title,content from news')
    re = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return re


rows = getdata(databasename)
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
dr = re.compile(r'•')
with open('news.json', 'w') as f:
    for row in rows:
        text = client.topic(str(row[0]), str(dr.sub('', row[1])))
        f.write(json.dumps(text).decode('utf-8'))
