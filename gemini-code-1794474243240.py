"""
Módulo: calculos.py
Descripción: Lógica matemática modular, validación de datos, bases de datos normativas
y generación de memorias de cálculo paso a paso para Análisis de Cargas Estructurales.
"""

from typing import Dict, Any, Tuple, List

# ==============================================================================
# 1. BASE DE DATOS DE GEOLOCALIZACIÓN Y NORMATIVA VIGENTE (MÉXICO)
# ==============================================================================
ESTADOS_MUNICIPIOS_MX: Dict[str, Dict[str, Any]] = {
    "Campeche": {
        "municipios": ["Campeche", "Carmen", "Champotón", "Escárcega", "Calkiní", "Hopelchén"],
        "zona_sismica": "Zona A (Baja sismicidad)",
        "zona_eolica": "Zona Costera / Huracanes (Vientos regionales altos ~ 160-190 km/h)",
        "norma_recomendada": "Manual de Diseño de Obras Civiles (MDOC-CFE) + Reglamento de Construcción Municipal"
    },
    "Ciudad de México": {
        "municipios": ["Cuauhtémoc", "Benito Juárez", "Miguel Hidalgo", "Coyoacán", "Iztapalapa", "Álvaro Obregón"],
        "zona_sismica": "Zona de Lago / Transición / Lomas (Alta sismicidad)",
        "zona_eolica": "Zona Urbana Interior (Viento moderado)",
        "norma_recomendada": "NTC-CDMX 2023 (Normas Técnicas Complementarias sobre Criterios y Acciones)"
    },
    "Yucatán": {
        "municipios": ["Mérida", "Progreso", "Valladolid", "Tizimín", "Kanasín"],
        "zona_sismica": "Zona A (Baja sismicidad)",
        "zona_eolica": "Zona Península / Exposición a Ciclones Tropicales",
        "norma_recomendada": "Reglamento de Construcciones del Municipio de Mérida + MDOC-CFE"
    },
    "Jalisco": {
        "municipios": ["Guadalajara", "Zapopan", "Puerto Vallarta", "Tlaquepaque", "Tonalá"],
        "zona_sismica": "Zona C y D (Sismicidad alta a muy alta)",
        "zona_eolica": "Mixta (Costa del Pacífico e Interior)",
        "norma_recomendada": "Reglamento de Construcción de Guadalajara + MDOC-CFE Sismo"
    },
    "Nuevo León": {
        "municipios": ["Monterrey", "San Pedro Garza García", "Apodaca", "Guadalupe", "Santa Catarina"],
        "zona_sismica": "Zona B (Sismicidad moderada)",
        "zona_eolica": "Zona Noreste (Ráfagas convectivas)",
        "norma_recomendada": "Reglamento de Construcciones de Monterrey + MDOC-CFE Viento"
    },
    "Oaxaca": {
        "municipios": ["Oaxaca de Juárez", "Salina Cruz", "Juchitán", "Huatulco", "Tuxtepec"],
        "zona_sismica": "Zona D (Muy alta sismicidad - Brecha de Tehuantepec)",
        "zona_eolica": "Zona Istmo (Vientos extremadamente altos > 200 km/h)",
        "norma_recomendada": "Reglamento de Construcción de Oaxaca + MDOC-CFE Sismo y Viento"
    }
}

NORMATIVAS_INFO: Dict[str, Dict[str, Any]] = {
    "NTC-CDMX (Criterios y Acciones para el Diseño Estructural)": {
        "fc_cm": 1.3,
        "fc_cv": 1.5,
        "fc_grupo_a": 1.5,  # Para edificaciones esenciales (escuelas, hospitales)
        "descripcion": "Establece factores de carga de 1.3 para cargas permanentes (CM) y 1.5 para variables (CV) en estructuras del Grupo B (vivienda/oficinas)."
    },
    "MDOC-CFE (Manual de Diseño de Obras Civiles - CFE)": {
        "fc_cm": 1.3,
        "fc_cv": 1.5,
        "fc_grupo_a": 1.5,
        "descripcion": "Referencia nacional en México fuera de CDMX, especialmente para diseño por sismo y viento."
    },
    "ASCE 7 / ACI 318 (Referencia Internacional)": {
        "fc_cm": 1.2,
        "fc_cv": 1.6,
        "fc_grupo_a": 1.2,
        "descripcion": "Combinación estándar estadounidense (1.2D + 1.6L) utilizada comúnmente en proyectos industriales o académicos comparativos."
    }
}

