from flask import Flask, render_template, jsonify, request
import requests
import plotly.graph_objs as go
import plotly.io as pio
import threading
import time

app = Flask(__name__)

# Monitored servers
MONITORED_SERVERS = {
    "Monitored Server (Agent)": "http://10.10.1.2:5000/metrics",
    "Server Two": "http://35.211.165.75:5000/metrics",
}

# Global variable for storing metrics
latest_metrics = {}

# Default thresholds (user adjustable)
thresholds = {
    "CPU_Usage": 80,    # Notify if CPU exceeds 80%
    "Memory_Usage": 75, # Notify if Memory exceeds 75%
    "Disk_Usage": 80,   # Notify if Disk exceeds 80%
    "Network_Usage": 1000000000,  # Alert if Network usage exceeds 1GB (in bytes)
    "Load_Average": 5   # Notify if Load Average exceeds 5
}

# Function to fetch metrics from monitored servers
def fetch_metrics():
    global latest_metrics
    data = {}
    for server_name, url in MONITORED_SERVERS.items():
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                metrics = response.json()
                if isinstance(metrics.get("Load_Average"), list):
                    metrics["Load_Average"] = metrics["Load_Average"][0]  # Extract first value
                data[server_name] = metrics
                
                # Print the results for debugging
                print(f"\n[DEBUG] Metrics from {server_name}:")
                print(f"  - CPU Usage: {metrics.get('CPU_Usage', 0)}%")
                print(f"  - Memory Usage: {metrics.get('Memory_Usage', 0)}%")
                print(f"  - Disk Usage: {metrics.get('Disk_Usage', 0)}%")
                print(f"  - Network Usage: {metrics.get('Network_Usage', 0) / 1e6} MB")
                print(f"  - Load Average: {metrics.get('Load_Average', 0)}\n")

            else:
                data[server_name] = {"error": "No response from server"}
        except requests.exceptions.RequestException:
            pass  # Ignore connection failures

    latest_metrics = data

# Background thread to update metrics every 10 seconds
def start_background_fetch():
    while True:
        fetch_metrics()
        time.sleep(10)

# Start background thread
threading.Thread(target=start_background_fetch, daemon=True).start()

# Route to fetch JSON metrics (for AJAX updates)
@app.route("/metrics")
def metrics():
    return jsonify(latest_metrics)

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
