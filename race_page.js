 results_timer = null




//Start the race function, asks an are you sure question before starting.
// ---- pass in the race id to start -----



function start_race3(raceID) {
    if (raceID == 0) return;
    $("<div>Are you sure you want to start the race?</div>").dialog({
        title: "Confirm Start Race",
        modal: true,
        buttons: {
            "Yes": function() {
                $(this).dialog("close");
                race_start(raceID);
                
            },
            "No": function() {
                $(this).dialog("close");
            }
        }
    });
}

function confirmStartRace() {
    return new Promise((resolve) => {
        $("<div>Are you sure you want to start the race?</div>").dialog({
            title: "Confirm Start Race",
            modal: true,
            buttons: {
                "Yes": function () {
                    $(this).dialog("close");
                    resolve(true); // User confirmed
                },
                "No": function () {
                    $(this).dialog("close");
                    resolve(false); // User declined
                }
            }
        });
    });
}

function end_race(raceID) {
    if (raceID == 0) return;
    $("<div>Are you sure you want to end the selected race?</div>").dialog({
        title: "Confirm Start Race",
        modal: true,
        buttons: {
            "Yes": function() {
                $(this).dialog("close");
                race_end(raceID);
            },
            "No": function() {
                $(this).dialog("close");
            }
        }
    });
}

function add_race_participants() {

}

function update_race_participants(tableid, raceID) {
    (async () => {
        try {
            const race_participents_data = await get_race_participants(raceID);
            $("#"+tableid+" tbody").empty();
            race_participents_data.forEach(participent => {
                var newRow = "<tr><td>"+`${participent.ParticipentID}`+"</td><td>"+`${participent.BibNum}`+"</td><td>"+`${participent.firstname}`+"</td><td>"+`${participent.lastname}`+"</td><td>"+`${participent.age}`+"</td><td>"+`${participent.gender}`+"</td>"+
                "<td><button class=\"edit-btn\" onclick=\"edit_participents_in_table("+`${participent.ParticipentID}`+")\">Edit</button>" +
                "<button class=\"delete-btn\" onclick=\"delete_participents_in_table("+`${participent.ParticipentID}`+")\">Delete</button></td></tr>"
                //console.log("Adding row ", newRow);
                $("#"+tableid+" tbody").append(newRow);
            });

        } catch (err) {
            console.error("Error fetching race participant:", err);
        }
    })();
}


function update_current_race_table(tableid, raceID){
    (async () => {
        try {
            const current_participent_data = await get_current_race_participants(raceID);
            $("#"+tableid+" tbody").empty();
            current_participent_data.forEach(participent => {
                var newRow = "<tr><td>"+`${participent.ParticipentID}`+"</td><td>"+`${participent.Name}`+"</td><td>"+`${participent.Bibnum}`+"</td><td>"+`${participent.time}`+"</td>"+
                "<td><button class=\"edit-btn\" onclick=\"edit_participents_in_table("+`${participent.ParticipentID}`+")\">Edit</button>" +
                "<button class=\"delete-btn\" onclick=\"delete_participents_in_table("+`${participent.ParticipentID}`+")\">Delete</button></td></tr>"
                console.log("Adding row ", newRow);
                $("#"+tableid+" tbody").append(newRow);
            });

        } catch (err) {
            console.error("Error fetching race participant:", err);
        }
    })();
}















