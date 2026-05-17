$ErrorActionPreference = "Stop"

function Say($msg) { Write-Host $msg }
function EnsureDir($p) { New-Item -ItemType Directory -Force -Path $p | Out-Null }
function SafeResolve($p) { try { (Resolve-Path $p -ErrorAction Stop).Path } catch { $null } }

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Desktop = [Environment]::GetFolderPath("Desktop")
$Downloads = Join-Path $env:USERPROFILE "Downloads"

Say "========================================"
Say " PTA merge helper"
Say "========================================"
Say "Working folder: $Here"
Say ""

$SearchRoots = @($Here, $Desktop, $Downloads) | Where-Object { $_ -and (Test-Path $_) } | Select-Object -Unique

Say "Searching for base ZIP and evidence ZIPs..."

$BaseZip = Get-ChildItem -Path $SearchRoots -Recurse -File -Filter "pta_site_public_cleanup_v26*.zip" -ErrorAction SilentlyContinue |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1

if (-not $BaseZip) {
  Say "ERROR: Base ZIP was not found."
  Say "Put pta_site_public_cleanup_v26_saitama_pdf_local_integrated.zip in this folder or Downloads."
  exit 1
}

Say "Base ZIP: $($BaseZip.FullName)"

$AllEvidence = Get-ChildItem -Path $SearchRoots -Recurse -File -Filter "pta_evidence_sendai_kagoshima_*_part-*-of-29.zip" -ErrorAction SilentlyContinue

if (-not $AllEvidence -or $AllEvidence.Count -eq 0) {
  Say "ERROR: No evidence ZIP files found."
  Say "Need files named like: pta_evidence_sendai_kagoshima_YYYYMMDD_HHMMSS_part-1-of-29.zip"
  exit 1
}

# Group by timestamp and choose a complete set of 29 parts, latest first.
$sets = @{}
foreach ($f in $AllEvidence) {
  if ($f.Name -match '^pta_evidence_sendai_kagoshima_(.+)_part-(\d+)-of-29\.zip$') {
    $stamp = $Matches[1]
    $part = [int]$Matches[2]
    if (-not $sets.ContainsKey($stamp)) { $sets[$stamp] = @{} }
    if (-not $sets[$stamp].ContainsKey($part) -or $f.LastWriteTime -gt $sets[$stamp][$part].LastWriteTime) {
      $sets[$stamp][$part] = $f
    }
  }
}

if ($sets.Count -eq 0) {
  Say "ERROR: Evidence ZIP names did not match expected pattern."
  exit 1
}

$chosenStamp = $null
$chosenMap = $null
foreach ($stamp in ($sets.Keys | Sort-Object -Descending)) {
  $map = $sets[$stamp]
  $missing = @()
  for ($i=1; $i -le 29; $i++) { if (-not $map.ContainsKey($i)) { $missing += $i } }
  Say "Found set $stamp : $($map.Keys.Count)/29 parts"
  if ($missing.Count -eq 0 -and -not $chosenStamp) {
    $chosenStamp = $stamp
    $chosenMap = $map
  }
}

if (-not $chosenStamp) {
  Say ""
  Say "ERROR: No complete 29-part set found."
  Say "Put all part-1-of-29 through part-29-of-29 ZIPs in one folder, then run again."
  exit 1
}

$EvidenceZips = for ($i=1; $i -le 29; $i++) { $chosenMap[$i] }
Say ""
Say "Using evidence set: $chosenStamp"
Say "Evidence ZIP count: $($EvidenceZips.Count)"

$OutDir = Join-Path $Here "site"
$TmpDir = Join-Path $Here "_tmp_merge"

Say ""
Say "Preparing output folders..."
Remove-Item $OutDir -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item $TmpDir -Recurse -Force -ErrorAction SilentlyContinue
EnsureDir $OutDir
EnsureDir $TmpDir

Say "Expanding base site..."
Expand-Archive -Path $BaseZip.FullName -DestinationPath $OutDir -Force

