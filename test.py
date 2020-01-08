import pymysql
import os
import time

conn = pymysql.connect(host='192.168.1.6', port=3388, user='root', passwd='5LiarZp6', db='books', charset='utf8mb4')

with open("hanvon.txt", encoding= 'utf-8') as f:
    line = f.readline() 
    els = [] 
    bookCount = 0
    record = []
    while line:
        if line != "\n":
            els.append(line[:-1])
        else:
            if len(els) > 1:
                if els[0][-1:] == ":":
                    path = els[0][:-1]
                    lastIndex = path.rfind("/")
                    info = ""
                    fulltext = ""
                    picName = ""
                    tttt = path.split("/")
                    classified = tttt[2] if (len(tttt) > 2) else ""
                    classified_second = ""

                    

                    for e in els[1:]:
                        dotIndex = e.rfind(".")
                        if dotIndex > -1 and not(e.endswith("/")) and not(e[dotIndex + 1:] == "db" or e[dotIndex + 1:] == "opf" or e[dotIndex + 1:] == "DS_Store"):
                            if e.endswith(".txt"):
                                t = "c:\\temp\\" + e
                                fulltext = open("c:\\temp\\" + e, encoding="latin-1").read()
                                fulltext = fulltext.decode(encoding="utf-8")
                            bookCount = bookCount + 1
                            record.append((e[:dotIndex], e[dotIndex + 1:], path, picName,info,fulltext,classified,classified_second,"Hanvon",path[lastIndex + 1:]))
            els = []
        line = f.readline()
        if len(record) > 0:
                conn = pymysql.connect(host='192.168.1.6', port=3388, user='root', passwd='5LiarZp6', db='books', charset='utf8mb4')
                cur = conn.cursor()
                cur.executemany('insert into `book_txt` (`book_name`,`ext`,`path`,`cover`, `abstract`,`full_text`,`classified`,`classified_second`,`source`,`last_dir`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', record)
                conn.commit()
                cur.close()
                conn.close()
                record = []
                print(bookCount)
                
    if len(record) > 0:
        conn = pymysql.connect(host='192.168.1.6', port=3388, user='root', passwd='5LiarZp6', db='books', charset='utf8mb4')
        cur = conn.cursor()
        cur.executemany('insert into `book_txt` (`book_name`,`ext`,`path`,`cover`, `abstract`,`full_text`,`classified`,`classified_second`,`source`,`last_dir`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', record)
        conn.commit()
        print(bookCount)
        cur.close()
        conn.close()
    
    print(bookCount)
    print("finish.")

        
