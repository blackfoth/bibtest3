
import time
from flask import Flask
from markupsafe import escape
from flask import render_template
from flask import jsonify
from flask import Response, send_file, render_template_string
import databasepostg as database
from flask import request
from flask_cors import CORS  #
import detectrunners 
import race_clock as clock
import threading
import logging



#The name of the no image jpg file.
no_feed_image = "NoFeed.jpg"

#Create an instance of the Flask server.
app = Flask(__name__)
#Create an instance of the stopwatch for the races (max 10 only)
race_stopwatch =clock.racestopwatch()

race_thread = None
#The connection to the database created and deleted across different API calls. 
database_connection = None
#Are we sending videos to the browser for a race this is not multi race safe.
streaming = False


# Enable CORS for all routes in the app so we don't get a cross scripting error in the 
# browser.
CORS(app)


@app.route("/")
def index():
    """
    Placeholder for the imdex page. Should use this to server the main
    html page. This should read the main html file and send it to the browser
    """
    return send_file ("race.html",mimetype='text/html')
#    return "Index Page"

@app.route("/javascript/<file_name>",methods=['GET'])
def get_javascript(file_name):
    return send_file ("javascript/"+file_name,mimetype='application/javascript')

@app.route("/image/<file_name>",methods=['GET'])
def get_image(file_name):
    return send_file ("images/"+file_name,mimetype='image/jpeg')

@app.route('/api/race',methods=['GET'])
def get_races():
    """
    Returns all the races within the database. The races are returned in a
    json structure. <details here>
    """
    conn = database.db_connection()

    races=database.get_all_races(conn)
    database.db_close(conn)
    return jsonify (races)
    

@app.route('/api/race/<race_id>',methods=['GET'])
def get_race(race_id):
    """
    Returns information about the selected. Not currently implemented.
    """
    return f'race {escape(race_id)}'


@app.route('/api/race/<race_id>/duration',methods=['GET'])
def get_race_time(race_id):
    """
    Returns the current time (as a string) from the race clock for race id.
    The api will return a json reponse {'status':'ok','race_duration':'00:00:00.000'} 
    """
    duration = race_stopwatch.get_formatted_time(int(race_id))
    return jsonify({"status":"ok","race_duration":duration})


@app.route('/api/race/<race_id>/video_feed')
def video_feed(race_id):
    """
    This will serve either a video stream for the race if one is running or a static image. This 
    approch was suggested by a chatGPT search. On the html page an img tag points to this 
    api will call this function which will return a picture or a video if streaming is true/false.

    The mimetype tells the browser what to expect and how to process it. 
    """
    global streaming
    print("Streaming : ",streaming)
    if streaming: 
        return Response(detectrunners.run_race_processing(race_id),mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return send_file(no_feed_image,mimetype='image/jpeg')

@app.route('/api/race/<race_id>/start',methods=['GET'])
def get_race_start(race_id):
    """
    To start a race this api is called with the race_id. This will start the stop watch for the race
    establish a connection to the database and call race_start on the detectrunners 
    package. Detect runners start will return and an ok status is returned with 
    the race id. The detection process will continue until end_race is called.
    """
    global streaming
    race_stopwatch.start_race(int(race_id))
    
    streaming = True
    database_connection = database.db_connection()
    detectrunners.race_start(database_connection,race_id)
    time.sleep(1)
    #database.update_race_state(database_connection,race_id,True)
    #race_thread = threading.Thread(target=detectrunners.race_start, args=(database_connection, race_id))
    #race_thread.start()
    #detectrunners.race_start(conn,race_id)
    return jsonify({"status":"ok","race_id":race_id})

@app.route('/api/race/<race_id>/end',methods=['GET'])
def get_race_end(race_id):
    """
    Will end the race for race_id. It stop the race clock. Set streaming to false
    to stop the video being sent to the browser, close the database connection and 
    call race end on the detectrunners package.
    """
    global streaming
    race_stopwatch.stop_race(int(race_id))
    streaming = False
    
    detectrunners.race_end(race_id)
    database.db_close(database_connection)
    return jsonify({"status":"ok","race_id":race_id})

@app.route('/api/race/<race_id>/participant',methods=['GET'])
def get_race_participant(race_id):
    """ 
    Gets all race participents for a given race and returns them as a json 
    structure <show structure here>
    
    """
    conn = database.db_connection()
    racers = database.get_race_participents(conn, race_id)
    database.db_close(conn)
    return jsonify(racers)




@app.route('/api/race/<race_id>/results', methods=['GET'])
def race_results_endpoint(race_id):  
    conn = database.db_connection()  
    results = database.get_race_results(conn, race_id) 
    print(results) 
    database.db_close(conn)  
    return jsonify(results)  

@app.errorhandler(404)
def page_not_found(error):
    """
    If the page/api requested is not found display this for the flask package
    """
    print (error)
    page_not_found_html = "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>Page Not Found</title></head><body>    <h1>Page not found</h1></body>"
    return page_not_found_html, 404

@app.route('/api/participent',methods=['POST'])
def add_participent():
    """
    Add a new participent to the database via a POST method. The data to add is sent
    in a JSON structure and extracted into first_name, last_name, age and gender.
    This information is passed to the database package add_participent
    """
    conn = database.db_connection()
    data = request.get_json()
    print(data)
    first_name = data.get('first_name')  # Use .get() to avoid errors if the field doesn't exist
    last_name = data.get('last_name')
    age = data.get('age')
    gender = data.get('gender')
    database.add_participent(conn,first_name,last_name,age,gender)
    database.db_close(conn)
    return f'participent {data}'


@app.route('/api/participent', methods=['GET'])
def get_all_add_participent():
    """
    Returns a list of all the participants within the database. These are not 
    participants for a race, this is the full list of participants within the 
    database. Returned as a JSON stucture <show structure here>
    """
    conn = database.db_connection()
    all_participents = database.get_all_participents(conn)
    #print(all_participents)
    database.db_close(conn)
    return jsonify(all_participents)

@app.route('/api/participent/<participent_id>', methods=['GET'])
def get_a_participent(participent_id):
    """
    Get the details from the database of a participent whos ID is given. Returns
    the details in a JSON structure.
    """
    conn = database.db_connection()
    participent = database.get_a_participent(conn,participent_id)
    database.db_close(conn)
    return jsonify(participent)

@app.route('/api/participent/<participent_id>', methods=['PUT'])
def update_a_participent(participent_id):
    """
    Enable participant details to be updated via a PUT method. The details are 
    contained within the body of the request and the ID of the participant 
    is <participent_id>. The structure of the body is in JSON and looks like 
    this <put it here>
    """
    #Get the request data from the request body
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400

    # You can now access the data as a Python dictionary
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    age = data.get('age')
    gender = data.get('gender')

    print(firstname,lastname,age,gender)
    conn = database.db_connection()
    database.update_a_participent(conn,participent_id,data)
    database.db_close(conn)
    return jsonify({"status":"ok"})

@app.route('/api/participent/<participent_id>', methods=['DELETE'])
def delete_a_participent(participent_id):
    """
    This deletes the partisipant from the database whos ID is given in the 
    URL using the DELETE method (see RESTFul).  
    """
    conn = database.db_connection()
    database.delete_a_participent(conn,participent_id)
    database.db_close(conn)
    return jsonify({"status":"ok"})

if __name__ == '__main__':
    app.run(debug=True)