# -*- coding: utf-8 -*-
"""
Material Catalog Module - Catálogos de materiais de tubulação
Fornecedores: Saint Gobain, Politejo, Tigre e outros
"""

class MaterialCatalog:
    """Catálogo de materiais de tubulação reconhecidos"""
    
    MATERIALS = {
        'INOX 316L': {
            'roughness': 0.015,  # mm
            'description': 'Aço Inoxidável 316L (Saint Gobain)',
            'supplier': 'Saint Gobain',
            'diameters': [16, 20, 25, 32, 40, 50, 63, 75, 90, 110, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1200],
            'color': '#C0C0C0',
            'notes': 'Alta resistência à corrosão, uso em ambientes agressivos',
            'cost_factor': 3.5
        },
        'PVC-U': {
            'roughness': 0.007,  # mm
            'description': 'PVC-U (Politejo, Tigre)',
            'supplier': 'Politejo / Tigre',
            'diameters': [16, 20, 25, 32, 40, 50, 63, 75, 90, 110, 160, 200, 250, 315, 400, 500, 630, 800],
            'color': '#E8E8E8',
            'notes': 'Material mais econômico, bom custo-benefício',
            'cost_factor': 1.0
        },
        'PEAD Liso': {
            'roughness': 0.001,  # mm
            'description': 'Polietileno de Alta Densidade - Liso (Tigre, Politejo)',
            'supplier': 'Tigre / Politejo',
            'diameters': [16, 20, 25, 32, 40, 50, 63, 75, 90, 110, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1200],
            'color': '#000000',
            'notes': 'Excelente custo, baixa perda de carga, flexível',
            'cost_factor': 1.2
        },
        'Ferro Fundido (FF)': {
            'roughness': 0.25,  # mm
            'description': 'Ferro Fundido Cinzento (Fundições tradicionais)',
            'supplier': 'Diversas',
            'diameters': [50, 75, 100, 150, 200, 250, 300, 400, 500, 600, 800, 1000, 1200],
            'color': '#4B4B4B',
            'notes': 'Durável, resistente, maior perda de carga com tempo',
            'cost_factor': 2.0
        },
        'PVC Reforçado': {
            'roughness': 0.010,  # mm
            'description': 'PVC-O Reforçado (Tigre Azulão)',
            'supplier': 'Tigre',
            'diameters': [50, 75, 100, 150, 200, 250, 300, 400, 500, 630, 800],
            'color': '#1E90FF',
            'notes': 'Maior resistência à pressão que PVC-U',
            'cost_factor': 1.5
        }
    }
    
    @staticmethod
    def get_material(material_name):
        """Retorna dados do material"""
        return MaterialCatalog.MATERIALS.get(material_name)
    
    @staticmethod
    def get_roughness(material_name):
        """Retorna rugosidade em mm"""
        material = MaterialCatalog.MATERIALS.get(material_name)
        return material['roughness'] if material else 0.015
    
    @staticmethod
    def get_available_materials():
        """Retorna lista de materiais disponíveis"""
        return list(MaterialCatalog.MATERIALS.keys())
    
    @staticmethod
    def get_available_diameters(material_name):
        """Retorna diâmetros disponíveis para um material"""
        material = MaterialCatalog.MATERIALS.get(material_name)
        return material['diameters'] if material else []
    
    @staticmethod
    def validate_diameter(material_name, diameter):
        """Verifica se o diâmetro existe para o material"""
        available_diameters = MaterialCatalog.get_available_diameters(material_name)
        return diameter in available_diameters
    
    @staticmethod
    def get_material_info(material_name):
        """Retorna informações completas do material"""
        return MaterialCatalog.MATERIALS.get(material_name, {})
