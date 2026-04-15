@echo off
REM Script para executar a aplicação Head Loss Calculator

echo.
echo ========================================
echo Head Loss Calculator - Windows Launcher
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não encontrado no PATH
    echo Por favor, instale Python 3.8+ de https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Verificar se venv existe
if not exist "venv" (
    echo [INFO] Criando ambiente virtual...
    python -m venv venv
)

REM Ativar venv
echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instalar dependências se necessário
if not exist "venv\Lib\site-packages\streamlit" (
    echo [INFO] Instalando dependências...
    pip install -r requirements.txt
)

REM Executar aplicação
echo.
echo [INFO] Iniciando aplicação...
echo [INFO] Acesse http://localhost:8501 em seu navegador
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

streamlit run app.py

pause
