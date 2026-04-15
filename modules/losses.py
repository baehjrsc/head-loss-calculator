# -*- coding: utf-8 -*-
"""
Localized Losses Module - Perdas localizadas (curvas, tés, válvulas, etc)
"""

class LocalizedLosses:
    """Cálculo de perdas localizadas em componentes"""
    
    COMPONENTS = {
        'Curva 90°': {
            'K': 0.9,
            'description': 'Curva de 90 graus',
            'notes': 'Coeficiente médio'
        },
        'Curva 45°': {
            'K': 0.4,
            'description': 'Curva de 45 graus',
            'notes': 'Coeficiente reduzido'
        },
        'Tê (fluxo principal)': {
            'K': 0.6,
            'description': 'Tê sem desvio de fluxo',
            'notes': 'Fluxo passa reto'
        },
        'Tê (90° derivação)': {
            'K': 1.3,
            'description': 'Tê com derivação a 90°',
            'notes': 'Fluxo em T'
        },
        'Válvula de gaveta': {
            'K': 0.2,
            'description': 'Válvula de gaveta (aberta)',
            'notes': 'Abertura total'
        },
        'Válvula de esfera': {
            'K': 0.05,
            'description': 'Válvula de esfera (aberta)',
            'notes': 'Perda mínima, abertura total'
        },
        'Válvula de retenção': {
            'K': 2.0,
            'description': 'Válvula de retenção (gaveta)',
            'notes': 'Bidimensional'
        },
        'Válvula borboleta': {
            'K': 0.3,
            'description': 'Válvula borboleta (aberta)',
            'notes': 'Perda reduzida'
        },
        'Redução gradual': {
            'K': 0.1,
            'description': 'Redução gradual de diâmetro',
            'notes': 'Bem dimensionada'
        },
        'Ampliação gradual': {
            'K': 0.3,
            'description': 'Ampliação gradual de diâmetro',
            'notes': 'Recuperação de pressão'
        },
        'Entrada de canalização': {
            'K': 0.5,
            'description': 'Entrada de canalização',
            'notes': 'Borda viva'
        },
        'Saída de canalização': {
            'K': 1.0,
            'description': 'Saída de canalização',
            'notes': 'Perda total de carga'
        },
        'Medidor de vazão': {
            'K': 5.0,
            'description': 'Medidor de vazão (turbina)',
            'notes': 'Valores típicos variam'
        },
        'Filtro (limpo)': {
            'K': 0.5,
            'description': 'Filtro em bom estado',
            'notes': 'Pressão diferencial baixa'
        },
        'Filtro (sujo)': {
            'K': 3.0,
            'description': 'Filtro necessitando limpeza',
            'notes': 'Pressão diferencial elevada'
        }
    }
    
    @staticmethod
    def get_component(component_name):
        """Retorna dados do componente"""
        return LocalizedLosses.COMPONENTS.get(component_name)
    
    @staticmethod
    def get_available_components():
        """Retorna lista de componentes disponíveis"""
        return list(LocalizedLosses.COMPONENTS.keys())
    
    @staticmethod
    def calculate_localized_loss(velocity_ms, K_coefficient):
        """
        Calcula perda de carga localizada
        hL = K * V²/(2g)
        
        Args:
            velocity_ms: Velocidade em m/s
            K_coefficient: Coeficiente de perda (K)
            
        Returns:
            Perda de carga localizada em metros
        """
        G = 9.81
        head_loss = K_coefficient * (velocity_ms ** 2) / (2 * G)
        return head_loss
    
    @staticmethod
    def calculate_total_localized_losses(velocity_ms, components_dict):
        """
        Calcula perda de carga total de perdas localizadas
        
        Args:
            velocity_ms: Velocidade em m/s
            components_dict: Dicionário {nome_componente: quantidade}
            
        Returns:
            Perda total e detalhamento
        """
        total_K = 0
        details = []
        
        for component_name, quantity in components_dict.items():
            if quantity > 0:
                component = LocalizedLosses.get_component(component_name)
                if component:
                    K = component['K'] * quantity
                    total_K += K
                    details.append({
                        'component': component_name,
                        'quantity': quantity,
                        'K_unit': component['K'],
                        'K_total': K,
                        'head_loss_m': LocalizedLosses.calculate_localized_loss(velocity_ms, K)
                    })
        
        total_head_loss = LocalizedLosses.calculate_localized_loss(velocity_ms, total_K)
        
        return {
            'total_K': total_K,
            'total_head_loss_m': total_head_loss,
            'details': details
        }
    
    @staticmethod
    def estimate_K_coefficient(components_list):
        """Estima K total a partir de lista de componentes"""
        total_K = sum(LocalizedLosses.get_component(comp)['K'] for comp in components_list)
        return total_K
