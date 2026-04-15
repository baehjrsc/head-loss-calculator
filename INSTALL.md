# Guia de Instalação e Uso

## 🚀 Instalação Local

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### Passos

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/head-loss-calculator.git
   cd head_loss_calculator
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**
   ```bash
   streamlit run app.py
   ```

   A aplicação abrirá automaticamente em `http://localhost:8501`

## 🌐 Hospedagem Online (Streamlit Cloud)

### Passos para Deploy

1. **Push para GitHub**
   - Crie um repositório GitHub privado ou público
   - Faça push de todos os arquivos

2. **Deploy no Streamlit Cloud**
   - Acesse [streamlit.io/cloud](https://streamlit.io/cloud)
   - Clique em "New app"
   - Selecione seu repositório, branch e arquivo principal (`app.py`)
   - Clique em "Deploy"

3. **Link compartilhável**
   - Sua aplicação terá um URL tipo: `https://seu-app.streamlit.app`

## 📋 Funcionalidades

### Cálculo Principal
- ✅ Múltiplos trechos com diferentes DN e materiais
- ✅ Cálculos de perda de carga (Darcy-Weisbach)
- ✅ Suporte a diversos materiais (INOX, PVC, PEAD, FF)
- ✅ Cálculo de número de Reynolds e fator de fricção

### Perdas Localizadas
- ✅ Curvas, tés, válvulas, medidores
- ✅ Controles dinâmicos (+/-)
- ✅ Cálculo automático de perda total

### Validações
- ✅ Velocidades recomendadas
- ✅ Perda de carga limite
- ✅ Validação de linha piezométrica
- ✅ Recomendações automáticas

### Gráficos
- ✅ Perda de carga por trecho
- ✅ Velocidade por trecho
- ✅ Linha piezométrica

### Relatórios
- ✅ Geração de Excel automático
- ✅ Sumário completo do dimensionamento
- ✅ Pronto para colar em relatórios

## 🛠️ Estrutura do Projeto

```
head_loss_calculator/
├── app.py                      # Aplicação Streamlit principal
├── modules/
│   ├── __init__.py
│   ├── calculations.py         # Cálculos hidráulicos
│   ├── materials.py            # Catálogos de materiais
│   ├── validators.py           # Validação de normas
│   ├── losses.py               # Perdas localizadas
│   └── reports.py              # Geração de relatórios
├── .streamlit/
│   └── config.toml             # Configurações do Streamlit
├── requirements.txt
├── .gitignore
├── setup.cfg
└── README.md
```

## 📚 Catálogos de Materiais

### INOX 316L
- **Fornecedor:** Saint Gobain
- **Rugosidade:** 0.015 mm
- **Diâmetros:** 16-315 mm
- **Uso:** Ambientes agressivos

### PVC-U
- **Fornecedor:** Politejo, Tigre
- **Rugosidade:** 0.007 mm
- **Diâmetros:** 16-400 mm
- **Uso:** Geral, melhor custo-benefício

### PEAD Liso
- **Fornecedor:** Tigre, Politejo
- **Rugosidade:** 0.001 mm
- **Diâmetros:** 16-630 mm
- **Uso:** Drenagem, flexível, baixa perda

### Ferro Fundido
- **Fornecedor:** Diversas
- **Rugosidade:** 0.25 mm
- **Diâmetros:** 50-600 mm
- **Uso:** Aplicações robustas

## 📖 Normas de Referência

- **Eurocódigos** (EN normas)
- **Boas práticas de hidráulica**
- **Normas de tratamento de água**

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install streamlit
```

### Erro ao gerar Excel
- Certifique-se que tem permissão de escrita na pasta Downloads
- Verifique se openpyxl está instalado: `pip install openpyxl`

### Aplicação lenta
- Reduz número de trechos
- Limpa cache do navegador
- Reinicia o servidor Streamlit

## 🔄 Atualizações

Para atualizar o projeto com novos recursos:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## 📧 Suporte

Para relatórios de bugs ou sugestões, crie uma issue no GitHub.

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para detalhes.

---

**Desenvolvido com ❤️ usando Python e Streamlit**
