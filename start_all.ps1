<#
.SYNOPSIS
  Start Generic Swarm Ops backend (uvicorn) and frontend (Next.js).

.DESCRIPTION
  By default starts in Production mode: pre-builds the frontend (pnpm build) then
  serves with "next start" so you do NOT see continuous "Rendering / Compiling"
  from next dev. Use -Dev for hot-reload during coding.

  Writes PIDs to .run/servers.json for stop_all.ps1.

.PARAMETER BackendPort
  Backend listen port (default 8000).

.PARAMETER FrontendPort
  Frontend listen port (default 3000).

.PARAMETER PidFile
  Path to write server PIDs (default: <repo>/.run/servers.json).

.PARAMETER DemoMode
  If set, frontend uses NEXT_PUBLIC_DEMO_MODE=true (must be set at build time in prod).

.PARAMETER Dev
  Use next dev + uvicorn --reload (slower first paint / ongoing "Rendering...").

.PARAMETER SkipBuild
  In production mode, skip pnpm build if .next already exists.

.EXAMPLE
  .\start_all.ps1
  .\start_all.ps1 -Dev
  .\start_all.ps1 -SkipBuild
#>
[CmdletBinding()]
param(
  [int]$BackendPort = 8000,
  [int]$FrontendPort = 3000,
  [string]$PidFile = "",
  [switch]$DemoMode,
  [switch]$Dev,
  [switch]$SkipBuild
)

$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot
if (-not $Root) { $Root = Get-Location | Select-Object -ExpandProperty Path }

$BackendDir = Join-Path $Root "backend"
$FrontendDir = Join-Path $Root "frontend"
$RunDir = Join-Path $Root ".run"
$LogDir = Join-Path $RunDir "logs"
$NextDir = Join-Path $FrontendDir ".next"

if (-not $PidFile) {
  $PidFile = Join-Path $RunDir "servers.json"
}

if (-not (Test-Path $BackendDir)) {
  throw "Backend directory not found: $BackendDir"
}
if (-not (Test-Path (Join-Path $FrontendDir "package.json"))) {
  throw "Frontend package.json not found under: $FrontendDir"
}

New-Item -ItemType Directory -Force -Path $RunDir, $LogDir | Out-Null

if (Test-Path $PidFile) {
  Write-Warning "Existing PID file found: $PidFile"
  Write-Warning "Run .\stop_all.ps1 first if those processes are still running."
}

function Test-PortInUse([int]$Port) {
  try {
    $listeners = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    return $null -ne $listeners
  } catch {
    $out = netstat -ano | Select-String ":$Port\s+.*LISTENING"
    return $null -ne $out
  }
}

if (Test-PortInUse $BackendPort) {
  throw "Port $BackendPort is already in use (backend). Run .\stop_all.ps1 or choose -BackendPort."
}
if (Test-PortInUse $FrontendPort) {
  throw "Port $FrontendPort is already in use (frontend). Run .\stop_all.ps1 or choose -FrontendPort."
}

$backendOut = Join-Path $LogDir "backend.out.log"
$backendErr = Join-Path $LogDir "backend.err.log"
$frontendOut = Join-Path $LogDir "frontend.out.log"
$frontendErr = Join-Path $LogDir "frontend.err.log"
$buildOut = Join-Path $LogDir "frontend.build.out.log"
$buildErr = Join-Path $LogDir "frontend.build.err.log"

$demoValue = if ($DemoMode) { "true" } else { "false" }
$apiBase = "http://127.0.0.1:$BackendPort/api/v1"
$mode = if ($Dev) { "dev" } else { "production" }

# --- Optional frontend production build (precompile all routes) ---
if (-not $Dev) {
  $needBuild = -not (Test-Path $NextDir) -or -not $SkipBuild
  if ($SkipBuild -and -not (Test-Path $NextDir)) {
    Write-Warning ".next missing; cannot SkipBuild. Building..."
    $needBuild = $true
  }
  if ($needBuild) {
    Write-Host "Building frontend (production) — eliminates on-demand 'Rendering...' ..." -ForegroundColor Cyan
    Write-Host "  Logs: $buildOut / $buildErr"
    # NEXT_PUBLIC_* must be set at build time for Next.js
    # Redirect stdout/stderr to DIFFERENT files (Start-Process requirement on Windows).
    $buildCmd = "set NEXT_PUBLIC_DEMO_MODE=$demoValue&& set NEXT_PUBLIC_API_BASE_URL=$apiBase&& pnpm build"
    $buildProc = Start-Process `
      -FilePath "cmd.exe" `
      -ArgumentList @("/c", $buildCmd) `
      -WorkingDirectory $FrontendDir `
      -Wait `
      -PassThru `
      -NoNewWindow `
      -RedirectStandardOutput $buildOut `
      -RedirectStandardError $buildErr
    if ($buildProc.ExitCode -ne 0) {
      Write-Host "Build failed. Last log lines:" -ForegroundColor Red
      Get-Content $buildErr -Tail 30 -ErrorAction SilentlyContinue
      Get-Content $buildOut -Tail 30 -ErrorAction SilentlyContinue
      throw "pnpm build failed with exit code $($buildProc.ExitCode). See $buildOut and $buildErr"
    }
    Write-Host "Frontend build complete." -ForegroundColor Green
  } else {
    Write-Host "Using existing frontend build (.next) — SkipBuild." -ForegroundColor Cyan
  }
}

