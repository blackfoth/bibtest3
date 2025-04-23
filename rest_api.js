//The top level address of the api server, all requests will be prepended to this string
const url = 'http://127.0.0.1:5000/api';

//Calls the /race api to get all the racers defined within the database. If succesful this function will update the
//race html select box whos selector id is equal to the parameter race_selector. The html selector will also have a none entry that 
//has not come from the database. Error calling the api will show an error in the console.log.
function get_races(race_selector){
    fetch(url+'/race')
        .then(response =>{
            if(!response.ok){
                throw new Error('unable to read race info'+ response.statusText)
            }
            //console.log(response.json())
            return response.json()
        })
        .then(data=>{
            console.log(data);
            
                var select = $('#'+race_selector);
                
                // Clear existing options
                select.empty();
                //Add an empty row
                select.append('<option value=\"0\">None</option>');
                // Iterate over the JSON data and add options
                $.each(data, function(index, item) {
                    console.log(item);
                    select.append('<option value="' + item.ID + '">' + item.Title + '</option>');
                });
            
        })
        .catch(error=>{
            console.error('there is issues')
            console.error(error)
        });

        
}
//Calls the race start API with a race id, the call will wait for a response. The format for a race start call is /race/1/start where 1 is the id of the race to start.
//Any errors starting he race throws a Error with unable to start. If success then the race is started, with no feedback to the user.
//Could add something to grey out & disable the start button to avoid double starts. 
async function race_start(raceID) {
    try {
        const response = await fetch(url+'/race/'+raceID+'/start');
        if (!response.ok) {
            throw new Error('Unable to start the race : ' + response.statusText);
        }
        return await response.json(); // Return the parsed JSON data
    } catch (error) {
        console.error('There was an issue calling ' + url + '/race/' + raceID+'/start');
        console.error(error);
        throw error; // Let the caller handle the error
    }
}

//Calls the race end API with a race id. The format for a race end call is /race/1/end where 1 is the id of the race to end.
//Any errors starting he race throws a Error with unable to start. If success then the race is started, with no feedback to the user.
//Could add something to grey out & disable the end button to avoid double end. 
function race_end(raceID) {
    fetch(url+'/race/'+raceID+'/end')
    .then(response =>{
        if(!response.ok){
            throw new Error('Unable to end race '+ response.statusText)
        }
        //console.log(response.json())
        return response.json()
    })
    .then(data=>{
        console.log(data);
    })
    .catch(error=>{
        console.error('There is issue ending the race.')
        console.error(error)
    });
}
//Returns a list of participant in an asynchronous way, this avoid blocking other threads in the UI. Once a response is recived the calling function will
//get the results which will be can then be further processed. The format of the call is /race/2/participant where 2 is the race id. 
//
//A list of participants is returned as a JSON object and errors are reported in the console.log of the browser.
async function get_race_participants(raceID) {
    try {
        const response = await fetch(url+'/race/'+raceID+'/participant');
        if (!response.ok) {
            throw new Error('Unable to read race participant info: ' + response.statusText);
        }
        return await response.json(); // Return the parsed JSON data
    } catch (error) {
        console.error('There was an issue calling ' + url + '/participant/' + raceID+'/participant');
        console.error(error);
        throw error; // Let the caller handle the error
    }
}

// updates results table for the race 
async function get_current_race_results(raceID) {
    try {
        const response = await fetch(url+'/race/'+raceID+'/results');
        if (!response.ok) {
            throw new Error('Unable to read race results info: ' + response.statusText);
        }
        return await response.json(); // Return the parsed JSON data
    } catch (error) {
        console.error('There was an issue calling ' + url + '/result/' + raceID+'/result');
        console.error(error);
        throw error; // Let the caller handle the error
    }
}





