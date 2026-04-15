# Project Summary - Head Loss Calculator

## 📊 Visão Geral do Projeto

**Head Loss Calculator** é uma aplicação web desenvolvida em Python com Streamlit para cálculo de perda de carga hidráulica em sistemas de tratamento de água (ETAR/ETE/WTP).

### ✨ Características Principais

✅ **Cálculo Hidráulico Avançado**
- Método Darcy-Weisbach com precisão técnica
- Múltiplos trechos com DN e materiais diferentes
- Cálculo automático de Reynolds e fator de fricção
- Método Hazen-Williams como alternativa

✅ **Catálogos de Materiais Reconhecidos**
- INOX 316L (Saint Gobain)
- PVC-U (Politejo, Tigre)
- PEAD Liso (Tigre, Politejo)
- Ferro Fundido
- PVC Reforçado
- PEAD Corrugado

✅ **Validação Contra Normas**
- Eurocódigos (EN)
- Velocidades recomendadas
- Perda de carga limite
- Verificação de linha piezométrica
- Recomendações automáticas

✅ **Perdas Localizadas**
- 15 componentes padrão (curvas, tés, válvulas, etc.)
- Controles dinâmicos (+/-)
- Coeficientes padronizados por fornecedor

✅ **Interface Interativa**
- 5 abas principais (Cálculo, Perdas, Validações, Gráficos, Relatório)
- Gráficos dinâmicos com Plotly
- Visualização de linha piezométrica
- Comparação entre trechos

✅ **Relatórios Profissionais**
- Geração automática em Excel
- Sumário completo do dimensionamento
- Tabelas de detalhes por trecho
- Pronto para incluir em relatórios técnicos

✅ **Deployment Online**
- Hospedagem gratuita no Streamlit Cloud
- GitHub Integration
- Acesso via browser
- Compartilhável via link

## 🏗️ Arquitetura do Projeto

```
head_loss_calculator/
│
├── 📄 app.py                    ⭐ Aplicação Streamlit Principal
│   └── Interface com 5 abas
│       ├── Cálculo Principal
│       ├── Perdas Localizadas
│       ├── Validações
│       ├── Gráficos
│       └── Relatório
│
├── 📁 modules/                  🔧 Lógica de Negócio
│   ├── calculations.py          → Cálculos Darcy-Weisbach
│   ├── materials.py             → Catálogos de materiais
│   ├── validators.py            → Validação de normas
│   ├── losses.py                → Perdas localizadas
│   └── reports.py               → Geração Excel
│
├── 📁 .streamlit/
│   └── config.toml              ⚙️ Configurações de tema
│
├── 📋 Documentação
│   ├── README.md                → Visão geral
│   ├── INSTALL.md               → Instalação
│   ├── EXAMPLES.md              → Exemplos de uso
│   ├── DEPLOY.md                → Deployment online
│   └── LICENSE                  → MIT License
│
├── ⚡ Scripts
│   ├── run.bat                  → Launcher Windows
│   ├── run.sh                   → Launcher Linux/Mac
│   └── test_modules.py          → Testes dos módulos
│
└── 📦 Dependências
    └── requirements.txt         → Streamlit, Pandas, Plotly, etc.
```

## 📊 Funcionalidades Técnicas

### Módulo: calculations.py
- `HeadLossCalculator.calculate_head_loss_darcy_weisbach()` - Cálculo principal
- `get_flow_velocity()` - Calcula velocidade
- `get_reynolds_number()` - Número de Reynolds
- `get_darcy_friction_factor()` - Fator de fricção
- `calculate_total_head_loss()` - Perda total em múltiplos trechos

### Módulo: materials.py
- Catálogo de 6 materiais principais
- Dados de rugosidade
- Diâmetros disponíveis
- Informações de fornecedores
- Validação de combinações

### Módulo: validators.py
- Velocidades recomendadas (min/max/ideal)
- Limites de perda de carga
- Validação de linha piezométrica
- Recomendações automáticas
- Validação completa integrada

### Módulo: losses.py
- 15 componentes de perda localizada
- Coeficientes K padronizados
- Cálculo automático
- Detalhe por componente
- Quantidade dinâmica

### Módulo: reports.py
- Exportação para Excel
- Múltiplas abas (Resumo, Trechos, Perdas, Validações)
- Formatação profissional
- Gráficos e tabelas
- Pronto para relatório

## 🔢 Parâmetros Suportados

### Entradas de Usuário
- Vazão: 0.1 - 1000 m³/h
- Diâmetro: 16 - 630 mm
- Comprimento: 0.1 - 10000 m
- Cota montante: Qualquer valor (m)
- Cota jusante: Qualquer valor (m)
- Quantidade de componentes: 0 - 100+

