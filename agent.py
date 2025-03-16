import os
import psutil
import threading
from flask import Flask, jsonify

app = Flask(__name__)

PIPE_PATH = "/tmp/monitoring_pipe"

# Function to write data to the named pipe
def write_to_pipe(data):
    def writer():
        try:
            with open(PIPE_PATH, "w", buffering=1) as fifo:
                fifo.write(data + "\n")
        except Exception as e:
            print(f"Error writing to pipe: {e}")

    # Start a new thread to execute writer function
    threading.Thread(target=writer, daemon=True).start()

@app.route('/metrics', methods=['GET'])
def get_metrics():
    metrics = {
        "CPU_Usage": psutil.cpu_percent(interval=1),
        "Memory_Usage": psutil.virtual_memory().percent,
        "Disk_Usage": psutil.disk_usage('/').percent,
        "Network_Usage": psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv,
        "Load_Average": os.getloadavg()[0]  # 1-minute load avg
    }

    # Write data to the named pipe
    write_to_pipe(str(metrics))

    return jsonify(metrics)



if __name__ == '__main__':
    if not os.path.exists(PIPE_PATH):
        os.mkfifo(PIPE_PATH)  # Ensure named pipe exists

    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
