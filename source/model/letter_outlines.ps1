param([string]$Text='厦门',[string]$Font='KaiTi',[string]$Output='letter-contours.json')
Add-Type -AssemblyName System.Drawing
$letterFont = New-Object System.Drawing.FontFamily($Font)
$letterPath = New-Object System.Drawing.Drawing2D.GraphicsPath
$letterPath.AddString($Text, $letterFont, 0, 1000, (New-Object System.Drawing.PointF(0,0)), [System.Drawing.StringFormat]::GenericTypographic)
$letterPath.Flatten($null, 0.7)
$letterContours = [System.Collections.Generic.List[object]]::new()
$letterContour = [System.Collections.Generic.List[object]]::new()
for ($letterIndex=0; $letterIndex -lt $letterPath.PointCount; $letterIndex++) {
    $letterPoint=$letterPath.PathPoints[$letterIndex]
    $letterContour.Add(@([double]$letterPoint.X,[double]$letterPoint.Y))
    if (($letterPath.PathTypes[$letterIndex] -band 128) -ne 0) {
        $letterContours.Add($letterContour.ToArray())
        $letterContour=[System.Collections.Generic.List[object]]::new()
    }
}
@{font=$letterFont.Name;text=$Text;contours=$letterContours.ToArray()} | ConvertTo-Json -Depth 8 -Compress | Set-Content -LiteralPath (Join-Path $PSScriptRoot $Output) -Encoding utf8
$letterPath.Dispose()
$letterFont.Dispose()
