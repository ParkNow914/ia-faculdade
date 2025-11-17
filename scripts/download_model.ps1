Param(
    [Parameter(Mandatory=$false)]
    [string]$ModelUrl = $env:MODEL_URL
)

if (-not $ModelUrl) {
    Write-Host "USAGE: set MODEL_URL env var or pass -ModelUrl 'https://...'"
    exit 1
}

New-Item -ItemType Directory -Force -Path src\model\saved_models | Out-Null
$tmp = Join-Path $env:TEMP ([IO.Path]::GetFileName($ModelUrl))
Write-Host "🔁 Baixando $ModelUrl -> $tmp"

Invoke-WebRequest -Uri $ModelUrl -OutFile $tmp -UseBasicParsing

$fileType = & file $tmp 2>$null | Out-String
if ($fileType -match 'Zip') {
    Write-Host "📦 Extraindo zip..."
    Expand-Archive -Force -Path $tmp -DestinationPath .
    Remove-Item $tmp -Force
} else {
    Write-Host "📁 Movendo artefato para src\model\saved_models\regression_model.pkl"
    Move-Item -Force $tmp src\model\saved_models\regression_model.pkl
}

Write-Host "✅ Modelo instalado em src\model\saved_models\"
