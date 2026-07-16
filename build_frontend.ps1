<#
.SYNOPSIS
  Pre-build the Next.js frontend for production (eliminates on-demand "Rendering...").

.EXAMPLE
  .\build_frontend.ps1
  .\build_frontend.ps1 -ApiBase "http://127.0.0.1:8000/api/v1"
#>
[CmdletBinding()]
param(
  [string]$ApiBase = "http://127.0.0.1:8000/api/v1",
  [switch]$DemoMode
)

$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot
$FrontendDir = Join-Path $Root "frontend"
$LogDir = Join-Path $Root ".run\logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$buildOut = Join-Path $LogDir "frontend.build.out.log"
$buildErr = Join-Path $LogDir "frontend.build.err.log"

$demoValue = if ($DemoMode) { "true" } else { "false" }

Write-Host "Building frontend..." -ForegroundColor Cyan
Write-Host "  NEXT_PUBLIC_DEMO_MODE=$demoValue"
Write-Host "  NEXT_PUBLIC_API_BASE_URL=$ApiBase"
Write-Host "  Logs: $buildOut / $buildErr"

$buildCmd = "set NEXT_PUBLIC_DEMO_MODE=$demoValue&& set NEXT_PUBLIC_API_BASE_URL=$ApiBase&& pnpm build"
# stdout and stderr must be different paths for Start-Process on Windows
$p = Start-Process -FilePath "cmd.exe" -ArgumentList @("/c", $buildCmd) `
  -WorkingDirectory $FrontendDir -Wait -PassThru -NoNewWindow `
  -RedirectStandardOutput $buildOut -RedirectStandardError $buildErr

if ($p.ExitCode -ne 0) {
  Get-Content $buildErr -Tail 40 -ErrorAction SilentlyContinue
  Get-Content $buildOut -Tail 40 -ErrorAction SilentlyContinue
  throw "Build failed (exit $($p.ExitCode))"
}

Write-Host "Build OK. Start with: .\start_all.ps1 -SkipBuild" -ForegroundColor Green
