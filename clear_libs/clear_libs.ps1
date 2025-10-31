# === Force cleanup of problematic .NET and VC++ runtimes ===
Write-Host "=== Starting hard cleanup of .NET & Visual C++ 2010 runtimes ===" -ForegroundColor Cyan

$targets = @(
    "Microsoft ASP.NET Core 8.0.16 Shared Framework (x64)",
    "Microsoft Windows Desktop Runtime - 8.0.16 (x64)",
    "Microsoft Visual C++ 2010  x64 Redistributable - 10.0.40219",
    "Microsoft Visual C++ 2010  x86 Redistributable - 10.0.40219"
)

foreach ($pkg in $targets) {
    Write-Host "`n--- Checking $pkg ---" -ForegroundColor Yellow
    $product = Get-WmiObject -Class Win32_Product | Where-Object { $_.Name -eq $pkg }

    if ($product) {
        $guid = $product.IdentifyingNumber
        Write-Host "Found $pkg (GUID: $guid). Trying to uninstall..."
        try {
            Start-Process "msiexec.exe" -ArgumentList "/x $guid /qn /norestart" -Wait -ErrorAction Stop
            Write-Host "✔ Uninstalled via msiexec"
        } catch {
            Write-Host "⚠ msiexec failed, cleaning registry manually"
        }

        # Удаляем записи из реестра
        $regPaths = @(
            "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        )
        foreach ($path in $regPaths) {
            Get-ChildItem $path | ForEach-Object {
                $displayName = (Get-ItemProperty $_.PSPath -ErrorAction SilentlyContinue).DisplayName
                if ($displayName -and $displayName -eq $pkg) {
                    Remove-Item $_.PSPath -Recurse -Force -ErrorAction SilentlyContinue
                    Write-Host "🧹 Removed registry entry under $path"
                }
            }
        }
    } else {
        Write-Host "❌ Package not found via WMI"
    }
}

# Чистим остатки файлов
$folders = @(
    "C:\Program Files\dotnet\shared\Microsoft.AspNetCore.App\8.0.16",
    "C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App\8.0.16"
)
foreach ($f in $folders) {
    if (Test-Path $f) {
        takeown /f $f /r /d y | Out-Null
        icacls $f /grant Administrators:F /t | Out-Null
        Remove-Item $f -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "🗑 Deleted $f"
    }
}

Write-Host "`n=== Cleanup complete. Please restart your computer. ===" -ForegroundColor Green
