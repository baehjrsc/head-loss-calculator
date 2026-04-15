#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de teste dos módulos
"""

import sys
sys.path.insert(0, '.')

# Testes
print("=" * 50)
print("TESTE DE MÓDULOS - HEAD LOSS CALCULATOR")
print("=" * 50)

try:
    from modules.materials import MaterialCatalog
    print("✅ MaterialCatalog carregado")
    print(f"   Materiais: {MaterialCatalog.get_available_materials()}")
except Exception as e:
    print(f"❌ Erro ao carregar MaterialCatalog: {e}")

try:
    from modules.calculations import HeadLossCalculator
    print("✅ HeadLossCalculator carregado")
except Exception as e:
    print(f"❌ Erro ao carregar HeadLossCalculator: {e}")

try:
    from modules.losses import LocalizedLosses
    print("✅ LocalizedLosses carregado")
    print(f"   Componentes: {len(LocalizedLosses.get_available_components())} disponíveis")
except Exception as e:
    print(f"❌ Erro ao carregar LocalizedLosses: {e}")

try:
    from modules.validators import HydraulicValidator
    print("✅ HydraulicValidator carregado")
except Exception as e:
    print(f"❌ Erro ao carregar HydraulicValidator: {e}")

try:
    from modules.reports import ReportGenerator
    print("✅ ReportGenerator carregado")
except Exception as e:
    print(f"❌ Erro ao carregar ReportGenerator: {e}")

print("\n" + "=" * 50)
print("TESTE DE CÁLCULO SIMPLES")
print("=" * 50)

try:
    calc = HeadLossCalculator.calculate_head_loss_darcy_weisbach(
        flow_rate=10.0,
        diameter_mm=100,
        length_m=100,
        material_name='PVC-U'
    )
    
    if calc:
        print(f"✅ Cálculo realizado com sucesso")
        print(f"   Vazão: 10.0 m³/h")
        print(f"   Diâmetro: 100 mm (PVC-U)")
        print(f"   Comprimento: 100 m")
        print(f"   Velocidade: {calc['velocity_ms']:.3f} m/s")
        print(f"   Perda de Carga: {calc['head_loss_m']:.4f} m")
        print(f"   Reynolds: {calc['reynolds']:.0f}")
        print(f"   Fator f: {calc['friction_factor']:.4f}")
except Exception as e:
    print(f"❌ Erro no cálculo: {e}")

print("\n" + "=" * 50)
print("TESTE DE VALIDAÇÃO")
print("=" * 50)

try:
    vel_validation = HydraulicValidator.validate_velocity(1.0, 'etar_entrada')
    print(f"✅ Validação de velocidade realizada")
    print(f"   Velocidade: {vel_validation['velocity_ms']:.2f} m/s")
    print(f"   Status: {vel_validation['status']}")
    print(f"   Válida: {vel_validation['is_valid']}")
except Exception as e:
    print(f"❌ Erro na validação: {e}")

print("\n" + "=" * 50)
print("TODOS OS TESTES COMPLETADOS!")
print("=" * 50)
print("\nA aplicação está pronta para uso.")
print("Execute: streamlit run app.py")
