import ipaddress
import socket
import re

MAX_PORT = 65535

def validate_target(target: str) -> str:
    target = target.strip()

    if not target:
        raise ValueError("Target cannot be empty.")

    if len(target) > 253:
        raise ValueError("Target is too long.")

    # Accept IPv4/IPv6 literals and ordinary hostnames.
    try:
        ipaddress.ip_address(target)
        return target
    except ValueError:
        pass

    hostname_pattern = re.compile(
        r"^(?=.{1,253}$)([A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)*"
        r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$"
    )

    if not hostname_pattern.match(target):
        raise ValueError("Invalid hostname or IP address.")

    return target

def parse_ports(value: str) -> list[int]:
    """Parse 22,80,443,8000-8010 into sorted unique ports."""
    if not value.strip():
        raise ValueError("Port specification cannot be empty.")

    ports = set()

    for token in value.split(","):
        token = token.strip()
        if not token:
            continue

        if "-" in token:
            pieces = token.split("-")
            if len(pieces) != 2:
                raise ValueError(f"Invalid port range: {token}")

            start, end = (int(x.strip()) for x in pieces)

            if not (1 <= start <= MAX_PORT and 1 <= end <= MAX_PORT):
                raise ValueError("Ports must be between 1 and 65535.")

            if start > end:
                raise ValueError(f"Invalid range: {token}")

            if end - start > 5000:
                raise ValueError("A single range may contain at most 5001 ports.")

            ports.update(range(start, end + 1))
        else:
            port = int(token)

            if not 1 <= port <= MAX_PORT:
                raise ValueError("Ports must be between 1 and 65535.")

            ports.add(port)

    if not ports:
        raise ValueError("No valid ports supplied.")

    if len(ports) > 5001:
        raise ValueError("A scan may contain at most 5001 unique ports.")

    return sorted(ports)
