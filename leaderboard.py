import sqlite3
import datetime
import time

conn = sqlite3.connect("leaderBoard.db")
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS leaderBoard(name TEXT, datestamp TEXT, score INT, status REAL)')

def add_player(puan):
    if table_full():#checks if the table is full
        if not lowest_score(puan):#if the table full and the score is higher than at least the last score add the score to the table
            c.execute('DELETE FROM leaderBoard WHERE rowid=10')
            date = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
            status = 'Normal'
            c.execute("INSERT INTO leaderBoard (name,datestamp,score,status) VALUES (?,?,?,?)",
                          ("Sinan", date, puan, status))
            c.execute("CREATE TABLE ordered_board(name TEXT, datestamp TEXT, score INT, status REAL)")#creates a temperor table for sorting the data
            c.execute("INSERT INTO ordered_board (name,datestamp,score,status) SELECT name,datestamp,score,status FROM leaderBoard ORDER BY score DESC ")#sorts the data by getting from the original table
            c.execute("DROP TABLE leaderBoard")#drops the original table
            c.execute("ALTER TABLE ordered_board RENAME TO leaderBoard")#renames the sorted table
            update_highscore()#updates the highscore
    else:#add the player if the table isn't full
        date = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
        status = 'Normal'
        c.execute("INSERT INTO leaderBoard (name,datestamp,score,status) VALUES (?,?,?,?)",
                  ("Sinan", date, puan, status))
        c.execute(
            "CREATE TABLE ordered_board(name TEXT, datestamp TEXT, score INT, status REAL)")  # creates a temperor table for sorting the data
        c.execute(
            "INSERT INTO ordered_board (name,datestamp,score,status) SELECT name,datestamp,score,status FROM leaderBoard ORDER BY score DESC ")  # sorts the data by getting from the original table
        c.execute("DROP TABLE leaderBoard")  # drops the original table
        c.execute("ALTER TABLE ordered_board RENAME TO leaderBoard")  # renames the sorted table
        update_highscore()  # updates the highscore
    conn.commit()
    c.close()
    conn.close()

def update_highscore():
    c.execute("UPDATE leaderBoard SET status='Normal' WHERE status='High Score'")
    c.execute("UPDATE leaderBoard SET status='High Score' WHERE rowid=1")

    conn.commit()

def get_high_score():
    c.execute('SELECT score FROM leaderBoard WHERE rowid=1')
    highScore = c.fetchone()
    return highScore[0]

def show_table():
    c.execute('SELECT ROWID, name, score FROM leaderBoard')
    table = ""
    for row in c.fetchall():
        table += str(row[0])+"."+ str(row[1])+": "+str(row[2])+" pts\n"

    return table

def table_full():
    c.execute('SELECT * FROM leaderBoard')
    amount = c.fetchall()

    return len(amount)>=10

def lowest_score(puan):
    c.execute('SELECT score FROM leaderBoard WHERE score<?',(puan,))
    amount = c.fetchall()
    return len(amount)==0




