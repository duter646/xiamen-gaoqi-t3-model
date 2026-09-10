$ErrorActionPreference = 'Stop'
$bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$pythonCommand = if (Test-Path -LiteralPath $bundledPython) { $bundledPython } else { 'python' }
Write-Host 'Open http://127.0.0.1:8766/index.html in your browser.'
Write-Host 'Press Ctrl+C to stop the local preview server.'
& $pythonCommand -m http.server 8766 --bind 127.0.0.1 --directory $PSScriptRoot
