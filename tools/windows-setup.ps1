# Onnoy native Windows keyboard installer and uninstaller.
# Run from the extracted release directory in 64-bit elevated PowerShell:
#   powershell -ExecutionPolicy Bypass -File .\setup.ps1
#   powershell -ExecutionPolicy Bypass -File .\setup.ps1 -Uninstall
param([switch]$Uninstall)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

if (-not [Environment]::Is64BitOperatingSystem -or -not [Environment]::Is64BitProcess) {
    throw "This package requires 64-bit Windows PowerShell on x64 Windows."
}
$identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = [Security.Principal.WindowsPrincipal]::new($identity)
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    throw "Run PowerShell as Administrator to install or uninstall a system keyboard layout."
}

$reg = "HKLM:\SYSTEM\CurrentControlSet\Control\Keyboard Layouts\A0010845"
$mainDll = Join-Path $env:WINDIR "System32\onnoy.dll"
$wowDll = Join-Path $env:WINDIR "SysWOW64\onnoy.dll"
if (Test-Path $reg) {
    $existing = Get-ItemProperty $reg
    if ($existing.'Layout Text' -ne 'Onnoy') {
        throw "Keyboard layout A0010845 belongs to another keyboard; refusing to overwrite it."
    }
}

if ($Uninstall) {
    if (Test-Path $reg) {
        Remove-Item $reg -Force
    }
    foreach ($dll in @($mainDll, $wowDll)) {
        if (Test-Path $dll) {
            Remove-Item $dll -Force
        }
    }
    Write-Host "Onnoy removed. Sign out and in to refresh Windows keyboard layouts."
    exit 0
}

$amd64 = Join-Path $PSScriptRoot "x64\onnoy.dll"
$x86 = Join-Path $PSScriptRoot "x86\onnoy.dll"
foreach ($dll in @($amd64, $x86)) {
    if (-not (Test-Path $dll -PathType Leaf)) {
        throw "Native Onnoy DLL missing from extracted package: $dll"
    }
}

# Copy both architecture-specific binaries; Windows loads these as system DLLs.
Copy-Item $amd64 $mainDll -Force
Copy-Item $x86 $wowDll -Force
$null = New-Item -Path $reg -Force
New-ItemProperty -Path $reg -Name "Layout File" -Value "onnoy.dll" -PropertyType String -Force | Out-Null
New-ItemProperty -Path $reg -Name "Layout Text" -Value "Onnoy" -PropertyType String -Force | Out-Null
New-ItemProperty -Path $reg -Name "Layout Id" -Value "00D8" -PropertyType String -Force | Out-Null
Write-Host "Onnoy installed. Add it in Windows Language & region keyboard settings; sign out/in if necessary."
