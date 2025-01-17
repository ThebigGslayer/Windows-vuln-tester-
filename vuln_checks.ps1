# vuln_checks.ps1 - PowerShell script to check for vulnerabilities

# Check for open ports
Write-Output "Scanning for open ports..."
Get-NetTCPConnection | Where-Object { $_.State -eq "Listen" } | Select-Object LocalPort

# Check if Windows Firewall is enabled
Write-Output "`nChecking firewall status..."
(Get-NetFirewallProfile -Profile Domain,Public,Private).Enabled

# Check for outdated Windows updates
Write-Output "`nChecking Windows Update status..."
Get-WindowsUpdateLog

# Check for user accounts without passwords
Write-Output "`nChecking for user accounts without passwords..."
Get-WmiObject -Class Win32_UserAccount | Where-Object { $_.PasswordRequired -eq $false } | Select-Object Name