# ==============================================================================
# 2. GLOSARIO DE CONCEPTOS BÁSICOS DE INGENIERÍA ESTRUCTURAL
# ==============================================================================
CONCEPTOS_BASICOS: List[Dict[str, str]] = [
    {"termino": "Estructura", "definicion": "Sistema ensamblado de elementos resistentes diseñados para soportar cargas y transmitirlas de forma segura hasta el suelo de cimentación sin sufrir fallas ni deformaciones excesivas."},
    {"termino": "Carga Estructural", "definicion": "Fuerza externa o interna (peso propio, ocupación, viento, sismo) que actúa sobre una estructura y genera esfuerzos y deformaciones."},
    {"termino": "Elementos Estructurales", "definicion": "Componentes individuales que conforman el esqueleto resistente: losas, vigas (trabes), columnas, muros de carga y cimentaciones."},
    {"termino": "Transmisión de Cargas", "definicion": "Ruta física o flujo que siguen las fuerzas desde su punto de aplicación (ej. losa) hacia elementos secundarios (vigas), verticales (columnas/muros) y finalmente al terreno (cimentación)."},
    {"termino": "Deformación", "definicion": "Cambio en la forma o dimensiones de un cuerpo estructural debido a la aplicación de fuerzas o cambios de temperatura."},
    {"termino": "Esfuerzo", "definicion": "Intensidad de la fuerza interna distribuida sobre un área transversal específica (σ = F / A). Se mide en kg/cm², MPa o kPa."},
    {"termino": "Tipos de Cargas Estructurales", "definicion": "Se clasifican según su duración y naturaleza en: Cargas Muertas (permanentes), Cargas Vivas (variables por uso) y Cargas Accidentales (sismo, viento, nieve)."},
    {"termino": "Carga Concentrada (Puntual)", "definicion": "Fuerza aplicada sobre un área muy pequeña en comparación con el tamaño del elemento (ej. una columna apoyada sobre una viga o maquinaria pesada). Unidad: kgf, kN, ton."},
    {"termino": "Carga Distribuida", "definicion": "Fuerza repartida de manera continua a lo largo de una longitud (carga lineal, kg/m o kN/m) o sobre una superficie (carga superficial, kg/m² o kPa)."},
    {"termino": "Flexión", "definicion": "Esfuerzo combinado en el que un elemento (como una viga) tiende a curvarse, generando compresión en una cara y tensión en la cara opuesta."},
    {"termino": "Compresión", "definicion": "Esfuerzo axial que tiende a aplastar o acortar el elemento estructural (típico en columnas y muros de mampostería)."},
    {"termino": "Tensión (Tracción)", "definicion": "Esfuerzo axial que tiende a estirar o alargar el elemento estructural (típico en tensores, cables y acero de refuerzo)."},
    {"termino": "Cortante", "definicion": "Esfuerzo paralelo a la sección transversal que tiende a deslizar una parte del elemento respecto a la adyacente."},
    {"termino": "Torsión", "definicion": "Efecto de giro alrededor del eje longitudinal de un elemento causado por un momento torsor (par de fuerzas excéntricas)."},
    {"termino": "Capacidad de Carga", "definicion": "Carga máxima que un elemento estructural o el suelo puede soportar antes de alcanzar la falla o un estado límite de servicio."},
    {"termino": "Factor de Seguridad (FS)", "definicion": "Relación adimensional entre la resistencia última (capacidad) de un elemento y la carga real esperada (FS = Resistencia / Carga Actuante). Debe ser mayor a 1.0."}
]

# ==============================================================================
# 3. VALIDACIÓN DE DATOS DE ENTRADA
# ==============================================================================
def validar_positivos(campos: Dict[str, float], permitir_cero: List[str] = None) -> Tuple[bool, str]:
    """Valida que los datos numéricos sean físicamente coherentes."""
    if permitir_cero is None:
        permitir_cero = []
    for nombre, valor in campos.items():
        if valor is None:
            return False, f"El campo '{nombre}' no puede estar vacío."
        if nombre in permitir_cero:
            if valor < 0:
                return False, f"El campo '{nombre}' no puede ser negativo ({valor})."
        else:
            if valor <= 0:
                return False, f"El campo '{nombre}' debe ser estrictamente mayor a cero (valor ingresado: {valor})."
    return True, "Datos validados correctamente."

