<#
.SYNOPSIS
  Stop servers started by start_all.ps1.

.DESCRIPTION
  Reads PIDs from the PID file written by start_all.ps1 (default .run/servers.json),
  or accepts explicit -BackendPid / -FrontendPid. Kills each process tree (cmd + children).

.PARAMETER PidFile
  Path to servers.json written by start_all.ps1.

.PARAMETER BackendPid
  Optional explicit backend (or wrapper) process id.

.PARAMETER FrontendPid
  Optional explicit frontend (or wrapper) process id.

.PARAMETER Force
  Use forceful kill (default: true for Windows process trees).

.EXAMPLE
  .\stop_all.ps1
  .\stop_all.ps1 -PidFile .\.run\servers.json
  .\stop_all.ps1 -BackendPid 12345 -FrontendPid 67890
#>
[CmdletBinding()]
param(
  [string]$PidFile = "",
  [int]$BackendPid = 0,
  [int]$FrontendPid = 0,
  [switch]$KeepPidFile
)

$ErrorActionPreference = "Continue"
$Root = $PSScriptRoot
if (-not $Root) { $Root = Get-Location | Select-Object -ExpandProperty Path }

if (-not $PidFile) {
  $PidFile = Join-Path $Root ".run\servers.json"
}

$toStop = New-Object System.Collections.Generic.List[int]

if ($BackendPid -gt 0) { $toStop.Add($BackendPid) | Out-Null }
if ($FrontendPid -gt 0) { $toStop.Add($FrontendPid) | Out-Null }

if ($toStop.Count -eq 0) {
  if (-not (Test-Path $PidFile)) {
    Write-Error "No PID file at '$PidFile' and no -BackendPid/-FrontendPid provided."
    Write-Host "Usage:"
    Write-Host "  .\stop_all.ps1"
    Write-Host "  .\stop_all.ps1 -BackendPid <pid> -FrontendPid <pid>"
    exit 1
  }

  try {
    $state = Get-Content -Path $PidFile -Raw | ConvertFrom-Json
  } catch {
    Write-Error "Failed to parse PID file: $PidFile — $_"
    exit 1
  }

  if ($state.backend.pid) { $toStop.Add([int]$state.backend.pid) | Out-Null }
  if ($state.frontend.pid) { $toStop.Add([int]$state.frontend.pid) | Out-Null }
  if ($state.pids) {
    foreach ($p in $state.pids) {
      $id = [int]$p
      if ($id -gt 0 -and -not $toStop.Contains($id)) { $toStop.Add($id) | Out-Null }
    }
  }

  Write-Host "Loaded PIDs from $PidFile"
  if ($state.backend.pid) {
    Write-Host ("  Backend  PID {0}  (port {1})" -f $state.backend.pid, $state.backend.port)
  }
  if ($state.frontend.pid) {
    Write-Host ("  Frontend PID {0}  (port {1})" -f $state.frontend.pid, $state.frontend.port)
  }
}

function Stop-ProcessTree([int]$ProcessId) {
  if ($ProcessId -le 0) { return $false }
  $proc = Get-Process -Id $ProcessId -ErrorAction SilentlyContinue
  if (-not $proc) {
    Write-Host "  PID $ProcessId already stopped."
    return $true
  }

  Write-Host "  Stopping process tree PID $ProcessId ($($proc.ProcessName))..."
  # /T = tree (children of cmd.exe / uvicorn --reload / node)
  $result = & taskkill.exe /PID $ProcessId /T /F 2>&1
  if ($LASTEXITCODE -eq 0) {
    Write-Host "  Stopped PID $ProcessId" -ForegroundColor Green
    return $true
  }

  # Fallback
  try {
    Stop-Process -Id $ProcessId -Force -ErrorAction Stop
    Write-Host "  Stop-Process forced PID $ProcessId" -ForegroundColor Yellow
    return $true
  } catch {
    Write-Warning "  Failed to stop PID $ProcessId : $_"
    Write-Host "  taskkill: $result"
    return $false
  }
}

$failed = 0
Write-Host ""
Write-Host "Stopping Generic Swarm Ops servers..." -ForegroundColor Yellow
foreach ($processId in ($toStop | Select-Object -Unique)) {
  if (-not (Stop-ProcessTree -ProcessId $processId)) {
    $failed++
  }
}

# Also free common ports if orphaned children remain (best-effort)
function Stop-ListenersOnPort([int]$Port) {
  try {
    $conns = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    foreach ($c in $conns) {
      $opid = [int]$c.OwningProcess
      if ($opid -gt 0) {
        Write-Host "  Port $Port still held by PID $opid — killing tree..."
        Stop-ProcessTree -ProcessId $opid | Out-Null
      }
    }
  } catch {
    # ignore
  }
}

Stop-ListenersOnPort 8000
Stop-ListenersOnPort 3000

if ((Test-Path $PidFile) -and -not $KeepPidFile) {
  Remove-Item -Path $PidFile -Force -ErrorAction SilentlyContinue
  Write-Host "Removed PID file: $PidFile"
}

Write-Host ""
if ($failed -gt 0) {
  Write-Host "Completed with $failed failure(s)." -ForegroundColor Yellow
  exit 1
}
Write-Host "All requested servers stopped." -ForegroundColor Green
exit 0
