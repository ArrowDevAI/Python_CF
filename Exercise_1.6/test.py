# MicroPython Server Code
from machine import Pin, Timer
import time

VALVE_PIN = 2
valve = Pin(VALVE_PIN, Pin.OUT)
timer = Timer(-1)

def close_valve_after_delay():
    valve.on()
    print("Valve auto-closed after timer")

def route_handler(path):
    print("\n--- Route Handler Debug ---")
    print("Received path:", repr(path))
    print("Valve status:", valve.value())
    
    if path == "/":
        return "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + """
        <html>
            <head>
                <style>
                    body {
                        font-size: 2em;
                    }
                    .button {
                        display: inline-block;
                        padding: 10px 20px;
                        margin: 10px;
                        cursor: pointer;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        font-size: 1.5em;
                    }
                    .button:hover {
                        background-color: #45a049;
                    }
                    .input {
                        padding: 8px;
                        margin: 10px;
                        border-radius: 4px;
                        border: 1px solid #ddd;
                        font-size: 1.5em;
                    }
                    #status {
                        margin-top: 20px;
                        font-size: 1.2em;
                        color: #333;
                    }
                </style>
            </head>
            <body>
                <h1>Welcome to Irrigate</h1>
                <p>Valve Control:</p>
                <button class="button" onclick="controlValve('open')">Open Valve</button>
                <button class="button" onclick="controlValve('close')">Close Valve</button>
                
                <div style="margin-top: 20px;">
                    <label>Open for duration (minutes):</label>
                    <input type="number" id="duration" class="input" min="1" max="60" value="5">
                    <button class="button" onclick="openWithDuration()">Start</button>
                </div>

                <p id="status">Status will appear here...</p>

                <script>
                    // Control Valve Open/Close
                    function controlValve(action) {
                        document.getElementById('status').textContent = 'Processing...';
                        fetch('/' + action, {
                            method: 'GET',
                        })
                        .then(response => response.text())
                        .then(text => {
                            document.getElementById('status').textContent = text;
                        })
                        .catch(error => {
                            document.getElementById('status').textContent = 'Error: ' + error;
                        });
                    }
                    
                    // Open Valve with Duration and Countdown
                    function openWithDuration() {
                        const minutes = parseInt(document.getElementById('duration').value, 10);
                        const statusElement = document.getElementById('status');

                        if (isNaN(minutes) || minutes <= 0) {
                            statusElement.textContent = 'Please enter a valid duration (greater than 0 minutes).';
                            return;
                        }

                        let remainingSeconds = minutes * 60; // Convert minutes to seconds

                        statusElement.textContent = 'Starting countdown...';

                        // Start the countdown
                        const countdownInterval = setInterval(() => {
                            if (remainingSeconds > 0) {
                                const mins = Math.floor(remainingSeconds / 60);
                                const secs = remainingSeconds % 60;
                                statusElement.textContent = `Time Remaining: ${mins}m ${secs}s`;
                                remainingSeconds--;
                            } else {
                                clearInterval(countdownInterval);
                                statusElement.textContent = 'Waiting for server response...';
                            }
                        }, 1000); // Update every second

                        // Send Fetch Request
                        fetch('/open_timer/' + minutes, {
                            method: 'GET',
                        })
                        .then(response => response.text())
                        .then(text => {
                            clearInterval(countdownInterval); // Ensure countdown stops
                            statusElement.textContent = text; // Display server response
                        })
                        .catch(error => {
                            clearInterval(countdownInterval); // Ensure countdown stops
                            statusElement.textContent = 'Error: ' + error;
                        });
                    }
                </script>
            </body>
        </html>
        """
    
    elif path.startswith("/open_timer/"):
        try:
            # Extract minutes from path and convert to milliseconds
            minutes = int(path.split("/")[-1])
            if minutes > 0:
                valve.off()
                # Convert minutes to milliseconds for the timer
                ms = minutes * 60 * 1000
                timer.init(period=ms, mode=Timer.ONE_SHOT, callback=lambda t: close_valve_after_delay())
                return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nValve opened for {minutes} minutes"
            else:
                return "HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nInvalid duration"
        except ValueError:
            return "HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nInvalid duration format"
            
    elif path == "/open":
        valve.off()
        return "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nValve opened"
    
    elif path == "/close":
        valve.on()
        # Cancel any running timer
        timer.deinit()
        return "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nValve closed"
    
    else:
        print(f"No match found - path: '{path}'")
        return "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nInvalid endpoint"

