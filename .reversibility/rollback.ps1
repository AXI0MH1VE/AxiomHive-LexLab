#Requires -Version 5.1
<#
.SYNOPSIS
    AxiomHive LexLab Rollback Protocol
.DESCRIPTION
    Safely removes files and directories created by setup-lexlab.ps1,
    with hash verification to prevent accidental deletion of modified files.
.PARAMETER WhatIf
    Show what would be deleted without actually deleting
.PARAMETER Confirm
    Require confirmation before deletion (default: true)
.PARAMETER RunId
    Target specific run ID (default: all runs in reverse order)
.PARAMETER Force
    Delete even if file hashes don't match (dangerous)
.EXAMPLE
    .\rollback.ps1 -WhatIf
.NOTES
    Architect: Alexis Adams (@devdollzai)
    Safety: Hash verification prevents deletion of modified files
#>

[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory=$false)]
    [switch]$WhatIfPreview,
    
    [Parameter(Mandatory=$false)]
    [bool]$RequireConfirm = $true,
    
    [Parameter(Mandatory=$false)]
    [string]$RunId,
    
    [Parameter(Mandatory=$false)]
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ManifestPath = Join-Path $PSScriptRoot "manifest.json"

function Get-Sha256 {
    param([string]$Path)
    if (!(Test-Path $Path)) { return $null }
    $Hasher = [System.Security.Cryptography.SHA256]::Create()
    try {
        $Bytes = [System.IO.File]::ReadAllBytes($Path)
        $Hash = $Hasher.ComputeHash($Bytes)
        return [System.BitConverter]::ToString($Hash).Replace("-", "").ToLower()
    } finally {
        $Hasher.Dispose()
    }
}

if (!(Test-Path $ManifestPath)) {
    Write-Error "Manifest not found: $ManifestPath"
    exit 1
}

$Manifest = Get-Content $ManifestPath -Raw | ConvertFrom-Json

$TargetRuns = if ($RunId) {
    $Manifest.runs | Where-Object { $_.id -eq $RunId }
} else {
    $Manifest.runs | Sort-Object startedUtc -Descending
}

if (!$TargetRuns) {
    Write-Warning "No runs found to rollback"
    exit 0
}

$ItemsToDelete = @()
foreach ($Run in $TargetRuns) {
    $ItemsToDelete += $Run.items | Sort-Object type, path
}

# Group by type: files first, then directories
$Files = $ItemsToDelete | Where-Object { $_.type -eq "file" }
$Directories = $ItemsToDelete | Where-Object { $_.type -eq "dir" } | Sort-Object path -Descending

$DeletedCount = 0
$SkippedCount = 0
$ErrorCount = 0

Write-Host "AxiomHive LexLab Rollback Protocol" -ForegroundColor Cyan
$RunCount = if ($TargetRuns -is [array]) { $TargetRuns.Count } else { if ($TargetRuns) { 1 } else { 0 } }
$FileCount = if ($Files -is [array]) { $Files.Count } else { if ($Files) { 1 } else { 0 } }
$DirCount = if ($Directories -is [array]) { $Directories.Count } else { if ($Directories) { 1 } else { 0 } }
Write-Host "Runs: $RunCount, Files: $FileCount, Dirs: $DirCount" -ForegroundColor Yellow

if ($WhatIfPreview) {
    Write-Host "`n[SIMULATION MODE - No files will be deleted]" -ForegroundColor Magenta
}

# Delete files first
foreach ($Item in $Files) {
    $Path = $Item.path
    
    if (!(Test-Path $Path)) {
        Write-Host "Already deleted: $($Item.rel)" -ForegroundColor Gray
        continue
    }
    
    if (!$Force -and $Item.sha256) {
        $CurrentHash = Get-Sha256 $Path
        if ($CurrentHash -ne $Item.sha256) {
            Write-Warning "Hash mismatch, skipping: $($Item.rel)"
            Write-Host "  Expected: $($Item.sha256)" -ForegroundColor Red
            Write-Host "  Current:  $CurrentHash" -ForegroundColor Red
            $SkippedCount++
            continue
        }
    }
    
    if ($WhatIfPreview -or $PSCmdlet.ShouldProcess($Path, "Delete File")) {
        try {
            if (!$WhatIfPreview) {
                Remove-Item $Path -Force
            }
            Write-Host "Deleted: $($Item.rel)" -ForegroundColor Green
            $DeletedCount++
        }
        catch {
            Write-Error "Failed to delete $($Item.rel): $_"
            $ErrorCount++
        }
    }
}

# Delete directories (in reverse path order)
foreach ($Item in $Directories) {
    $Path = $Item.path
    
    if (!(Test-Path $Path)) {
        Write-Host "Already deleted: $($Item.rel)" -ForegroundColor Gray
        continue
    }
    
    if (!$Force) {
        $Contents = Get-ChildItem $Path -Force
        if ($Contents) {
            Write-Warning "Directory not empty, skipping: $($Item.rel)"
            $SkippedCount++
            continue
        }
    }
    
    if ($WhatIfPreview -or $PSCmdlet.ShouldProcess($Path, "Delete Directory")) {
        try {
            if (!$WhatIfPreview) {
                Remove-Item $Path -Force -Recurse:$Force
            }
            Write-Host "Deleted: $($Item.rel)/" -ForegroundColor Green
            $DeletedCount++
        }
        catch {
            Write-Error "Failed to delete $($Item.rel): $_"
            $ErrorCount++
        }
    }
}

Write-Host "`nRollback Summary:" -ForegroundColor Cyan
Write-Host "  Deleted: $DeletedCount" -ForegroundColor Green
Write-Host "  Skipped: $SkippedCount" -ForegroundColor Yellow
Write-Host "  Errors:  $ErrorCount" -ForegroundColor Red

if ($ErrorCount -gt 0) {
    exit 1
} elseif ($SkippedCount -gt 0) {
    exit 2
} else {
    exit 0
}