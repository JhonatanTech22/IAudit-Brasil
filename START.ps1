# IAudit Launch Script
# Use this script to start the entire system
$baseDir = "c:\Users\Micro\Desktop\alan turing 10.02.2026"

Write-Host "🚀 Iniciando IAudit Ecosystem..." -ForegroundColor Cyan

# Kill existing processes if any
Stop-Process -Name "streamlit" -ErrorAction SilentlyContinue
Stop-Process -Name "python" -ErrorAction SilentlyContinue

# 1. Start Mock n8n Server
Write-Host "🤖 Iniciando Mock n8n Server..." -ForegroundColor Cyan
Start-Process python -ArgumentList "$baseDir\IAudit\mock_n8n_server.py" -WorkingDirectory "$baseDir\IAudit" -NoNewWindow

# 2. Start PDF Server
Write-Host "📂 Iniciando Servidor de Certificados..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-File '$baseDir\server.ps1'" -WorkingDirectory $baseDir -NoNewWindow

# 3. Start Streamlit Dashboard
Write-Host "📊 Iniciando IAudit Dashboard..." -ForegroundColor Cyan
$streamlitProcess = Start-Process streamlit -ArgumentList "run frontend/Home.py" -WorkingDirectory "$baseDir\IAudit" -PassThru -NoNewWindow

Write-Host "✨ Tudo pronto!" -ForegroundColor Yellow
Write-Host "--------------------------------------------------" -ForegroundColor Gray
Write-Host "🛡️ Dashboard: http://localhost:8501" -ForegroundColor Green
Write-Host "🤖 n8n Mock:  http://localhost:5678" -ForegroundColor Green
Write-Host "📂 Certificados: http://localhost:8000/file.pdf" -ForegroundColor Green
Write-Host "--------------------------------------------------" -ForegroundColor Gray
Write-Host "Pressione qualquer tecla para encerrar todos os servidores."

$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Stop-Process -Id $streamlitProcess.Id
Stop-Process -Name "python" -ErrorAction SilentlyContinue
