# Build a system-native Windows keyboard installer (build-time tool only) using Microsoft Keyboard Layout Creator 1.4.
# Run on Windows with MSKLC and its command-line kbdutool.exe installed.
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")
$tool = Get-Command kbdutool.exe -ErrorAction SilentlyContinue
if (-not $tool) {
    throw "kbdutool.exe not found. Install Microsoft Keyboard Layout Creator 1.4 and add its bin directory to PATH."
}
python -m onnoy check
New-Item -ItemType Directory -Force build/windows | Out-Null
Copy-Item dist/windows/onnoy.klc build/windows/onnoy.klc
Push-Location build/windows
try {
    & $tool.Source -u -s onnoy.klc
    if ($LASTEXITCODE -ne 0) { throw "MSKLC build failed (exit $LASTEXITCODE)." }
} finally {
    Pop-Location
}
Write-Host "Inspect build/windows for the MSKLC-generated setup files and test the layout before distributing."
