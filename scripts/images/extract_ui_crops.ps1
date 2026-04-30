param(
    [Parameter(Mandatory = $true)]
    [string]$Manifest,

    [Parameter(Mandatory = $true)]
    [string]$OutputRoot
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Drawing

function Ensure-Directory {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Path $Path | Out-Null
    }
}

function Get-Font {
    param(
        [float]$Size,
        [System.Drawing.FontStyle]$Style = [System.Drawing.FontStyle]::Regular
    )

    return New-Object System.Drawing.Font("Arial", $Size, $Style)
}

$manifestPath = Resolve-Path -LiteralPath $Manifest
$outputRootPath = [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $OutputRoot))

Ensure-Directory -Path $outputRootPath
Ensure-Directory -Path (Join-Path $outputRootPath "crops")
Ensure-Directory -Path (Join-Path $outputRootPath "review")

$manifestData = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$sourcePath = Resolve-Path -LiteralPath $manifestData.source

$sourceImage = [System.Drawing.Image]::FromFile($sourcePath)
$annotatedBitmap = New-Object System.Drawing.Bitmap($sourceImage.Width, $sourceImage.Height)
$graphics = [System.Drawing.Graphics]::FromImage($annotatedBitmap)
$graphics.DrawImage($sourceImage, 0, 0, $sourceImage.Width, $sourceImage.Height)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias

$pen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 255, 207, 64), 4)
$brush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(200, 0, 0, 0))
$textBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
$labelFont = Get-Font -Size 18 -Style ([System.Drawing.FontStyle]::Bold)

$sheetColumns = 3
$sheetMargin = 24
$tileWidth = 360
$tileHeight = 210
$tileHeader = 58
$sheetRows = [Math]::Ceiling($manifestData.controls.Count / $sheetColumns)
$sheetWidth = ($sheetColumns * $tileWidth) + (($sheetColumns + 1) * $sheetMargin)
$sheetHeight = ($sheetRows * ($tileHeight + $tileHeader)) + (($sheetRows + 1) * $sheetMargin)
$sheetBitmap = New-Object System.Drawing.Bitmap($sheetWidth, $sheetHeight)
$sheetGraphics = [System.Drawing.Graphics]::FromImage($sheetBitmap)
$sheetGraphics.Clear([System.Drawing.Color]::FromArgb(244, 244, 244))
$sheetGraphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$sheetTitleFont = Get-Font -Size 14 -Style ([System.Drawing.FontStyle]::Bold)
$sheetMetaFont = Get-Font -Size 11
$sheetBorderPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 110, 110, 110), 2)

$index = 0

foreach ($control in $manifestData.controls) {
    $bbox = $control.bbox
    $x = [int]$bbox[0]
    $y = [int]$bbox[1]
    $w = [int]$bbox[2]
    $h = [int]$bbox[3]

    $rect = New-Object System.Drawing.Rectangle($x, $y, $w, $h)
    $graphics.DrawRectangle($pen, $rect)
    $labelRect = New-Object System.Drawing.RectangleF($x, [Math]::Max(0, $y - 28), 260, 24)
    $graphics.FillRectangle($brush, $labelRect)
    $graphics.DrawString($control.control_id, $labelFont, $textBrush, $x + 6, [Math]::Max(0, $y - 26))

    $cropBitmap = New-Object System.Drawing.Bitmap($w, $h)
    $cropGraphics = [System.Drawing.Graphics]::FromImage($cropBitmap)
    $cropGraphics.DrawImage($sourceImage, (New-Object System.Drawing.Rectangle(0, 0, $w, $h)), $rect, [System.Drawing.GraphicsUnit]::Pixel)

    $typeDir = Join-Path (Join-Path $outputRootPath "crops") $control.type
    Ensure-Directory -Path $typeDir
    $cropPath = Join-Path $typeDir ($control.control_id + ".png")
    $cropBitmap.Save($cropPath, [System.Drawing.Imaging.ImageFormat]::Png)
    $cropGraphics.Dispose()
    $cropBitmap.Dispose()

    $row = [Math]::Floor($index / $sheetColumns)
    $col = $index % $sheetColumns
    $tileX = $sheetMargin + ($col * ($tileWidth + $sheetMargin))
    $tileY = $sheetMargin + ($row * ($tileHeight + $tileHeader + $sheetMargin))

    $sheetGraphics.FillRectangle([System.Drawing.Brushes]::White, $tileX, $tileY, $tileWidth, $tileHeight + $tileHeader)
    $sheetGraphics.DrawRectangle($sheetBorderPen, $tileX, $tileY, $tileWidth, $tileHeight + $tileHeader)
    $sheetGraphics.DrawString($control.control_id, $sheetTitleFont, [System.Drawing.Brushes]::Black, $tileX + 12, $tileY + 10)
    $sheetGraphics.DrawString(($control.type + " / " + $control.state), $sheetMetaFont, [System.Drawing.Brushes]::DimGray, $tileX + 12, $tileY + 32)

    $cropForSheet = [System.Drawing.Image]::FromFile($cropPath)
    $fitScale = [Math]::Min($tileWidth / $cropForSheet.Width, $tileHeight / $cropForSheet.Height)
    $fitWidth = [int]($cropForSheet.Width * $fitScale)
    $fitHeight = [int]($cropForSheet.Height * $fitScale)
    $fitX = $tileX + [int](($tileWidth - $fitWidth) / 2)
    $fitY = $tileY + $tileHeader + [int](($tileHeight - $fitHeight) / 2)
    $sheetGraphics.DrawImage($cropForSheet, $fitX, $fitY, $fitWidth, $fitHeight)
    $cropForSheet.Dispose()

    $index += 1
}

$annotatedPath = Join-Path (Join-Path $outputRootPath "review") ($manifestData.id + "-annotated.png")
$contactSheetPath = Join-Path (Join-Path $outputRootPath "review") ($manifestData.id + "-contact-sheet.png")

$annotatedBitmap.Save($annotatedPath, [System.Drawing.Imaging.ImageFormat]::Png)
$sheetBitmap.Save($contactSheetPath, [System.Drawing.Imaging.ImageFormat]::Png)

$graphics.Dispose()
$annotatedBitmap.Dispose()
$sheetGraphics.Dispose()
$sheetBitmap.Dispose()
$sourceImage.Dispose()
$pen.Dispose()
$brush.Dispose()
$textBrush.Dispose()
$labelFont.Dispose()
$sheetTitleFont.Dispose()
$sheetMetaFont.Dispose()
$sheetBorderPen.Dispose()

Write-Output ("Manifest: " + $manifestPath)
Write-Output ("Annotated: " + $annotatedPath)
Write-Output ("ContactSheet: " + $contactSheetPath)
Write-Output ("ControlsExported: " + $manifestData.controls.Count)