# --- Backend ---
# Production: no --reload (avoids restarts). Dev: --reload for code changes.
$backendUvicorn = if ($Dev) {
  "python -m uvicorn app.main:app --reload --host 127.0.0.1 --port $BackendPort"
} else {
  "python -m uvicorn app.main:app --host 127.0.0.1 --port $BackendPort --workers 1"
}
$backendCmd = "set PYTHONPATH=.&& $backendUvicorn"

$backendProc = Start-Process `
  -FilePath "cmd.exe" `
  -ArgumentList @("/c", $backendCmd) `
  -WorkingDirectory $BackendDir `
  -PassThru `
  -WindowStyle Minimized `
  -RedirectStandardOutput $backendOut `
  -RedirectStandardError $backendErr

# --- Frontend ---
$frontendCmd = if ($Dev) {
  "set NEXT_PUBLIC_DEMO_MODE=$demoValue&& set NEXT_PUBLIC_API_BASE_URL=$apiBase&& pnpm dev --port $FrontendPort"
} else {
  # next start serves the pre-built .next output (no Turbopack compile-on-navigate)
  "set NEXT_PUBLIC_DEMO_MODE=$demoValue&& set NEXT_PUBLIC_API_BASE_URL=$apiBase&& pnpm exec next start -H 127.0.0.1 -p $FrontendPort"
}

$frontendProc = Start-Process `
  -FilePath "cmd.exe" `
  -ArgumentList @("/c", $frontendCmd) `
  -WorkingDirectory $FrontendDir `
  -PassThru `
  -WindowStyle Minimized `
  -RedirectStandardOutput $frontendOut `
  -RedirectStandardError $frontendErr

$state = [ordered]@{
  schema_version = "1.0"
  started_at     = (Get-Date).ToString("o")
  root           = $Root
  pid_file       = $PidFile
  mode           = $mode
  backend        = [ordered]@{
    name    = "backend"
    pid     = $backendProc.Id
    port    = $BackendPort
    url     = "http://127.0.0.1:$BackendPort"
    health  = "http://127.0.0.1:$BackendPort/api/v1/health/ready"
    cwd     = $BackendDir
    log_out = $backendOut
    log_err = $backendErr
    reload  = [bool]$Dev
  }
  frontend       = [ordered]@{
    name      = "frontend"
    pid       = $frontendProc.Id
    port      = $FrontendPort
    url       = "http://127.0.0.1:$FrontendPort"
    login     = "http://127.0.0.1:$FrontendPort/login"
    cwd       = $FrontendDir
    log_out   = $frontendOut
    log_err   = $frontendErr
    demo_mode = $demoValue
    api_base  = $apiBase
    command   = if ($Dev) { "next dev" } else { "next start (prebuilt)" }
  }
  pids = @($backendProc.Id, $frontendProc.Id)
}

$state | ConvertTo-Json -Depth 6 | Set-Content -Path $PidFile -Encoding UTF8

Write-Host ""
Write-Host "Generic Swarm Ops servers started ($mode)." -ForegroundColor Green
Write-Host ""
Write-Host ("  Backend  PID {0,-8}  {1}" -f $backendProc.Id, $state.backend.url)
Write-Host ("  Frontend PID {0,-8}  {1}" -f $frontendProc.Id, $state.frontend.url)
Write-Host ("  Frontend mode: {0}" -f $state.frontend.command)
Write-Host ""
Write-Host "  Login:   $($state.frontend.login)"
Write-Host "  Health:  $($state.backend.health)"
Write-Host "  PID file: $PidFile"
Write-Host "  Logs:     $LogDir"
if (-not $Dev) {
  Write-Host ""
  Write-Host "  Tip: No continuous 'Rendering...' — pages are prebuilt." -ForegroundColor Cyan
  Write-Host "  After code changes: .\stop_all.ps1 then .\start_all.ps1  (rebuilds)"
  Write-Host "  Or: .\start_all.ps1 -SkipBuild  (reuse .next)"
  Write-Host "  Dev hot-reload: .\start_all.ps1 -Dev"
} else {
  Write-Host ""
  Write-Host "  Dev mode: first visit to each route compiles on demand ('Rendering...')." -ForegroundColor Yellow
  Write-Host "  Faster browsing: .\stop_all.ps1 ; .\start_all.ps1   (production prebuild)"
}
Write-Host ""
Write-Host "Stop with: .\stop_all.ps1" -ForegroundColor Yellow
Write-Host "Seed login: admin@example.com / admin-password" -ForegroundColor Cyan
Write-Host ""

[pscustomobject]@{
  BackendPid  = $backendProc.Id
  FrontendPid = $frontendProc.Id
  PidFile     = $PidFile
  Mode        = $mode
}
