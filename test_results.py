import json
from flask import Flask, jsonify
from flask_socketio import SocketIO

import psycopg2
from psycopg2.extras import RealDictCursor
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'race',
    'user': 'chris',
    'password': 'password'
}

def get_db_connection():
    """Create a new database connection."""
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

def listen_to_db():
    """Listen to the PostgreSQL NOTIFY channel."""
    conn = get_db_connection()
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute('LISTEN results_channel;')
    
    print('Waiting for notifications on results_channel...')
    while True:
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            payload = notify.payload
            data = json.loads(payload)
            socketio.emit(f'update_{data["race_id"]}', data)  # Emit only for the specific race_id
            print(f'Notification received for race_id {data["race_id"]}: {payload}')


# def background_task():
#     """Background task that checks for new data in the results table."""
#     conn = get_db_connection()
#     cursor = conn.cursor(cursor_factory=RealDictCursor)
#     last_id = 0  # Track the last processed ID to check for new data
    
#     while True:
#         cursor.execute('SELECT * FROM results WHERE id > %s ORDER BY id ASC', (last_id,))
#         rows = cursor.fetchall()
        
#         if rows:
#             last_id = rows[-1]['id']  # Update last_id to the latest ID
#             socketio.emit('update', rows)  # Send new data to all connected clients
#         time.sleep(1)  # Check for new data every second
    
#     cursor.close()
#     conn.close()

@app.route('/api/results', methods=['GET'])
def get_results():
    """Fetch all rows from the results table."""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute('SELECT * FROM results')
        rows = cursor.fetchall()
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/results/<int:race_id>', methods=['GET'])
def get_results_by_race_id(race_id):
    """Fetch results for a specific race_id from the results table."""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute('SELECT * FROM results WHERE race_id = %s', (race_id,))
        rows = cursor.fetchall()
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/')
def index():
    """Serve the HTML page."""
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Real-Time Results</title>
        <!-- Include jQuery and jQuery UI -->
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <link rel="stylesheet" href="https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
        <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.min.js"></script>
        <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }

        #resultsTable {
            width: 100%;
            margin-top: 20px;
            border-collapse: collapse;
        }

        #resultsTable th, #resultsTable td {
            padding: 10px;
            text-align: center;
            border: 1px solid #ddd;
        }

        #resultsTable th {
            background-color: #f2f2f2;
        }

        #subscribeButton {
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
            margin-top: 10px;
        }

        #subscribeButton:hover {
            background-color: #45a049;
        }

        input[type="number"] {
            padding: 5px;
            width: 100px;
        }

        table.ui-widget-content {
            border: 1px solid #ccc;
            border-radius: 5px;
        }
    </style>
    </head>
    <body>
        <h1>Leader Board</h1>
        
        <!-- Input field for race ID -->
        <label for="race_id">Enter Race ID:</label>
        <input type="number" id="race_id" />
        <button id="subscribeButton">Subscribe</button>

        <!-- Table to display results -->
        <table id="resultsTable" class="ui-widget ui-widget-content" border="1">
            <thead>
                <tr class="ui-widget-header">
                    <th>Position</th>
                    <th>Racer Number</th>
                    <th>Race Name</th>
                    <th>Time</th>
                    <th>Recorded Timestamp</th>
                </tr>
            </thead>
            <tbody>
                <!-- New rows will be added here -->
            </tbody>
        </table>

        <script>
            $(document).ready(function() {
                const socket = io();
                let currentRaceId = null;

                // Function to handle subscription to a specific race_id
                $('#subscribeButton').click(function() {
                    const raceIdInput = $('#race_id').val();
                    if (raceIdInput && raceIdInput !== currentRaceId) {
                        currentRaceId = raceIdInput;

                        // Clear the table before subscribing to a new race
                        $('#resultsTable tbody').empty();

                        // Unsubscribe from any previous race_id updates
                        socket.off(`update_${currentRaceId}`);
                        
                        // Subscribe to the new race_id
                        socket.on(`update_${currentRaceId}`, function(data) {
                            const result = data.data;  // The actual data object received from the backend
                            const operation = data.operation;  // Operation type (INSERT, UPDATE, DELETE)
                            
                            // Create a new row for the table
                            const row = $('<tr></tr>')
                                .append($('<td></td>').text(result.position))
                                .append($('<td></td>').text(result.race_number))
                                .append($('<td></td>').text(result.racer_name))
                                .append($('<td></td>').text(result.time))
                                .append($('<td></td>').text(new Date().toLocaleString()));  // Timestamp of update

                            // Append the row to the table
                            $('#resultsTable tbody').append(row);
                            // Sort the table based on position after each new row
                            sortTableByPosition();
                        });
                    }
                });

                            // Function to sort the table based on the position column
            function sortTableByPosition() {
                const rows = $('#resultsTable tbody tr').get();

                rows.sort(function(a, b) {
                    const positionA = parseInt($(a).find('td').eq(0).text());  // Get position column
                    const positionB = parseInt($(b).find('td').eq(0).text());  // Get position column

                    return positionA - positionB;  // Sort in ascending order of position
                });

                // Re-append sorted rows to the table body
                $.each(rows, function(index, row) {
                    $('#resultsTable tbody').append(row);
                });
            }
            });
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    threading.Thread(target=listen_to_db, daemon=True).start()
    socketio.run(app, debug=True)
#    app.run(debug=True)
    