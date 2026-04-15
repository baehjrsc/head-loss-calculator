# -*- coding: utf-8 -*-
"""
Hydraulic Calculations Module
Cálculos de perda de carga usando Hazen-Williams e Darcy-Weisbach
"""

import math
from .materials import MaterialCatalog

class HeadLossCalculator:
    """Calculadora de perda de carga hidráulica"""
    
    # Constantes
    G = 9.81  # aceleração da gravidade (m/s²)
    PI = math.pi
    
    @staticmethod
    def get_flow_velocity(flow_rate, diameter_mm):
        """
        Calcula velocidade do fluxo
        
        Args:
            flow_rate: Vazão em m³/h
            diameter_mm: Diâmetro em mm
            
        Returns:
            Velocidade em m/s
        """
        flow_m3_s = flow_rate / 3600  # Converter m³/h para m³/s
        diameter_m = diameter_mm / 1000  # Converter mm para m
        area = HeadLossCalculator.PI * (diameter_m / 2) ** 2
        velocity = flow_m3_s / area
        return velocity
    
    @staticmethod
    def get_reynolds_number(velocity, diameter_mm, kinematic_viscosity=1.0e-6):
        """
        Calcula número de Reynolds
        
        Args:
            velocity: Velocidade em m/s
            diameter_mm: Diâmetro em mm
            kinematic_viscosity: Viscosidade cinemática em m²/s (água a 20°C = 1.0e-6)
            
        Returns:
            Número de Reynolds (adimensional)
        """
        diameter_m = diameter_mm / 1000
        reynolds = (velocity * diameter_m) / kinematic_viscosity
        return reynolds
    
    @staticmethod
    def get_darcy_friction_factor(reynolds, roughness_mm, diameter_mm):
        """
        Calcula fator de fricção de Darcy usando equação de Colebrook-White
        
        Args:
            reynolds: Número de Reynolds
            roughness_mm: Rugosidade em mm
            diameter_mm: Diâmetro em mm
            
        Returns:
            Fator de fricção de Darcy (f)
        """
        if reynolds < 2300:  # Regime laminar
            return 64 / reynolds
        
        # Regime turbulento - Equação de Colebrook-White (iterativo)
        # Aproximação explícita (Swamee-Jain)
        relative_roughness = roughness_mm / diameter_mm
        
        term1 = relative_roughness / 3.7
        term2 = 5.74 / (reynolds ** 0.9)
        
        f = 0.25 / ((math.log10(term1 + term2)) ** 2)
        return f
    
    @staticmethod
    def calculate_head_loss_darcy_weisbach(flow_rate, diameter_mm, length_m, material_name):
        """
        Calcula perda de carga usando equação de Darcy-Weisbach
        ΔH = f * (L/D) * (V²/2g)
        
        Args:
            flow_rate: Vazão em m³/h
            diameter_mm: Diâmetro em mm
            length_m: Comprimento do trecho em metros
            material_name: Nome do material
            
        Returns:
            Dict com perda de carga em m e outros dados
        """
        # Verificar se material é válido
        if not MaterialCatalog.validate_diameter(material_name, diameter_mm):
            return None
        
        # Calcular velocidade
        velocity = HeadLossCalculator.get_flow_velocity(flow_rate, diameter_mm)
        
        # Verificar se velocidade é válida
        if velocity == 0:
            return {'head_loss_m': 0, 'velocity_ms': 0, 'reynolds': 0, 'friction_factor': 0}
        
        # Calcular Reynolds
        reynolds = HeadLossCalculator.get_reynolds_number(velocity, diameter_mm)
        
        # Obter rugosidade do material
        roughness_mm = MaterialCatalog.get_roughness(material_name)
        
        # Calcular fator de fricção
        friction_factor = HeadLossCalculator.get_darcy_friction_factor(reynolds, roughness_mm, diameter_mm)
        
        # Calcular perda de carga
        diameter_m = diameter_mm / 1000
        head_loss = friction_factor * (length_m / diameter_m) * (velocity ** 2) / (2 * HeadLossCalculator.G)
        
        return {
            'head_loss_m': head_loss,
            'velocity_ms': velocity,
            'reynolds': reynolds,
            'friction_factor': friction_factor,
            'flow_m3_h': flow_rate,
            'diameter_mm': diameter_mm,
            'length_m': length_m,
            'material': material_name
        }
    
    @staticmethod
    def calculate_head_loss_hazen_williams(flow_rate, diameter_mm, length_m, material_name):
        """
        Calcula perda de carga usando equação de Hazen-Williams (simplificada)
        J = 10.643 * Q^1.852 / (C^1.852 * D^4.871)
        
        Args:
            flow_rate: Vazão em m³/h
            diameter_mm: Diâmetro em mm
            length_m: Comprimento do trecho em metros
            material_name: Nome do material
            
        Returns:
            Perda de carga em m
        """
        # Coeficiente de Hazen-Williams por material
        hazen_williams_coefficients = {
            'INOX 316L': 150,
            'PVC-U': 150,
            'PEAD Liso': 150,
            'Ferro Fundido (FF)': 100,
            'PVC Reforçado': 150,
            'PEAD Corrugado': 100
        }
        
        C = hazen_williams_coefficients.get(material_name, 130)
        
        # Converter vazão de m³/h para L/s
        flow_lps = flow_rate * 1000 / 3600
        
        # Converter diâmetro de mm para polegadas (para fórmula tradicional)
        # Aqui usaremos a fórmula em unidades SI adaptada
        D_m = diameter_mm / 1000
        
        # J em m/m (perda unitária)
        J = 10.643 * ((flow_lps ** 1.852) / ((C ** 1.852) * ((D_m * 1000) ** 4.871))) / 1000
        
        # Perda total
        head_loss = J * length_m
        
        velocity = HeadLossCalculator.get_flow_velocity(flow_rate, diameter_mm)
        
        return {
            'head_loss_m': head_loss,
            'velocity_ms': velocity,
            'method': 'Hazen-Williams',
            'C_coefficient': C,
            'J_unitaria': J,
            'flow_m3_h': flow_rate,
            'diameter_mm': diameter_mm,
            'length_m': length_m,
            'material': material_name
        }
    
    @staticmethod
    def calculate_total_head_loss(segments):
        """
        Calcula perda de carga total para múltiplos trechos
        
        Args:
            segments: Lista de dicts com dados de cada trecho
            
        Returns:
            Perda de carga total em metros
        """
        total_loss = 0
        for segment in segments:
            loss = HeadLossCalculator.calculate_head_loss_darcy_weisbach(
                segment['flow_rate'],
                segment['diameter'],
                segment['length'],
                segment['material']
            )
            if loss:
                total_loss += loss['head_loss_m']
        return total_loss
