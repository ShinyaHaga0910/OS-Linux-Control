[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$sourceRoot = Join-Path $root 'assets\figure-sources-v1.2'
$d2Root = Join-Path $sourceRoot 'd2'
$typstRoot = Join-Path $sourceRoot 'typst'
$freezeRoot = Join-Path $sourceRoot 'freeze'
$generatedRoot = Join-Path $sourceRoot 'generated'
$outputRoot = Join-Path $root 'assets\figures'
$fontSans = if ($env:JDU_FONT_SANS) { $env:JDU_FONT_SANS } else { 'C:\Windows\Fonts\NotoSansJP-VF.ttf' }

function Resolve-Tool {
    param([string]$Name, [string[]]$Candidates)
    $command = Get-Command $Name -ErrorAction SilentlyContinue
    if ($command) { return $command.Source }
    foreach ($candidate in $Candidates) {
        if (Test-Path -LiteralPath $candidate) { return $candidate }
    }
    throw "$Name was not found. Install it before building diagrams."
}

$d2 = Resolve-Tool 'd2' @('C:\Program Files\D2\d2.exe')
$typst = Resolve-Tool 'typst' @(
    "$env:LOCALAPPDATA\Microsoft\WinGet\Packages\Typst.Typst_Microsoft.Winget.Source_8wekyb3d8bbwe\typst-x86_64-pc-windows-msvc\typst.exe"
)
$freeze = Resolve-Tool 'freeze' @(
    "$env:LOCALAPPDATA\Microsoft\WinGet\Packages\charmbracelet.freeze_Microsoft.Winget.Source_8wekyb3d8bbwe\freeze_0.2.2_Windows_x86_64\freeze.exe"
)

New-Item -ItemType Directory -Force -Path $generatedRoot, $outputRoot | Out-Null

Push-Location $d2Root
try {
    Get-ChildItem -LiteralPath $d2Root -Filter 'fig*.d2' | Sort-Object Name | ForEach-Object {
        $outputName = [IO.Path]::GetFileNameWithoutExtension($_.Name) + '.svg'
        $outputPath = Join-Path $outputRoot $outputName
        & $d2 --layout elk --pad 36 --font-regular $fontSans --font-bold $fontSans --font-semibold $fontSans $_.Name $outputPath
        if ($LASTEXITCODE -ne 0) { throw "D2 failed: $($_.Name)" }

        # D2 embeds the complete font as a data URI. That makes the SVG very large
        # and prevents svglib from importing it on Windows. The textbook PDF has
        # NotoSansJP registered, so keep text as text and use that registered font.
        $svg = Get-Content -LiteralPath $outputPath -Raw -Encoding utf8
        $svg = [regex]::Replace($svg, '@font-face\s*\{.*?\}', '', [Text.RegularExpressions.RegexOptions]::Singleline)
        $svg = [regex]::Replace($svg, 'd2-\d+-font-(regular|bold|semibold|italic)', 'NotoSansJP')
        Set-Content -LiteralPath $outputPath -Value $svg -Encoding utf8 -NoNewline

        $pdfRaster = Join-Path $generatedRoot ($_.BaseName + '-pdf.png')
        & $d2 --layout elk --pad 36 --scale 2 --font-regular $fontSans --font-bold $fontSans --font-semibold $fontSans $_.Name $pdfRaster
        if ($LASTEXITCODE -ne 0) { throw "D2 PNG fallback failed: $($_.Name)" }
    }
}
finally {
    Pop-Location
}

$terminalSvg = Join-Path $generatedRoot 'fig16-terminal.svg'
& $freeze (Join-Path $freezeRoot 'fig16-ss-output.txt') --config (Join-Path $freezeRoot 'freeze-config.json') --output $terminalSvg --font.file 'C:\Windows\Fonts\consola.ttf'
if ($LASTEXITCODE -ne 0) { throw 'Freeze failed: fig16-ss-output.txt' }

Get-ChildItem -LiteralPath $typstRoot -Filter 'fig*.typ' | Sort-Object Name | ForEach-Object {
    $outputName = [IO.Path]::GetFileNameWithoutExtension($_.Name) + '.svg'
    $outputPath = Join-Path $outputRoot $outputName
    & $typst compile --root $sourceRoot --format svg $_.FullName $outputPath
    if ($LASTEXITCODE -ne 0) { throw "Typst failed: $($_.Name)" }

    $pdfRaster = Join-Path $generatedRoot ($_.BaseName + '-pdf.png')
    & $typst compile --root $sourceRoot --format png --ppi 220 $_.FullName $pdfRaster
    if ($LASTEXITCODE -ne 0) { throw "Typst PNG fallback failed: $($_.Name)" }
}

$outputs = Get-ChildItem -LiteralPath $outputRoot -Filter 'fig*.svg' | Sort-Object Name
if ($outputs.Count -ne 21) {
    throw "Expected 21 SVG figures, found $($outputs.Count)."
}

Write-Output "Generated $($outputs.Count) SVG figures in $outputRoot"
