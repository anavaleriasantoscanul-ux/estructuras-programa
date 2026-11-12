"""
Aplicación Web: ESTRUCTURAS | Análisis de Cargas - Ingeniería Civil
Práctica 6: Modelado de problemas aplicados a la Ingeniería Civil
Ejecución: streamlit run app.py
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from calculos import (
    ESTADOS_MUNICIPIOS_MX,
    NORMATIVAS_INFO,
    CONCEPTOS_BASICOS,
    calcular_cargas_generales,
    calcular_muro_mamposteria,
    calcular_elemento_estructural,
    calcular_carga_m2,
    calcular_combinacion_cargas
)

# ==============================================================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS CSS PERSONALIZADOS (AZUL CELESTE / INGENIERÍA)
# ==============================================================================
st.set_page_config(
    page_title="ESTRUCTURAS | Análisis de Cargas",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fondo general limpio */
    .stApp {
        background-color: #F4F8FB;
    }

    /* Barra lateral */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #E3F2FD 0%, #EDF6FC 100%);
        border-right: 1px solid #BBDEFB;
    }

    /* Banner Hero Principal estilo Corporativo de Ingeniería */
    .hero-banner {
        background: linear-gradient(135deg, #0D47A1 0%, #0288D1 60%, #29B6F6 100%);
        padding: 2.2rem 2.5rem;
        border-radius: 16px;
        color: white;
        box-shadow: 0 8px 24px rgba(2, 136, 209, 0.18);
        margin-bottom: 1.5rem;
        border-bottom: 5px solid #81D4FA;
    }
    .hero-badge {
        background-color: rgba(255, 255, 255, 0.2);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        display: inline-block;
        margin-bottom: 0.6rem;
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #E1F5FE;
        margin-top: 0.3rem;
        font-weight: 400;
    }

    /* Tarjetas estilo Dashboard moderno */
    .eng-card {
        background-color: #FFFFFF;
        border-radius: 14px;
        padding: 1.4rem;
        box-shadow: 0 4px 14px rgba(13, 71, 161, 0.06);
        border: 1px solid #E1F5FE;
        margin-bottom: 1rem;
    }
    .kpi-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 1.2rem;
        border-left: 5px solid #0288D1;
        box-shadow: 0 4px 12px rgba(2, 136, 209, 0.08);
        text-align: left;
    }
    .kpi-label {
        font-size: 0.82rem;
        color: #546E7A;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }
    .kpi-value {
        font-size: 1.65rem;
        font-weight: 700;
        color: #01579B;
        margin-top: 0.25rem;
    }
    .kpi-unit {
        font-size: 0.85rem;
        color: #0288D1;
        font-weight: 500;
    }

    /* Caja de Memoria de Cálculo Paso a Paso */
    .memoria-box {
        background-color: #FFFFFF;
        border: 1px solid #B3E5FC;
        border-top: 4px solid #0288D1;
        border-radius: 12px;
        padding: 1.3rem 1.5rem;
        margin-top: 1rem;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.03);
    }
    .memoria-step {
        background-color: #F0F9FF;
        padding: 0.65rem 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border-left: 3px solid #29B6F6;
        color: #102A43;
        font-size: 0.94rem;
    }
    .interpretacion-box {
        background-color: #E1F5FE;
        border-left: 4px solid #01579B;
        padding: 0.9rem 1.1rem;
        border-radius: 8px;
        color: #01579B;
        font-weight: 500;
        margin-top: 0.8rem;
    }

    /* Tarjeta de Concepto Básico */
    .concept-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 1.1rem;
        border: 1px solid #E1F5FE;
        border-top: 3px solid #29B6F6;
        height: 100%;
        box-shadow: 0 2px 8px rgba(2, 136, 209, 0.05);
    }
    .concept-title {
        color: #0277BD;
        font-weight: 700;
        font-size: 1.02rem;
        margin-bottom: 0.4rem;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# FUNCIONES DE VISUALIZACIÓN GRÁFICA Y MODELADO CAD 3D (PLOTLY)
# ==============================================================================

def generar_modelo_3d_estructura(tipo: str = "Marco", w_carga: float = 1200.0) -> go.Figure:
    """Genera un modelo 3D interactivo estilo software CAD estructural (STAAD/ETABS)."""
    fig = go.Figure()

    if tipo == "Muro":
        # Muro de mampostería 3D con cimentación y flechas de carga superior
        x = [0, 4, 4, 0, 0, 4, 4, 0]
        y = [0, 0, 0.25, 0.25, 0, 0, 0.25, 0.25]
        z = [0, 0, 0, 0, 2.8, 2.8, 2.8, 2.8]
        fig.add_trace(go.Mesh3d(
            x=x, y=y, z=z,
            i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
            j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
            k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
            color='#4FC3F7', opacity=0.75, name='Muro Mampostería'
        ))
        # Cimentación corrida
        fig.add_trace(go.Mesh3d(
            x=[-0.2, 4.2, 4.2, -0.2, -0.2, 4.2, 4.2, -0.2],
            y=[-0.2, -0.2, 0.45, 0.45, -0.2, -0.2, 0.45, 0.45],
            z=[-0.4, -0.4, -0.4, -0.4, 0, 0, 0, 0],
            color='#546E7A', opacity=0.9, name='Cimentación'
        ))
        # Vectores de carga distribuida superior
        xs_f = np.linspace(0.2, 3.8, 8)
        for xf in xs_f:
            fig.add_trace(go.Scatter3d(
                x=[xf, xf], y=[0.125, 0.125], z=[3.5, 2.85],
                mode='lines+markers', line=dict(color='#D32F2F', width=4),
                marker=dict(size=4, color='#D32F2F'), showlegend=False
            ))
    else:
        # Pórtico estructural 3D (Columnas, Vigas y Losa) tipo software de análisis
        cols = [(0, 0), (5, 0), (0, 4), (5, 4)]
        for cx, cy in cols:
            fig.add_trace(go.Scatter3d(
                x=[cx, cx], y=[cy, cy], z=[0, 3.2],
                mode='lines', line=dict(color='#01579B', width=10), name='Columna'
            ))
            # Zapata aislada
            fig.add_trace(go.Mesh3d(
                x=[cx-0.4, cx+0.4, cx+0.4, cx-0.4],
                y=[cy-0.4, cy-0.4, cy+0.4, cy+0.4],
                z=[0, 0, 0, 0], color='#37474F', opacity=0.9, showlegend=False
            ))
        # Vigas perimetrales
        vigas_x = [([0, 5], [0, 0]), ([0, 5], [4, 4])]
        vigas_y = [([0, 0], [0, 4]), ([5, 5], [0, 4])]
        for vx, vy in vigas_x + vigas_y:
            fig.add_trace(go.Scatter3d(
                x=vx, y=vy, z=[3.2, 3.2],
                mode='lines', line=dict(color='#0288D1', width=8), name='Viga / Trabe'
            ))
        # Losa superior
        fig.add_trace(go.Mesh3d(
            x=[0, 5, 5, 0], y=[0, 0, 4, 4], z=[3.25, 3.25, 3.25, 3.25],
            color='#81D4FA', opacity=0.55, name='Losa de Entrepiso'
        ))
        # Vectores de carga sobre la viga frontal
        for xf in np.linspace(0.4, 4.6, 7):
            fig.add_trace(go.Scatter3d(
                x=[xf, xf], y=[0, 0], z=[4.0, 3.3],
                mode='lines+markers', line=dict(color='#E53935', width=4),
                marker=dict(size=4, color='#E53935'), showlegend=False
            ))

    fig.update_layout(
        title=dict(text=f"Modelo Estructural 3D — Carga Actuante: {w_carga:,.1f} kg/m", font=dict(size=14, color="#01579B")),
        scene=dict(
            xaxis_title="X (m)", yaxis_title="Y (m)", zaxis_title="Z (m)",
            bgcolor="#F8FBFE",
            xaxis=dict(gridcolor="#CFD8DC"), yaxis=dict(gridcolor="#CFD8DC"), zaxis=dict(gridcolor="#CFD8DC")
        ),
        margin=dict(l=0, r=0, t=38, b=0),
        height=360,
        showlegend=False
    )
    return fig


def diagrama_viga_2d(claro: float, w_dist: float, p_puntual: float = 0.0) -> go.Figure:
    """Diagrama estructural 2D de viga con cargas distribuida, puntual y reacciones."""
    r = (w_dist * claro + p_puntual) / 2.0
    fig = go.Figure()

    # Cuerpo de la viga
    fig.add_shape(type="rect", x0=0, y0=-0.12, x1=claro, y1=0.12,
                  fillcolor="#0288D1", line=dict(color="#01579B", width=2))

    # Apoyos triangulares
    fig.add_trace(go.Scatter(x=[0], y=[-0.22], mode="markers+text",
                             marker=dict(symbol="triangle-up", size=18, color="#37474F"),
                             text=[f"R1 = {r:,.1f} kg"], textposition="bottom center", showlegend=False))
    fig.add_trace(go.Scatter(x=[claro], y=[-0.22], mode="markers+text",
                             marker=dict(symbol="triangle-up", size=18, color="#37474F"),
                             text=[f"R2 = {r:,.1f} kg"], textposition="bottom center", showlegend=False))

    # Carga distribuida uniforme
    xs = np.linspace(0, claro, 12)
    fig.add_shape(type="line", x0=0, y0=0.65, x1=claro, y1=0.65, line=dict(color="#0277BD", width=2))
    for x in xs:
        fig.add_annotation(x=x, y=0.15, ax=x, ay=0.65, xref="x", yref="y", axref="x", ayref="y",
                           showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=1.8, arrowcolor="#0277BD")
    fig.add_annotation(x=claro/2, y=0.78, text=f"w = {w_dist:,.1f} kg/m", showarrow=False, font=dict(color="#01579B", size=12, weight="bold"))

    # Carga puntual al centro si existe
    if p_puntual > 0:
        fig.add_annotation(x=claro/2, y=0.15, ax=claro/2, ay=1.15, xref="x", yref="y", axref="x", ayref="y",
                           showarrow=True, arrowhead=2, arrowsize=1.6, arrowwidth=3, arrowcolor="#D32F2F")
        fig.add_annotation(x=claro/2, y=1.25, text=f"P = {p_puntual:,.1f} kg", showarrow=False, font=dict(color="#D32F2F", size=12, weight="bold"))

    fig.update_layout(
        title=dict(text=f"Diagrama de Cuerpo Libre (Claro L = {claro:.2f} m)", font=dict(size=13, color="#01579B")),
        xaxis=dict(range=[-0.6, claro + 0.6], title="Longitud (m)", showgrid=True, gridcolor="#ECEFF1"),
        yaxis=dict(range=[-0.65, 1.5], visible=False),
        plot_bgcolor="#FFFFFF", height=270, margin=dict(l=20, r=20, t=40, b=30)
    )
    return fig


def mostrar_memoria_calculo(proc: dict):
    """Renderiza el bloque estructurado de procedimiento paso a paso e interpretación."""
    st.markdown(f"""
    <div class="memoria-box">
        <h4 style="color:#01579B; margin-top:0;">📐 Memoria de Cálculo Paso a Paso</h4>
        <p><strong>1. Datos Ingresados:</strong> {proc['datos']}</p>
        <p><strong>2. Fórmula Utilizada:</strong> <code>{proc['formula']}</code></p>
        <p><strong>3. Sustitución de Valores:</strong> <code>{proc['sustitucion']}</code></p>
        <p><strong>4. Procedimiento Detallado:</strong></p>
    """, unsafe_allow_html=True)

    for paso in proc["pasos"]:
        st.markdown(f'<div class="memoria-step">{paso}</div>', unsafe_allow_html=True)

    st.markdown(f"""
        <p style="margin-top:0.8rem; font-size:1.05rem; color:#01579B;"><strong>5. Resultado Final:</strong> {proc['resultado_final']}</p>
        <div class="interpretacion-box">
            <strong>💡 Interpretación Estructural:</strong> {proc['interpretacion']}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# MENÚ DE NAVEGACIÓN LATERAL Y CONFIGURACIÓN REGIONAL
