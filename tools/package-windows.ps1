# Compile native Windows keyboard DLLs and assemble a standalone installation ZIP.
# MSKLC (kbdutool.exe) is a build dependency only, never included in the ZIP.
param(
    [string]$CompilerPath
)
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $root

python -m onnoy check
if ($LASTEXITCODE -ne 0) { throw "Onnoy generated source verification failed." }

$possible = @()
if ($CompilerPath) { $possible += $CompilerPath }
$command = Get-Command "kbdutool.exe" -ErrorAction SilentlyContinue
if ($command) { $possible += $command.Source }
$possible += @(
    "C:\MSKLC\bin\i386\kbdutool.exe",
    "${env:ProgramFiles(x86)}\Microsoft Keyboard Layout Creator 1.4\bin\i386\kbdutool.exe",
    "${env:ProgramFiles}\Microsoft Keyboard Layout Creator 1.4\bin\i386\kbdutool.exe"
)
$compiler = $possible | Where-Object { $_ -and (Test-Path $_ -PathType Leaf) } | Select-Object -First 1
if (-not $compiler) {
    throw "kbdutool.exe not found. Install Microsoft Keyboard Layout Creator 1.4, or pass -CompilerPath."
}
$compiler = (Resolve-Path $compiler).Path

$output = Join-Path $root "build/windows"
$staging = Join-Path $output "onnoy-windows-native"
$null = New-Item -ItemType Directory -Force (Join-Path $staging "x64")
$null = New-Item -ItemType Directory -Force (Join-Path $staging "x86")

foreach ($architecture in @(
    @{ Label = "x64"; Flag = "-m" },
    @{ Label = "x86"; Flag = "-x" }
)) {
    $work = Join-Path $output $architecture.Label
    $null = New-Item -ItemType Directory -Force $work
    Copy-Item (Join-Path $root "dist/windows/onnoy.klc") (Join-Path $work "onnoy.klc") -Force
    Push-Location $work
    try {
        & $compiler -u -w $architecture.Flag "onnoy.klc"
        if ($LASTEXITCODE -ne 0) {
            throw "MSKLC compilation for $($architecture.Label) failed (exit $LASTEXITCODE)."
        }
        $dll = Join-Path $work "onnoy.dll"
        if (-not (Test-Path $dll -PathType Leaf)) {
            throw "MSKLC produced no $($architecture.Label) DLL; source files alone are not an installer."
        }
        if ((Get-Item $dll).Length -lt 2048) { throw "Generated DLL is suspiciously small: $dll" }
        Copy-Item $dll (Join-Path $staging "$($architecture.Label)/onnoy.dll") -Force
    }
    finally {
        Pop-Location
    }
}

Copy-Item (Join-Path $PSScriptRoot "windows-setup.ps1") (Join-Path $staging "setup.ps1") -Force
Copy-Item (Join-Path $root "dist/windows/onnoy.klc") (Join-Path $staging "onnoy.klc") -Force
$archive = Join-Path $output "onnoy-windows-native.zip"
if (Test-Path $archive) { Remove-Item $archive -Force }
Compress-Archive -Path "$staging\*" -DestinationPath $archive
if (-not (Test-Path $archive) -or (Get-Item $archive).Length -lt 4096) {
    throw "Native Windows installer archive was not created."
}
Write-Host "Built $archive with x64/x86 native DLLs and setup.ps1 (no Keyman runtime)."
