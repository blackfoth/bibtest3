# #username = user
# #password = password
# #database name = run_info
# #table name = bib_info

import psycopg2

# Database connection
def db_connection():
    conn = psycopg2.connect(
        host="localhost",
        user="zack",
        password="password",
        database="race_database"
    )
    return conn

# Close the database connection
def db_close(conn):
    if conn:
        conn.close()

# Get all participants
def get_all_participents(conn):
    cursor = conn.cursor()
    sql = "SELECT \"ID\", firstname, lastname, age, gender FROM public.participents"
    cursor.execute(sql)
    results = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    results_as_dict = [dict(zip(columns, row)) for row in results]
    cursor.close()
    return results_as_dict

# Get all race participants by race ID
def get_all_race_participents(conn, ID):
    cursor = conn.cursor()
    sql = """
        SELECT participents.FirstName, participents.LatName, partrace.BibNum 
        FROM partrace 
        JOIN participents ON partrace.ParticipentID = participents.ID 
        JOIN race ON partrace.RaceID = race.ID 
        WHERE race.ID = %s
    """
    cursor.execute(sql, (ID,))
    results = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    results_as_dict = [dict(zip(columns, row)) for row in results]
    cursor.close()
    return results_as_dict

def  get_race_participents(conn, raceID):
    cursor = conn.cursor()
    sql = """
        SELECT participents.firstname, participents.lastname,participents.age,participents.gender, partrace.\"BibNum\", participents.lastname,partrace.\"ParticipentID\"
        FROM partrace 
        JOIN participents ON partrace.\"ParticipentID\" = participents.\"ID\"
        JOIN race ON partrace.\"RaceID\" = race.\"ID\" 
        WHERE race.\"ID\" = %s
    """
    cursor.execute(sql, (raceID, ))
    results = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    results_as_dict = [dict(zip(columns, row)) for row in results]
    cursor.close()
    return results_as_dict

# Get specific race participant by race ID and BibNum
def get_race_participent(conn, raceID, BibNum):
    cursor = conn.cursor()
    # sql = """
    #     SELECT participents.FirstName, participents.LatName, partrace.BibNum 
    #     FROM partrace 
    #     JOIN participents ON partrace.ParticipentID = participents.ID 
    #     JOIN race ON partrace.RaceID = race.ID 
    #     WHERE race.ID = %s AND partrace.BibNum = %s
    # """
    sql = """
    SELECT participents.firstName, participents.lastname, partrace."BibNum", partrace."ParticipentID" 
        FROM partrace 
        JOIN participents ON partrace."ParticipentID" = participents."ID" 
        JOIN race ON partrace."RaceID" = race."ID" 
        WHERE race."ID" = %s AND partrace."BibNum" = %s
    """
    cursor.execute(sql, (raceID, BibNum))
    results = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    results_as_dict = [dict(zip(columns, row)) for row in results]
    cursor.close()
    return results_as_dict

# Get all races
def get_all_races(conn):
    cursor = conn.cursor()
    sql = "SELECT \"ID\", \"Title\", \"Date\", \"Description\", \"StartTime\" FROM race"
    cursor.execute(sql)
    results = cursor.fetchall()
    if results:
        columns = [col[0] for col in cursor.description]
        results_as_dict = [dict(zip(columns, row)) for row in results]
    else:
        results_as_dict = None
    cursor.close()
    print(results_as_dict)
    return results_as_dict

#add participent
def add_participent(conn,firstname, latname, age,gender):
    cursor = conn.cursor()
# SQL query to insert data into a table (replace table_name and column names accordingly)
    insert_query = """
        INSERT INTO participents (firstname, lastname, age,gender)
        VALUES (%s, %s, %s,%s);
    """
    data = (firstname, latname, age,gender)
    # Execute the query with data
    cursor.execute(insert_query, data)
# Commit the transaction to the database
    conn.commit()
# Print a success message
    print("Data inserted successfully!")
# Close the cursor and connection
    cursor.close()

def get_a_participent(conn,pID):
 
    cursor = conn.cursor()
    sql = "SELECT \"ID\", firstname, lastname, gender, age FROM participents where \"ID\" = %s"
    cursor.execute(sql,(pID,))
    result = cursor.fetchone()  # return one row as we only asked for one get a part...
    if result:
        columns = [col[0] for col in cursor.description]
        result_as_dict = dict(zip(columns, result))
    else:
        result_as_dict = None  # Return None if no participant for the id give found

    cursor.close()
    return result_as_dict

def update_a_participent(conn,pID,data):

    firstname = data.get('firstname')
    lastname = data.get('lastname')
    age = data.get('age')
    gender = data.get('gender')

    cursor = conn.cursor()
# SQL query to insert data into a table (replace table_name and column names accordingly)
    insert_query = """
        UPDATE participents SET
        firstname = %s,
        lastname = %s,
        gender = %s,
        age = %s
        WHERE \"ID\"= %s;
    """
    #
    cursor.execute(insert_query,(firstname,lastname,gender,age,pID))
    conn.commit()
# Print a success message
    print("Data updated successfully!")
# Close the cursor and connection
    cursor.close()

def delete_a_participent(conn,pID):
    cursor = conn.cursor()
# SQL query to insert data into a table (replace table_name and column names accordingly)
    delete_query = """
        DELETE FROM participents
        WHERE \"ID\"= %s;
    """
    #
    cursor.execute(delete_query,(pID,))
    conn.commit()
# Print a success message
    print("Data deleted successfully!")
# Close the cursor and connection
    cursor.close()
#sql
#get working in code
#put into finsih and update 

def add_result(conn,BibNum,firstname,lastname,raceclock,raceID):
    cursor = conn.cursor()
    racer_name = firstname + " " + lastname
    sql = """
    INSERT INTO race_results (race_number, racer_name, time, race_id)
    VALUES (%s, %s, %s, %s);


          """
    cursor.execute(sql,(BibNum,racer_name,raceclock,raceID))
    conn.commit()
    cursor.close()


def get_race_results(conn, raceID):
    cursor = conn.cursor()
    sql ="""
            SELECT * FROM public.race_results
            WHERE race_id = %s
            ORDER BY CAST(time AS INTEGER) ASC;

         """
    cursor.execute(sql, (raceID,))
    results = cursor.fetchall()  # Fetch results

    if results:
        columns = [col[0] for col in cursor.description]
        result_as_dict =[dict(zip(columns,row)) for row in results]
    else:
        result_as_dict = None  # Return None if no participant for the id give found

    cursor.close()
    print("results as dict ",result_as_dict)  # Close cursor before returning
    return result_as_dict 
# # Example usage
# connection = db_connection()
# #add_result(connection,11,'to','om','2435',1)
# #print(get_race_participent(connection,1,"77"))


# race = get_race_results(connection, 1)
# print(race)




# # Fetch data
#try:
#     # Uncomment as needed
#    all_participents = get_all_participents(connection)
#    print(all_participents)

#     race_participents = get_all_race_participents(connection, 1)
#     print("Race Participants:", race_participents)

#     # participent = get_race_participent(connection, 1, 288)
#     # print("Specific Participant:", participent)

#     # races = get_all_races(connection)
#     # print("Races:", races)
# #finally:
# db_close(connection)
