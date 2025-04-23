# #username = user
# #password = password
# #database name = run_info
# #table name = bib_info

import mysql.connector

def db_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="user",
        password="password",
        database='run_info'
    )
    return mydb

def db_close(conn):
    if conn.is_connected():
        conn.close()

def get_all_participents(conn):
    cursor=conn.cursor()
    sql = "SELECT ID,FirstName, LatName, Age FROM participents"
    cursor.execute(sql)
    results=cursor.fetchall()
    colums = [col[0] for col in cursor.description]
    results_as_dict = [dict(zip(colums, row))for row in results]
    # for row in results:
    #     print (row)
    cursor.close()
    return results_as_dict


def get_all_race_participents(conn,ID):
    cursor=conn.cursor()
    sql = "SELECT participents.FirstName, participents.LatName,partrace.BibNum FROM partrace JOIN participents ON partrace.ParticipentID = participents.ID JOIN race ON partrace.RaceID = race.ID WHERE race.ID =%s"
    cursor.execute(sql,(ID,))
    results=cursor.fetchall()
    colums = [col[0] for col in cursor.description]
    results_as_dict = [dict(zip(colums, row))for row in results]
    # for row in results:
    #     print (row)
    cursor.close()
    return results_as_dict


def get_race_participent(conn,raceID,BibNum):
    cursor=conn.cursor()
    sql = "SELECT participents.FirstName, participents.LatName,partrace.BibNum FROM partrace JOIN participents ON partrace.ParticipentID = participents.ID JOIN race ON partrace.RaceID = race.ID WHERE race.ID =%s AND partrace.BibNum=%s"
    cursor.execute(sql,(raceID,BibNum))
    results=cursor.fetchall()
    colums = [col[0] for col in cursor.description]
    results_as_dict = [dict(zip(colums, row))for row in results]
    # for row in results:
    #     print (row)
    cursor.close()
    return results_as_dict

def get_all_races(conn):
    cursor=conn.cursor()
    #sql = "SELECT ID,Title,Date,StartTime,Description FROM race"
    sql = "SELECT ID,Title,Date,Description FROM race"
    cursor.execute(sql)
    results=cursor.fetchall()
    colums = [col[0] for col in cursor.description]
    results_as_dict = [dict(zip(colums, row))for row in results]
    # for row in results:
    #     print (row)
    cursor.close()
    return results_as_dict


connection= db_connection()

#all_participents = get_all_participents(connection)
#print(all_participents)
race_participents=get_all_race_participents(connection,1)
participent=get_race_participent(connection,1,288)
races= get_all_races(connection)
print(races)
db_close(connection)