# ==============================================================================
with st.sidebar:
    st.markdown("### 🏗️ ESTRUCTURAS")
    st.caption("Sistema de Análisis de Cargas • Ingeniería Civil")
    st.divider()

    seccion = st.radio(
        "Navegación Principal",
        [
            "🏠 Inicio y Resumen Ejecutivo",
            "📚 Conceptos Básicos",
            "📍 Geolocalización y Normativa",
            "🧮 Módulos de Cálculo",
            "📝 Ejercicios Resueltos y Simulador"
        ]
    )

    st.divider()
    st.markdown("**Contexto Normativo Activo:**")
    estado_sel = st.selectbox("Estado (México)", list(ESTADOS_MUNICIPIOS_MX.keys()), index=0)
    municipio_sel = st.selectbox("Municipio", ESTADOS_MUNICIPIOS_MX[estado_sel]["municipios"])
    norma_sel = st.selectbox("Reglamento / Norma", list(NORMATIVAS_INFO.keys()), index=0)

    st.info(f"📍 **{municipio_sel}, {estado_sel}**\n\n⚖️ Factores base: CM={NORMATIVAS_INFO[norma_sel]['fc_cm']} | CV={NORMATIVAS_INFO[norma_sel]['fc_cv']}")

# ==============================================================================
# BANNER SUPERIOR DE LA APLICACIÓN
# ==============================================================================
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">INGENIERÍA CIVIL • ANÁLISIS ESTRUCTURAL APLICADO</div>
    <h1 class="hero-title">ESTRUCTURAS | Análisis de Cargas</h1>
    <p class="hero-subtitle">Plataforma académica para el modelado gravitacional, bajada de cargas, combinación normativa y verificación de elementos estructurales.</p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# SECCIÓN 1: INICIO Y DASHBOARD EJECUTIVO
