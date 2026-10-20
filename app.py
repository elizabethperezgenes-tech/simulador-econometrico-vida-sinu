
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

st.set_page_config(
    page_title="Simulador Econométrico | Vida Sinú",
    page_icon="📊",
    layout="wide"
)

# Datos anuales transcritos de los estados financieros.
# Deben contrastarse con los documentos oficiales antes de la entrega.
datos = {
    "Indicador": [
        "Activos totales",
        "Activos corrientes",
        "Efectivo y equivalentes",
        "Cuentas por cobrar",
        "Pasivos totales",
        "Pasivos corrientes",
        "Patrimonio total",
        "Venta neta de servicios",
        "Costo de servicios",
        "Utilidad bruta",
        "Resultado operacional",
        "Resultado neto"
    ],
    "2024": [
        96585506698.80, 22495973071.87, 10335608090.05,
        26883724610.49, 3555738799.09, 3555738799.09,
        93029767899.71, 114183160662.30, 87760112971.79,
        26423047690.51, 2522647387.00, 3388534241.24
    ],
    "2025": [
        109813912660.87, 32022514010.06, 11023975204.20,
        33568958657.45, 14991917648.55, 14900256599.44,
        94821995012.32, 118108012704.28, 101173639203.03,
        16934373501.25, -7346997297.73, 2505605311.82
    ]
}

df = pd.DataFrame(datos).set_index("Indicador")

st.title("📊 Simulador Econométrico Financiero")
st.subheader("E.S.E. Vida Sinú — Montería, Córdoba")
st.write(
    "Herramienta académica para explorar información financiera, "
    "comparar indicadores y preparar análisis econométricos."
)

st.warning(
    "Base anual preliminar 2024–2025. Las cifras deben validarse "
    "con los estados financieros oficiales. Dos años de datos "
    "no son suficientes para una regresión econométrica confiable."
)

# Navegación
seccion = st.sidebar.radio(
    "Menú principal",
    [
        "Panel financiero",
        "Comparación de cifras",
        "Explorar archivo Excel",
        "Simulador de regresión"
    ]
)

def cop(valor):
    return "$" + f"{valor:,.0f}".replace(",", ".")

if seccion == "Panel financiero":
    st.header("1. Panel financiero")
    st.write("Resumen comparativo de los cierres de 2024 y 2025.")

    razon_2024 = df.loc["Activos corrientes", "2024"] / df.loc[
        "Pasivos corrientes", "2024"
    ]
    razon_2025 = df.loc["Activos corrientes", "2025"] / df.loc[
        "Pasivos corrientes", "2025"
    ]

    efectivo_2024 = df.loc["Efectivo y equivalentes", "2024"] / df.loc[
        "Pasivos corrientes", "2024"
    ]
    efectivo_2025 = df.loc["Efectivo y equivalentes", "2025"] / df.loc[
        "Pasivos corrientes", "2025"
    ]

    margen_neto_2024 = df.loc["Resultado neto", "2024"] / df.loc[
        "Venta neta de servicios", "2024"
    ] * 100
    margen_neto_2025 = df.loc["Resultado neto", "2025"] / df.loc[
        "Venta neta de servicios", "2025"
    ] * 100

    deuda_2024 = df.loc["Pasivos totales", "2024"] / df.loc[
        "Activos totales", "2024"
    ] * 100
    deuda_2025 = df.loc["Pasivos totales", "2025"] / df.loc[
        "Activos totales", "2025"
    ] * 100

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Activos 2025", cop(df.loc["Activos totales", "2025"]))
    c2.metric("Razón corriente 2025", f"{razon_2025:.2f} veces",
              delta=f"{razon_2025 - razon_2024:.2f} frente a 2024")
    c3.metric("Margen neto 2025", f"{margen_neto_2025:.2f}%",
              delta=f"{margen_neto_2025 - margen_neto_2024:.2f} puntos")
    c4.metric("Pasivos / activos 2025", f"{deuda_2025:.2f}%",
              delta=f"{deuda_2025 - deuda_2024:.2f} puntos")

    st.subheader("Indicadores de liquidez")

    liquidez = pd.DataFrame({
        "Indicador": ["Razón corriente", "Razón de efectivo"],
        "2024": [razon_2024, efectivo_2024],
        "2025": [razon_2025, efectivo_2025]
    }).set_index("Indicador")

    st.dataframe(liquidez.round(2), use_container_width=True)

    st.subheader("Lectura inicial")
    st.markdown(
        f"""
        - La razón corriente pasó de **{razon_2024:.2f}** a
          **{razon_2025:.2f} veces**.
        - La razón de efectivo pasó de **{efectivo_2024:.2f}** a
          **{efectivo_2025:.2f} veces**.
        - El margen neto sobre las ventas de servicios pasó de
          **{margen_neto_2024:.2f}%** a **{margen_neto_2025:.2f}%**.
        - La relación entre pasivos y activos aumentó de
          **{deuda_2024:.2f}%** a **{deuda_2025:.2f}%**.
        """
    )
    st.caption(
        "Estos indicadores son descriptivos y no sustituyen "
        "una evaluación integral de la situación financiera."
    )

