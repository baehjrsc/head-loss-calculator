# -*- coding: utf-8 -*-
"""
Head Loss Calculator - ETAR/ETE/WTP
Aplicação Streamlit para cálculo de perda de carga em sistemas de tratamento de água
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

# Importar módulos locais
from modules.materials import MaterialCatalog
from modules.calculations import HeadLossCalculator
from modules.losses import LocalizedLosses
from modules.validators import HydraulicValidator
from modules.reports import ReportGenerator

# Configuração da página
st.set_page_config(
    page_title="Head Loss Calculator",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .main {
        padding-top: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 0.95rem;
    }
    .stButton button {
        font-size: 0.85rem;
        padding: 0.4rem 0.8rem;
        height: 2.5rem;
    }
    .stMetric {
        font-size: 0.85rem;
    }
    h1 {
        margin-top: 0rem;
        margin-bottom: 0.5rem;
        font-size: 2rem;
    }
    h2 {
        font-size: 1.3rem;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    h3 {
        font-size: 1rem;
        margin-top: 0.3rem;
        margin-bottom: 0.3rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Inicializar estado da sessão
if 'num_segments' not in st.session_state:
    st.session_state.num_segments = 2

if 'segments_data' not in st.session_state:
    st.session_state.segments_data = []

if 'localized_components' not in st.session_state:
    st.session_state.localized_components = {comp: 0 for comp in LocalizedLosses.get_available_components()}

# Header
st.title("💧 Head Loss Calculator")
st.subheader("Dimensionamento Hidráulico de Sistemas ETAR/ETE/WTP")
st.markdown("---")

# Sidebar - Configurações gerais
with st.sidebar:
    st.header("⚙️ Configurações")
    
    project_name = st.text_input("Nome do Projeto", value="Projeto Sem Nome")
    
    st.subheader("Dados Gerais")
    flow_rate_m3h = st.number_input(
        "Vazão (m³/h)", 
        value=10.0, 
        min_value=0.1, 
        step=0.5,
        help="Vazão de projeto do sistema"
    )
    
    st.subheader("Cotas de Elevação")
    col1, col2 = st.columns(2)
    with col1:
        piezometric_up = st.number_input(
            "Cota Montante (m)",
            value=10.0,
            help="Cota piezométrica de montante da interligação"
        )
    with col2:
        piezometric_down = st.number_input(
            "Cota Jusante (m)",
            value=5.0,
            help="Cota piezométrica de jusante da interligação"
        )
    
    st.subheader("Trechos")
    num_seg = st.number_input(
        "Número de Trechos",
        value=2,
        min_value=1,
        max_value=10,
        help="Define quantos trechos com DN/material diferentes"
    )
    
    if num_seg != st.session_state.num_segments:
        st.session_state.num_segments = num_seg
        st.session_state.segments_data = []
        st.rerun()

# Abas principais
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Cálculo Principal",
    "📍 Perdas Localizadas",
    "✅ Validações",
    "📈 Gráficos",
    "📄 Relatório"
])

# ============ ABA 1: CÁLCULO PRINCIPAL ============
with tab1:
    st.header("Dados dos Trechos")
    
    # Tabela de referência DN/DI/DE
    with st.expander("📊 Referência: DN/DI/DE de Tubos Forçados", expanded=False):
        st.markdown("**Tabela de Especificações por Material**")
        
        # Material reference data
        material_specs = {
            'INOX 316L': {
                'DN (mm)': [16, 20, 25, 32, 40, 50, 63, 75, 90, 110, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1200],
                'DI (mm)': [14, 18, 22, 30, 38, 47, 59, 70, 85, 103, 118, 150, 189, 236, 297, 376, 470, 594, 750, 940, 1128],
                'DE (mm)': [22, 28, 35, 42, 48, 60, 75, 88, 104, 125, 140, 180, 220, 273, 355, 426, 533, 660, 850, 1057, 1270]
            },
            'PVC-U': {
                'DN (mm)': [16, 20, 25, 32, 40, 50, 63, 75, 90, 110, 125, 160, 200, 250, 315, 400, 500, 630, 800],
                'DI (mm)': [12, 16, 20, 26, 32, 40, 50, 60, 71, 87, 100, 126, 160, 200, 250, 315, 400, 500, 630],
                'DE (mm)': [20, 25, 32, 40, 50, 63, 75, 90, 110, 140, 160, 200, 250, 315, 400, 500, 630, 800, 1000]
            },
            'PEAD Liso': {
                'DN (mm)': [20, 25, 32, 40, 50, 63, 75, 90, 110, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1200],
                'DI (mm)': [16, 20, 26, 32, 40, 50, 60, 71, 88, 100, 127, 160, 200, 250, 315, 400, 500, 630, 800, 950],
                'DE (mm)': [20, 25, 32, 40, 50, 63, 75, 90, 110, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1200]
            },
            'Ferro Fundido (FF)': {
                'DN (mm)': [50, 75, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 700, 800, 900, 1000, 1100, 1200],
                'DI (mm)': [52, 78, 103, 154, 206, 257, 309, 360, 412, 464, 515, 567, 618, 720, 823, 926, 1029, 1132, 1235],
                'DE (mm)': [80, 110, 135, 190, 244, 295, 349, 402, 457, 510, 562, 615, 670, 775, 880, 985, 1092, 1200, 1310]
            },
            'PVC Reforçado': {
                'DN (mm)': [50, 63, 75, 90, 110, 125, 160, 200, 250, 315, 400, 500, 630, 800],
                'DI (mm)': [40, 50, 60, 71, 88, 100, 126, 160, 200, 250, 315, 400, 500, 630],
                'DE (mm)': [63, 75, 90, 110, 140, 160, 200, 250, 315, 400, 500, 630, 800, 1000]
            }
        }
        
        # Create tabs for each material
        material_tabs = st.tabs(MaterialCatalog.get_available_materials())
        
        for tab, material in zip(material_tabs, MaterialCatalog.get_available_materials()):
            with tab:
                if material in material_specs:
                    spec_data = material_specs[material]
                    df_spec = pd.DataFrame(spec_data)
                    st.dataframe(df_spec, use_container_width=True, hide_index=True)
                    
                    material_info = MaterialCatalog.get_material_info(material)
                    st.caption(f"**Fornecedor:** {material_info.get('supplier', 'N/A')} | **Rugosidade:** {material_info.get('roughness', 0)} mm")
                else:
                    st.info(f"Especificações não disponíveis para {material}")
    
    
    segments_data = []
    
    for i in range(st.session_state.num_segments):
        with st.expander(f"🔧 Trecho {chr(65+i)} - {'Configurar' if i == 0 else 'Configurar'}", expanded=(i==0)):
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                material = st.selectbox(
                    f"Material - Trecho {chr(65+i)}",
                    MaterialCatalog.get_available_materials(),
                    key=f"material_{i}"
                )
            
            with col2:
                available_diameters = MaterialCatalog.get_available_diameters(material)
                diameter = st.selectbox(
                    f"Diâmetro (mm) - Trecho {chr(65+i)}",
                    available_diameters,
                    key=f"diameter_{i}"
                )
            
            with col3:
                length = st.number_input(
                    f"Comprimento (m) - Trecho {chr(65+i)}",
                    value=100.0,
                    min_value=0.1,
                    step=10.0,
                    key=f"length_{i}"
                )
            
            with col4:
                system_type = st.selectbox(
                    f"Tipo Sistema - Trecho {chr(65+i)}",
                    ['etar_entrada', 'etar_saida', 'tubulacao_pressao_agua', 'tubulacao_drenagem'],
                    key=f"system_{i}"
                )
            
            # Mostrar informações do material
            material_info = MaterialCatalog.get_material_info(material)
            if material_info:
                st.info(f"**Fornecedor:** {material_info.get('supplier', 'N/A')}")
            
            segments_data.append({
                'name': f'Trecho {chr(65+i)}',
                'material': material,
                'diameter': diameter,
                'length': length,
                'system_type': system_type,
                'flow_rate': flow_rate_m3h
            })
    
    # Botão para calcular
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        calculate_btn = st.button("🔄 CALCULAR", type="primary", use_container_width=True)
    
    with col2:
        reset_btn = st.button("🔄 Limpar", use_container_width=True)
    
    if reset_btn:
        st.session_state.segments_data = []
        st.rerun()
    
    # Executar cálculos
    if calculate_btn or st.session_state.segments_data:
        st.markdown("---")
        st.subheader("📊 Resultados de Cálculo")
        
        calculations_results = []
        total_head_loss = 0
        avg_velocity = 0
        
        # Criar colunas para exibir resultados
        result_cols = st.columns(st.session_state.num_segments)
        
        for idx, segment in enumerate(segments_data):
            calc = HeadLossCalculator.calculate_head_loss_darcy_weisbach(
                segment['flow_rate'],
                segment['diameter'],
                segment['length'],
                segment['material']
            )
            
            if calc:
                calculations_results.append(calc)
                total_head_loss += calc['head_loss_m']
                avg_velocity = calc['velocity_ms']
                
                with result_cols[idx]:
                    st.metric(
                        f"Trecho {chr(65+idx)} - Perda de Carga",
                        f"{calc['head_loss_m']:.3f} m"
                    )
                    
                    # Mini-validação
                    vel_val = HydraulicValidator.validate_velocity(
                        calc['velocity_ms'],
                        segment['system_type']
                    )
                    
                    status_color = "🟢" if vel_val['is_valid'] else "🔴"
                    st.caption(f"{status_color} V = {calc['velocity_ms']:.2f} m/s")
        
        # Resumo geral
        st.markdown("---")
        st.subheader("📈 Resumo Geral")
        
        summary_cols = st.columns(4)
        
        with summary_cols[0]:
            st.metric("Vazão", f"{flow_rate_m3h:.1f} m³/h")
        
        with summary_cols[1]:
            st.metric("Perda Total", f"{total_head_loss:.3f} m")
        
        with summary_cols[2]:
            st.metric("Vel. Média", f"{avg_velocity:.2f} m/s")
        
        with summary_cols[3]:
            margem = piezometric_up - piezometric_down - total_head_loss
            color = "🟢" if margem > 0 else "🔴"
            st.metric("Margem Piezom.", f"{margem:.3f} m", f"{color}")
        
        # Tabela detalhada
        st.markdown("---")
        st.subheader("📋 Tabela Detalhada")
        
        df_results = pd.DataFrame(calculations_results)
        if not df_results.empty:
            display_cols = ['material', 'diameter_mm', 'length_m', 'velocity_ms', 'head_loss_m', 'reynolds', 'friction_factor']
            df_display = df_results[display_cols].round(4)
            df_display.columns = ['Material', 'Diâmetro (mm)', 'Comprimento (m)', 
                                 'Velocidade (m/s)', 'Perda (m)', 'Reynolds', 'Fator f']
            st.dataframe(df_display, use_container_width=True)
        
        # Armazenar para abas posteriores
        st.session_state.segments_data = segments_data
        st.session_state.calculations_results = calculations_results
        st.session_state.total_head_loss = total_head_loss

# ============ ABA 2: PERDAS LOCALIZADAS ============
with tab2:
    st.header("Perdas de Carga Localizadas")
    st.info("Ajuste a quantidade de cada componente usando os botões + e -")
    
    components = LocalizedLosses.get_available_components()
    
    # Criar interface com + e - para cada componente
    col1, col2 = st.columns(2)
    
    components_data = {}
    
    for i, component in enumerate(components):
        col = col1 if i % 2 == 0 else col2
        
        with col:
            component_info = LocalizedLosses.get_component(component)
            
            st.subheader(f"🔧 {component}")
            
            c1, c2, c3 = st.columns([1, 3, 1])
            
            with c1:
                st.button("➖", key=f"minus_{component}", use_container_width=True)
            
            with c2:
                qty = st.number_input(
                    "Quantidade",
                    value=st.session_state.localized_components.get(component, 0),
                    min_value=0,
                    key=f"qty_{component}",
                    label_visibility="collapsed"
                )
                st.session_state.localized_components[component] = qty
            
            with c3:
                st.button("➕", key=f"plus_{component}", use_container_width=True)
            
            st.caption(f"K = {component_info['K']} | {component_info['description']}")
            components_data[component] = qty
    
    # Calcular perdas localizadas
    if st.session_state.segments_data and 'calculations_results' in st.session_state:
        st.markdown("---")
        st.subheader("Resumo de Perdas Localizadas")
        
        velocity = st.session_state.calculations_results[0]['velocity_ms'] if st.session_state.calculations_results else 1.0
        
        localized_loss_calc = LocalizedLosses.calculate_total_localized_losses(
            velocity,
            components_data
        )
        
        st.metric("Perda Total Localizada", f"{localized_loss_calc['total_head_loss_m']:.4f} m")
        
        # Tabela de detalhes
        if localized_loss_calc['details']:
            df_losses = pd.DataFrame(localized_loss_calc['details'])
            st.dataframe(df_losses, use_container_width=True)
        
        st.session_state.localized_loss = localized_loss_calc['total_head_loss_m']

# ============ ABA 3: VALIDAÇÕES ============
with tab3:
    st.header("✅ Validações Hidráulicas")
    st.info("Verificação contra Eurocódigos e boas práticas de hidráulica")
    
    if st.session_state.segments_data and 'calculations_results' in st.session_state:
        
        for idx, (segment, calc) in enumerate(zip(st.session_state.segments_data, st.session_state.calculations_results)):
            with st.expander(f"🔍 Trecho {chr(65+idx)}", expanded=(idx==0)):
                
                # Validação de velocidade
                vel_validation = HydraulicValidator.validate_velocity(
                    calc['velocity_ms'],
                    segment['system_type']
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Velocidade")
                    status_color = "✅" if vel_validation['is_valid'] else "⚠️"
                    st.write(f"**Status:** {status_color} {vel_validation['status']}")
                    st.write(f"**Velocidade:** {vel_validation['velocity_ms']:.3f} m/s")
                    st.write(f"**Intervalo:** {vel_validation['limits']['min']:.2f} - {vel_validation['limits']['max']:.2f} m/s")
                    st.write(f"**Recomendado:** {vel_validation['limits']['recomendado']:.2f} m/s")
                
                with col2:
                    st.subheader("Perda de Carga")
                    hl_validation = HydraulicValidator.validate_head_loss(
                        calc['head_loss_m'],
                        segment['length'],
                        segment['system_type']
                    )
                    
                    status_color = "✅" if hl_validation['is_valid'] else "⚠️"
                    st.write(f"**Status:** {status_color} {hl_validation['status']}")
                    st.write(f"**J:** {hl_validation['J_m_per_100m']:.2f} m/100m")
                    st.write(f"**Limite:** {hl_validation['limit']:.2f} m/100m")
                
                if vel_validation['recommendations']:
                    st.markdown("**💡 Recomendações (Velocidade):**")
                    for rec in vel_validation['recommendations']:
                        st.write(f"• {rec}")
                
                if hl_validation['recommendations']:
                    st.markdown("**💡 Recomendações (Perda de Carga):**")
                    for rec in hl_validation['recommendations']:
                        st.write(f"• {rec}")
        
        # Validação de linha piezométrica
        st.markdown("---")
        st.subheader("Linha Piezométrica")
        
        total_loss = st.session_state.total_head_loss + st.session_state.get('localized_loss', 0)
        
        pz_validation = HydraulicValidator.validate_piezometric_line(
            piezometric_up,
            piezometric_down,
            total_loss
        )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Cota Montante", f"{piezometric_up:.2f} m")
        
        with col2:
            st.metric("Cota Jusante", f"{piezometric_down:.2f} m")
        
        with col3:
            st.metric("Diferença", f"{piezometric_up - piezometric_down:.2f} m")
        
        st.markdown("---")
        
        status_color = "✅" if pz_validation['is_valid'] else "🔴"
        st.write(f"**Status:** {status_color} {pz_validation['status']}")
        st.write(f"**Perda Total:** {total_loss:.3f} m")
        st.write(f"**Margem:** {pz_validation['margin']:.3f} m")
        
        if pz_validation['recommendations']:
            st.markdown("**💡 Recomendações:**")
            for rec in pz_validation['recommendations']:
                st.write(f"• {rec}")

# ============ ABA 4: GRÁFICOS ============
with tab4:
    st.header("📈 Visualizações")
    
    if st.session_state.segments_data and 'calculations_results' in st.session_state:
        
        col1, col2 = st.columns(2)
        
        # Gráfico de Perda de Carga
        with col1:
            st.subheader("Perda de Carga por Trecho")
            
            names = [f"Trecho {chr(65+i)}" for i in range(len(st.session_state.calculations_results))]
            losses = [calc['head_loss_m'] for calc in st.session_state.calculations_results]
            
            fig_loss = go.Figure(data=[
                go.Bar(x=names, y=losses, marker_color='rgba(68, 114, 196, 0.8)')
            ])
            fig_loss.update_layout(
                title="Perda de Carga por Trecho",
                yaxis_title="Perda (m)",
                hovermode='x unified'
            )
            st.plotly_chart(fig_loss, use_container_width=True)
        
        # Gráfico de Velocidade
        with col2:
            st.subheader("Velocidade por Trecho")
            
            velocities = [calc['velocity_ms'] for calc in st.session_state.calculations_results]
            
            fig_vel = go.Figure(data=[
                go.Bar(x=names, y=velocities, marker_color='rgba(112, 173, 71, 0.8)')
            ])
            fig_vel.update_layout(
                title="Velocidade por Trecho",
                yaxis_title="Velocidade (m/s)",
                hovermode='x unified'
            )
            st.plotly_chart(fig_vel, use_container_width=True)
        
        # Linha Piezométrica
        st.subheader("Linha Piezométrica e Geométrica")
        
        cumulative_loss = 0
        piezometric_line = [piezometric_up]
        
        for calc in st.session_state.calculations_results:
            cumulative_loss += calc['head_loss_m']
            piezometric_line.append(piezometric_up - cumulative_loss)
        
        # Linha geométrica (linear de montante a jusante)
        num_points = len(piezometric_line)
        geometric_line = [piezometric_up - (piezometric_up - piezometric_down) * (i / (num_points - 1)) for i in range(num_points)]
        
        fig_pz = go.Figure()
        
        # Linha Piezométrica
        fig_pz.add_trace(go.Scatter(
            x=list(range(len(piezometric_line))),
            y=piezometric_line,
            mode='lines+markers',
            name='Linha Piezométrica',
            line=dict(color='rgba(192, 0, 0, 1)', width=3),
            marker=dict(size=6)
        ))
        
        # Linha Geométrica
        fig_pz.add_trace(go.Scatter(
            x=list(range(len(geometric_line))),
            y=geometric_line,
            mode='lines',
            name='Linha Geométrica',
            line=dict(color='rgba(0, 176, 0, 0.6)', width=2, dash='dash'),
            marker=dict(size=0)
        ))
        
        fig_pz.add_hline(y=piezometric_down, line_dash="dot", line_color="rgba(70, 130, 180, 0.5)", 
                        annotation_text="Cota Jusante")
        
        fig_pz.update_layout(
            title="Evolução da Linha Piezométrica",
            xaxis_title="Trecho",
            yaxis_title="Cota (m)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_pz, use_container_width=True)

# ============ ABA 5: RELATÓRIO ============
with tab5:
    st.header("📄 Gerar Relatório")
    
    if st.session_state.segments_data and 'calculations_results' in st.session_state:
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            filename = st.text_input(
                "Nome do Arquivo",
                value=f"relatorio_head_loss_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            )
        
        with col2:
            if st.button("📥 Gerar Excel", use_container_width=True, type="primary"):
                
                project_data = {
                    'project_name': project_name,
                    'flow_rate': flow_rate_m3h,
                    'num_segments': st.session_state.num_segments,
                    'piezometric_upstream': piezometric_up,
                    'piezometric_downstream': piezometric_down,
                    'segments': st.session_state.segments_data,
                    'localized_losses': {k: v for k, v in st.session_state.localized_components.items() if v > 0}
                }
                
                calculations = {
                    'total_head_loss': st.session_state.total_head_loss,
                    'avg_velocity': st.session_state.calculations_results[0]['velocity_ms'] if st.session_state.calculations_results else 0,
                    'localized_loss': st.session_state.get('localized_loss', 0),
                    'segments': st.session_state.calculations_results
                }
                
                total_loss = calculations['total_head_loss'] + calculations['localized_loss']
                
                validations = {
                    'velocity': HydraulicValidator.validate_velocity(calculations['avg_velocity']),
                    'head_loss': HydraulicValidator.validate_head_loss(calculations['total_head_loss'], 100),
                    'margin': piezometric_up - piezometric_down - total_loss
                }
                
                try:
                    filepath = os.path.join(os.path.expanduser("~"), "Downloads", filename)
                    ReportGenerator.create_excel_report(filepath, project_data, calculations, validations)
                    
                    st.success(f"✅ Relatório gerado com sucesso!")
                    st.info(f"Arquivo salvo em: {filepath}")
                    
                    with open(filepath, "rb") as file:
                        st.download_button(
                            label="📥 Baixar Arquivo",
                            data=file.read(),
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                
                except Exception as e:
                    st.error(f"❌ Erro ao gerar relatório: {str(e)}")
        
        st.markdown("---")
        st.subheader("Informações do Projeto")
        
        info_cols = st.columns(2)
        with info_cols[0]:
            st.write(f"**Nome:** {project_name}")
            st.write(f"**Vazão:** {flow_rate_m3h:.1f} m³/h")
        
        with info_cols[1]:
            st.write(f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            st.write(f"**Trechos:** {st.session_state.num_segments}")
    
    else:
        st.warning("⚠️ Realize os cálculos nas abas anteriores para gerar um relatório.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px;'>
    <p>💧 Head Loss Calculator v1.0 | Desenvolvido com Python & Streamlit</p>
    <p>Para hospedar online: <a href='https://github.com'>GitHub</a> → <a href='https://streamlit.io/cloud'>Streamlit Cloud</a></p>
    </div>
    """, unsafe_allow_html=True)