# ==============================================================================
# 4. MÓDULOS DE CÁLCULO CON PROCEDIMIENTO PASO A PASO
# ==============================================================================

def calcular_cargas_generales(cm: float, cv: float, longitud_viga: float, carga_puntual: float) -> Dict[str, Any]:
    """Módulo A: Cargas estructurales básicas (Muerta, Viva, Total, Distribuida y Puntual equivalente)."""
    valido, msg = validar_positivos(
        {"Carga Muerta (CM)": cm, "Carga Viva (CV)": cv, "Longitud de análisis": longitud_viga, "Carga Puntual (P)": carga_puntual},
        permitir_cero=["Carga Puntual (P)"]
    )
    if not valido:
        return {"error": msg}

    carga_total = cm + cv
    carga_distribuida = carga_total  # En kg/m o kN/m si se ingresa lineal
    # Efecto total de carga distribuida + puntual sobre el tramo
    fuerza_total_tramo = (carga_distribuida * longitud_viga) + carga_puntual

    procedimiento = {
        "datos": f"CM = {cm:,.2f} kg/m | CV = {cv:,.2f} kg/m | L = {longitud_viga:,.2f} m | P = {carga_puntual:,.2f} kg",
        "formula": "CT = CM + CV   |   F_total = (CT × L) + P",
        "sustitucion": f"CT = {cm:,.2f} + {cv:,.2f}   |   F_total = ({carga_total:,.2f} × {longitud_viga:,.2f}) + {carga_puntual:,.2f}",
        "pasos": [
            f"1. Sumar la carga permanente y la carga variable: CT = {cm:,.2f} + {cv:,.2f} = {carga_total:,.2f} kg/m.",
            f"2. Integrar la carga distribuida en la longitud L = {longitud_viga:,.2f} m: W_dist = {carga_total * longitud_viga:,.2f} kg.",
            f"3. Adicionar la carga puntual concentrada (P = {carga_puntual:,.2f} kg): F_total = {fuerza_total_tramo:,.2f} kg."
        ],
        "resultado_final": f"Carga Distribuida Total (CT) = {carga_total:,.2f} kg/m | Reacción Total en Tramo = {fuerza_total_tramo:,.2f} kg",
        "interpretacion": (
            f"El elemento soporta una carga distribuida de servicio de {carga_total:,.2f} kg/m "
            f"(donde el {(cm/carga_total)*100:.1f}% corresponde a peso muerto permanente). "
            f"La carga gravitacional acumulada total es de {fuerza_total_tramo:,.2f} kg ({fuerza_total_tramo/1000:.2f} toneladas)."
        )
    }
    return {
        "error": None,
        "cm": cm, "cv": cv, "ct": carga_total,
        "w_dist_total": carga_total * longitud_viga,
        "puntual": carga_puntual,
        "fuerza_total": fuerza_total_tramo,
        "procedimiento": procedimiento
    }