// Show the add a new participant dialog and when ok is pressed call the add_participant function to make the
//call to add the data into the database.
function add_new_participant() {
    $("<div id=\"new_participant_dialog\">"+
        "<h3>Enter new participent details</h3>"+
        "<label for=\"fname\">First name:</label><br>"+
        "<input type=\"text\" id=\"fname\" name=\"fname\" value=\"John\"><br>"+
        "<label for=\"lname\">Last name:</label><br>"+
        "<input type=\"text\" id=\"lname\" name=\"lname\" value=\"Doe\"><br><br>"+
        "<label for=\"participentAge\">Age:</label>"+
        "<select id=\"participentAge\">"+
        "<option value=\"18-39\">18-39</option>"+
        "<option value=\"40-49\">40-49</option>"+
        "<option value=\"50-59\">50-59</option>"+
        "<option value=\"60-69\">60-69</option>"+
        "<option value=\"senior\">senior</option>"+
        "</select>"+
        "<br><label for=\"Gender\">Gender:</label>"+
        "<select id=\"Gender\">"+
        "<option value=\"Male\">Male</option>"+
        "<option value=\"Female\">Female</option>"+
        "</select>"+
        "</div>").dialog({
        title: "Confirm Start Race",
        modal: true,
        close: function() {
            $("#new_participant_dialog").remove();
        },
        buttons: {
            "Ok": function() {
                
                var firstname= $('#fname').val();
                var lastname= $('#lname').val();
                var age= $('#participentAge').val();
                var gender= $('#Gender').val();
                //console.log("Dialog vals : "+firstname, lastname, age, gender);
                $(this).dialog("close");
                add_participant(firstname,lastname,age,gender)

            },
            "Cancel": function() {
                $(this).dialog("close");
            }
        }
    });
} 
//Easy method to force an update of the table 
function refesh_participent_table() {
    get_all_participents('participantsTable');
}

//Gets the participents from the database and shows them in the participents table.
function load_participents_into_table(participents_data) {
    
    $("#participentsTable tbody").empty();
    participents_data.forEach(participent => {
        var newRow = "<tr><td>"+`${participent.ID}`+"</td><td>"+`${participent.firstname}`+"</td><td>"+`${participent.lastname}`+"</td><td>"+`${participent.age}`+"</td><td>"+`${participent.gender}`+"</td>"+
        "<td><button class=\"edit-btn\" onclick=\"edit_participents_in_table("+`${participent.ID}`+")\">Edit</button>" +
        "<button class=\"delete-btn\" onclick=\"delete_participents_in_table("+`${participent.ID}`+")\">Delete</button></td></tr>"
        //console.log("Adding row ", newRow);
        $("#participentsTable tbody").append(newRow);
    });
}

function load_results_into_table(results_data) {
    
    $("#LiveResultsTable tbody").empty();
    results_data.forEach(result => {
        var newRow = "<tr><td>"+`${result.racer_name}`+"</td><td>"+`${result.race_number}`+"</td><td>"+`${result.time}`+"</td></tr>"
        $("#LiveResultsTable tbody").append(newRow);
    });
}

async function update_results_table(){
    race_id = $('#raceSelect').val();
    current_results= await get_current_race_results(race_id);
            
    load_results_into_table(current_results);
    

}


function delete_participents_in_table(pID) {
    //should ask an are you sure question.
    delete_a_participent(pID)
}
//Enable a user to edit the details of a partisipant. 
function edit_participents_in_table(pID) {

    (async () => {
        try {
            const data = await get_a_participent(pID);
            $("<div id=\"edit_participent_dialog\">"+
                "<h3>Enter new participent details</h3>"+
                "<label for=\"fname\">First name:</label><br>"+
                "<input type=\"text\" id=\"fname\" name=\"fname\" value=\""+data.firstname+"\"><br>"+
                "<label for=\"lname\">Last name:</label><br>"+
                "<input type=\"text\" id=\"lname\" name=\"lname\" value=\""+data.lastname+"\"><br><br>"+
                "<label for=\"participentAge\">Age:</label>"+
                "<select id=\"participentAge\">"+
                "<option value=\"18-39\">18-39</option>"+
                "<option value=\"40-49\">40-49</option>"+
                "<option value=\"50-59\">50-59</option>"+
                "<option value=\"60-69\">60-69</option>"+
                "<option value=\"senior\">senior</option>"+
                "</select>"+
                "<br><label for=\"Gender\">Gender:</label>"+
                "<select id=\"Gender\">"+
                "<option value=\"Male\">Male</option>"+
                "<option value=\"Female\">Female</option>"+
                "</select>"+
                "</div>").dialog({
                title: "Confirm Start Race",
                modal: true,
                open: function() {
                    // Set the Gender and Age values dynamically
                    $("#Gender").val(data.gender); 
                    $("#participentAge").val(data.age); 
                },
                close: function() {
                    $("#edit_participent_dialog").remove();
                },
                buttons: {
                    "Ok": function() {
                    
                        var firstname= $('#fname').val();
                        var lastname= $('#lname').val();
                        var age= $('#participentAge').val();
                        var gender= $('#Gender').val();
                        $(this).dialog("close");
                        update_a_participent(pID,firstname,lastname,age,gender);

                    },
                    "Cancel": function() {
                        $(this).dialog("close");
                    }
                }
            });
        
            console.log("Fetched participant:", data); // Use the data
        } catch (err) {
            console.error("Error fetching participant:", err);
        }
    })();

    //pData = get_a_participent(pID);
    //console.log("pData : "+pData);
    
}
// updates the video with correct id and add date time to force reload
function update_video(race_id) {

    document.getElementById("race_video").src = "/api/race/"+race_id+"/video_feed?"+new Date().getTime();
}