//Enables a participant to be added to the database via the UI. Given the participant first name, last name, age (range) and gender these are package up
//into a json object, added to the body of the request and sent to the api /participent as a POST request.
//The function will not tell the calling function it successfully added the participent and there is not error capture defined.
function add_participant(firstn,lastn,age,gender){
   
    // Data to be sent as JSON
    data = {
        first_name: firstn,
        last_name: lastn,
        gender: gender,
        age: age
    };
    //console.log("Date ->",data)
    // Sending a POST request with JSON
    fetch(url+"/participent", {
        method: 'POST',                // HTTP method
        headers: {
            'Content-Type': 'application/json'  // Set the content type to JSON
        },
        body: JSON.stringify(data)  // Convert the data object to a JSON string
    })
    .then(response => response.json())  // Parse the JSON response
    .then(data => {
        console.log('Success:', data);  // Handle the response data
    })
    .catch(error => {
        // console.error('Error:', error);  // Handle any errors that occur during the request
    });
}

//Returns all the participents in the database by calling /participent. The retured values are in json format and are passed to the 
//load_participents_into_table function which will update the html table, adding a new row per person in the json respons data.
function get_all_participents(table_id) {
    fetch(url+'/participent')
    .then(response =>{
        if(!response.ok){
            throw new Error('unable to read race info'+ response.statusText)
        }
        //console.log(response.json())
        return response.json()
    })
    .then(data=>{
        console.log(data);
        load_participents_into_table(data);
    })
    .catch(error=>{
        console.error('There was an issue calling '+url+'/participant')
        console.error(error)
    });
}

//Newer version that wait for a response before returning. Given a participent id this call will return the details of that participent 
//to the calling process. It uses the async flag to enable the results of the call to be read by the calling function. The api called 
//is /participent/3 where three is the participent id to get the results for, Error are reported t the console.log 
async function get_a_participent(pID) {
    try {
        const response = await fetch(url + '/participent/' + pID);
        if (!response.ok) {
            throw new Error('Unable to read participant info: ' + response.statusText);
        }
        return await response.json(); // Return the parsed JSON data
    } catch (error) {
        console.error('There was an issue calling ' + url + '/participant/' + pID);
        console.error(error);
        throw error; // Let the caller handle the error
    }
}
//Enables a exisitng participant to be updated withn the database via the UI. Given the participant id, first name, last name, age (range) and gender these are package up
//into a json object, added to the body of the request and sent to the api /participent as a PUT request (PUT means to update all). 
//The function will call a refesh_participent_table function to flush the changes to the UI ***Spelling of function name****
function update_a_participent(pID,firstname,lastname,age,gender) {
   
    data = {
        firstname: firstname,
        lastname: lastname,
        gender: gender,
        age: age
    };
    fetch(url+"/participent/"+pID, {
        method: 'PUT',                // HTTP method
        headers: {
            'Content-Type': 'application/json'  // Set the content type to JSON
        },
        body: JSON.stringify(data)  // Convert the data object to a JSON string
    })
    .then(response => response.json())  // Parse the JSON response
    .then(data => {
        refesh_participent_table();
        console.log('Success:', data);  // Handle the response data
    })
    .catch(error => {
        // console.error('Error:', error);  // Handle any errors that occur during the request
    });
}
//Enables a exisitng participant to be deleted from the database via the UI. Given the participant id this is sent to 
//the api /participent/44 as a DELETE request where 44 is the id of the participant to be deleted. The function will 
//call a refesh_participent_table function to flush the changes to the UI ***Spelling of function name****
function delete_a_participent(pID) {
   
    fetch(url+"/participent/"+pID, {
        method: 'DELETE',                // HTTP method
        headers: {
            'Content-Type': 'application/json'  // Set the content type to JSON
        },
    })
    .then(response => response.json())  // Parse the JSON response
    .then(data => {
        refesh_participent_table();
        console.log('Success:', data);  // Handle the response data
    })
    .catch(error => {
        // console.error('Error:', error);  // Handle any errors that occur during the request
    });
}