def calcular_muro_mamposteria(
    longitud: float, altura_libre: float, espesor_cm: float,
    num_niveles: int, altura_nivel: float, tipo_mamposteria: str,
    peso_volumetrico: float, resistencia_fm: float,
    carga_sobrepuesta_ml: float = 0.0
) -> Dict[str, Any]:
    """Módulo B: Análisis gravitacional de muros de mampostería."""
    valido, msg = validar_positivos({
        "Longitud del muro": longitud,
        "Altura libre": altura_libre,
        "Espesor (cm)": espesor_cm,
        "Número de niveles": num_niveles,
        "Altura por nivel": altura_nivel,
        "Peso volumétrico": peso_volumetrico,
        "Resistencia f'm": resistencia_fm
    })
    if not valido:
        return {"error": msg}

    espesor_m = espesor_cm / 100.0
    area_muro_nivel = longitud * altura_libre          # m² (elevación)
    area_transversal_cm2 = (longitud * 100) * espesor_cm  # cm² (sección horizontal)
    volumen_nivel = area_muro_nivel * espesor_m        # m³
    peso_propio_nivel = volumen_nivel * peso_volumetrico  # kg

    # Carga muerta acumulada en la base considerando los N niveles
    peso_propio_total_niveles = peso_propio_nivel * num_niveles
    carga_muerta_total = peso_propio_total_niveles + (carga_sobrepuesta_ml * longitud * num_niveles)
    carga_por_metro_lineal = carga_muerta_total / longitud

    # Esfuerzo axial actuante vs resistencia
    esfuerzo_actuante = carga_muerta_total / area_transversal_cm2  # kg/cm²
    fs_estimado = resistencia_fm / esfuerzo_actuante if esfuerzo_actuante > 0 else 999.0

    procedimiento = {
        "datos": (
            f"L = {longitud:.2f} m | h_libre = {altura_libre:.2f} m | t = {espesor_cm:.1f} cm ({espesor_m:.3f} m) | "
            f"Niveles = {num_niveles} (h_nivel = {altura_nivel:.2f} m) | Material: {tipo_mamposteria} "
            f"(γ = {peso_volumetrico:,.0f} kg/m³, f'm = {resistencia_fm:.1f} kg/cm²)"
        ),
        "formula": "A_elev = L × h   |   V = A_elev × t   |   W_propio = V × γ   |   CM_total = (W_propio × N) + W_sobrepuesta",
        "sustitucion": (
            f"A_elev = {longitud:.2f} × {altura_libre:.2f}   |   V = {area_muro_nivel:.2f} × {espesor_m:.3f}   |   "
            f"W_propio = {volumen_nivel:.3f} × {peso_volumetrico:,.0f}"
        ),
        "pasos": [
            f"1. Área en elevación por nivel: A_elev = {longitud:.2f} m × {altura_libre:.2f} m = {area_muro_nivel:.2f} m².",
            f"2. Volumen de mampostería por nivel: V = {area_muro_nivel:.2f} m² × {espesor_m:.3f} m = {volumen_nivel:.3f} m³.",
            f"3. Peso propio de un nivel: W_propio = {volumen_nivel:.3f} m³ × {peso_volumetrico:,.0f} kg/m³ = {peso_propio_nivel:,.2f} kg.",
            f"4. Acumulación en {num_niveles} nivel(es) + carga muerta sobrepuesta ({carga_sobrepuesta_ml * longitud * num_niveles:,.2f} kg): CM_total = {carga_muerta_total:,.2f} kg.",
            f"5. Carga distribuida en la base del muro: w_base = {carga_muerta_total:,.2f} kg / {longitud:.2f} m = {carga_por_metro_lineal:,.2f} kg/m.",
            f"6. Esfuerzo de compresión en base (A_transversal = {area_transversal_cm2:,.0f} cm²): σ = {esfuerzo_actuante:.2f} kg/cm² vs f'm = {resistencia_fm:.1f} kg/cm²."
        ],
        "resultado_final": f"Peso Propio (1 nivel) = {peso_propio_nivel:,.2f} kg | Carga Total en Base = {carga_muerta_total:,.2f} kg ({carga_por_metro_lineal:,.2f} kg/m)",
        "interpretacion": (
            f"El muro de {tipo_mamposteria} transmite {carga_por_metro_lineal:,.2f} kg/m a la cimentación. "
            f"El esfuerzo axial de trabajo es de {esfuerzo_actuante:.2f} kg/cm², lo que representa el {(esfuerzo_actuante/resistencia_fm)*100:.1f}% "
            f"de la resistencia básica a compresión de la mampostería (f'm = {resistencia_fm:.1f} kg/cm²)."
        )
    }

    return {
        "error": None,
        "area_muro": area_muro_nivel,
        "volumen_muro": volumen_nivel,
        "peso_propio": peso_propio_nivel,
        "carga_muerta_total": carga_muerta_total,
        "carga_lineal": carga_por_metro_lineal,
        "esfuerzo_actuante": esfuerzo_actuante,
        "fs_estimado": fs_estimado,
        "procedimiento": procedimiento
    }


