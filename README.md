# Head Loss Calculator - ETAR/ETE/WTP

Aplicação web para cálculo de perda de carga hidráulica em sistemas de tratamento de água (ETAR/ETE/WTP).

## Características

✅ **Cálculo de Perda de Carga (Hazen-Williams e Darcy-Weisbach)**
- Suporte a múltiplos materiais de tubo
- Múltiplos trechos com configurações diferentes

✅ **Catálogos de Materiais Reconhecidos**
- INOX 316L (Saint Gobain)
- PVC-U (Politejo, Tigre)
- PEAD Liso
- Ferro Fundido

✅ **Validação Hidráulica**
- Verificação contra Eurocódigos
- Boas práticas de hidráulica
- Velocidades recomendadas
- Perda de carga limite

✅ **Perdas Localizadas**
- Curvas, tês, válvulas
- Controles dinâmicos de quantidade
- Coeficientes de perda padronizados

✅ **Relatórios**
- Geração automática de planilha Excel
- Resumo de dimensionamento
- Pronto para incluir em relatórios

## Instalação

```bash
pip install -r requirements.txt
```

## Executar Localmente

```bash
streamlit run app.py
```

## Hospedagem Online

Este projeto pode ser hospedado gratuitamente no Streamlit Cloud:

1. Fazer push para GitHub
2. Conectar repositório no [Streamlit Cloud](https://streamlit.io/cloud)
3. A aplicação será acessível online automaticamente

## Estrutura do Projeto

```
head_loss_calculator/
├── app.py                      # Aplicação principal Streamlit
├── modules/
│   ├── calculations.py         # Cálculos hidráulicos
│   ├── materials.py            # Catálogos de materiais
│   ├── validators.py           # Validação de normas
│   ├── losses.py               # Perdas localizadas
│   └── reports.py              # Geração de relatórios
├── data/
│   └── catalogs.json           # Catálogos de materiais
├── requirements.txt
└── README.md
```

## Autor

Desenvolvido com Python e Streamlit

## Licença

MIT
