[CmdletBinding()]
param(
    [switch]$CollectOnly
)

$ErrorActionPreference = 'Stop'

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptRoot

Push-Location $repoRoot
try {
    $pythonExe = Join-Path $repoRoot '.venv\Scripts\python.exe'

    if (-not (Test-Path $pythonExe)) {
        throw 'Virtual environment not found. Create it first with: python -m venv .venv'
    }

    Write-Host 'Installing Python dependencies...'
    & $pythonExe -m pip install -r requirements.txt

    Write-Host 'Installing Playwright browser dependencies...'
    & $pythonExe -m playwright install --with-deps chromium

    $env:HEADLESS = 'true'
    $env:SLOW_MO = '0'

    $pytestArgs = @('--html=report.html', '--self-contained-html')
    if ($CollectOnly) {
        $pytestArgs += @('--collect-only', '-q')
    }
    else {
        $pytestArgs += '-v'
    }

    Write-Host ('Running pytest ' + ($pytestArgs -join ' '))
    & $pythonExe -m pytest @pytestArgs
}
finally {
    Pop-Location
}