# ============================================================
# Minimal universal cleanup script (English only)
# - Forsite uninstaller (exe) + folder removal
# - Uninstall by registry UninstallString (primary)
# - Winget fallback (secondary)
# - Remove leftover folders (dotnet shared, TightVNC, mwcc, etc.)
# - No Get-WmiObject, no duplicate attempts
# ============================================================

# --- Admin check ---
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltinRole] "Administrator")) {
    Write-Host "Please run PowerShell as Administrator!" -ForegroundColor Red
    exit 1
}

Write-Host "`n=== CLEANUP START ===`n" -ForegroundColor Cyan

$removedItems = New-Object System.Collections.ArrayList

function Log-Item($text) {
    $null = $removedItems.Add($text)
}

function Show-Status($msg, $level="INFO") {
    switch ($level) {
        "OK"    { Write-Host "OK:    $msg" -ForegroundColor Green }
        "WARN"  { Write-Host "WARN:  $msg" -ForegroundColor Yellow }
        "ERROR" { Write-Host "ERROR: $msg" -ForegroundColor Red }
        default { Write-Host "INFO:  $msg" -ForegroundColor White }
    }
}

# --- Run Forsite uninstaller exe if present, then remove folder ---
function Remove-Forsite() {
    $forsiteExe = "C:\Program Files\Forsite M-Wall Control Center\unins000.exe"
    $forsiteFolder = "C:\Program Files\Forsite M-Wall Control Center"

    if (Test-Path $forsiteExe) {
        Show-Status "Found Forsite uninstaller: $forsiteExe" "INFO"
        try {
            # common silent flags; if not supported it will run non-interactively
            Start-Process -FilePath $forsiteExe -ArgumentList "/VERYSILENT","/NORESTART" -Wait -NoNewWindow -ErrorAction Stop
            Show-Status "Forsite uninstaller executed." "OK"
            Log-Item("Forsite uninstalled (unins000.exe)")
        } catch {
            Show-Status "Forsite uninstaller execution failed: $_. Exception" "WARN"
            # try running without args as fallback
            try {
                Start-Process -FilePath $forsiteExe -Wait -NoNewWindow -ErrorAction Stop
                Show-Status "Forsite uninstaller executed (fallback)." "OK"
                Log-Item("Forsite uninstalled (unins000.exe, fallback)")
            } catch {
                Show-Status "Forsite uninstaller fallback failed." "ERROR"
            }
        }
    } else {
        Show-Status "Forsite uninstaller not found." "WARN"
    }

    # Remove folder if exists
    if (Test-Path $forsiteFolder) {
        try {
            takeown /f "$forsiteFolder" /r /d y | Out-Null
            icacls "$forsiteFolder" /grant Administrators:F /t | Out-Null
            Remove-Item -LiteralPath "$forsiteFolder" -Recurse -Force -ErrorAction Stop
            Show-Status "Forsite folder removed: $forsiteFolder" "OK"
            Log-Item($forsiteFolder)
        } catch {
            Show-Status "Failed to remove Forsite folder: $_" "ERROR"
        }
    } else {
        Show-Status "Forsite folder not present." "INFO"
    }
}

# --- Uninstall helper: try registry UninstallString, then winget fallback ---
function Uninstall-PackageByName($displayNamePattern) {
    $foundAndUninstalled = $false

    $regRoots = @(
        "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
        "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
    )

    foreach ($root in $regRoots) {
        Get-ChildItem -Path $root -ErrorAction SilentlyContinue | ForEach-Object {
            $props = Get-ItemProperty -Path $_.PSPath -ErrorAction SilentlyContinue
            if ($props -and $props.DisplayName -and ($props.DisplayName -like "*$displayNamePattern*")) {
                $disp = $props.DisplayName
                $uninst = $props.UninstallString
                if ($uninst) {
                    Show-Status "Registry entry found for '$disp' in $root" "INFO"
                    try {
                        if ($uninst -match "msiexec" -or $uninst -match "MsiExec") {
                            # ensure /X and silent flags
                            if ($uninst -match "/I") { $uninst = $uninst -replace "/I","/X" }
                            # Extract GUID if only GUID present or keep full string if present
                            # Add silent flags if not present
                            if ($uninst -notmatch "/qn" -and $uninst -notmatch "/quiet") {
                                $uninst = "$uninst /qn /norestart"
                            }
                            Start-Process -FilePath "cmd.exe" -ArgumentList "/c $uninst" -Wait -NoNewWindow -ErrorAction Stop
                        } else {
                            # likely an exe uninstall string; run it directly
                            # If uninstall string contains parameters, keep them; else try with /S /VERYSILENT
                            $exe, $args = $null, $null
                            if ($uninst -match '\"(.+?)\"(.*)') {
                                $exe = $matches[1]
                                $args = $matches[2].Trim()
                            } else {
                                $parts = $uninst -split ' '
                                $exe = $parts[0]
                                $args = ($parts[1..($parts.Length - 1)] -join ' ')
                            }
                            if (-not (Test-Path $exe)) {
                                # try as-is
                                Start-Process -FilePath "cmd.exe" -ArgumentList "/c $uninst" -Wait -NoNewWindow -ErrorAction Stop
                            } else {
                                # run exe with common silent flags if none provided
                                if ([string]::IsNullOrWhiteSpace($args)) {
                                    Start-Process -FilePath $exe -ArgumentList "/VERYSILENT","/NORESTART" -Wait -NoNewWindow -ErrorAction Stop
                                } else {
                                    Start-Process -FilePath $exe -ArgumentList $args -Wait -NoNewWindow -ErrorAction Stop
                                }
                            }
                        }
                        Show-Status "Uninstalled (registry) : $disp" "OK"
                        Log-Item($disp)
                        $foundAndUninstalled = $true
                    } catch {
                        Show-Status ("Failed uninstall (registry) for {0}: {1}" -f $disp, $_) "ERROR"

                    }
                } else {
                    # Found a registry key but no UninstallString: remove key (optional)
                    Show-Status "Registry entry for $disp has no UninstallString; skipping execution." "WARN"
                }
            }
        }
    }

    if (-not $foundAndUninstalled) {
        # Winget fallback: try exact first, then fallback without exact
        Show-Status "Attempting winget uninstall for pattern: '$displayNamePattern'" "INFO"
        try {
            # try exact match on name (works when exact name matches)
            winget uninstall --name "$displayNamePattern" --exact --scope machine -h
            Show-Status "Uninstalled via winget (exact): $displayNamePattern" "OK"
            Log-Item("winget: $displayNamePattern (exact)")
            $foundAndUninstalled = $true
        } catch {
            # try without exact (partial)
            try {
                winget uninstall --name "$displayNamePattern" --scope machine -h
                Show-Status "Uninstalled via winget (partial): $displayNamePattern" "OK"
                Log-Item("winget: $displayNamePattern (partial)")
                $foundAndUninstalled = $true
            } catch {
                Show-Status "winget uninstall not found for: $displayNamePattern" "WARN"
            }
        }
    }

    return $foundAndUninstalled
}