def calcular_elemento_estructural(
    tipo_elemento: str, dim1: float, dim2: float, dim3: float,
    gamma_material: float, carga_externa: float
) -> Dict[str, Any]:
    """
    Módulo C: Análisis de cargas en elementos estructurales:
    - Viga: dim1=base(cm), dim2=peralte(cm), dim3=claro(m), carga_externa=carga sobrepuesta(kg/m)
    - Columna: dim1=ancho b(cm), dim2=largo h(cm), dim3=altura H(m), carga_externa=carga axial bajada(kg)
    - Losa: dim1=ancho Lx(m), dim2=largo Ly(m), dim3=espesor t(cm), carga_externa=acabados+CV(kg/m²)
    - Muro: dim1=longitud(m), dim2=altura(m), dim3=espesor(cm), carga_externa=carga superior(kg/m)
    """
    valido, msg = validar_positivos(
        {"Dimensión 1": dim1, "Dimensión 2": dim2, "Dimensión 3": dim3, "Peso volumétrico": gamma_material, "Carga externa": carga_externa},
        permitir_cero=["Carga externa"]
    )
    if not valido:
        return {"error": msg}

    if tipo_elemento == "Viga":
        b_m, h_m, claro = dim1 / 100.0, dim2 / 100.0, dim3
        area_sec = b_m * h_m
        peso_propio_ml = area_sec * gamma_material  # kg/m
        w_total = peso_propio_ml + carga_externa     # kg/m
        reaccion_apoyo = (w_total * claro) / 2.0     # kg
        momento_max = (w_total * (claro ** 2)) / 8.0 # kg·m

        procedimiento = {
            "datos": f"Viga b = {dim1:.1f} cm, h = {dim2:.1f} cm, Claro L = {claro:.2f} m | γ = {gamma_material:,.0f} kg/m³ | w_ext = {carga_externa:,.2f} kg/m",
            "formula": "w_pp = (b × h) × γ   |   w_total = w_pp + w_ext   |   R = (w_total × L)/2   |   M_max = (w_total × L²)/8",
            "sustitucion": f"w_pp = ({b_m:.3f} × {h_m:.3f}) × {gamma_material:,.0f}   |   w_total = {peso_propio_ml:,.2f} + {carga_externa:,.2f}",
            "pasos": [
                f"1. Sección transversal de la viga: A = {b_m:.3f} m × {h_m:.3f} m = {area_sec:.4f} m².",
                f"2. Peso propio lineal: w_pp = {area_sec:.4f} m² × {gamma_material:,.0f} kg/m³ = {peso_propio_ml:,.2f} kg/m.",
                f"3. Carga distribuida total: w_total = {peso_propio_ml:,.2f} + {carga_externa:,.2f} = {w_total:,.2f} kg/m.",
                f"4. Reacción en cada apoyo (viga simplemente apoyada): R = ({w_total:,.2f} × {claro:.2f}) / 2 = {reaccion_apoyo:,.2f} kg.",
                f"5. Momento flexionante máximo al centro del claro: M_max = ({w_total:,.2f} × {claro:.2f}²) / 8 = {momento_max:,.2f} kg·m."
            ],
            "resultado_final": f"w_total = {w_total:,.2f} kg/m | Reacción R = {reaccion_apoyo:,.2f} kg | M_max = {momento_max:,.2f} kg·m",
            "interpretacion": f"La viga transmite {reaccion_apoyo:,.2f} kg a cada columna de apoyo y experimenta un momento flexionante máximo de {momento_max:,.2f} kg·m al centro del claro."
        }
        return {
            "error": None, "peso_propio": peso_propio_ml * claro, "carga_total": w_total * claro,
            "metrica_1_lbl": "Carga Lineal Total", "metrica_1_val": f"{w_total:,.2f} kg/m",
            "metrica_2_lbl": "Reacción por Apoyo", "metrica_2_val": f"{reaccion_apoyo:,.2f} kg",
            "metrica_3_lbl": "Momento Máximo", "metrica_3_val": f"{momento_max:,.2f} kg·m",
            "procedimiento": procedimiento
        }

    elif tipo_elemento == "Columna":
        b_m, h_m, altura = dim1 / 100.0, dim2 / 100.0, dim3
        area_cm2 = dim1 * dim2
        volumen = b_m * h_m * altura
        peso_propio = volumen * gamma_material
        carga_axial_total = peso_propio + carga_externa
        esfuerzo_compresion = carga_axial_total / area_cm2

        procedimiento = {
            "datos": f"Columna b = {dim1:.1f} cm, h = {dim2:.1f} cm, Altura H = {altura:.2f} m | γ = {gamma_material:,.0f} kg/m³ | P_bajada = {carga_externa:,.2f} kg",
            "formula": "W_pp = (b × h × H) × γ   |   P_total = W_pp + P_bajada   |   σ = P_total / A_cm²",
            "sustitucion": f"W_pp = ({b_m:.3f} × {h_m:.3f} × {altura:.2f}) × {gamma_material:,.0f}   |   P_total = {peso_propio:,.2f} + {carga_externa:,.2f}",
            "pasos": [
                f"1. Volumen de la columna: V = {b_m:.3f} m × {h_m:.3f} m × {altura:.2f} m = {volumen:.4f} m³.",
                f"2. Peso propio de la columna: W_pp = {volumen:.4f} m³ × {gamma_material:,.0f} kg/m³ = {peso_propio:,.2f} kg.",
                f"3. Carga axial total en la base: P_total = {peso_propio:,.2f} + {carga_externa:,.2f} = {carga_axial_total:,.2f} kg.",
                f"4. Esfuerzo normal promedio de compresión: σ = {carga_axial_total:,.2f} kg / {area_cm2:,.1f} cm² = {esfuerzo_compresion:.2f} kg/cm²."
            ],
            "resultado_final": f"Peso Propio = {peso_propio:,.2f} kg | Carga Axial Total = {carga_axial_total:,.2f} kg | σ = {esfuerzo_compresion:.2f} kg/cm²",
            "interpretacion": f"La columna trabaja a compresión pura bajo una carga axial acumulada de {carga_axial_total:,.2f} kg ({carga_axial_total/1000:.2f} ton), generando un esfuerzo de {esfuerzo_compresion:.2f} kg/cm²."
        }
        return {
            "error": None, "peso_propio": peso_propio, "carga_total": carga_axial_total,
            "metrica_1_lbl": "Peso Propio Columna", "metrica_1_val": f"{peso_propio:,.2f} kg",
            "metrica_2_lbl": "Carga Axial Total", "metrica_2_val": f"{carga_axial_total:,.2f} kg",
            "metrica_3_lbl": "Esfuerzo Compresión", "metrica_3_val": f"{esfuerzo_compresion:.2f} kg/cm²",
            "procedimiento": procedimiento
        }

    elif tipo_elemento == "Losa":
        lx, ly, espesor_m = dim1, dim2, dim3 / 100.0
        area_losa = lx * ly
        peso_propio_m2 = espesor_m * gamma_material
        carga_total_m2 = peso_propio_m2 + carga_externa
        peso_total_tablero = carga_total_m2 * area_losa

        procedimiento = {
            "datos": f"Tablero de Losa Lx = {lx:.2f} m, Ly = {ly:.2f} m, Espesor t = {dim3:.1f} cm | γ = {gamma_material:,.0f} kg/m³ | Sobrecarga = {carga_externa:,.2f} kg/m²",
            "formula": "w_pp = t × γ   |   w_total = w_pp + w_ext   |   W_tablero = w_total × (Lx × Ly)",
            "sustitucion": f"w_pp = {espesor_m:.3f} × {gamma_material:,.0f}   |   w_total = {peso_propio_m2:,.2f} + {carga_externa:,.2f}",
            "pasos": [
                f"1. Área del tablero de losa: A = {lx:.2f} m × {ly:.2f} m = {area_losa:.2f} m².",
                f"2. Peso propio por metro cuadrado: w_pp = {espesor_m:.3f} m × {gamma_material:,.0f} kg/m³ = {peso_propio_m2:,.2f} kg/m².",
                f"3. Carga superficial total de servicio: w_total = {peso_propio_m2:,.2f} + {carga_externa:,.2f} = {carga_total_m2:,.2f} kg/m².",
                f"4. Carga total que baja del tablero hacia las trabes perimetrales: W_tablero = {carga_total_m2:,.2f} × {area_losa:.2f} = {peso_total_tablero:,.2f} kg."
            ],
            "resultado_final": f"Carga Superficial = {carga_total_m2:,.2f} kg/m² | Carga Total del Tablero = {peso_total_tablero:,.2f} kg",
            "interpretacion": f"Cada metro cuadrado de losa pesa {peso_propio_m2:,.2f} kg/m² por sí mismo y soporta {carga_total_m2:,.2f} kg/m² en total, transfiriendo {peso_total_tablero/1000:.2f} toneladas al sistema de vigas."
        }
        return {
            "error": None, "peso_propio": peso_propio_m2 * area_losa, "carga_total": peso_total_tablero,
            "metrica_1_lbl": "Peso Propio Losa", "metrica_1_val": f"{peso_propio_m2:,.2f} kg/m²",
            "metrica_2_lbl": "Carga Total / m²", "metrica_2_val": f"{carga_total_m2:,.2f} kg/m²",
            "metrica_3_lbl": "Carga Total Tablero", "metrica_3_val": f"{peso_total_tablero:,.2f} kg",
            "procedimiento": procedimiento
        }

    else:  # Muro
        long_m, alt_m, esp_m = dim1, dim2, dim3 / 100.0
        peso_propio_total = long_m * alt_m * esp_m * gamma_material
        carga_total_muro = peso_propio_total + (carga_externa * long_m)
        carga_lineal_base = carga_total_muro / long_m

        procedimiento = {
            "datos": f"Muro L = {long_m:.2f} m, H = {alt_m:.2f} m, Espesor t = {dim3:.1f} cm | γ = {gamma_material:,.0f} kg/m³ | Carga sup. = {carga_externa:,.2f} kg/m",
            "formula": "W_pp = (L × H × t) × γ   |   W_total = W_pp + (w_sup × L)   |   w_base = W_total / L",
            "sustitucion": f"W_pp = ({long_m:.2f} × {alt_m:.2f} × {esp_m:.3f}) × {gamma_material:,.0f}",
            "pasos": [
                f"1. Peso propio del paño de muro: W_pp = {long_m:.2f} × {alt_m:.2f} × {esp_m:.3f} × {gamma_material:,.0f} = {peso_propio_total:,.2f} kg.",
                f"2. Carga total bajada en la base: W_total = {peso_propio_total:,.2f} + ({carga_externa:,.2f} × {long_m:.2f}) = {carga_total_muro:,.2f} kg.",
                f"3. Carga distribuida linealmente sobre el cimiento: w_base = {carga_total_muro:,.2f} / {long_m:.2f} = {carga_lineal_base:,.2f} kg/m."
            ],
            "resultado_final": f"Peso Propio = {peso_propio_total:,.2f} kg | Carga Lineal Base = {carga_lineal_base:,.2f} kg/m",
            "interpretacion": f"El muro descarga {carga_lineal_base:,.2f} kg por cada metro lineal de cimentación corrida."
        }
        return {
            "error": None, "peso_propio": peso_propio_total, "carga_total": carga_total_muro,
            "metrica_1_lbl": "Peso Propio Muro", "metrica_1_val": f"{peso_propio_total:,.2f} kg",
            "metrica_2_lbl": "Carga Total Base", "metrica_2_val": f"{carga_total_muro:,.2f} kg",
            "metrica_3_lbl": "Carga Lineal Base", "metrica_3_val": f"{carga_lineal_base:,.2f} kg/m",
            "procedimiento": procedimiento
        }


