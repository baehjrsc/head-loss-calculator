# Guia de Deployment - GitHub e Streamlit Cloud

## 🚀 Parte 1: Preparar o Repositório Git

### 1.1 Inicializar Git Localmente

```bash
cd head_loss_calculator
git init
git config user.name "Seu Nome"
git config user.email "seu.email@example.com"
```

### 1.2 Criar .gitignore (já existe)

Certifique-se que o arquivo `.gitignore` contém:
```
__pycache__/
*.pyc
.streamlit/
venv/
*.xlsx
```

### 1.3 Fazer Commit Inicial

```bash
git add .
git commit -m "Initial commit: Head Loss Calculator v1.0"
```

## 🔗 Parte 2: Criar Repositório no GitHub

### 2.1 Criar Novo Repositório

1. Acesse [github.com](https://github.com)
2. Faça login com sua conta
3. Clique no ícone **+** (canto superior direito)
4. Selecione **New repository**

### 2.2 Configurar Repositório

- **Repository name:** `head-loss-calculator`
- **Description:** "Aplicação web para cálculo de perda de carga em sistemas ETAR/ETE/WTP"
- **Visibility:** Public (para usar Streamlit Cloud gratuitamente)
- **Initialize:** Deixe desmarcado

### 2.3 Fazer Push para GitHub

```bash
git remote add origin https://github.com/seu-usuario/head-loss-calculator.git
git branch -M main
git push -u origin main
```

**Nota:** Substitua `seu-usuario` pelo seu nome de usuário do GitHub.

## 🌐 Parte 3: Deploy no Streamlit Cloud

### 3.1 Acessar Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Clique em **Sign up** ou **Sign in**
3. Use sua conta GitHub para autenticar

### 3.2 Deploy da Aplicação

1. Clique em **New app**
2. Preencha os campos:
   - **Repository:** seu-usuario/head-loss-calculator
   - **Branch:** main
   - **Main file path:** app.py
3. Clique em **Deploy**

### 3.3 Configurações Adicionais (Opcional)

No painel de settings do Streamlit Cloud:

```
Advanced settings:
- Python version: 3.9+
- Client error details: Enabled
- Logger message level: Warning
```

## 📋 Parte 4: Verificar Deploy

- Aguarde 2-5 minutos para o deploy completar
- Você receberá um URL tipo: `https://head-loss-calculator.streamlit.app`
- Teste a aplicação com dados de exemplo

## 🔄 Parte 5: Atualizações Futuras

### Fazer Alterações Locais

```bash
# Fazer mudanças nos arquivos

# Testar localmente
streamlit run app.py

# Commit e push
git add .
git commit -m "Descrição das alterações"
git push origin main
```

### Deploy Automático

O Streamlit Cloud detectará o push automaticamente e fará redeploy.

## 🛡️ Boas Práticas

### Segurança

1. **Nunca commitar credenciais** (senhas, tokens, etc.)
2. **Usar variáveis de ambiente** para dados sensíveis

Exemplo de `.streamlit/secrets.toml` (não fazer commit):
```toml
[database]
url = "sua-url-secreta"
password = "sua-senha"
```

### Performance

1. Usar `@st.cache_data` para dados que não mudam
2. Usar `@st.cache_resource` para recursos pesados
3. Limitar uploads de arquivo

### Monitoramento

- Verificar logs no painel do Streamlit Cloud
- Usar `st.write()` para debug
- Implementar tratamento de erros

## 📦 Parte 6: Estrutura Final do Repositório

```
head-loss-calculator/
├── .github/
│   └── workflows/  (CI/CD opcional)
├── modules/
│   ├── __init__.py
│   ├── calculations.py
│   ├── materials.py
│   ├── validators.py
│   ├── losses.py
│   └── reports.py
├── .streamlit/
│   └── config.toml
├── .gitignore
├── app.py
├── requirements.txt
├── README.md
├── INSTALL.md
├── EXAMPLES.md
├── DEPLOY.md  (este arquivo)
├── setup.cfg
├── test_modules.py
├── run.bat
├── run.sh
└── LICENSE
```

## 🔧 Troubleshooting

### Erro: "ModuleNotFoundError"
- Verifique se `requirements.txt` está atualizado
- Confirme que `app.py` importa corretamente

### Erro: "Timeout"
- Reduza tamanho de cálculos
- Implementar cache com `@st.cache_data`

### Erro: "Memory exceeded"
- Limpar cache local
- Usar variáveis mais eficientes

### Deploy não atualiza
- Esperar alguns minutos
- Fazer refresh manual no painel
- Verificar se push foi bem-sucedido: `git log`

## 📚 Recursos Adicionais

- [Streamlit Documentation](https://docs.streamlit.io)
- [GitHub Getting Started](https://docs.github.com/en/get-started)
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-cloud)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

## 🤝 Compartilhando com Outros

### URL Pública

Após deploy, compartilhe o link:
```
https://seu-usuario-head-loss-calculator.streamlit.app
```

### README no GitHub

Certifique-se que seu README.md inclui:
- ✅ Descrição clara
- ✅ Links de demo/live
- ✅ Instruções de instalação
- ✅ Exemplos de uso
- ✅ Licença
- ✅ Contato para suporte

## 📈 Próximas Melhorias

Depois de fazer deploy, considere:

1. **Adicionar testes automatizados** (pytest)
2. **CI/CD pipeline** (GitHub Actions)
3. **Documentação expandida** (Sphinx)
4. **Histórico de cálculos** (SQLite)
5. **Multi-idioma** (i18n)
6. **API REST** (FastAPI)
7. **Docker container**
8. **Análise de dados** (analytics)

---

**Parabéns!** Sua aplicação está online e acessível ao mundo! 🎉