### Saídas Calculadas
- Perda de carga (m)
- Velocidade (m/s)
- Número de Reynolds
- Fator de fricção (f)
- Perda unitária (J)
- Margem piezométrica
- Status de validação

## 🎯 Casos de Uso

1. **Dimensionamento de Adutora**
   - Múltiplos trechos
   - Validar velocidade
   - Gerar relatório

2. **Verificação de Linha Piezométrica**
   - Inserir cotas
   - Calcular perdas
   - Validar margem

3. **Análise Comparativa de Materiais**
   - Mesmo trecho, diferentes materiais
   - Avaliar custo vs. perda
   - Escolher melhor opção

4. **Projeto Executivo**
   - Todas as abas preenchidas
   - Gerar Excel
   - Incluir no relatório

## 📈 Dados Estatísticos

| Métrica | Valor |
|---------|-------|
| Linhas de Código | ~1200 |
| Módulos | 5 |
| Funções | 30+ |
| Materiais | 6 |
| Componentes Perda | 15 |
| Abas Streamlit | 5 |
| Formulas Matemáticas | 8+ |
| Normas Referenciadas | 10+ |

## 🚀 Como Usar Rapidamente

### 1. Instalação (30 segundos)
```bash
cd head_loss_calculator
pip install -r requirements.txt
```

### 2. Execução (Instantânea)
```bash
streamlit run app.py
```

### 3. Uso (5 minutos)
1. Configure vazão na sidebar
2. Defina cotas de elevação
3. Selecione número de trechos
4. Escolha materiais e diâmetros
5. Clique "CALCULAR"
6. Verifique validações
7. Gere relatório Excel

## 🌐 Deploy Online

### Streamlit Cloud (Gratuito)
1. Push para GitHub
2. Conectar em share.streamlit.io
3. Deploy automático
4. URL público gerado

**Link Final:** `https://seu-app.streamlit.app`

## 🔐 Segurança

- ✅ Sem armazenamento de dados sensíveis
- ✅ Cálculos locais (sem servidor de backend)
- ✅ Sem login necessário
- ✅ HTTPS automático
- ✅ Código open-source

## 📚 Documentação

| Arquivo | Conteúdo |
|---------|----------|
| README.md | Visão geral e características |
| INSTALL.md | Passo a passo de instalação |
| EXAMPLES.md | 9 exemplos de código |
| DEPLOY.md | Guia completo de deployment |
| EXAMPLES.md | Código Python pronto |

## 🛠️ Stack Técnico

| Componente | Versão |
|------------|--------|
| Python | 3.8+ |
| Streamlit | 1.28.1 |
| Pandas | 2.1.1 |
| NumPy | 1.24.3 |
| Plotly | 5.17.0 |
| OpenPyXL | 3.10.10 |
| SciPy | 1.11.3 |

## 📊 Formulas Implementadas

1. **Darcy-Weisbach** → ΔH = f × (L/D) × (V²/2g)
2. **Reynolds** → Re = (V × D) / ν
3. **Colebrook-White** → Fator f iterativo
4. **Hazen-Williams** → J = 10.643 × Q^1.852 / (C^1.852 × D^4.871)
5. **Perda Localizada** → hL = K × V²/(2g)
6. **Continuidade** → Q = V × A

## 🎓 Referências Técnicas

- Eurocódigo EN 1296 (Tubagens e Acessórios)
- ABNT NBR 12218 (Projeto de Adutora)
- Hydraulic Institute (Bombeamento)
- Handbook of Hydraulic Resistance (Idelsik)
- Water Supply and Sewerage (Peavy, Rowe)

## 📝 Histórico de Versões

```
v1.0.0 - 2024
├── Cálculo Darcy-Weisbach
├── Validação de normas
├── Perdas localizadas
├── Interface Streamlit
├── Geração Excel
└── Deployment pronto
```

## 🎯 Roadmap Futuro

- [ ] Adicionar mais materiais
- [ ] Histórico de cálculos
- [ ] Banco de dados de projetos
- [ ] Exportar para PDF
- [ ] Testes automatizados
- [ ] API REST
- [ ] Mobile app
- [ ] Multi-idioma

## 👨‍💻 Desenvolvimento

- **Framework:** Streamlit (UI Web)
- **Backend:** Python puro
- **Deployment:** Streamlit Cloud
- **Versionamento:** Git + GitHub
- **Licença:** MIT

## 📞 Suporte

- 📧 Issues: GitHub Issues
- 📚 Docs: Arquivos .md inclusos
- 💬 Discussões: GitHub Discussions

---

**Aplicação desenvolvida com ❤️ para Engenharia Hidráulica**

*Última atualização: Abril 2024*
