import customtkinter as ctk

def create_controls(parent, scan_command, quick_command, demo_command, stop_command):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="x", padx=30, pady=8)

    ctk.CTkButton(
        frame, text="Scan", command=scan_command,
        width=100, height=42, corner_radius=10
    ).pack(side="left")

    ctk.CTkButton(
        frame, text="Quick Common Ports", command=quick_command,
        width=165, height=42, corner_radius=10
    ).pack(side="left", padx=8)

    ctk.CTkButton(
        frame, text="Localhost Demo", command=demo_command,
        width=140, height=42, corner_radius=10
    ).pack(side="left")

    ctk.CTkButton(
        frame, text="Stop", command=stop_command,
        width=90, height=42, corner_radius=10,
        fg_color="#3b3f46", hover_color="#4b5058"
    ).pack(side="right")
