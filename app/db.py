import sqlite3

testdata = [
'Hårddisk',
'Processor',
'Hertz',
'RAM-Minne',
'Dator',
'Data ',
'Byte',
'Bit',
'Mega',
'Mus',
'Tangent',
'Windows',
'System',
'Program',
'Hårdvara',
'Mjukvara',
'Kilo',
'Skärm',
'Kontakt',
'Nätverk',
'Sladd',
'Frekvens',
'Ett',
'Noll',
'Backup',
'Server',
'Spel',
'Kommunikation',
'Filer',
'Text',
'Utrymme',
'Teknik',
'Anslutning',
'Kylare',
'Ström',
'Spänning',
'Buss',
'Klock',
'Hastighet',
'Pinnar',
'Webb-kamera',
'Linux',
'Mac',
'Apple',
'PC',
'NTFS',
'FAT32',
'UPS',
'Nätaggregat',
'Intel',
'AMD',
'DVD-skiva',
'SSD-hårddisk',
]

def initDB() -> (sqlite3.Connection, sqlite3.Cursor):
    con = sqlite3.connect("tutorial.db", check_same_thread=False)

    cur = con.cursor()

    # Create table words
    res = cur.execute("SELECT name FROM sqlite_master WHERE name='words'")

    if res.fetchone() is None:
        cur.execute("""CREATE TABLE words(WordID INTEGER PRIMARY KEY,
                         Name STRING NOT NULL,
                         ListID INTEGER NOT NULL,
                         FOREIGN KEY (ListID) REFERENCES Lists(ListID)
                 )""")


    # Create table lists
    res = cur.execute("SELECT name FROM sqlite_master WHERE name='lists'")

    if res.fetchone() is None:
        cur.execute("""CREATE TABLE lists(
                        ListID INTEGER PRIMARY KEY,
                        Name STRING NOT NULL UNIQUE
            
        )""")
    return (con, cur)


# Insert list
def InsertList(name: str, con: sqlite3.Connection, cur: sqlite3.Cursor):
    s = (name, )
    res = cur.execute("""
                        INSERT INTO lists( Name) VALUES (?)
                    """, s)
    con.commit()

# Insert word
def InsertWord(text: str, listName: str, con: sqlite3.Connection, cur: sqlite3.Cursor):
    st = (text, )
    sl = (listName, )
    res = cur.execute("SELECT ListID FROM lists WHERE Name=?", sl)
    dataID = res.fetchone()
    if dataID is None:
        print(f"List does not exist {listName}")
        return 
    datalist = (st[0], dataID[0])
    res = cur.execute("Insert INTO words(Name, ListID) VALUES (?, ?)", datalist)
    con.commit()


def GetWordsFromList(listName: str, con: sqlite3.Connection, cur: sqlite3.Cursor) -> list[any]:
    sl = (listName, )
    res = cur.execute("SELECT ListID FROM lists WHERE Name=?", sl)
    dataID = res.fetchone()
    if dataID is None:
        return 
    res = cur.execute("SELECT name FROM words WHERE ListID = ?", dataID)
    l = res.fetchall()
    return l

def GetLists(con: sqlite3.Connection, cur: sqlite3.Cursor) -> list[any]:
    res = cur.execute("SELECT Name FROM lists")
    return [i[0] for i in res.fetchall()]
    


if __name__ == '__main__':
    print("hejj")
    #for name in testdata:
        #InsertWord(name, 'data')
    Con, Cur = initDB()
    print(GetWordsFromList('data', Con, Cur) )
    print(GetLists(Con, Cur))
    