import os
import psutil
from flask import Flask, jsonify

app = Flask(__name__)

# Named pipe path
PIPE_PATH = "/tmp/monitoring_pipe"

# Function to write data to the named pipe
def write_to_pipe(data):
    try:
        with open(PIPE_PATH, "w") as fifo:
            fifo.write(data + "\n")
    except Exception as e:
        print(f"Error writing to pipe: {e}")

@app.route('/metrics', methods=['GET'])
def get_metrics():
    print("Request received for metrics")  # Debugging print statement
    try:
        metrics = {
            "CPU_Usage": psutil.cpu_percent(interval=1),
            "Memory_Usage": psutil.virtual_memory().percent,
            "Disk_Usage": psutil.disk_usage('/').percent,
            "Network_Usage": psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv,
            "Load_Average": os.getloadavg()[0]
        }
        print("Metrics fetched successfully")  # Debugging print statement
        return jsonify(metrics)
    except Exception as e:
        print(f"Error fetching metrics: {e}")  # Print error if any
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists(PIPE_PATH):
        os.mkfifo(PIPE_PATH)  # Ensure named pipe exists

    app.run(host="0.0.0.0", port=5000, debug=False)

