# Cloud-Based Linux Server Performance Remote Dashboard Project

## Overview
This project provides a **performance monitoring solution** for a remote, cloud-based Linux infrastructure. The system consists of an **agent** running on monitored servers and a **dashboard** that visualizes key system metrics. The dashboard is designed to help track system performance in real time, detect anomalies, and provide alerts based on user-defined thresholds.

## Features
- **Cloud Deployment**: Hosted on Google Cloud Platform (GCP) using Ubuntu/Debian VMs.
- **Simulated Load Testing**: Uses `stress-ng` (optional) to simulate various system loads.
- **Systemd Service**: The monitoring agent can run as a systemd service.
- **Remote Monitoring API/Agent**: A Flask-based API collects and exposes system metrics.
- **Named Pipes**: Used for inter-process communication.
- **User & Group Management**: The API runs under a dedicated system user/group.
- **Dashboard**: A Flask-based web application using Plotly for visualizations.
- **Key Performance Metrics**: Tracks CPU, Memory, Disk, Network, and Load Average.
- **Data Visualization**: Provides real-time and historical graphs of system performance.
- **Notification System**: Alerts users when performance thresholds are exceeded.
- **Security**: Implements firewall rules to restrict API access.
- **Failure Handling**: Uses cron jobs to restart the agent upon failure.
- **Version Control**: Managed using GitHub for collaboration.

## Architecture
The system consists of two main components:
1. **Agent (`agent.py`)** - Runs on each monitored server, collecting system metrics.
2. **Dashboard (`dashboard.py`)** - A web interface to visualize real-time and historical data.

## Installation & Setup
### 1. Deploy the Server on GCP
- Create a **VPC** and an Ubuntu/Debian VM instance on Google Cloud Platform.
- Configure **firewall rules** to allow traffic on required ports (5000 for the agent, 5001 for the dashboard).

### 2. Install Dependencies
On each monitored server (agent VM):
```sh
sudo apt update && sudo apt install python3 python3-pip
pip3 install flask psutil
```
On the dashboard VM:
```sh
sudo apt update && sudo apt install python3 python3-pip
pip3 install flask requests plotly
```

### 3. Start the Monitoring Agent
On the monitored server, run:
```sh
python3 agent.py
```
The agent will start collecting metrics and expose them at:
```
http://<agent_internal_ip>:5000/metrics
```

### 4. Start the Dashboard
On the dashboard VM, run:
```sh
python3 dashboard.py
```
The dashboard will be accessible at:
```
http://<dashboard_internal_ip>:5001
```

### 5. Access the Dashboard
- Open a web browser and enter `http://<dashboard_internal_ip>:5001`.
- The dashboard will display performance graphs and allow users to adjust thresholds.

## Configuration
### 1. Modifying Monitored Servers
Edit `dashboard.py` to add new monitored servers:
```python
MONITORED_SERVERS = {
    "Server 1": "http://Your Server IP Here:5000/metrics",
    "Server 2": "http://Your 2nd Server IP Here:5000/metrics",
}
```

### 2. Setting Notification Thresholds
Thresholds can be modified in `dashboard.py`:
```python
thresholds = {
    "CPU_Usage": 80,
    "Memory_Usage": 75,
    "Disk_Usage": 80,
    "Network_Usage": 1000000000,
    "Load_Average": 5,
}
```
Or dynamically updated through the dashboard UI.

## Automating the Agent
### 1. Create a Systemd Service
To ensure the agent starts on boot, create a systemd service file:
```sh
sudo nano /etc/systemd/system/monitoring-agent.service
```
Add the following:
```ini
[Unit]
Description=Linux Server Monitoring Agent
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/agent.py
Restart=always
User=nobody
Group=nogroup

[Install]
WantedBy=multi-user.target
```
Then enable and start the service:
```sh
sudo systemctl enable monitoring-agent.service
sudo systemctl start monitoring-agent.service
```

### 2. Set Up Failure Handling
Create a cron job to check if the agent is running every 5 minutes:
```sh
crontab -e
```
Add:
```sh
*/5 * * * * pgrep -f agent.py || /usr/bin/python3 /path/to/agent.py
```

## Security
- **Firewall Rules**: Ensure only authorized IPs can access the API and dashboard.
- **User Privileges**: The agent runs as a dedicated user for security.

## Version Control
- The project is managed in a GitHub repository for collaboration and tracking changes.

## Conclusion
This project provides a complete solution for monitoring cloud-based Linux servers, offering **real-time monitoring, data visualization, notifications, and automated failure handling**. Future improvements can include database integration for long-term trend analysis and authentication mechanisms for access control.

