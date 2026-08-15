# 🌐 Simple Port Scanner

A lightweight, defensive Python TCP port scanner for authorized hosts and lab environments.

> **Safety:** Use only against systems you own or have explicit permission to test. The tool performs TCP connection checks and does not exploit services, bypass authentication, or attempt credential attacks.

## 🎯 Features

- TCP connect scanning
- Single port scanning
- Port-range scanning
- Common-port quick scan
- Configurable timeout
- Optional concurrency
- Service-name hints from the local service database
- Open / closed / error classification
- Risk scoring based on exposed ports
- CustomTkinter GUI
- Safe localhost demo
- Unit tests
- Modular GitHub-ready structure

## 🧠 Architecture

```text
Target + Port Configuration
          ↓
     Input Validation
          ↓
     TCP Connect Probe
          ↓
 ┌──────────────────────┐
 │ OPEN                 │
 │ CLOSED               │
 │ ERROR / TIMEOUT      │
 └──────────────────────┘
          ↓
   Service Hint Lookup
          ↓
    Exposure Risk Score
          ↓
      GUI Report
```

## ⚠️ Authorized Use

Only scan:

- Your own computer
- Your own servers
- CTF/lab environments
- Systems where you have explicit authorization

Avoid aggressive scanning of public IP ranges or third-party systems.

## 🚀 Installation

```bash
git clone https://github.com/aryanshrma03/Simple-Port-Scanner.git
cd Simple-Port-Scanner

python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

No external scanning library is required.

## ▶️ Run

```bash
python src/main.py
```

Example:

```text
Target: 127.0.0.1
Ports: 1-1024
Timeout: 0.5
```

The scanner uses standard TCP connect behavior.

## 🖥️ GUI

The application includes:

- Target input
- Port input
- Timeout input
- Quick common-port scan
- Scan button
- Stop button
- Results table
- Open-port count
- Risk score
- Event log

### Port input formats

Single port:

```text
443
```

Range:

```text
1-1024
```

Comma-separated:

```text
22,80,443,3389
```

Mixed:

```text
22,80,443,8000-8010
```

## 📊 Risk Model

The risk score is **not a vulnerability scanner**. It is only an exposure indicator.

Example weights:

| Port | Typical Service | Weight |
|---:|---|---:|
| 21 | FTP | 20 |
| 23 | Telnet | 30 |
| 22 | SSH | 10 |
| 25 | SMTP | 10 |
| 80 | HTTP | 5 |
| 443 | HTTPS | 2 |
| 445 | SMB | 25 |
| 3389 | RDP | 25 |

The score is capped at 100.

```text
0–19     NORMAL
20–39    LOW
40–59    MEDIUM
60–79    HIGH
80–100   CRITICAL
```

An open port is not inherently vulnerable. Security depends on service configuration, authentication, patching, network exposure, and access controls.

## 🧪 Safe Demo

The **Localhost Demo** scans:

```text
127.0.0.1
```

and a small predefined set of common ports.

It is intended for demonstrating the application without scanning a third-party system.

## 📂 Project Structure

```text
Simple-Port-Scanner/
│
├── src/
│   ├── main.py
│   ├── app/
│   │   ├── __init__.py
│   │   └── gui.py
│   ├── scanner/
│   │   ├── __init__.py
│   │   ├── validator.py
│   │   ├── tcp.py
│   │   └── scoring.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── header.py
│   │   ├── controls.py
│   │   ├── results.py
│   │   └── risk_meter.py
│   └── config/
│       ├── __init__.py
│       └── theme.py
│
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

## 🔮 Future Improvements

- [ ] UDP checks with explicit opt-in
- [ ] CSV/JSON report export
- [ ] Service-version identification
- [ ] Banner analysis with safe protocol handshakes
- [ ] CIDR input with strict authorization warning
- [ ] Local firewall integration
- [ ] Historical scan comparison
- [ ] CVE enrichment from trusted vulnerability databases
- [ ] Nmap-compatible report import
- [ ] SIEM integration

## 👨‍💻 Author

**Aryan Sharma**

Cybersecurity-focused Python project demonstrating basic network reconnaissance concepts in a controlled and authorized environment.
