# -*- coding: utf-8 -*-
"""
Validators Module - Validação contra normas e boas práticas
Eurocódigos e normas de hidráulica
"""

class HydraulicValidator:
    """Validador de parâmetros hidráulicos contra normas"""
    
    # Velocidades recomendadas por tipo de sistema (m/s)
    VELOCITY_LIMITS = {
        'tubulacao_pressao_agua': {'min': 0.6, 'max': 2.0, 'recomendado': 1.0},
        'tubulacao_drenagem': {'min': 0.3, 'max': 1.5, 'recomendado': 0.75},
        'etar_entrada': {'min': 0.3, 'max': 1.2, 'recomendado': 0.6},
        'etar_saida': {'min': 0.3, 'max': 1.5, 'recomendado': 0.9},
        'elevatoria': {'min': 1.0, 'max': 2.5, 'recomendado': 1.5}
    }
    
    # Perda de carga limite por 100 m (J em m/100m)
    HEAD_LOSS_LIMITS = {
        'tubulacao_distribuicao': 5.0,  # m/100m
        'adutora': 3.0,  # m/100m
        'etar': 2.0,  # m/100m
        'elevatoria': 5.0  # m/100m
    }
    
    @staticmethod
    def validate_velocity(velocity_ms, system_type='tubulacao_pressao_agua'):
        """
        Valida se velocidade está dentro dos limites recomendados
        
        Args:
            velocity_ms: Velocidade em m/s
            system_type: Tipo de sistema
            
        Returns:
            Dict com validação e recomendações
        """
        limits = HydraulicValidator.VELOCITY_LIMITS.get(system_type, HydraulicValidator.VELOCITY_LIMITS['tubulacao_pressao_agua'])
        
        validation = {
            'velocity_ms': velocity_ms,
            'limits': limits,
            'is_valid': limits['min'] <= velocity_ms <= limits['max'],
            'status': '',
            'warnings': [],
            'recommendations': []
        }
        
        if velocity_ms < limits['min']:
            validation['status'] = '⚠️ BAIXA'
            validation['warnings'].append(f"Velocidade abaixo do mínimo ({limits['min']} m/s)")
            validation['recommendations'].append("Risco de sedimentação. Aumentar diâmetro do tubo ou vazão.")
        elif velocity_ms > limits['max']:
            validation['status'] = '⚠️ ALTA'
            validation['warnings'].append(f"Velocidade acima do máximo ({limits['max']} m/s)")
            validation['recommendations'].append("Risco de erosão e ruído. Aumentar diâmetro do tubo.")
        else:
            if abs(velocity_ms - limits['recomendado']) < 0.1:
                validation['status'] = '✅ ÓTIMA'
                validation['recommendations'].append("Velocidade muito próxima do recomendado.")
            else:
                validation['status'] = '✅ ADEQUADA'
                validation['recommendations'].append(f"Velocidade dentro dos limites. Recomendado: {limits['recomendado']} m/s")
        
        return validation
    
    @staticmethod
    def validate_head_loss(head_loss_m, length_m, system_type='tubulacao_distribuicao'):
        """
        Valida perda de carga contra limites recomendados
        
        Args:
            head_loss_m: Perda de carga em metros
            length_m: Comprimento em metros
            system_type: Tipo de sistema
            
        Returns:
            Dict com validação e recomendações
        """
        # Calcular J em m/100m
        J = (head_loss_m / length_m) * 100 if length_m > 0 else 0
        limit = HydraulicValidator.HEAD_LOSS_LIMITS.get(system_type, 3.0)
        
        validation = {
            'head_loss_m': head_loss_m,
            'J_m_per_100m': J,
            'limit': limit,
            'is_valid': J <= limit,
            'status': '',
            'warnings': [],
            'recommendations': []
        }
        
        if J <= limit:
            validation['status'] = '✅ ACEITÁVEL'
            if J < (limit * 0.5):
                validation['recommendations'].append("Perda de carga muito reduzida. Possível otimizar diâmetro.")
            else:
                validation['recommendations'].append(f"Perda de carga dentro do limite ({limit} m/100m).")
        else:
            validation['status'] = '⚠️ ELEVADA'
            validation['warnings'].append(f"Perda de carga acima do limite ({limit} m/100m)")
            validation['recommendations'].append("Aumentar diâmetro do tubo ou reduzir comprimento.")
        
        return validation
    
    @staticmethod
    def validate_piezometric_line(piezometric_upstream, piezometric_downstream, head_losses_total):
        """
        Valida coerência da linha piezométrica
        
        Args:
            piezometric_upstream: Cota de montante em m
            piezometric_downstream: Cota de jusante em m
            head_losses_total: Perda de carga total em m
            
        Returns:
            Dict com validação
        """
        delta_h = piezometric_upstream - piezometric_downstream
        
        validation = {
            'piezometric_upstream': piezometric_upstream,
            'piezometric_downstream': piezometric_downstream,
            'delta_h': delta_h,
            'head_losses': head_losses_total,
            'margin': delta_h - head_losses_total,
            'is_valid': (piezometric_upstream > piezometric_downstream) and (delta_h >= head_losses_total),
            'status': '',
            'warnings': [],
            'recommendations': []
        }
        
        if not validation['is_valid']:
            if piezometric_upstream <= piezometric_downstream:
                validation['status'] = '❌ INVÁLIDA'
                validation['warnings'].append("Cota de montante menor que cota de jusante")
                validation['recommendations'].append("Revisar dados de elevação. Verificar se sistema é em gravidade.")
            else:
                validation['status'] = '❌ INSUFICIENTE'
                validation['warnings'].append(f"Perda de carga ({head_losses_total:.2f}m) maior que diferença de cota ({delta_h:.2f}m)")
                validation['recommendations'].append("Aumentar diâmetro dos tubos ou instalar bomba.")
        else:
            if validation['margin'] < 0.5:
                validation['status'] = '⚠️ MARGEM REDUZIDA'
                validation['warnings'].append(f"Margem de segurança reduzida ({validation['margin']:.2f}m)")
                validation['recommendations'].append("Considerar aumento de diâmetro para margem de segurança.")
            else:
                validation['status'] = '✅ VÁLIDA'
                validation['recommendations'].append(f"Margem satisfatória de {validation['margin']:.2f}m")
        
        return validation
    
    @staticmethod
    def full_validation(flow_rate, diameter_mm, length_m, velocity_ms, 
                        head_loss_m, piezometric_up, piezometric_down, 
                        system_type='etar_entrada'):
        """
        Executa validação completa do sistema
        
        Returns:
            Dict consolidado com todas as validações
        """
        return {
            'velocity': HydraulicValidator.validate_velocity(velocity_ms, system_type),
            'head_loss': HydraulicValidator.validate_head_loss(head_loss_m, length_m, system_type),
            'piezometric': HydraulicValidator.validate_piezometric_line(
                piezometric_up, piezometric_down, head_loss_m
            )
        }