def calcular_carga_m2(peso_losa: float, acabados: float, instalaciones: float, muro_divisorio: float, carga_viva: float) -> Dict[str, Any]:
    """Módulo D: Bajada de cargas por metro cuadrado (Sistema de piso)."""
    valido, msg = validar_positivos(
        {"Peso propio losa": peso_losa, "Acabados": acabados, "Instalaciones": instalaciones, "Muros divisorios": muro_divisorio, "Carga viva": carga_viva},
        permitir_cero=["Acabados", "Instalaciones", "Muros divisorios"]
    )
    if not valido:
        return {"error": msg}

    cm_total = peso_losa + acabados + instalaciones + muro_divisorio
    carga_total_m2 = cm_total + carga_viva

    procedimiento = {
        "datos": f"Peso Losa = {peso_losa:.1f} kg/m² | Acabados = {acabados:.1f} kg/m² | Instalaciones = {instalaciones:.1f} kg/m² | Muros div. = {muro_divisorio:.1f} kg/m² | CV = {carga_viva:.1f} kg/m²",
        "formula": "CM = W_losa + W_acabados + W_inst + W_muros   |   W_total/m² = CM + CV",
        "sustitucion": f"CM = {peso_losa:.1f} + {acabados:.1f} + {instalaciones:.1f} + {muro_divisorio:.1f}   |   W_total/m² = {cm_total:.1f} + {carga_viva:.1f}",
        "pasos": [
            f"1. Integración de Carga Muerta (CM): {peso_losa:.1f} + {acabados:.1f} + {instalaciones:.1f} + {muro_divisorio:.1f} = {cm_total:,.2f} kg/m².",
            f"2. Suma de Carga Viva reglamentaria (CV = {carga_viva:,.2f} kg/m²): W_total/m² = {cm_total:,.2f} + {carga_viva:,.2f} = {carga_total_m2:,.2f} kg/m²."
        ],
        "resultado_final": f"Carga Muerta (CM) = {cm_total:,.2f} kg/m² | Carga Total de Servicio = {carga_total_m2:,.2f} kg/m²",
        "interpretacion": (
            f"El sistema de entrepiso/azotea genera una carga muerta de {cm_total:,.2f} kg/m² ({(cm_total/carga_total_m2)*100:.1f}% del total) "
            f"y una carga total de servicio de {carga_total_m2:,.2f} kg/m² para el diseño de losas y vigas."
        )
    }
    return {
        "error": None, "cm": cm_total, "cv": carga_viva, "total_m2": carga_total_m2,
        "desglose": {"Peso Propio Losa": peso_losa, "Acabados": acabados, "Instalaciones": instalaciones, "Muros Divisorios": muro_divisorio, "Carga Viva": carga_viva},
        "procedimiento": procedimiento
    }


