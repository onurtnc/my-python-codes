## Python Security & Automation Scripts

This repository includes Python scripts developed to support
security analysis, detection engineering, and SOC-style automation tasks.

### Included Scripts
- **DNS Beaconing Detector**
  - Parses DNS logs to identify repetitive query patterns
  - Helps detect potential command-and-control (C2) beaconing behavior
  - Demonstrates log analysis and threshold-based detection logic

- **EDR-Style Process Detection**
  - Analyzes endpoint process telemetry (Sysmon-like events)
  - Detects suspicious parent-child process chains
    (e.g., Office applications spawning PowerShell)
  - Identifies encoded PowerShell command execution
  - Simulates real-world EDR detection logic

### Skills Demonstrated
- Log parsing and data extraction
- Security-focused automation using Python
- Detection logic design and implementation
- MITRE ATT&CK-aligned behavioral analysis
- SOC mindset: detection → investigation → response

### Purpose
These scripts were created to demonstrate how Python can be used
to automate repetitive security tasks, support incident detection,
and provide actionable insights for SOC analysts.

> Note: The focus of these scripts is defensive security and detection engineering,
not offensive exploitation.
