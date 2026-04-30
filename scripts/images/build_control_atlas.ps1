param(
    [Parameter(Mandatory = $true)]
    [string]$Manifest,

    [Parameter(Mandatory = $true)]
    [string]$Output
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

function Resolve-AssetPath {
    param(
        [string]$Root,
        [string]$Path
    )

    return [System.IO.Path]::GetFullPath((Join-Path $Root $Path))
}

function Draw-TextLine {
    param(
        [System.Drawing.Graphics]$Graphics,
        [string]$Text,
        [System.Drawing.Font]$Font,
        [System.Drawing.Brush]$Brush,
        [float]$X,
        [float]$Y,
        [float]$Width = 320
    )

    $format = New-Object System.Drawing.StringFormat
    $format.Alignment = [System.Drawing.StringAlignment]::Near
    $format.LineAlignment = [System.Drawing.StringAlignment]::Near
    $Graphics.DrawString($Text, $Font, $Brush, [System.Drawing.RectangleF]::new($X, $Y, $Width, 60), $format)
    $format.Dispose()
}

function Get-PreviewRect {
    param([System.Drawing.Image]$Image)

    $bitmap = [System.Drawing.Bitmap]$Image
    $left = 0
    $top = 0
    $right = $bitmap.Width - 1
    $bottom = $bitmap.Height - 1
    $whiteThreshold = 744

    function Test-ColumnHasContent {
        param([int]$X)
        for ($y = 0; $y -lt $bitmap.Height; $y++) {
            $pixel = $bitmap.GetPixel($X, $y)
            if ($pixel.A -gt 16 -and (($pixel.R + $pixel.G + $pixel.B) -lt $whiteThreshold)) {
                return $true
            }
        }
        return $false
    }

    function Test-RowHasContent {
        param([int]$Y)
        for ($x = 0; $x -lt $bitmap.Width; $x++) {
            $pixel = $bitmap.GetPixel($x, $Y)
            if ($pixel.A -gt 16 -and (($pixel.R + $pixel.G + $pixel.B) -lt $whiteThreshold)) {
                return $true
            }
        }
        return $false
    }

    while ($left -lt $right -and -not (Test-ColumnHasContent -X $left)) { $left++ }
    while ($right -gt $left -and -not (Test-ColumnHasContent -X $right)) { $right-- }
    while ($top -lt $bottom -and -not (Test-RowHasContent -Y $top)) { $top++ }
    while ($bottom -gt $top -and -not (Test-RowHasContent -Y $bottom)) { $bottom-- }

    $padding = 6
    $left = [Math]::Max(0, $left - $padding)
    $top = [Math]::Max(0, $top - $padding)
    $right = [Math]::Min($bitmap.Width - 1, $right + $padding)
    $bottom = [Math]::Min($bitmap.Height - 1, $bottom + $padding)

    return [System.Drawing.Rectangle]::new($left, $top, $right - $left + 1, $bottom - $top + 1)
}

$manifestPath = Resolve-Path -LiteralPath $Manifest
$manifestRoot = Split-Path -Path $manifestPath -Parent
$manifestData = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json

$assets = @()
foreach ($asset in $manifestData.assets) {
    $assetPath = Resolve-AssetPath -Root (Get-Location) -Path $asset.output_path
    if (Test-Path -LiteralPath $assetPath) {
        $sourceSheet = ""
        if ($asset.PSObject.Properties.Name -contains "source_sheet") {
            $sourceSheet = [string]$asset.source_sheet
        }
        $assets += [PSCustomObject]@{
            asset_id = [string]$asset.asset_id
            category = [string]$asset.category
            content_type = [string]$asset.content_type
            source_sheet = $sourceSheet
            output_path = $assetPath
        }
    }
}

if ($assets.Count -eq 0) {
    throw "No assets found from manifest."
}

$groupOrder = $assets | Group-Object category | Sort-Object Name

$pagePadding = 56
$sectionGap = 42
$headerHeight = 90
$sectionTitleHeight = 34
$cardWidth = 360
$cardHeight = 292
$cardGapX = 24
$cardGapY = 28
$columns = 3
$innerImageWidth = 316
$innerImageHeight = 180

$pageWidth = ($pagePadding * 2) + ($columns * $cardWidth) + (($columns - 1) * $cardGapX)
$pageHeight = $pagePadding + $headerHeight

foreach ($group in $groupOrder) {
    $rows = [int][Math]::Ceiling($group.Count / [double]$columns)
    $pageHeight += $sectionTitleHeight + ($rows * $cardHeight) + (($rows - 1) * $cardGapY) + $sectionGap
}

$pageHeight += $pagePadding

$bitmap = New-Object System.Drawing.Bitmap($pageWidth, $pageHeight, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
$graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
$graphics.Clear([System.Drawing.Color]::FromArgb(255, 246, 246, 244))

$titleFont = New-Object System.Drawing.Font("Segoe UI", 26, [System.Drawing.FontStyle]::Bold)
$subtitleFont = New-Object System.Drawing.Font("Segoe UI", 12, [System.Drawing.FontStyle]::Regular)
$sectionFont = New-Object System.Drawing.Font("Segoe UI", 18, [System.Drawing.FontStyle]::Bold)
$labelFont = New-Object System.Drawing.Font("Segoe UI", 13, [System.Drawing.FontStyle]::Bold)
$metaFont = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Regular)

$titleBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 24, 24, 26))
$subtitleBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 96, 96, 102))
$sectionBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 52, 52, 56))
$labelBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 26, 26, 28))
$metaBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 110, 110, 118))
$cardFill = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 255, 255, 255))
$imageFill = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 250, 250, 248))
$borderPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 214, 214, 219), 1)
$imageBorderPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 226, 226, 230), 1)
$sectionLinePen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 205, 205, 210), 1)

