from flask import Flask, render_template, jsonify
import requests
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

# Monitored servers (replace with actual server IPs)
MONITORED_SERVERS = {
    "Monitored Server (Agent)": "10.10.1.2",  # Internal IP for GCP communication
    "Server Two": "35.211.165.75",
}

# Function to fetch metrics from monitored servers
def fetch_metrics():
    data = {}
    for server_name, ip in MONITORED_SERVERS.items():
        try:
            response = requests.get(f"http://{ip}:5000/metrics", timeout=3)
            if response.status_code == 200:
                data[server_name] = response.json()
            else:
                data[server_name] = {"error": "No response from server"}
        except requests.exceptions.RequestException:
            data[server_name] = {"error": "Connection failed"}
    return data

# Route to fetch JSON metrics
@app.route("/metrics")
def metrics():
    data = fetch_metrics()
    return jsonify(data)

# Route to render the main dashboard
@app.route("/dashboard")
def dashboard():
    data = fetch_metrics()
    traces = []

    for server_name, metrics in data.items():
        if "error" not in metrics:
            traces.append(go.Bar(
                name=server_name,
                x=["CPU", "Memory", "Disk", "Network", "Load Avg"],
                y=[
                    metrics.get("CPU_Usage", 0),
                    metrics.get("Memory_Usage", 0),
                    metrics.get("Disk_Usage", 0),
                    metrics.get("Network_Usage", 0) / 1e6,  # Convert bytes to MB
                    metrics.get("Load_Average", 0)
                ]
            ))

    fig = go.Figure(data=traces)
    fig.update_layout(
        title="Server Performance Metrics",
        xaxis_title="Metric",
        yaxis_title="Usage (%)",
        barmode="group"
    )

    graph_html = pio.to_html(fig, full_html=False)
    return render_template("dashboard.html", graph_html=graph_html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
