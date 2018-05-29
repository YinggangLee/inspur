# -*- coding: utf-8 -*- 
import json
import re
import sqlite3
import jieba
import jieba.analyse
import csv
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

databasename = 'data.db'
stopwords=''

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


def fenci(rows):
    dr = re.compile(r'</?\w+[^>]*>')
    line = re.compile(r'\n+')
    result = []
    for row in rows:
        text = line.sub('\n', dr.sub('', row[0])+dr.sub('', row[1]).replace('&nbsp;', '').replace(
            '&gt;', '>').replace('&lt;', '<').replace('&amp;', '&').replace('&quot;', '"')).decode('utf8', 'ignore')[0:100].encode('utf8')
        words=delstop(text,stopwords)
        result.append(words)
        # result.append(jieba.analyse.extract_tags(text,20))
    return result


def stopword(stopword):
    with open(stopword, "r") as fp:
        words = fp.read()
    result = jieba.cut(words)
    new_words = []
    for r in result:
        new_words.append(r)
    return set(new_words)


def delstop(words, stopset):
    result = jieba.cut(words)
    new_words = []
    for r in result:
        if r not in stopset:
            new_words.append(r)
    return new_words


rows = getdata(databasename)
stopwords=stopword('stopword.txt')
# jieba.analyse.set_stop_words('stopword.txt')
lines = fenci(rows)
with open('words.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(lines)
    # for line in lines:
    #     for word in line:
    #         f.write(unicode(word, encoding="utf-8"))
    #         f.write(',')
    #     f.write('\n')


