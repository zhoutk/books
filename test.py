import pymysql

conn = pymysql.connect(host='192.168.1.6', port=3388, user='root',
                       passwd='5LiarZp6', db='books', charset='utf8mb4')

with open("list.txt", encoding= 'utf-8') as f:
    line = f.readline()
    els = []
    bookCount = 0
    record = []
    while line:
        if line != "\n":
            els.append(line[:-1])
        else:
            if len(els) > 1:
                if els[0][-1:] == ":" and els[1][-1:] != "/":
                    info = ""
                    picName = ""
                    for e in els[1:]:
                        if e.startswith("pic."):
                            picName = e
                        elif e.endswith(".txt"):
                            try:
                                info = open("/home/zhoutk/" + els[0][:-1] + "/" + e, encoding="utf-8").read()
                            except:
                                print(els)
                    for e in els[1:]:
                        dotIndex = e.rfind(".")
                        if dotIndex > -1 and not(e[:dotIndex] == "info" or e[:dotIndex] == "pic"):
                            bookCount = bookCount + 1
                            record.append((e[:dotIndex], e[dotIndex + 1:], els[0][:-1], picName,info))
            els = []
        line = f.readline()
        if len(record) >= 1000:
            cur = conn.cursor()
            cur.executemany('insert into `book` (`book_name`,`category`,`path`,`cover`, `abstract`) values (%s,%s,%s,%s,%s)', record)
            conn.commit()
            print(bookCount)
            record = []
    if len(record) > 0:
        cur = conn.cursor()
        cur.executemany('insert into `book` (`book_name`,`category`,`path`,`cover`, `abstract`) values (%s,%s,%s,%s,%s)', record)
        conn.commit()
        print(bookCount)
    cur.close()
    conn.close()
    
    print(bookCount)

        
