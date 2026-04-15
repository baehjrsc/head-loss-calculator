#!/bin/bash
# Script para executar a aplicação Head Loss Calculator

echo ""
echo "========================================"
echo "Head Loss Calculator - Linux/Mac Launch"
echo "========================================"
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python não encontrado no PATH"
    echo "Por favor, instale Python 3.8+ de https://www.python.org/downloads/"
    exit 1
fi

# Verificar se venv existe
if [ ! -d "venv" ]; then
    echo "[INFO] Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar venv
echo "[INFO] Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências se necessário
if ! pip list | grep -q streamlit; then
    echo "[INFO] Instalando dependências..."
    pip install -r requirements.txt
fi

# Executar aplicação
echo ""
echo "[INFO] Iniciando aplicação..."
echo "[INFO] Acesse http://localhost:8501 em seu navegador"
echo ""
echo "Pressione Ctrl+C para parar o servidor"
echo ""

streamlit run app.py