elif seccion == "Comparación de cifras":
    st.header("2. Comparación financiera 2024–2025")

    seleccion = st.selectbox(
        "Selecciona las cuentas que quieres comparar",
        [
            "Activos totales",
            "Activos corrientes",
            "Efectivo y equivalentes",
            "Cuentas por cobrar",
            "Pasivos totales",
            "Patrimonio total",
            "Venta neta de servicios",
            "Costo de servicios",
            "Utilidad bruta",
            "Resultado operacional",
            "Resultado neto"
        ]
    )

    valores = df.loc[seleccion]
    variacion = valores["2025"] - valores["2024"]

    if valores["2024"] != 0:
        porcentaje = variacion / abs(valores["2024"]) * 100
    else:
        porcentaje = np.nan

    c1, c2, c3 = st.columns(3)
    c1.metric("Valor 2024", cop(valores["2024"]))
    c2.metric("Valor 2025", cop(valores["2025"]))
    c3.metric(
        "Variación absoluta",
        cop(variacion),
        delta=f"{porcentaje:.2f}%" if pd.notna(porcentaje) else "No disponible"
    )

    figura, eje = plt.subplots()
    eje.bar(["2024", "2025"], [valores["2024"], valores["2025"]])
    eje.set_title(seleccion)
    eje.set_ylabel("Pesos colombianos (COP)")
    eje.ticklabel_format(axis="y", style="plain")
    eje.grid(axis="y", alpha=0.25)
st.pyplot(figura, clear_figure=True, use_container_width=True)
st.write("Gráfica financiera generada correctamente.")
plt.close(figura)

    st.subheader("Tabla general de cifras")
    st.dataframe(
        df.style.format(lambda x: f"${x:,.2f}"),
        use_container_width=True
    )

    st.download_button(
        "Descargar comparación en CSV",
        data=df.to_csv().encode("utf-8-sig"),
        file_name="comparacion_vida_sinu_2024_2025.csv",
        mime="text/csv"
    )

elif seccion == "Explorar archivo Excel":
    st.header("3. Explorar una base de datos")
    archivo = st.file_uploader(
        "Carga un archivo Excel (.xlsx)",
        type=["xlsx"]
    )

    if archivo is not None:
        try:
            libro = pd.ExcelFile(archivo)
            hoja = st.selectbox("Selecciona la hoja", libro.sheet_names)
            tabla = pd.read_excel(archivo, sheet_name=hoja)

            st.success("Archivo cargado correctamente.")
            st.write("Filas:", tabla.shape[0], "| Columnas:", tabla.shape[1])
            st.dataframe(tabla, use_container_width=True)

            numericas = tabla.select_dtypes(include=np.number).columns.tolist()

            if numericas:
                st.subheader("Estadísticas descriptivas")
                st.dataframe(tabla[numericas].describe().T,
                             use_container_width=True)

                variable = st.selectbox(
                    "Variable para graficar", numericas
                )
                figura, eje = plt.subplots()
                eje.plot(range(1, len(tabla) + 1), tabla[variable], marker="o")
                eje.set_title(variable)
                eje.set_xlabel("Orden de las filas")
                eje.set_ylabel(variable)
                eje.grid(alpha=0.25)
                st.pyplot(figura)
                plt.close(figura)

            st.download_button(
                "Descargar tabla como CSV",
                data=tabla.to_csv(index=False).encode("utf-8-sig"),
                file_name="datos_vida_sinu.csv",
                mime="text/csv"
            )
        except Exception as error:
            st.error(f"No se pudo leer el archivo: {error}")

