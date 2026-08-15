RISK_WEIGHTS = {
    21: 20,    # FTP
    22: 10,    # SSH
    23: 30,    # Telnet
    25: 10,    # SMTP
    53: 5,     # DNS
    80: 5,     # HTTP
    110: 10,   # POP3
    143: 10,   # IMAP
    443: 2,    # HTTPS
    445: 25,   # SMB
    3306: 20,  # MySQL
    3389: 25,  # RDP
    5432: 20,  # PostgreSQL
    6379: 20,  # Redis
    8080: 5,   # HTTP alternate
}

def score_open_ports(ports: list[int]) -> tuple[int, str]:
    score = sum(RISK_WEIGHTS.get(port, 3) for port in ports)
    score = min(100, score)

    if score >= 80:
        severity = "CRITICAL"
    elif score >= 60:
        severity = "HIGH"
    elif score >= 40:
        severity = "MEDIUM"
    elif score >= 20:
        severity = "LOW"
    else:
        severity = "NORMAL"

    return score, severity
