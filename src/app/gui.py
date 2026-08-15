import threading
import customtkinter as ctk
from tkinter import messagebox

from components.controls import create_controls
from components.header import create_header
from components.results import ResultsTable
from components.risk_meter import RiskMeter
from config.theme import load_theme
from scanner.scoring import score_open_ports
from scanner.tcp import scan_port
from scanner.validator import parse_ports, validate_target

load_theme()

COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 135, 139,
    143, 443, 445, 993, 995, 1433, 3306,
    3389, 5432, 5900, 6379, 8080,
]

class PortScannerApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Simple Port Scanner")
        self.root.geometry("1050x800")
        self.root.minsize(900, 700)

        self.stop_event = threading.Event()
        self.scan_thread = None

        create_header(self.root)

        form = ctk.CTkFrame(self.root, fg_color="transparent")
        form.pack(fill="x", padx=30, pady=5)

        ctk.CTkLabel(form, text="Target").grid(row=0, column=0, sticky="w")
        self.target_entry = ctk.CTkEntry(
            form, placeholder_text="127.0.0.1 or hostname", width=260
        )
        self.target_entry.grid(row=1, column=0, padx=(0, 10), pady=5)

        ctk.CTkLabel(form, text="Ports").grid(row=0, column=1, sticky="w")
        self.ports_entry = ctk.CTkEntry(
            form, placeholder_text="22,80,443 or 1-1024", width=260
        )
        self.ports_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(form, text="Timeout (seconds)").grid(row=0, column=2, sticky="w")
        self.timeout_entry = ctk.CTkEntry(
            form, placeholder_text="0.5", width=130
        )
        self.timeout_entry.insert(0, "0.5")
        self.timeout_entry.grid(row=1, column=2, padx=10, pady=5)

        create_controls(
            self.root,
            self.start_scan,
            self.quick_scan,
            self.localhost_demo,
            self.stop_scan,
        )

        self.risk = RiskMeter(self.root)
        self.results = ResultsTable(self.root)

        self.stats = ctk.CTkLabel(
            self.root,
            text="Scanned: 0 | Open: 0 | Closed: 0 | Errors: 0",
            text_color="#9aa4b2",
            font=("Segoe UI", 11),
        )
        self.stats.pack(anchor="w", padx=30, pady=(2, 5))

        ctk.CTkLabel(
            self.root,
            text="⚠ Authorized use only. This tool performs TCP connect checks and does not exploit services.",
            text_color="#9aa4b2",
            font=("Segoe UI", 11),
        ).pack(anchor="w", padx=30, pady=(0, 18))

    def _prepare_scan(self, target_text, ports_text):
        target = validate_target(target_text)
        ports = parse_ports(ports_text)

        try:
            timeout = float(self.timeout_entry.get().strip())
        except ValueError:
            raise ValueError("Timeout must be a number.")

        if not 0.1 <= timeout <= 5:
            raise ValueError("Timeout must be between 0.1 and 5 seconds.")

        return target, ports, timeout

    def start_scan(self):
        if self.scan_thread and self.scan_thread.is_alive():
            messagebox.showinfo("Scan Running", "A scan is already running.")
            return

        try:
            target, ports, timeout = self._prepare_scan(
                self.target_entry.get(),
                self.ports_entry.get(),
            )
        except ValueError as exc:
            messagebox.showerror("Input Error", str(exc))
            return

        self._run_scan(target, ports, timeout)

    def quick_scan(self):
        try:
            target = validate_target(self.target_entry.get())
            timeout = float(self.timeout_entry.get().strip())
        except ValueError as exc:
            messagebox.showerror("Input Error", str(exc))
            return

        if not 0.1 <= timeout <= 5:
            messagebox.showerror("Input Error", "Timeout must be between 0.1 and 5 seconds.")
            return

        self.ports_entry.delete(0, "end")
        self.ports_entry.insert(0, ",".join(map(str, COMMON_PORTS)))
        self._run_scan(target, COMMON_PORTS, timeout)

    def localhost_demo(self):
        self.target_entry.delete(0, "end")
        self.target_entry.insert(0, "127.0.0.1")

        demo_ports = [22, 80, 443, 5000, 8000, 8080]
        self.ports_entry.delete(0, "end")
        self.ports_entry.insert(0, ",".join(map(str, demo_ports)))

        self._run_scan("127.0.0.1", demo_ports, 0.3)

    def _run_scan(self, target, ports, timeout):
        self.stop_event.clear()
        self.results.clear()
        self.stats.configure(text=f"Scanning {target} | Ports: {len(ports)}")
        self.results.add(f"[INFO] Target: {target}")
        self.results.add(f"[INFO] TCP ports: {len(ports)}")
        self.results.add("")

        self.scan_thread = threading.Thread(
            target=self._worker,
            args=(target, ports, timeout),
            daemon=True,
        )
        self.scan_thread.start()

    def _worker(self, target, ports, timeout):
        results = []

        for port in ports:
            if self.stop_event.is_set():
                break

            result = scan_port(target, port, timeout)
            results.append(result)

            if result.state == "OPEN":
                line = f"[OPEN] {result.port:5}  {result.service}"
            else:
                line = f"[{result.state}] {result.port:5}  {result.service}"

            self.root.after(0, lambda text=line: self.results.add(text))

        self.root.after(0, lambda: self._finish(results, target))

    def _finish(self, results, target):
        open_ports = [item.port for item in results if item.state == "OPEN"]
        closed = sum(item.state == "CLOSED" for item in results)
        errors = len(results) - len(open_ports) - closed

        score, severity = score_open_ports(open_ports)
        self.risk.update(score, severity)

        self.stats.configure(
            text=(
                f"Target: {target} | Scanned: {len(results)} | "
                f"Open: {len(open_ports)} | Closed: {closed} | Errors: {errors}"
            )
        )

        self.results.add("")
        self.results.add(f"[SUMMARY] Open ports: {len(open_ports)}")
        self.results.add(f"[SUMMARY] Exposure score: {score}/100 ({severity})")

        if self.stop_event.is_set():
            self.results.add("[INFO] Scan stopped by user.")

    def stop_scan(self):
        self.stop_event.set()
        self.results.add("[INFO] Stop requested...")

    def run(self):
        self.root.mainloop()