# --- Compose one unified package list (patterns) ---
$packagePatterns = @(
    "Microsoft ASP.NET Core 6.0.20",
    "Microsoft ASP.NET Core 8.0.16",
    "Microsoft .NET Runtime 6.0.20",
    "Microsoft .NET Runtime 8.0.16",
    "Microsoft Windows Desktop Runtime 6.0.20",
    "Microsoft Windows Desktop Runtime 8.0.16",
    "Microsoft Windows Desktop Runtime 8.0.21",
    "Microsoft Visual C++ 2010",
    "Microsoft Visual C++ 2013",
    "Microsoft Visual C++ 2015-2022",
    "TightVNC",
    "Forsite M-Wall Control Center",
    "Microsoft Visual C++ 2008"  # optional, older family
)

# --- Remove Forsite at the start (exe + folder) ---
Remove-Forsite

# --- Iterate uninstall list (registry primary, winget fallback) ---
foreach ($pattern in $packagePatterns) {
    Show-Status "Processing pattern: $pattern" "INFO"
    Uninstall-PackageByName $pattern | Out-Null
}

# --- Remove leftover known folders (single pass) ---
$foldersToRemove = @(
    "C:\Program Files\TightVNC",
    "$env:LOCALAPPDATA\mwcc",
    "$env:LOCALAPPDATA\mwcc_backup",
    "C:\Program Files\dotnet\shared\Microsoft.AspNetCore.App\6.0.20",
    "C:\Program Files\dotnet\shared\Microsoft.AspNetCore.App\8.0.16",
    "C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App\6.0.20",
    "C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App\8.0.16",
    "C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App\8.0.21",
    "C:\Program Files\Forsite M-Wall Control Center"
)

foreach ($p in $foldersToRemove) {
    if (Test-Path $p) {
        try {
            takeown /f "$p" /r /d y | Out-Null
            icacls "$p" /grant Administrators:F /t | Out-Null
            Remove-Item -LiteralPath "$p" -Recurse -Force -ErrorAction Stop
            Show-Status "Removed folder: $p" "OK"
            Log-Item($p)
        } catch {
            Show-Status "Failed to remove folder: $p - $_" "ERROR"
        }
    }
}

# --- Optional: clean registry keys that are orphaned and match keywords (non-destructive attempt) ---
$keywords = @("Visual C\+\+","ASP.NET","\.NET Runtime","Windows Desktop Runtime","Forsite","M-Wall","TightVNC")
$regRoots = @("HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall","HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall")
foreach ($root in $regRoots) {
    Get-ChildItem -Path $root -ErrorAction SilentlyContinue | ForEach-Object {
        $props = Get-ItemProperty -Path $_.PSPath -ErrorAction SilentlyContinue
        if ($props.DisplayName) {
            foreach ($kw in $keywords) {
                if ($props.DisplayName -match $kw) {
                    # If an UninstallString is present, we already handled it; if not, safe to remove orphan key
                    if (-not $props.UninstallString) {
                        try {
                            Remove-Item -LiteralPath $_.PSPath -Recurse -Force -ErrorAction Stop
                            Show-Status "Removed orphan registry key for: $($props.DisplayName)" "OK"
                            Log-Item("RegKey: $($props.DisplayName)")
                        } catch {
                            # ignore failures
                        }
                    }
                    break
                }
            }
        }
    }
}

# --- Final summary ---
Write-Host "`n=== SUMMARY ===`n" -ForegroundColor Cyan
if ($removedItems.Count -gt 0) {
    $removedItems | Sort-Object | Get-Unique | ForEach-Object { Write-Host " - $_" -ForegroundColor Green }
} else {
    Write-Host "No items were removed." -ForegroundColor Yellow
}

Write-Host "`n=== CLEANUP FINISHED ===`n" -ForegroundColor Cyan
