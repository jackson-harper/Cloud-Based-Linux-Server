  #!/bin/bash

# Define the log file to store test results
LOG_FILE=/var/log/stress_test.log

# Set the duration for each stress test (e.g., 20 seconds)
DURATION=20s

# Print a starting message and log it
echo "Starting stress-ng test..." | tee -a $LOG_FILE

# Loop through different types of stress tests
for TEST in "CPU Stress (4 workers)" "Memory Stress (Use 500MB)" "Disk Stress (Write 100MB)" "Network Stress (2 sockets)" "Load Average Test (Simulating system load)"; do
    # Log which test is being executed
    echo "Running $TEST for $DURATION..." | tee -a $LOG_FILE

    # Execute different stress tests based on the current test name
    case "$TEST" in
        "CPU Stress (4 workers)")
            # Simulates CPU stress by spawning 4 workers
            stress-ng --cpu 4 --timeout $DURATION --metrics-brief | tee -a $LOG_FILE
            ;;
        "Memory Stress (Use 500MB)")
            # Allocates and uses 500MB of memory for the duration
            stress-ng --vm 1 --vm-bytes 500M --timeout $DURATION --metrics-brief | tee -a $LOG_FILE
            ;;
        "Disk Stress (Write 100MB)")
            # Simulates heavy disk write operations (4 processes, writing 1GB total)
            stress-ng --hdd 4 --hdd-bytes 1G --timeout $DURATION --metrics-brief | tee -a $LOG_FILE
            ;;
        "Network Stress (2 sockets)")
            # Simulates network socket stress using 2 sockets
            stress-ng --sock 2 --timeout $DURATION --metrics-brief | tee -a $LOG_FILE
            ;;
        "Load Average Test (Simulating system load)")
            # Generates mixed CPU, IO, and memory load to simulate high system usage
            stress-ng --cpu 8 --io 4 --vm 2 --vm-bytes 1G --timeout $DURATION --metrics-brief | tee -a $LOG_FILE
            ;;
    esac
done

# Print and log a completion message
echo "Stress test completed!" | tee -a $LOG_FILE
