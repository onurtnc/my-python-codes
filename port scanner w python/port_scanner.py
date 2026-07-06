#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import argparse
import ipaddress
import json
import csv
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# -----------------------------
# Data Models
# -----------------------------
@dataclass
class ScanResult:
    host: str
    ip: str
    port: int
    status: str  # "open" | "closed" | "filtered"
    service: str
    banner: str | None
    rtt_ms: float | None


# -----------------------------
# Port Scanner
# -----------------------------
class PortScanner:
    COMMON_PORTS = {
        20: "ftp-data",
        21: "ftp",
        22: "ssh",
        23: "telnet",
        25: "smtp",
        53: "dns",
        80: "http",
        110: "pop3",
        111: "rpcbind",
        135: "msrpc",
        139: "netbios-ssn",
        143: "imap",
        389: "ldap",
        443: "https",
        445: "microsoft-ds",
        465: "smtps",
        587: "smtp-submission",
        631: "ipp",
        993: "imaps",
        995: "pop3s",
        1433: "mssql",
        1521: "oracle",
        2049: "nfs",
        2375: "docker",
        3306: "mysql",
        3389: "rdp",
        5432: "postgres",
        5900: "vnc",
        6379: "redis",
        8080: "http-alt",
        8443: "https-alt",
        9200: "elasticsearch",
        27017: "mongodb",
    }

    def __init__(
        self,
        target: str,
        ports: list[int],
        timeout: float = 1.0,
        workers: int = 200,
        grab_banner: bool = False,
        rate_limit: float = 0.0,  # seconds between launches (soft)
        family: str = "auto",  # auto|ipv4|ipv6
        verbose: bool = False,
    ):
        self.target = target
        self.ports = ports
        self.timeout = timeout
        self.workers = workers
        self.grab_banner = grab_banner
        self.rate_limit = rate_limit
        self.family = family
        self.verbose = verbose

        self.ip = None
        self.results: list[ScanResult] = []

    # ---------- Helpers ----------
    def resolve(self) -> str | None:
        """Resolve domain/IP to IP address (supports IPv4/IPv6 based on family)."""
        try:
            # If user already gave an IP, accept it
            try:
                ipaddress.ip_address(self.target)
                self.ip = self.target
                return self.ip
            except ValueError:
                pass

            if self.family == "ipv4":
                info = socket.getaddrinfo(self.target, None, socket.AF_INET, socket.SOCK_STREAM)
            elif self.family == "ipv6":
                info = socket.getaddrinfo(self.target, None, socket.AF_INET6, socket.SOCK_STREAM)
            else:
                info = socket.getaddrinfo(self.target, None, 0, socket.SOCK_STREAM)

            # pick first
            self.ip = info[0][4][0]
            return self.ip
        except socket.gaierror:
            return None

    def _service_name(self, port: int) -> str:
        return self.COMMON_PORTS.get(port, "unknown")

    def _try_banner(self, sock: socket.socket, port: int) -> str | None:
        """
        Minimal banner grabbing:
        - For HTTP(S) ports, send a basic HEAD request over plain TCP (HTTPS won't respond without TLS).
        - Otherwise, try recv() after connect (some services send banner immediately: SSH, FTP).
        """
        try:
            sock.settimeout(self.timeout)

            # Try receive first (SSH/FTP often speak first)
            try:
                data = sock.recv(128)
                if data:
                    return data.decode(errors="ignore").strip()
            except Exception:
                pass

            # For HTTP-ish ports, try a simple request (plain TCP)
            if port in (80, 8080, 8000, 8443, 8888):
                req = b"HEAD / HTTP/1.0\r\nHost: localhost\r\n\r\n"
                try:
                    sock.sendall(req)
                    data = sock.recv(256)
                    if data:
                        return data.decode(errors="ignore").splitlines()[0].strip()
                except Exception:
                    return None

            return None
        except Exception:
            return None

    # ---------- Core scan ----------
    def scan_port(self, port: int) -> ScanResult:
        start = time.perf_counter()
        fam = socket.AF_INET6 if (":" in (self.ip or "") ) else socket.AF_INET

        status = "closed"
        banner = None
        rtt_ms = None

        try:
            with socket.socket(fam, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                res = sock.connect_ex((self.ip, port))
                rtt_ms = (time.perf_counter() - start) * 1000.0

                if res == 0:
                    status = "open"
                    if self.grab_banner:
                        banner = self._try_banner(sock, port)
                else:
                    # Not perfect, but commonly:
                    # - connection refused => closed
                    # - timeout / no route => filtered
                    if res in (socket.errno.ETIMEDOUT if hasattr(socket, "errno") else (),):
                        status = "filtered"
        except socket.timeout:
            status = "filtered"
            rtt_ms = (time.perf_counter() - start) * 1000.0
        except Exception:
            # Unknown errors treated as filtered-ish
            status = "filtered"
            rtt_ms = (time.perf_counter() - start) * 1000.0

        return ScanResult(
            host=self.target,
            ip=self.ip or "",
            port=port,
            status=status,
            service=self._service_name(port),
            banner=banner,
            rtt_ms=rtt_ms,
        )

    def run(self) -> list[ScanResult]:
        ip = self.resolve()
        if not ip:
            raise RuntimeError(f"Target could not be resolved: {self.target}")

        started = datetime.now()
        if self.verbose:
            print("=" * 70)
            print("PYTHON PORT SCANNER (DEFENSIVE)")
            print("=" * 70)
            print(f"Target: {self.target} ({ip})")
            print(f"Ports: {len(self.ports)} ports")
            print(f"Timeout: {self.timeout}s | Workers: {self.workers} | Banner: {self.grab_banner}")
            print(f"Started: {started.strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 70)

        results: list[ScanResult] = []
        open_count = 0

        # Soft rate limit between task submissions
        with ThreadPoolExecutor(max_workers=self.workers) as ex:
            futures = []
            for p in self.ports:
                futures.append(ex.submit(self.scan_port, p))
                if self.rate_limit > 0:
                    time.sleep(self.rate_limit)

            for fut in as_completed(futures):
                r = fut.result()
                results.append(r)
                if self.verbose and r.status == "open":
                    open_count += 1
                    b = f" | banner: {r.banner}" if r.banner else ""
                    print(f"[OPEN] {r.ip}:{r.port} ({r.service}){b}")

        # Sort by port
        results.sort(key=lambda x: x.port)
        self.results = results
        return results


# -----------------------------
# Port parsing utils
# -----------------------------
def parse_ports(port_str: str, mode: str) -> list[int]:
    """
    port_str supports:
      - "1-1024"
      - "22,80,443"
      - "22,80,443,8000-8100"
    mode:
      - "quick": ignores port_str and returns common ports
      - "top1024": 1-1024
      - "custom": parse given string
    """
    if mode == "top1024":
        return list(range(1, 1025))

    if mode == "quick":
        return sorted(PortScanner.COMMON_PORTS.keys())

    # custom
    ports: set[int] = set()
    parts = [p.strip() for p in port_str.split(",") if p.strip()]
    for part in parts:
        if "-" in part:
            a, b = part.split("-", 1)
            start, end = int(a), int(b)
            if start < 1 or end > 65535 or start > end:
                raise ValueError(f"Invalid port range: {part}")
            for x in range(start, end + 1):
                ports.add(x)
        else:
            p = int(part)
            if p < 1 or p > 65535:
                raise ValueError(f"Invalid port: {p}")
            ports.add(p)

    return sorted(ports)


# -----------------------------
# Output writers
# -----------------------------
def save_json(path: str, results: list[ScanResult]):
    with open(path, "w", encoding="utf-8") as f:
        json.dump([asdict(r) for r in results], f, ensure_ascii=False, indent=2)

def save_csv(path: str, results: list[ScanResult]):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["host", "ip", "port", "status", "service", "banner", "rtt_ms"])
        for r in results:
            w.writerow([r.host, r.ip, r.port, r.status, r.service, r.banner or "", f"{r.rtt_ms:.2f}" if r.rtt_ms else ""])


def print_summary(results: list[ScanResult]):
    open_ports = [r for r in results if r.status == "open"]
    print("\n" + "=" * 70)
    print("SCAN SUMMARY")
    print("=" * 70)
    if open_ports:
        print(f"[+] Open ports found: {len(open_ports)}\n")
        print(f"{'PORT':<8} {'SERVICE':<18} {'RTT(ms)':<10} {'BANNER'}")
        print("-" * 70)
        for r in open_ports:
            banner = (r.banner[:60] + "…") if (r.banner and len(r.banner) > 60) else (r.banner or "")
            rtt = f"{r.rtt_ms:.2f}" if r.rtt_ms else ""
            print(f"{r.port:<8} {r.service:<18} {rtt:<10} {banner}")
        print("-" * 70)
    else:
        print("[-] No open ports detected in the selected range.")
    print("=" * 70)


# -----------------------------
# Main
# -----------------------------
def main():
    ap = argparse.ArgumentParser(
        description="Defensive TCP Port Scanner (Python). Use only on authorized targets."
    )
    ap.add_argument("target", help="Target IP or domain (e.g., scanme.nmap.org)")
    ap.add_argument(
        "--mode",
        choices=["quick", "top1024", "custom"],
        default="quick",
        help="Scan mode (default: quick)",
    )
    ap.add_argument(
        "--ports",
        default="1-1024",
        help="Custom ports, e.g. '22,80,443,8000-8100' (used only with --mode custom)",
    )
    ap.add_argument("--timeout", type=float, default=1.0, help="Socket timeout in seconds")
    ap.add_argument("--workers", type=int, default=200, help="Thread count (default: 200)")
    ap.add_argument("--banner", action="store_true", help="Enable basic banner grabbing")
    ap.add_argument("--rate", type=float, default=0.0, help="Soft delay (seconds) between task submissions")
    ap.add_argument("--family", choices=["auto", "ipv4", "ipv6"], default="auto", help="IP family preference")
    ap.add_argument("--verbose", action="store_true", help="Verbose output (prints open ports live)")
    ap.add_argument("--out-json", default=None, help="Save results to JSON file path")
    ap.add_argument("--out-csv", default=None, help="Save results to CSV file path")
    args = ap.parse_args()

    ports = parse_ports(args.ports, args.mode)

    # Safety-ish guardrails (you can adjust)
    if args.mode == "custom" and len(ports) > 5000:
        raise SystemExit("Too many ports selected (>5000). Narrow the range.")

    scanner = PortScanner(
        target=args.target,
        ports=ports,
        timeout=args.timeout,
        workers=args.workers,
        grab_banner=args.banner,
        rate_limit=args.rate,
        family=args.family,
        verbose=args.verbose,
    )

    start = time.perf_counter()
    results = scanner.run()
    duration = time.perf_counter() - start

    print_summary(results)
    print(f"Duration: {duration:.2f}s | Scanned: {len(ports)} ports")

    if args.out_json:
        save_json(args.out_json, results)
        print(f"Saved JSON: {args.out_json}")

    if args.out_csv:
        save_csv(args.out_csv, results)
        print(f"Saved CSV: {args.out_csv}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