$title = if ($manifestData.title) { [string]$manifestData.title } else { "Star Rail UI Atlas" }
$description = if ($manifestData.description) { [string]$manifestData.description } else { "AI-readable grouped UI atlas" }

Draw-TextLine -Graphics $graphics -Text $title -Font $titleFont -Brush $titleBrush -X $pagePadding -Y 28 -Width ($pageWidth - ($pagePadding * 2))
Draw-TextLine -Graphics $graphics -Text $description -Font $subtitleFont -Brush $subtitleBrush -X $pagePadding -Y 62 -Width ($pageWidth - ($pagePadding * 2))

$currentY = $pagePadding + $headerHeight

foreach ($group in $groupOrder) {
    $graphics.DrawLine($sectionLinePen, $pagePadding, $currentY, $pageWidth - $pagePadding, $currentY)
    $currentY += 14
    Draw-TextLine -Graphics $graphics -Text $group.Name -Font $sectionFont -Brush $sectionBrush -X $pagePadding -Y $currentY
    $currentY += $sectionTitleHeight

    for ($i = 0; $i -lt $group.Count; $i++) {
        $col = $i % $columns
        $row = [int][Math]::Floor($i / $columns)
        $cardX = $pagePadding + ($col * ($cardWidth + $cardGapX))
        $cardY = $currentY + ($row * ($cardHeight + $cardGapY))

        $graphics.FillRectangle($cardFill, $cardX, $cardY, $cardWidth, $cardHeight)
        $graphics.DrawRectangle($borderPen, $cardX, $cardY, $cardWidth, $cardHeight)

        $imageRect = [System.Drawing.Rectangle]::new($cardX + 22, $cardY + 18, $innerImageWidth, $innerImageHeight)
        $graphics.FillRectangle($imageFill, $imageRect)
        $graphics.DrawRectangle($imageBorderPen, $imageRect)

        $asset = $group.Group[$i]
        $image = [System.Drawing.Image]::FromFile($asset.output_path)
        try {
            $previewRect = Get-PreviewRect -Image $image
            $scale = [Math]::Min($imageRect.Width / [double]$previewRect.Width, $imageRect.Height / [double]$previewRect.Height)
            $drawWidth = [int][Math]::Round($previewRect.Width * $scale)
            $drawHeight = [int][Math]::Round($previewRect.Height * $scale)
            $drawX = $imageRect.X + [int][Math]::Floor(($imageRect.Width - $drawWidth) / 2)
            $drawY = $imageRect.Y + [int][Math]::Floor(($imageRect.Height - $drawHeight) / 2)
            $graphics.DrawImage($image, [System.Drawing.Rectangle]::new($drawX, $drawY, $drawWidth, $drawHeight), $previewRect, [System.Drawing.GraphicsUnit]::Pixel)
        }
        finally {
            $image.Dispose()
        }

        Draw-TextLine -Graphics $graphics -Text $asset.content_type -Font $labelFont -Brush $labelBrush -X ($cardX + 20) -Y ($cardY + 212)
        Draw-TextLine -Graphics $graphics -Text $asset.asset_id -Font $metaFont -Brush $metaBrush -X ($cardX + 20) -Y ($cardY + 244)
    }

    $rows = [int][Math]::Ceiling($group.Count / [double]$columns)
    $currentY += ($rows * $cardHeight) + (($rows - 1) * $cardGapY) + $sectionGap
}

$outputPath = [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $Output))
Ensure-Directory -Path (Split-Path -Path $outputPath -Parent)
$bitmap.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)

$titleFont.Dispose()
$subtitleFont.Dispose()
$sectionFont.Dispose()
$labelFont.Dispose()
$metaFont.Dispose()
$titleBrush.Dispose()
$subtitleBrush.Dispose()
$sectionBrush.Dispose()
$labelBrush.Dispose()
$metaBrush.Dispose()
$cardFill.Dispose()
$imageFill.Dispose()
$borderPen.Dispose()
$imageBorderPen.Dispose()
$sectionLinePen.Dispose()
$graphics.Dispose()
$bitmap.Dispose()

Write-Output ("SavedAtlas: " + $outputPath)
