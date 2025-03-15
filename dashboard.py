from flask import Flask, render_template, jsonify
import requests
import plotly.graph_objs as go
import plotly.io as pio
import threading
import time

app = Flask(__name__)

# Monitored servers
MONITORED_SERVERS = {
    "Monitored Server (Agent)": "http://10.10.1.2:5000/metrics",  # Internal IP for GCP communication
    "Server Two": "http://35.211.165.75:5000/metrics",
}

# Global variable for storing metrics
latest_metrics = {}

# Function to fetch metrics from monitored servers
def fetch_metrics():
    global latest_metrics
    data = {}
    for server_name, url in MONITORED_SERVERS.items():
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                metrics = response.json()
                # Ensure Load_Average is extracted correctly
                if isinstance(metrics.get("Load_Average"), list):
                    metrics["Load_Average"] = metrics["Load_Average"][0]  # Take only the 1-minute load avg
                data[server_name] = metrics
            else:
                data[server_name] = {"error": "No response from server"}
        except requests.exceptions.RequestException:
            pass
    
    latest_metrics = data
    print(f"[INFO] Updated metrics: {latest_metrics}")  # Debugging log

# Background thread to update metrics every 10 seconds
def start_background_fetch():
    while True:
        fetch_metrics()
        time.sleep(10) 

# Start the background thread
threading.Thread(target=start_background_fetch, daemon=True).start()

# Route to fetch JSON metrics (for AJAX updates)
@app.route("/metrics")
def metrics():
    return jsonify(latest_metrics)

# Route to render the main dashboard
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