//Button js to simulate switching between pages using a single html page. 
//Div's in the html page have id's each div represents a section/page on the screen. Changing the 
//visiblity shows different pages.

$(document).ready(function() {
    // Navigation between pages
    $('#loginButton').click(function() {
        $('#loginPage').hide();
        $('#mainMenuPage').show();
    });

    $('#adminButton').click(function() {
        $('#mainMenuPage').hide();
        $('#adminPage').show();
    });

    $('#raceButton').click(function() {
        $('#mainMenuPage').hide();
        $("#startRaceButton").prop("disabled", true);
        get_races('raceSelect');
        $('#racePage').show();
    });

    $('#resultsButton').click(function() {
        $('#mainMenuPage').hide();
        $('#resultsPage').show();
        
    });
    $('#showParticipents').click(function() {
        $('#participentPage').hide();
        $('#participentShowPage').show();
        refesh_participent_table();
    });

    

    // Back buttons
    $('#backToMainFromAdmin').click(function() {
        $('#adminPage').hide();
        $('#mainMenuPage').show();
    });

    $('#backToMainFromRace').click(function() {
        $('#racePage').hide();
        $('#mainMenuPage').show();
    });

    $('#backToMainFromResults').click(function() {
        $('#resultsPage').hide();
        $('#mainMenuPage').show();
    });
    
    $('#backToadminFrompart').click(function() {
        $('#participentPage').hide();
        $('#adminPage').show();
    });

    $('#backToparticipentPage').click(function() {
        $('#participentShowPage').hide();
        $('#participentPage').show();
    });
    
     $('#raceSelect').change(function(){
         
        if ($('#raceSelect').val() == 0) {
            $("#startRaceButton").prop("disabled", true);
            $("#raceParticipentsTable tbody").empty();
            return;
        }
        else {
            $("#startRaceButton").prop("disabled", false);
        }
            
        console.log("Update racers list for "+$('#raceSelect').val());
        update_race_participants("raceParticipentsTable",$('#raceSelect').val());
     })

    //admin controlls
    $('#participents').click(function(){
        $('#adminPage').hide();
        $('#participentPage').show();
    });
        // new participent
    $('#startRaceButton').click(async function(){
        $('#racePage').hide();
        $('#ActiveRacePage').show();
        


// Update: Fixed async issues - dad
// JavaScript executes actions asynchronously, so the original code didn't wait  
// for the user to press Yes/No in the Start Race dialog.  
// Within the dialog, `race_start` was called only after the user clicked "Yes".  
// However, `race_start` had already returned and triggered `update_video` to start the video stream.  
// Since the user had not yet clicked "Yes", `update_video` didn't detect that the race had started  
// and instead displayed the `no_video_feed` image.  
//  
// The fix makes the dialog call synchronous using `async/await`, ensuring that the code waits  
// for the user to confirm before starting the race and updating the video feed.

        const userConfirmed = await confirmStartRace();
         if (userConfirmed) {
            race_id = $('#raceSelect').val();
            results_timer = setInterval(update_results_table, 10000);
            race_start_status = race_start(race_id);
            console.log(race_start_status);
            update_video(race_id);
             
             //update_current_race_table(("LiveResults", raceID));
         }
    });



    $('#backToRacePage').click(function(){
        $('#ActiveRacePage').hide();
        $('#racePage').show();
        
    });
    



    $('#StopRace').click(function(){
        clearInterval(results_timer)
        end_race($('#raceSelect').val())
        
        
    });


    $('#addRaceParticipant').click(function(){add_race_participants()});
    // Start Race button
    $('#newParticipent').click(function() {add_new_participant()});
});
