from flask import Flask, jsonify
import psutil, os

app = Flask(__name__)

@app.route('/metrics', methods=['GET'])
def get_metrics():
    metrics = {
        "CPU_Usage": psutil.cpu_percent(interval=1),
        "Memory_Usage": psutil.virtual_memory().percent,
        "Disk_Usage": psutil.disk_usage('/').percent,
        "Network_Usage": psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv,
        "Load_Average": os.getloadavg()
    }
    return jsonify(metrics)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

