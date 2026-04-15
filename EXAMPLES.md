# Exemplos de Uso - Head Loss Calculator

## Exemplo 1: Cálculo Simples de Perda de Carga

```python
from modules.calculations import HeadLossCalculator

# Dados de entrada
flow_rate = 10.0  # m³/h
diameter = 100    # mm (PVC-U)
length = 100      # metros
material = 'PVC-U'

# Calcular perda de carga
result = HeadLossCalculator.calculate_head_loss_darcy_weisbach(
    flow_rate, diameter, length, material
)

print(f"Perda de Carga: {result['head_loss_m']:.4f} m")
print(f"Velocidade: {result['velocity_ms']:.3f} m/s")
print(f"Reynolds: {result['reynolds']:.0f}")
```

## Exemplo 2: Validar Velocidade

```python
from modules.validators import HydraulicValidator

velocity = 1.0  # m/s
system = 'etar_entrada'

validation = HydraulicValidator.validate_velocity(velocity, system)

print(f"Status: {validation['status']}")
print(f"Válida: {validation['is_valid']}")
print(f"Recomendações: {validation['recommendations']}")
```

## Exemplo 3: Calcular Perdas Localizadas

```python
from modules.losses import LocalizedLosses

# Definir componentes
components = {
    'Curva 90°': 2,
    'Tê (fluxo principal)': 1,
    'Válvula de gaveta': 1
}

velocity = 1.0  # m/s

# Calcular perdas
losses = LocalizedLosses.calculate_total_localized_losses(velocity, components)

print(f"K Total: {losses['total_K']:.2f}")
print(f"Perda Total: {losses['total_head_loss_m']:.4f} m")
```

## Exemplo 4: Múltiplos Trechos

```python
from modules.calculations import HeadLossCalculator

segments = [
    {'flow_rate': 10, 'diameter': 100, 'length': 50, 'material': 'PVC-U'},
    {'flow_rate': 10, 'diameter': 75, 'length': 100, 'material': 'INOX 316L'},
    {'flow_rate': 10, 'diameter': 50, 'length': 75, 'material': 'PEAD Liso'}
]

total_loss = 0
for segment in segments:
    result = HeadLossCalculator.calculate_head_loss_darcy_weisbach(
        segment['flow_rate'],
        segment['diameter'],
        segment['length'],
        segment['material']
    )
    total_loss += result['head_loss_m']
    print(f"Trecho: {result['head_loss_m']:.4f} m")

print(f"Perda Total: {total_loss:.4f} m")
```

## Exemplo 5: Catálogo de Materiais

```python
from modules.materials import MaterialCatalog

# Listar todos os materiais
materials = MaterialCatalog.get_available_materials()
print(f"Materiais disponíveis: {materials}")

# Obter diâmetros para um material
pvc_diameters = MaterialCatalog.get_available_diameters('PVC-U')
print(f"Diâmetros PVC-U: {pvc_diameters}")

# Obter informações completas
inox_info = MaterialCatalog.get_material_info('INOX 316L')
print(f"Rugosidade INOX: {inox_info['roughness']} mm")
print(f"Fornecedor: {inox_info['supplier']}")
```

## Exemplo 6: Validação Completa

```python
from modules.validators import HydraulicValidator

# Dados
flow_rate = 10
diameter = 100
length = 100
velocity = 1.0
head_loss = 0.05
piezometric_up = 10
piezometric_down = 5

# Validação completa
validation = HydraulicValidator.full_validation(
    flow_rate, diameter, length, velocity,
    head_loss, piezometric_up, piezometric_down,
    system_type='etar_entrada'
)

print(f"Velocidade: {validation['velocity']['status']}")
print(f"Perda de Carga: {validation['head_loss']['status']}")
print(f"Linha Piezométrica: {validation['piezometric']['status']}")
```

## Exemplo 7: Usando a Interface Streamlit

1. **Instalação:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Execução:**
   ```bash
   streamlit run app.py
   ```

3. **Interface:**
   - Configure o número de trechos na barra lateral
   - Defina vazão, cotas e tipo de sistema
   - Selecione materiais e diâmetros para cada trecho
   - Clique em "CALCULAR" para obter resultados
   - Configure perdas localizadas na aba "Perdas Localizadas"
   - Verifique as validações na aba "Validações"
   - Gere relatório em Excel na aba "Relatório"

## Exemplo 8: Comparar Materiais

```python
from modules.calculations import HeadLossCalculator
from modules.materials import MaterialCatalog

# Parâmetros fixos
flow_rate = 10
diameter = 100
length = 100

materials = MaterialCatalog.get_available_materials()

print("Comparação de Materiais")
print("-" * 50)

for material in materials:
    if MaterialCatalog.validate_diameter(material, diameter):
        result = HeadLossCalculator.calculate_head_loss_darcy_weisbach(
            flow_rate, diameter, length, material
        )
        print(f"{material:20s} → {result['head_loss_m']:.4f} m")
```

## Exemplo 9: Gerar Relatório

```python
from modules.reports import ReportGenerator
from modules.calculations import HeadLossCalculator
from modules.validators import HydraulicValidator

# Preparar dados
project_data = {
    'project_name': 'ETE Exemplo',
    'flow_rate': 10,
    'segments': [
        {'name': 'Trecho A', 'material': 'PVC-U', 'diameter': 100, 'length': 100}
    ]
}

calculations = {
    'total_head_loss': 0.05,
    'segments': [...]
}

validations = {
    'velocity': {...},
    'head_loss': {...},
    'margin': 4.95
}

# Gerar Excel
ReportGenerator.create_excel_report(
    'relatorio.xlsx',
    project_data,
    calculations,
    validations
)
```

---

Para mais informações, consulte a documentação completa em README.md
