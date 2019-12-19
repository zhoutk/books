import pymysql
import os
import time

conn = pymysql.connect(host='192.168.1.6', port=3388, user='root', passwd='5LiarZp6', db='books', charset='utf8mb4')

with open("kindBookStore.txt", encoding= 'utf-8') as f:
    line = f.readline() 
    els = [] 
    bookCount = 0
    record = []
    while line:
        if line != "\n":
            els.append(line[:-1])
        else:
            if len(els) > 1:
                if els[0][-1:] == ":" and os.path.exists("/home/zhoutk/" + els[0][:-1]):
                    path = els[0][:-1]
                    info = ""
                    picName = ""
                    classified = ""
                    classified_second = ""
                    c1 = path.find("中文书库")
                    c2 = path.find("英文书库")
                    if c1 > -1 or c2 > -1:
                        cindex = c1 if (c1 > -1) else c2
                        f1 = path.find("/", cindex + 1)
                        if f1 > -1:
                            classified = path[cindex + 1: f1]
                        else:
                            classified = path[cindex + 1:]
                    if c1 > -1 and (classified == "小说" or classified == "艺术"):
                        f2 = path.find("/", c1 + 8)
                        if f2 > -1:
                            classified_second = path[c1 + 8:f2]
                        else:
                            classified_second = path[c1 + 8]

                    for e in els[1:]:
                        dotIndex = e.rfind(".")
                        if dotIndex > -1 and not(e.endswith("/")) and not(e[dotIndex + 1:] == "db" or e[dotIndex + 1:] == "opf" or e[dotIndex + 1:] == "DS_Store"):
                            bookCount = bookCount + 1
                            record.append((e[:dotIndex], e[dotIndex + 1:], path, picName,info,classified,classified_second,"Kindle_Chinese_books_Public"))
            els = []
        line = f.readline()
        if len(record) >= 10000:
                conn = pymysql.connect(host='192.168.1.6', port=3388, user='root', passwd='5LiarZp6', db='books', charset='utf8mb4')
                cur = conn.cursor()
                cur.executemany('insert into `book` (`book_name`,`ext`,`path`,`cover`, `abstract`,`classified`,`classified_second`,`source`) values (%s,%s,%s,%s,%s,%s,%s,%s)', record)
                conn.commit()
                cur.close()
                conn.close()
                record = []
                print(bookCount)
                
    if len(record) > 0:
        conn = pymysql.connect(host='192.168.1.6', port=3388, user='root', passwd='5LiarZp6', db='books', charset='utf8mb4')
        cur = conn.cursor()
        cur.executemany('insert into `book` (`book_name`,`ext`,`path`,`cover`, `abstract`,`classified`,`classified_second`,`source`) values (%s,%s,%s,%s,%s,%s,%s,%s)', record)
        conn.commit()
        print(bookCount)
        cur.close()
        conn.close()
    
    print("finish.")

        
