
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

st.title("📊 Simulador Econométrico Financiero")
st.subheader("E.S.E. Vida Sinú — Montería, Córdoba")
st.write(
    "Herramienta académica para analizar información financiera, "
    "calcular indicadores y estudiar relaciones entre variables."
)

st.info(
    "Carga un archivo Excel con datos financieros oficiales. "
    "Los resultados dependerán de la calidad y estructura de los datos."
)

archivo = st.file_uploader(
    "Carga la base de datos en formato Excel (.xlsx)",
    type=["xlsx"]
)

if archivo is not None:
    try:
        libro = pd.ExcelFile(archivo)
        hoja = st.selectbox("Selecciona la hoja", libro.sheet_names)
        datos = pd.read_excel(archivo, sheet_name=hoja)

        st.success("Archivo cargado correctamente.")
        st.subheader("1. Vista previa de los datos")
        st.write("Filas:", datos.shape[0], "| Columnas:", datos.shape[1])
        st.dataframe(datos, use_container_width=True)

        st.download_button(
            "Descargar datos cargados en CSV",
            data=datos.to_csv(index=False).encode("utf-8-sig"),
            file_name="datos_vida_sinu.csv",
            mime="text/csv"
        )

        st.subheader("2. Estadísticas descriptivas")
        columnas_numericas = datos.select_dtypes(
            include=np.number
        ).columns.tolist()

        if columnas_numericas:
            st.dataframe(
                datos[columnas_numericas].describe().T,
                use_container_width=True
            )

            variable_grafico = st.selectbox(
                "Selecciona una variable para visualizar",
                columnas_numericas
            )

            figura, eje = plt.subplots()
            eje.plot(
                range(1, len(datos) + 1),
                datos[variable_grafico],
                marker="o"
            )
            eje.set_title(f"Comportamiento de {variable_grafico}")
            eje.set_xlabel("Observación")
            eje.set_ylabel(variable_grafico)
            eje.grid(True, alpha=0.3)
            st.pyplot(figura)
            plt.close(figura)

            st.caption(
                "El eje horizontal representa el orden de las filas, "
                "no necesariamente meses o fechas."
            )

            st.subheader("3. Simulador de regresión lineal")
            st.write(
                "Permite estudiar la asociación entre dos variables "
                "numéricas. La asociación no demuestra causalidad."
            )

            if len(columnas_numericas) >= 2:
                variable_x = st.selectbox(
                    "Variable explicativa (X)",
                    columnas_numericas,
                    index=0
                )
                opciones_y = [
                    c for c in columnas_numericas if c != variable_x
                ]
                variable_y = st.selectbox(
                    "Variable dependiente (Y)",
                    opciones_y,
                    index=0
                )

                if st.button("Ejecutar regresión"):
                    muestra = datos[[variable_x, variable_y]].copy()
                    muestra = muestra.replace(
                        [np.inf, -np.inf], np.nan
                    ).dropna()

                    if len(muestra) < 8:
                        st.error(
                            f"Solo hay {len(muestra)} observaciones válidas. "
                            "Se requieren al menos 8 para habilitar este "
                            "análisis exploratorio; preferiblemente se "
                            "necesitan más datos y una justificación "
                            "metodológica."
                        )
                    elif muestra[variable_x].nunique() < 2:
                        st.error(
                            "La variable X debe tener valores diferentes."
                        )
                    else:
                        X = sm.add_constant(muestra[variable_x])
                        Y = muestra[variable_y]
                        modelo = sm.OLS(Y, X).fit()

                        st.markdown("#### Resultados del modelo")
                        c1, c2, c3 = st.columns(3)
                        c1.metric(
                            "Observaciones",
                            str(int(modelo.nobs))
                        )
                        c2.metric(
                            "R²",
                            f"{modelo.rsquared:.4f}"
                        )
                        c3.metric(
                            "Valor p de X",
                            f"{modelo.pvalues[variable_x]:.4f}"
                        )

                        st.write(
                            f"**Ecuación estimada:** "
                            f"Y = {modelo.params['const']:.4f} "
                            f"+ ({modelo.params[variable_x]:.4f} × X)"
                        )

                        st.write(
                            f"**Interpretación de R²:** el modelo explica "
                            f"aproximadamente {modelo.rsquared * 100:.2f}% "
                            "de la variación observada en Y dentro de esta "
                            "muestra."
                        )

                        p = modelo.pvalues[variable_x]
                        if p < 0.05:
                            st.write(
                                "El coeficiente de X es estadísticamente "
                                "distinto de cero al nivel del 5%, bajo "
                                "los supuestos del modelo."
                            )
                        else:
                            st.write(
                                "No se encuentra evidencia estadística "
                                "suficiente para afirmar que el coeficiente "
                                "de X sea distinto de cero al nivel del 5%."
                            )

                        st.text(modelo.summary().as_text())

                        figura, eje = plt.subplots()
                        eje.scatter(
                            muestra[variable_x], Y,
                            label="Datos observados"
                        )
                        orden = np.argsort(muestra[variable_x].to_numpy())
                        x_ordenado = muestra[variable_x].to_numpy()[orden]
                        y_estimado = modelo.predict(
                            sm.add_constant(
                                pd.Series(
                                    x_ordenado,
                                    name=variable_x
                                ),
                                has_constant="add"
                            )
                        )
                        eje.plot(
                            x_ordenado,
                            y_estimado,
                            label="Regresión estimada"
                        )
                        eje.set_xlabel(variable_x)
                        eje.set_ylabel(variable_y)
                        eje.legend()
                        eje.grid(True, alpha=0.3)
                        st.pyplot(figura)
                        plt.close(figura)

                        st.warning(
                            "Antes de interpretar el modelo para el trabajo, "
                            "revisa la calidad de los datos, los supuestos "
                            "econométricos y la posible relación contable "
                            "entre las variables."
                        )
            else:
                st.warning(
                    "La hoja debe contener al menos dos columnas numéricas "
                    "para explorar una regresión."
                )
        else:
            st.warning(
                "No se encontraron columnas numéricas. Revisa el formato "
                "de la hoja seleccionada."
            )

    except Exception as error:
        st.error(
            "No se pudo leer el archivo. Verifica que sea un Excel válido. "
            f"Detalle técnico: {error}"
        )

else:
    st.subheader("¿Qué podrás hacer con este simulador?")
    st.markdown(
        """
        - Consultar y revisar datos financieros.
        - Obtener estadísticas descriptivas.
        - Visualizar variables en gráficos.
        - Ejecutar una regresión lineal cuando existan observaciones suficientes.
        - Consultar resultados estadísticos para apoyar el análisis académico.
        """
    )

st.divider()
st.caption(
    "Proyecto académico de Econometría Financiera | E.S.E. Vida Sinú"
)
