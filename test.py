import pymysql
import os
import time

conn = pymysql.connect(host='192.168.1.6', port=3388, user='root', passwd='5LiarZp6', db='books', charset='utf8mb4')

with open("classified.txt", encoding= 'utf-8') as f:
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
                    info = ""
                    picName = ""
                    for e in els[1:]:
                        dotIndex = e.rfind(".")
                        if dotIndex > -1 and not(e.endswith("/")) and not(e[dotIndex + 1:] == "db" or e[dotIndex + 1:] == "jpg" or e[dotIndex + 1:] == "jpeg" or e[dotIndex + 1:] == "png" or e[dotIndex + 1:] == "gif"):
                            bookCount = bookCount + 1
                            path = els[0][:-1]
                            rindex = path.rfind("/")
                            record.append((e[:dotIndex], e[dotIndex + 1:], path, picName,info,path[rindex+1:],"Kindle_Chinese_books_Public"))
            els = []
        line = f.readline()
        if len(record) >= 1000:
                conn = pymysql.connect(host='192.168.1.6', port=3388, user='root', passwd='5LiarZp6', db='books', charset='utf8mb4')
                cur = conn.cursor()
                cur.executemany('insert into `book` (`book_name`,`ext`,`path`,`cover`, `abstract`,`classified`,`source`) values (%s,%s,%s,%s,%s,%s,%s)', record)
                conn.commit()
                cur.close()
                conn.close()
                record = []
                print(bookCount)
                
    if len(record) > 0:
        conn = pymysql.connect(host='192.168.1.6', port=3388, user='root', passwd='5LiarZp6', db='books', charset='utf8mb4')
        cur = conn.cursor()
        cur.executemany('insert into `book` (`book_name`,`ext`,`path`,`cover`, `abstract`,`classified`,`source`) values (%s,%s,%s,%s,%s,%s,%s)', record)
        conn.commit()
        print(bookCount)
        cur.close()
        conn.close()
    
    print("finish.")

        
