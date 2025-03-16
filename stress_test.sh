#!/bin/bash

LOG_FILE="/var/log/stress_test.log"

echo "Starting stress-ng test..." | tee -a $LOG_FILE

# CPU Stress (4 workers, 30 seconds)
stress-ng --cpu 4 --timeout 30s --metrics-brief | tee -a $LOG_FILE

# Memory Stress (Use 500MB for 30 seconds)
stress-ng --vm 1 --vm-bytes 500M --timeout 30s --metrics-brief | tee -a $LOG_FILE

# Disk Stress (Write 100MB for 30 seconds)
stress-ng --hdd 1 --hdd-bytes 100M --timeout 30s --metrics-brief | tee -a $LOG_FILE

# I/O Stress (High read/write activity for 30 seconds)
stress-ng --io 4 --timeout 30s --metrics-brief | tee -a $LOG_FILE

# Load Average Test (Simulating system load)
stress-ng --cpu 2 --io 2 --vm 1 --vm-bytes 256M --timeout 30s --metrics-brief | tee -a $LOG_FILE

echo "Stress test completed!" | tee -a $LOG_FILE