elif seccion == "Simulador de regresión":
    st.header("4. Simulador de regresión lineal")
    st.write(
        "Carga una base con observaciones suficientes para explorar "
        "la asociación entre dos variables numéricas."
    )
    st.info(
        "No uses únicamente los cierres de 2024 y 2025 para estimar "
        "una regresión. Se recomienda construir una serie mensual "
        "validada y metodológicamente comparable."
    )

    archivo_reg = st.file_uploader(
        "Carga una base para regresión (.xlsx)",
        type=["xlsx"],
        key="archivo_regresion"
    )

    if archivo_reg is not None:
        try:
            libro_reg = pd.ExcelFile(archivo_reg)
            hoja_reg = st.selectbox(
                "Hoja de la base", libro_reg.sheet_names
            )
            base = pd.read_excel(archivo_reg, sheet_name=hoja_reg)
            columnas = base.select_dtypes(include=np.number).columns.tolist()

            if len(columnas) >= 2:
                x = st.selectbox("Variable explicativa (X)", columnas)
                y_opciones = [c for c in columnas if c != x]
                y = st.selectbox("Variable dependiente (Y)", y_opciones)

                if st.button("Ejecutar regresión"):
                    muestra = base[[x, y]].replace(
                        [np.inf, -np.inf], np.nan
                    ).dropna()

                    if len(muestra) < 8:
                        st.error(
                            f"Solo hay {len(muestra)} observaciones válidas. "
                            "No se ejecuta el modelo con tan pocos datos."
                        )
                    elif muestra[x].nunique() < 2:
                        st.error("La variable X debe tener valores diferentes.")
                    else:
                        modelo = sm.OLS(
                            muestra[y],
                            sm.add_constant(muestra[x])
                        ).fit()

                        a, b, c = st.columns(3)
                        a.metric("Observaciones", int(modelo.nobs))
                        b.metric("R²", f"{modelo.rsquared:.4f}")
                        c.metric("Valor p de X", f"{modelo.pvalues[x]:.4f}")

                        st.write(
                            f"**Ecuación estimada:** "
                            f"Y = {modelo.params['const']:.4f} "
                            f"+ ({modelo.params[x]:.4f} × X)"
                        )
                        st.text(modelo.summary().as_text())

                        figura, eje = plt.subplots()
                        eje.scatter(muestra[x], muestra[y], label="Observaciones")
                        orden = np.argsort(muestra[x].to_numpy())
                        xs = muestra[x].to_numpy()[orden]
                        ys = modelo.predict(
                            sm.add_constant(
                                pd.DataFrame({x: xs}),
                                has_constant="add"
                            )
                        )
                        eje.plot(xs, ys, label="Regresión estimada")
                        eje.set_xlabel(x)
                        eje.set_ylabel(y)
                        eje.legend()
                        eje.grid(alpha=0.25)
                        st.pyplot(figura)
                        plt.close(figura)

                        st.warning(
                            "La asociación estadística no demuestra causalidad. "
                            "Revisa los supuestos y la calidad de los datos."
                        )
            else:
                st.warning(
                    "La hoja debe tener al menos dos columnas numéricas."
                )
        except Exception as error:
            st.error(f"No se pudo procesar el archivo: {error}")

st.divider()
st.caption(
    "Proyecto académico de Econometría Financiera | E.S.E. Vida Sinú | "
    "Cifras anuales preliminares sujetas a validación."
)