def calcular_combinacion_cargas(cm: float, cv: float, ca: float, fc_cm: float, fc_cv: float, fc_ca: float, norma: str) -> Dict[str, Any]:
    """Módulo E: Combinación de cargas última (Estado Límite de Falla)."""
    valido, msg = validar_positivos(
        {"Carga Muerta (CM)": cm, "Carga Viva (CV)": cv, "Carga Accidental (CA)": ca, "Factor CM": fc_cm, "Factor CV": fc_cv, "Factor CA": fc_ca},
        permitir_cero=["Carga Accidental (CA)", "Factor CA"]
    )
    if not valido:
        return {"error": msg}

    carga_servicio = cm + cv + ca
    carga_ultima = (fc_cm * cm) + (fc_cv * cv) + (fc_ca * ca)
    incremento_pct = ((carga_ultima - carga_servicio) / carga_servicio) * 100 if carga_servicio > 0 else 0

    procedimiento = {
        "datos": f"Norma: {norma} | CM = {cm:,.2f}, CV = {cv:,.2f}, CA = {ca:,.2f} | Factores: Fc_CM = {fc_cm:.2f}, Fc_CV = {fc_cv:.2f}, Fc_CA = {fc_ca:.2f}",
        "formula": "Cu = (Fc_CM × CM) + (Fc_CV × CV) + (Fc_CA × CA)",
        "sustitucion": f"Cu = ({fc_cm:.2f} × {cm:,.2f}) + ({fc_cv:.2f} × {cv:,.2f}) + ({fc_ca:.2f} × {ca:,.2f})",
        "pasos": [
            f"1. Carga Muerta factorizada: {fc_cm:.2f} × {cm:,.2f} = {fc_cm * cm:,.2f}.",
            f"2. Carga Viva factorizada: {fc_cv:.2f} × {cv:,.2f} = {fc_cv * cv:,.2f}.",
            f"3. Carga Accidental factorizada: {fc_ca:.2f} × {ca:,.2f} = {fc_ca * ca:,.2f}.",
            f"4. Suma de acciones factorizadas: Cu = {carga_ultima:,.2f} (frente a {carga_servicio:,.2f} sin factorizar)."
        ],
        "resultado_final": f"Carga Última de Diseño (Cu) = {carga_ultima:,.2f} (Incremento por seguridad: +{incremento_pct:.1f}%)",
        "interpretacion": (
            f"Bajo los criterios de '{norma}', la estructura debe diseñarse para resistir una carga última mayorada de {carga_ultima:,.2f}, "
            f"incorporando un margen de seguridad del {incremento_pct:.1f}% sobre las cargas nominales de servicio."
        )
    }
    return {
        "error": None,
        "servicio": carga_servicio,
        "ultima": carga_ultima,
        "cm_fact": fc_cm * cm,
        "cv_fact": fc_cv * cv,
        "ca_fact": fc_ca * ca,
        "procedimiento": procedimiento
    }