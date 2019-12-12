import pymysql

conn = pymysql.connect(host='192.168.1.163', port=3306, user='root',
                       passwd='123456', db='books', charset='utf8mb4')

with open("booklist.txt", encoding= 'utf-8') as f:
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
                            break
                    for e in els[1:]:
                        dotIndex = e.rfind(".")
                        if dotIndex > -1 and not(e[:dotIndex] == "info" or e[:dotIndex] == "pic"):
                            bookCount = bookCount + 1
                            record.append((e[:dotIndex], e[dotIndex + 1:], els[0][:-1], picName))
            els = []
        line = f.readline()
    cur = conn.cursor()
    cur.executemany('insert into `book` (`book_name`,`category`,`path`,`cover`) values (%s,%s,%s,%s)', record)
    conn.commit()
    cur.close()
    conn.close()
    
    print(f"book count: {bookCount}")

        