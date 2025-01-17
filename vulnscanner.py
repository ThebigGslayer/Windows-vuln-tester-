import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import scrolledtext
import subprocess

# Function to run PowerShell commands and display output in the app
def run_scan():
    output_text.delete('1.0', ttk.END)  # Clear previous output
    
    # PowerShell commands for security checks
    commands = [
        "Write-Output 'Scanning for Open Ports...'; Get-NetTCPConnection | Where-Object { $_.State -eq 'Listen' } | Select-Object LocalPort",
        "Write-Output '\nChecking Firewall Status...'; (Get-NetFirewallProfile -Profile Domain,Public,Private).Enabled",
        "Write-Output '\nChecking Windows Update Status...'; Get-WindowsUpdateLog",
        "Write-Output '\nChecking for User Accounts Without Passwords...'; Get-WmiObject -Class Win32_UserAccount | Where-Object { $_.PasswordRequired -eq $false } | Select-Object Name"
    ]
    
    # Run each command and collect the output
    for command in commands:
        process = subprocess.Popen(
            ["powershell.exe", "-Command", command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        
        # Display output in the UI
        if stdout:
            output_text.insert(ttk.END, stdout + "\n")
        if stderr:
            output_text.insert(ttk.END, f"Error: {stderr}\n")
    
    # Scroll to the bottom of the output
    output_text.see(ttk.END)

# Create the main UI window with a ttkbootstrap theme
app = ttk.Window(themename="darkly")  # Try 'darkly', 'solar', 'journal', etc.
app.title("Windows Vulnerability Tester")
app.geometry("700x700")

# Add a title label
title_label = ttk.Label(app, text="Windows Vulnerability Tester", font=("Arial", 16, "bold"))
title_label.pack(pady=10)
# Add a button to trigger the scan
scan_button = ttk.Button(app, text="Start Scan", command=run_scan, bootstyle=SUCCESS)
scan_button.pack(pady=10)

# Add a scrolled text widget to display the output
output_text = scrolledtext.ScrolledText(app, wrap=ttk.WORD, width=80, height=20, font=("Courier", 10))
output_text.pack(pady=10, padx=10)

# Run the Tkinter event loop
app.mainloop()