# ==============================================================================
if seccion == "🏠 Inicio y Resumen Ejecutivo":
    col_info, col_3d = st.columns([1.25, 1])

    with col_info:
        st.markdown("""
        <div class="eng-card">
            <h3 style="color:#01579B; margin-top:0;">Importancia del Análisis de Cargas Estructurales</h3>
            <p style="color:#263238; line-height:1.65; text-align:justify;">
                Toda construcción está sometida a diferentes tipos de cargas, como el peso de sus propios materiales, las personas, los muebles, los equipos y las acciones ambientales, entre ellas el viento y los sismos. Estas fuerzas pueden afectar el comportamiento de una estructura y, si no se consideran adecuadamente durante su diseño, pueden provocar deformaciones excesivas, daños o fallas estructurales.
            </p>
            <p style="color:#263238; line-height:1.65; text-align:justify;">
                Por esta razón, es necesario realizar un análisis que permita identificar las cargas, calcular sus magnitudes, establecer sus combinaciones y evaluar sus efectos sobre los elementos que conforman una edificación.
            </p>
            <p style="color:#263238; line-height:1.65; text-align:justify; margin-bottom:0;">
                Esta investigación tiene como finalidad explicar los fundamentos del análisis de cargas estructurales, identificar los datos necesarios para realizarlo y establecer los procedimientos que podrían incorporarse en una aplicación web destinada a facilitar estos cálculos.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_3d:
        st.markdown('<div class="eng-card">', unsafe_allow_html=True)
        st.plotly_chart(generar_modelo_3d_estructura("Marco", 1450.0), use_container_width=True)
        st.caption("Visualización isométrica 3D de transmisión de cargas: Losa → Vigas → Columnas → Cimentación.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Panel estilo Dashboard con indicadores y gráficas resumen
    st.markdown("### 📊 Panorama General de Cargas Típicas en Edificación")
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown('<div class="kpi-card"><div class="kpi-label">Losa Maciza (12 cm)</div><div class="kpi-value">288 <span class="kpi-unit">kg/m²</span></div></div>', unsafe_allow_html=True)
    k2.markdown('<div class="kpi-card"><div class="kpi-label">Carga Viva Vivienda</div><div class="kpi-value">190 <span class="kpi-unit">kg/m²</span></div></div>', unsafe_allow_html=True)
    k3.markdown('<div class="kpi-card"><div class="kpi-label">Muro Tabique Rojo</div><div class="kpi-value">1,500 <span class="kpi-unit">kg/m³</span></div></div>', unsafe_allow_html=True)
    k4.markdown(f'<div class="kpi-card"><div class="kpi-label">Factor Carga ({norma_sel.split()[0]})</div><div class="kpi-value">{NORMATIVAS_INFO[norma_sel]["fc_cm"]} / {NORMATIVAS_INFO[norma_sel]["fc_cv"]}</div></div>', unsafe_allow_html=True)

    st.write("")
    g1, g2 = st.columns(2)
    with g1:
        df_comp = pd.DataFrame({
            "Uso de Edificación": ["Azotea (Pendiente > 5%)", "Casa Habitación", "Oficinas y Despachos", "Aulas Escolares", "Comercio / Reunión"],
            "Carga Muerta Est. (kg/m²)": [340, 380, 410, 420, 450],
            "Carga Viva Máx. (kg/m²)": [40, 190, 250, 250, 350]
        })
        fig_bar = px.bar(
            df_comp, x="Uso de Edificación", y=["Carga Muerta Est. (kg/m²)", "Carga Viva Máx. (kg/m²)"],
            barmode="stack", title="Comparativa de Cargas Gravitacionales por Uso (kg/m²)",
            color_discrete_sequence=["#0288D1", "#81D4FA"]
        )
        fig_bar.update_layout(plot_bgcolor="white", paper_bgcolor="white", height=320)
        st.plotly_chart(fig_bar, use_container_width=True)

    with g2:
        df_pie = pd.DataFrame({
            "Componente": ["Peso Propio Losa", "Acabados y Mortero", "Instalaciones", "Carga Viva"],
            "Valor (kg/m²)": [288, 75, 25, 190]
        })
        fig_pie = px.pie(
            df_pie, names="Componente", values="Valor (kg/m²)", hole=0.45,
            title="Distribución Típica en Entrepiso Habitacional (Total: 578 kg/m²)",
            color_discrete_sequence=["#01579B", "#0288D1", "#29B6F6", "#B3E5FC"]
        )
        fig_pie.update_layout(paper_bgcolor="white", height=320)
        st.plotly_chart(fig_pie, use_container_width=True)

# ==============================================================================
# SECCIÓN 2: CONCEPTOS BÁSICOS DE INGENIERÍA ESTRUCTURAL
# ==============================================================================
elif seccion == "📚 Conceptos Básicos":
    st.markdown("### 📚 Fundamentos Teóricos del Análisis Estructural")
    st.write("Glosario técnico con los 16 conceptos esenciales para el modelado y evaluación de estructuras:")

    busqueda = st.text_input("🔍 Filtrar concepto técnico:", placeholder="Ej. Factor de seguridad, flexión, carga distribuida...")
    conceptos_filtrados = [
        c for c in CONCEPTOS_BASICOS
        if busqueda.lower() in c["termino"].lower() or busqueda.lower() in c["definicion"].lower()
    ]

    cols = st.columns(2)
    for idx, item in enumerate(conceptos_filtrados):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="concept-card" style="margin-bottom: 1rem;">
                <div class="concept-title">🔹 {idx + 1}. {item['termino']}</div>
                <div style="color:#37474F; font-size:0.93rem; line-height:1.5;">{item['definicion']}</div>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# SECCIÓN 3: GEOLOCALIZACIÓN Y NORMATIVA VIGENTE (MÉXICO)
# ==============================================================================
elif seccion == "📍 Geolocalización y Normativa":
    st.markdown("### 📍 Zonificación Regional y Normativa Aplicable en México")

    c1, c2 = st.columns([1, 1.3])
    with c1:
        st.markdown('<div class="eng-card">', unsafe_allow_html=True)
        est_geo = st.selectbox("Selecciona el Estado de la República:", list(ESTADOS_MUNICIPIOS_MX.keys()), index=list(ESTADOS_MUNICIPIOS_MX.keys()).index(estado_sel))
        mun_geo = st.selectbox("Selecciona el Municipio:", ESTADOS_MUNICIPIOS_MX[est_geo]["municipios"])
        norm_geo = st.selectbox("Normativa Estructural de Referencia:", list(NORMATIVAS_INFO.keys()), index=list(NORMATIVAS_INFO.keys()).index(norma_sel))
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        info_est = ESTADOS_MUNICIPIOS_MX[est_geo]
        info_norm = NORMATIVAS_INFO[norm_geo]
        st.markdown(f"""
        <div class="eng-card">
            <h4 style="color:#01579B; margin-top:0;">Dictamen Preliminar de Sitio: {mun_geo}, {est_geo}</h4>
            <p><strong>🌎 Peligro Sísmico Regional:</strong> {info_est['zona_sismica']}</p>
            <p><strong>💨 Exposición Eólica Regional:</strong> {info_est['zona_eolica']}</p>
            <p><strong>📘 Reglamento Sugerido en Sitio:</strong> {info_est['norma_recomendada']}</p>
            <hr style="border-color:#E1F5FE;">
            <h5 style="color:#0277BD;">Parámetros de la Norma Seleccionada ({norm_geo})</h5>
            <p style="font-size:0.92rem; color:#37474F;">{info_norm['descripcion']}</p>
            <ul>
                <li><strong>Factor de Carga Muerta (Fc_CM):</strong> {info_norm['fc_cm']}</li>
                <li><strong>Factor de Carga Viva (Fc_CV):</strong> {info_norm['fc_cv']}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# SECCIÓN 4: MÓDULOS DE CÁLCULO INTERACTIVOS (A, B, C, D, E)
# ==============================================================================
elif seccion == "🧮 Módulos de Cálculo":
    st.markdown("### 🧮 Módulos de Cálculo Estructural")

    tab_a, tab_b, tab_c, tab_d, tab_e = st.tabs([
        "A. Cargas Estructurales",
        "B. Muros de Mampostería",
        "C. Elementos Estructurales",
        "D. Carga por m²",
        "E. Combinación de Cargas"
    ])

    # ---------------- MÓDULO A ----------------
    with tab_a:
        st.subheader("A. Análisis de Cargas Estructurales Generales")
        ca1, ca2 = st.columns([1, 1.3])
        with ca1:
            cm_a = st.number_input("Carga Muerta distribuida CM (kg/m):", min_value=0.0, value=450.0, step=10.0, key="a_cm")
            cv_a = st.number_input("Carga Viva distribuida CV (kg/m):", min_value=0.0, value=250.0, step=10.0, key="a_cv")
            long_a = st.number_input("Longitud del elemento L (m):", min_value=0.1, value=5.0, step=0.5, key="a_l")
            punt_a = st.number_input("Carga Puntual al centro P (kg):", min_value=0.0, value=600.0, step=50.0, key="a_p")

        res_a = calcular_cargas_generales(cm_a, cv_a, long_a, punt_a)
        with ca2:
            if res_a["error"]:
                st.error(res_a["error"])
            else:
                m1, m2, m3 = st.columns(3)
                m1.metric("Carga Distribuida Total", f"{res_a['ct']:,.2f} kg/m")
                m2.metric("Carga Dist. Acumulada", f"{res_a['w_dist_total']:,.2f} kg")
                m3.metric("Carga Total en Tramo", f"{res_a['fuerza_total']:,.2f} kg")
                st.plotly_chart(diagrama_viga_2d(long_a, res_a["ct"], punt_a), use_container_width=True)

        if not res_a["error"]:
            mostrar_memoria_calculo(res_a["procedimiento"])

    # ---------------- MÓDULO B ----------------
    with tab_b:
        st.subheader("B. Análisis Gravitacional de Muros de Mampostería")
        cb1, cb2 = st.columns([1, 1.3])
        with cb1:
            tipo_mamp = st.selectbox("Tipo de mampostería:", [
                "Tabique rojo recocido (γ ≈ 1,500 kg/m³)",
                "Block hueco de concreto (γ ≈ 1,350 kg/m³)",
                "Block macizo de concreto (γ ≈ 1,900 kg/m³)",
                "Piedra braza (γ ≈ 2,200 kg/m³)"
            ])
            pesos_def = {"Tabique": 1500.0, "Block hueco": 1350.0, "Block macizo": 1900.0, "Piedra": 2200.0}
            gamma_def = next(v for k, v in pesos_def.items() if k in tipo_mamp)

            l_muro = st.number_input("Longitud del muro L (m):", min_value=0.1, value=4.0, step=0.25)
            h_libre = st.number_input("Altura libre h (m):", min_value=0.1, value=2.70, step=0.10)
            esp_muro = st.number_input("Espesor del muro t (cm):", min_value=5.0, value=15.0, step=1.0)
            n_niveles = st.number_input("Número de niveles del edificio:", min_value=1, max_value=20, value=2, step=1)
            h_nivel = st.number_input("Altura total por nivel (m):", min_value=0.5, value=3.0, step=0.1)
            gamma_mamp = st.number_input("Peso volumétrico γ (kg/m³):", min_value=500.0, value=gamma_def, step=50.0)
            fm_mamp = st.number_input("Resistencia de diseño f'm (kg/cm²):", min_value=5.0, value=15.0, step=1.0)
            w_sobre = st.number_input("Carga muerta adicional de losa/pretil (kg/m):", min_value=0.0, value=350.0, step=25.0)

        res_b = calcular_muro_mamposteria(l_muro, h_libre, esp_muro, n_niveles, h_nivel, tipo_mamp, gamma_mamp, fm_mamp, w_sobre)
        with cb2:
            if res_b["error"]:
                st.error(res_b["error"])
            else:
                bm1, bm2, bm3 = st.columns(3)
                bm1.metric("Área / Vol. (1 Nivel)", f"{res_b['area_muro']:.2f} m² / {res_b['volumen_muro']:.2f} m³")
                bm2.metric("Peso Propio (1 Nivel)", f"{res_b['peso_propio']:,.1f} kg")
                bm3.metric("Carga Total Base", f"{res_b['carga_muerta_total']:,.1f} kg")
                st.plotly_chart(generar_modelo_3d_estructura("Muro", res_b["carga_lineal"]), use_container_width=True)

        if not res_b["error"]:
            mostrar_memoria_calculo(res_b["procedimiento"])

    # ---------------- MÓDULO C ----------------
    with tab_c:
        st.subheader("C. Análisis de Cargas en Elementos Estructurales")
        elem_sel = st.selectbox("Selecciona el elemento estructural:", ["Viga", "Columna", "Losa", "Muro"])
        cc1, cc2 = st.columns([1, 1.3])

        with cc1:
            if elem_sel == "Viga":
                d1 = st.number_input("Base de la viga b (cm):", min_value=5.0, value=25.0, step=5.0)
                d2 = st.number_input("Peralte total h (cm):", min_value=10.0, value=45.0, step=5.0)
                d3 = st.number_input("Claro libre L (m):", min_value=0.5, value=6.0, step=0.5)
                gam = st.number_input("Peso volumétrico concreto (kg/m³):", min_value=500.0, value=2400.0, step=50.0)
                cext = st.number_input("Carga lineal sobrepuesta de losa (kg/m):", min_value=0.0, value=850.0, step=50.0)
            elif elem_sel == "Columna":
                d1 = st.number_input("Ancho sección b (cm):", min_value=15.0, value=30.0, step=5.0)
                d2 = st.number_input("Largo sección h (cm):", min_value=15.0, value=30.0, step=5.0)
                d3 = st.number_input("Altura de entrepiso H (m):", min_value=1.0, value=3.2, step=0.2)
                gam = st.number_input("Peso volumétrico concreto (kg/m³):", min_value=500.0, value=2400.0, step=50.0)
                cext = st.number_input("Carga axial bajada de niveles superiores (kg):", min_value=0.0, value=18500.0, step=500.0)
            elif elem_sel == "Losa":
                d1 = st.number_input("Claro corto Lx (m):", min_value=0.5, value=4.0, step=0.25)
                d2 = st.number_input("Claro largo Ly (m):", min_value=0.5, value=5.0, step=0.25)
                d3 = st.number_input("Espesor de losa t (cm):", min_value=5.0, value=12.0, step=1.0)
                gam = st.number_input("Peso volumétrico concreto (kg/m³):", min_value=500.0, value=2400.0, step=50.0)
                cext = st.number_input("Acabados + Instalaciones + Carga Viva (kg/m²):", min_value=0.0, value=290.0, step=10.0)
            else:
                d1 = st.number_input("Longitud del muro L (m):", min_value=0.5, value=3.5, step=0.25)
                d2 = st.number_input("Altura del muro H (m):", min_value=0.5, value=2.8, step=0.1)
                d3 = st.number_input("Espesor del muro t (cm):", min_value=5.0, value=15.0, step=1.0)
                gam = st.number_input("Peso volumétrico mampostería (kg/m³):", min_value=500.0, value=1500.0, step=50.0)
                cext = st.number_input("Carga lineal superior (kg/m):", min_value=0.0, value=420.0, step=20.0)

        res_c = calcular_elemento_estructural(elem_sel, d1, d2, d3, gam, cext)
        with cc2:
            if res_c["error"]:
                st.error(res_c["error"])
            else:
                cm1, cm2, cm3 = st.columns(3)
                cm1.metric(res_c["metrica_1_lbl"], res_c["metrica_1_val"])
                cm2.metric(res_c["metrica_2_lbl"], res_c["metrica_2_val"])
                cm3.metric(res_c["metrica_3_lbl"], res_c["metrica_3_val"])

                if elem_sel == "Viga":
                    w_tot = (d1/100)*(d2/100)*gam + cext
                    st.plotly_chart(diagrama_viga_2d(d3, w_tot), use_container_width=True)
                else:
                    st.plotly_chart(generar_modelo_3d_estructura("Muro" if elem_sel == "Muro" else "Marco", res_c["carga_total"]), use_container_width=True)

        if not res_c["error"]:
            mostrar_memoria_calculo(res_c["procedimiento"])

    # ---------------- MÓDULO D ----------------
    with tab_d:
        st.subheader("D. Análisis de Carga por Metro Cuadrado (Bajada de Cargas)")
        cd1, cd2 = st.columns([1, 1.3])
        with cd1:
            p_losa = st.number_input("Peso propio de losa estructural (kg/m²):", min_value=10.0, value=288.0, step=10.0)
            p_acab = st.number_input("Acabados (firme, loseta, plafón) (kg/m²):", min_value=0.0, value=85.0, step=5.0)
            p_inst = st.number_input("Instalaciones hidrosanitarias/eléctricas (kg/m²):", min_value=0.0, value=25.0, step=5.0)
            p_mdiv = st.number_input("Carga equivalente por muros divisorios (kg/m²):", min_value=0.0, value=50.0, step=10.0)
            p_cv = st.number_input("Carga Viva reglamentaria CV (kg/m²):", min_value=10.0, value=190.0, step=10.0)

        res_d = calcular_carga_m2(p_losa, p_acab, p_inst, p_mdiv, p_cv)
        with cd2:
            if res_d["error"]:
                st.error(res_d["error"])
            else:
                dm1, dm2, dm3 = st.columns(3)
                dm1.metric("Carga Muerta Total", f"{res_d['cm']:,.2f} kg/m²")
                dm2.metric("Carga Viva", f"{res_d['cv']:,.2f} kg/m²")
                dm3.metric("Carga Total / m²", f"{res_d['total_m2']:,.2f} kg/m²")

                df_d = pd.DataFrame({"Concepto": list(res_d["desglose"].keys()), "Carga (kg/m²)": list(res_d["desglose"].values())})
                fig_d = px.bar(df_d, x="Concepto", y="Carga (kg/m²)", title="Integración de Cargas por m²", color="Concepto",
                               color_discrete_sequence=["#01579B", "#0277BD", "#0288D1", "#29B6F6", "#81D4FA"])
                fig_d.update_layout(showlegend=False, plot_bgcolor="white", height=280)
                st.plotly_chart(fig_d, use_container_width=True)

        if not res_d["error"]:
            mostrar_memoria_calculo(res_d["procedimiento"])

    # ---------------- MÓDULO E ----------------
    with tab_e:
        st.subheader("E. Combinación de Cargas (Estado Límite de Falla)")
        ce1, ce2 = st.columns([1, 1.3])
        with ce1:
            cm_e = st.number_input("Carga Muerta nominal CM (kg o kg/m):", min_value=0.0, value=1200.0, step=50.0, key="e_cm")
            cv_e = st.number_input("Carga Viva nominal CV (kg o kg/m):", min_value=0.0, value=650.0, step=50.0, key="e_cv")
            ca_e = st.number_input("Carga Accidental CA - Viento/Sismo (kg o kg/m):", min_value=0.0, value=0.0, step=50.0, key="e_ca")

            st.markdown("**Factores de Carga (Editables según reglamento):**")
            f1, f2, f3 = st.columns(3)
            fc_cm = f1.number_input("Fc (CM)", min_value=0.5, max_value=3.0, value=float(NORMATIVAS_INFO[norma_sel]["fc_cm"]), step=0.05)
            fc_cv = f2.number_input("Fc (CV)", min_value=0.5, max_value=3.0, value=float(NORMATIVAS_INFO[norma_sel]["fc_cv"]), step=0.05)
            fc_ca = f3.number_input("Fc (CA)", min_value=0.0, max_value=3.0, value=1.1, step=0.05)

        res_e = calcular_combinacion_cargas(cm_e, cv_e, ca_e, fc_cm, fc_cv, fc_ca, norma_sel)
        with ce2:
            if res_e["error"]:
                st.error(res_e["error"])
            else:
                em1, em2 = st.columns(2)
                em1.metric("Carga de Servicio (Sin Factorizar)", f"{res_e['servicio']:,.2f}")
                em2.metric("Carga Última Mayorada (Cu)", f"{res_e['ultima']:,.2f}", delta=f"+{res_e['ultima']-res_e['servicio']:,.2f}")

                df_e = pd.DataFrame({
                    "Condición": ["Servicio (Nominal)", "Última (Factorizada)"],
                    "Carga Muerta": [cm_e, res_e["cm_fact"]],
                    "Carga Viva": [cv_e, res_e["cv_fact"]],
                    "Carga Accidental": [ca_e, res_e["ca_fact"]]
                })
                fig_e = px.bar(df_e, x="Condición", y=["Carga Muerta", "Carga Viva", "Carga Accidental"],
                               barmode="stack", title="Comparación: Carga Nominal vs. Carga Factorizada",
                               color_discrete_sequence=["#01579B", "#0288D1", "#4FC3F7"])
                fig_e.update_layout(plot_bgcolor="white", height=290)
                st.plotly_chart(fig_e, use_container_width=True)

        if not res_e["error"]:
            mostrar_memoria_calculo(res_e["procedimiento"])

# ==============================================================================
# SECCIÓN 5: EJERCICIOS RESUELTOS E INTERACTIVOS CON GRÁFICAS
# ==============================================================================
elif seccion == "📝 Ejercicios Resueltos y Simulador":
    st.markdown("### 📝 Ejercicios Resueltos de Ingeniería Civil (Editables)")
    st.write("Selecciona un caso práctico universitario. Puedes modificar cualquiera de sus parámetros para comprobar cómo cambian los resultados y las gráficas estructurales en tiempo real.")

    ejercicio = st.selectbox("Selecciona el ejercicio de ejemplo:", [
        "Ejercicio 1: Cálculo de cargas gravitacionales en un muro de mampostería de 2 niveles",
        "Ejercicio 2: Análisis de carga muerta y carga viva en una losa de entrepiso",
        "Ejercicio 3: Cálculo de carga total, reacciones y momento máximo en una viga"
    ])

    if "Ejercicio 1" in ejercicio:
        st.info("**Enunciado:** Determinar el peso propio, la carga muerta total y el esfuerzo de compresión en la base de un muro de carga de tabique rojo recocido de 4.50 m de longitud, 2.60 m de altura libre y 15 cm de espesor en un edificio de 2 niveles (γ = 1,500 kg/m³, f'm = 15 kg/cm²), considerando una descarga de losa de 420 kg/m por nivel.")
        col_ex1, col_ex2 = st.columns([1, 1.3])
        with col_ex1:
            ex1_l = st.number_input("Longitud L (m)", value=4.50, min_value=0.5, key="ex1_l")
            ex1_h = st.number_input("Altura libre h (m)", value=2.60, min_value=0.5, key="ex1_h")
            ex1_t = st.number_input("Espesor t (cm)", value=15.0, min_value=5.0, key="ex1_t")
            ex1_n = st.number_input("Niveles", value=2, min_value=1, key="ex1_n")
            ex1_g = st.number_input("Peso volumétrico (kg/m³)", value=1500.0, min_value=500.0, key="ex1_g")
            ex1_w = st.number_input("Carga losa por nivel (kg/m)", value=420.0, min_value=0.0, key="ex1_w")
        r_ex1 = calcular_muro_mamposteria(ex1_l, ex1_h, ex1_t, ex1_n, 2.90, "Tabique rojo recocido", ex1_g, 15.0, ex1_w)
        with col_ex2:
            if not r_ex1["error"]:
                st.plotly_chart(generar_modelo_3d_estructura("Muro", r_ex1["carga_lineal"]), use_container_width=True)
        if not r_ex1["error"]:
            mostrar_memoria_calculo(r_ex1["procedimiento"])

    elif "Ejercicio 2" in ejercicio:
        st.info("**Enunciado:** Calcular la carga muerta total y la carga total de servicio por metro cuadrado para una losa maciza de concreto reforzado de 12 cm de espesor (γ = 2,400 kg/m³ → 288 kg/m²) destinada a casa habitación (CV = 190 kg/m²), con 75 kg/m² de acabados, 25 kg/m² de instalaciones y 40 kg/m² por muros divisorios.")
        col_ex1, col_ex2 = st.columns([1, 1.3])
        with col_ex1:
            ex2_losa = st.number_input("Peso propio losa (kg/m²)", value=288.0, min_value=10.0, key="ex2_1")
            ex2_acab = st.number_input("Acabados (kg/m²)", value=75.0, min_value=0.0, key="ex2_2")
            ex2_inst = st.number_input("Instalaciones (kg/m²)", value=25.0, min_value=0.0, key="ex2_3")
            ex2_muro = st.number_input("Muros divisorios (kg/m²)", value=40.0, min_value=0.0, key="ex2_4")
            ex2_cv = st.number_input("Carga Viva (kg/m²)", value=190.0, min_value=10.0, key="ex2_5")
        r_ex2 = calcular_carga_m2(ex2_losa, ex2_acab, ex2_inst, ex2_muro, ex2_cv)
        with col_ex2:
            if not r_ex2["error"]:
                df_ex2 = pd.DataFrame({"Rubro": list(r_ex2["desglose"].keys()), "kg/m²": list(r_ex2["desglose"].values())})
                fig_ex2 = px.pie(df_ex2, names="Rubro", values="kg/m²", hole=0.4, title="Composición de Carga en Losa",
                                 color_discrete_sequence=["#01579B", "#0288D1", "#29B6F6", "#81D4FA", "#B3E5FC"])
                fig_ex2.update_layout(height=310)
                st.plotly_chart(fig_ex2, use_container_width=True)
        if not r_ex2["error"]:
            mostrar_memoria_calculo(r_ex2["procedimiento"])

    else:
        st.info("**Enunciado:** Determinar la carga distribuida total, las reacciones en los apoyos y el momento flexionante máximo de una viga de concreto reforzado de sección 25 × 50 cm y 6.00 m de claro libre (γ = 2,400 kg/m³), que recibe una carga tributaria de losa y muro de 920 kg/m.")
        col_ex1, col_ex2 = st.columns([1, 1.3])
        with col_ex1:
            ex3_b = st.number_input("Base b (cm)", value=25.0, min_value=5.0, key="ex3_b")
            ex3_h = st.number_input("Peralte h (cm)", value=50.0, min_value=10.0, key="ex3_h")
            ex3_l = st.number_input("Claro L (m)", value=6.0, min_value=0.5, key="ex3_l")
            ex3_w = st.number_input("Carga sobrepuesta (kg/m)", value=920.0, min_value=0.0, key="ex3_w")
        r_ex3 = calcular_elemento_estructural("Viga", ex3_b, ex3_h, ex3_l, 2400.0, ex3_w)
        with col_ex2:
            if not r_ex3["error"]:
                w_tot_ex3 = (ex3_b/100)*(ex3_h/100)*2400.0 + ex3_w
                st.plotly_chart(diagrama_viga_2d(ex3_l, w_tot_ex3), use_container_width=True)
        if not r_ex3["error"]:
            mostrar_memoria_calculo(r_ex3["procedimiento"])

# ==============================================================================
# PIE DE PÁGINA Y ADVERTENCIA TÉCNICA ACADÉMICA
# ==============================================================================
st.divider()
st.warning(
    "⚠️ **Aviso Técnico y Académico:** Los resultados, memorias de cálculo y modelos generados por esta aplicación tienen fines estrictamente educativos y universitarios (Práctica 6 — Ingeniería Civil). No sustituyen la memoria de cálculo oficial, el análisis sísmico/eólico detallado ni la responsiva de un Director Responsable de Obra (DRO) o Corresponsable en Seguridad Estructural."
)