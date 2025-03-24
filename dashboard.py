from flask import Flask, render_template, jsonify, request
import requests
import plotly.graph_objs as go
import plotly.io as pio
import threading
import time

app = Flask(__name__)

# Monitored servers
MONITORED_SERVERS = {
    "Server Quy": "http://10.10.1.2:5000/metrics",
    "Server Jackson": "http://35.211.59.223:5000/metrics",
    "Server Sebas": "http://35.209.21.236:5000/metrics",
}

# Global variable for storing metrics
latest_metrics = {}

# Historical metrics storage for all servers and all 5 metrics
metric_history = {
    server: {
        "CPU_Usage": [],
        "Memory_Usage": [],
        "Disk_Usage": [],
        "Network_Usage": [],
        "Load_Average": [],
        "Timestamps": []
    } for server in MONITORED_SERVERS
}

# Default thresholds
thresholds = {
    "CPU_Usage": 80,    # changes color if CPU exceeds 80%
    "Memory_Usage": 75, # changes color if Memory exceeds 75%
    "Disk_Usage": 80,   # changes color if Disk exceeds 80%
    "Network_Usage": 1000000000,  # alert if Network usage exceeds 1GB (in bytes)
    "Load_Average": 5   # changes color Load Average exceeds 5
}

# Function to fetch metrics from monitored servers
def fetch_metrics():
    global latest_metrics
    data = {}
    timestamp = time.strftime("%H:%M:%S")  # Timestamp for history tracking

    for server_name, url in MONITORED_SERVERS.items():
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                metrics = response.json()
                if isinstance(metrics.get("Load_Average"), list):
                    metrics["Load_Average"] = metrics["Load_Average"][0]
                data[server_name] = metrics

                # Store metrics in history
                metric_history[server_name]["Timestamps"].append(timestamp)
                metric_history[server_name]["CPU_Usage"].append(metrics.get("CPU_Usage", 0))
                metric_history[server_name]["Memory_Usage"].append(metrics.get("Memory_Usage", 0))
                metric_history[server_name]["Disk_Usage"].append(metrics.get("Disk_Usage", 0))
                metric_history[server_name]["Network_Usage"].append(metrics.get("Network_Usage", 0) / 1e9)  # Convert to GB
                metric_history[server_name]["Load_Average"].append(metrics.get("Load_Average", 0))

                # Trim history to last 30 entries
                for key in metric_history[server_name]:
                    if len(metric_history[server_name][key]) > 30:
                        metric_history[server_name][key].pop(0)

                # Print the results for debugging
                print(f"\n Metrics from {server_name}:")
                print(f"  - CPU Usage: {metrics.get('CPU_Usage', 0)}%")
                print(f"  - Memory Usage: {metrics.get('Memory_Usage', 0)}%")
                print(f"  - Disk Usage: {metrics.get('Disk_Usage', 0)}%")
                print(f"  - Network Usage: {metrics.get('Network_Usage', 0) / 1e9} GB")
                print(f"  - Load Average: {metrics.get('Load_Average', 0)}\n")

            else:
                data[server_name] = {"error": "No response from server"}
        except requests.exceptions.RequestException:
            pass

    latest_metrics = data

# Background thread to update metrics every 5 seconds
def start_background_fetch():
    while True:
        fetch_metrics()
        time.sleep(5)

# Start background thread
threading.Thread(target=start_background_fetch, daemon=True).start()

# Route to fetch JSON metrics (for AJAX updates)
@app.route("/metrics")
def metrics():
    return jsonify(latest_metrics)

# Route to fetch historical metrics
@app.route("/history")
def history():
    return jsonify(metric_history)

# Route to update user-adjustable thresholds
@app.route("/update_thresholds", methods=["POST"])
def update_thresholds():
    global thresholds
    new_thresholds = request.json
    thresholds.update(new_thresholds)
    return jsonify({"message": "Thresholds updated successfully", "new_thresholds": thresholds})

# Route to render the dashboard
@app.route("/")
def dashboard():
    return render_template("dashboard.html", thresholds=thresholds)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)