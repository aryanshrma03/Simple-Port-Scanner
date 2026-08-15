from dataclasses import dataclass
import socket

@dataclass(frozen=True)
class PortResult:
    port: int
    state: str
    service: str
    error: str = ""

def service_hint(port: int) -> str:
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        common = {
            21: "ftp",
            22: "ssh",
            23: "telnet",
            25: "smtp",
            53: "dns",
            80: "http",
            110: "pop3",
            143: "imap",
            443: "https",
            445: "smb",
            3306: "mysql",
            3389: "rdp",
            5432: "postgresql",
            6379: "redis",
            8080: "http-alt",
        }
        return common.get(port, "unknown")

def scan_port(target: str, port: int, timeout: float = 0.5) -> PortResult:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            code = sock.connect_ex((target, port))

        if code == 0:
            return PortResult(port, "OPEN", service_hint(port))

        return PortResult(port, "CLOSED", service_hint(port))

    except socket.timeout:
        return PortResult(port, "TIMEOUT", service_hint(port), "Connection timed out.")
    except OSError as exc:
        return PortResult(port, "ERROR", service_hint(port), str(exc))
