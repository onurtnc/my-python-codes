# Python TCP Port Scanner

This project is a **defensive TCP port scanner** written in **Python**.  
It scans a target IP address or domain to identify **open TCP ports**, detect **common services**, and optionally perform **basic banner grabbing**.

⚠️ **Legal Notice:**  
This tool is intended **for educational and authorized security testing only**.  
Do NOT scan systems without explicit permission.

---

## 🚀 Features
- 🔍 TCP connect scan
- ⚡ Multi-threaded scanning (fast)
- 🎯 Multiple scan modes:
  - Quick scan (common ports)
  - Top 1024 ports
  - Custom port ranges
- 🧠 Common service detection (SSH, HTTP, MySQL, etc.)
- 🏷 Optional banner grabbing
- ⏱ Timeout & rate-limit control
- 📊 Scan progress & summary
- 💾 Export results to **JSON** or **CSV**
- 🌐 IPv4 / IPv6 support

---

## 🛠 Technologies Used
- Python 3
- `socket` (network communication)
- `threading` via `ThreadPoolExecutor`
- `argparse` (CLI interface)
- `dataclasses`
- `datetime`, `json`, `csv`

## ▶️ Run the Program
```bash
# Quick scan of common ports
python port_scanner.py scanme.nmap.org --mode quick

# Scan a custom port range with banner grabbing
python port_scanner.py 192.168.1.1 --mode custom --ports 22,80,443,8000-8100 --banner

# Export results to JSON/CSV
python port_scanner.py scanme.nmap.org --mode top1024 --out-json results.json --out-csv results.csv
```