Say "Expanding evidence ZIPs..."
foreach ($z in $EvidenceZips) {
  Say "  $($z.Name)"
  Expand-Archive -Path $z.FullName -DestinationPath $TmpDir -Force
}

Say "Copying PDF files and record pages..."
EnsureDir (Join-Path $OutDir "materials")
EnsureDir (Join-Path $OutDir "materials\documents")
EnsureDir (Join-Path $OutDir "records")
EnsureDir (Join-Path $OutDir "data")

$sendaiSrc = Join-Path $TmpDir "materials\documents\sendai"
$kagoSrc = Join-Path $TmpDir "materials\documents\kagoshima"
if (Test-Path $sendaiSrc) { Copy-Item $sendaiSrc (Join-Path $OutDir "materials\documents") -Recurse -Force }
if (Test-Path $kagoSrc) { Copy-Item $kagoSrc (Join-Path $OutDir "materials\documents") -Recurse -Force }

$recSrc = Join-Path $TmpDir "records"
if (Test-Path $recSrc) {
  Get-ChildItem $recSrc -File -Filter "sendai-*.html" -ErrorAction SilentlyContinue | Copy-Item -Destination (Join-Path $OutDir "records") -Force
  Get-ChildItem $recSrc -File -Filter "kagoshima-*.html" -ErrorAction SilentlyContinue | Copy-Item -Destination (Join-Path $OutDir "records") -Force
}

$catSrc = Join-Path $TmpDir "materials-catalog.html"
if (Test-Path $catSrc) { Copy-Item $catSrc (Join-Path $OutDir "materials-catalog-sendai-kagoshima.html") -Force }

$dataCat = Join-Path $TmpDir "data\evidence-catalog.json"
if (Test-Path $dataCat) { Copy-Item $dataCat (Join-Path $OutDir "data\evidence-catalog-sendai-kagoshima.json") -Force }
$dataIdx = Join-Path $TmpDir "data\evidence-page-index.json"
if (Test-Path $dataIdx) { Copy-Item $dataIdx (Join-Path $OutDir "data\evidence-page-index-sendai-kagoshima.json") -Force }

# Change back links in generated pages.
Get-ChildItem (Join-Path $OutDir "records") -File -Include "sendai-*.html","kagoshima-*.html" -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
  $p = $_.FullName
  (Get-Content $p -Raw) -replace '\.\./materials-catalog\.html', '../materials-catalog-sendai-kagoshima.html' | Set-Content $p -Encoding UTF8
}

Say "Checking result..."
$totalBytes = (Get-ChildItem $OutDir -Recurse -File | Measure-Object Length -Sum).Sum
if (-not $totalBytes) { $totalBytes = 0 }
$pdfBytes = (Get-ChildItem (Join-Path $OutDir "materials\documents") -Recurse -File -Filter "*.pdf" -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
if (-not $pdfBytes) { $pdfBytes = 0 }
$sendaiCount = (Get-ChildItem (Join-Path $OutDir "materials\documents\sendai") -File -Filter "*.pdf" -ErrorAction SilentlyContinue).Count
$kagoCount = (Get-ChildItem (Join-Path $OutDir "materials\documents\kagoshima") -File -Filter "*.pdf" -ErrorAction SilentlyContinue).Count
$recordCount = (Get-ChildItem (Join-Path $OutDir "records") -File -Include "sendai-*.html","kagoshima-*.html" -Recurse -ErrorAction SilentlyContinue).Count

Say ""
Say "========================================"
Say " MERGE COMPLETE"
Say "========================================"
Say ("Site size: {0:N1} MB" -f ($totalBytes / 1MB))
Say ("PDF size:  {0:N1} MB" -f ($pdfBytes / 1MB))
Say "Sendai PDFs: $sendaiCount"
Say "Kagoshima PDFs: $kagoCount"
Say "Record pages: $recordCount"
Say "Output folder: $OutDir"

$CheckPage = Join-Path $OutDir "materials-catalog-sendai-kagoshima.html"
if (Test-Path $CheckPage) {
  Say "Opening check page..."
  Start-Process $CheckPage
} else {
  Say "WARNING: Check page was not created."
}

Start-Process $OutDir
