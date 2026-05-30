import os
import pandas as pd

# =============================================================================
# 1. IMPORTAR EL ARCHIVO DE EXCEL A UN DATAFRAME DE PANDAS
# =============================================================================
# Usamos un "raw string" (r"...") para que Windows reconozca correctamente las barras invertidas (\)
ruta_excel = r"C:\UPMH\3er CUATRIMESTRE\03-Sabado1_APRENDISAJE AUTOMATICO NO SUPERVISADO-Marcos Yamir\Tarea\ESTABLECER LA GRANULARIDAD DE FILA CORRECTA\entertainment.xlsx"

try:
    df_original = pd.read_excel(ruta_excel)
    print("✔ ¡Archivo 'entertainment.xlsx' cargado exitosamente!")
except FileNotFoundError:
    print(
        f"❌ Error: No se encontró el archivo en la ruta especificada:\n{ruta_excel}"
    )
    print(
        "Intentando cargar el archivo desde el directorio local como respaldo..."
    )
    # Respaldo por si ejecutas el script guardado en la misma carpeta que el Excel
    if os.path.exists("entertainment.xlsx"):
        df_original = pd.read_excel("entertainment.xlsx")
        print("✔ Archivo cargado desde el directorio local.")
    else:
        raise FileNotFoundError(
            "No se pudo localizar el archivo en ninguna ruta."
        )

# =============================================================================
# 2. COMPROBAR EL NÚMERO DE FILAS Y COLUMNAS DEL DATASET ORIGINAL
# =============================================================================
print("\n=== Dimensiones del DataFrame Original ===")
filas_orig, columnas_orig = df_original.shape
print(f"• Total de filas originales: {filas_orig}")
print(f"• Total de columnas originales: {columnas_orig}")
print("\nVista previa de los primeros 5 registros originales:")
print(df_original.head())

# =============================================================================
# 3. DETERMINAR LA GRANULARIDAD DE LAS FILAS NECESARIA
# =============================================================================
# EXPLICACIÓN ANALÍTICA:
# La granularidad actual es demasiado fina (por transacciones o registros repetidos).
# El líder del proyecto requiere un análisis "a nivel de estudiante". Por lo tanto,
# la nueva granularidad debe ser: 1 Fila = 1 Estudiante Único.
# Gracias a la pista, sabemos que el objetivo final son exactamente 150 filas.

# =============================================================================
# 4. APLICAR LA TRANSFORMACIÓN ADECUADA AL DATAFRAME
# =============================================================================
# Como estamos preparando datos para Machine Learning No Supervisado, 
# la mejor forma de obtener 1 estudiante por fila es usando 'pivot_table'.
# Esto convertirá las categorías de entretenimiento en columnas.

df_transformado = df_original.pivot_table(
    index='name',                 # 1 fila por cada nombre de estudiante
    columns='entertainment',      # Las categorías (video_games, etc.) serán columnas
    values='hours_per_week',      # Los valores a rellenar son las horas
    aggfunc='sum'                 # Si hay duplicados, los sumamos
).reset_index()                   # Para que 'name' vuelva a ser una columna normal

# Llenamos con 0 en caso de que algún estudiante no tenga horas en alguna categoría
df_transformado = df_transformado.fillna(0)

# Para limpiar el nombre del eje de las columnas que genera pivot_table:
df_transformado.columns.name = None

# =============================================================================
# 5. GUARDAR LA TRANSFORMACIÓN COMO UN NUEVO DATAFRAME
# =============================================================================
# (La transformación ya ha sido almacenada en la variable `df_transformado`)

# =============================================================================
# 6. COMPROBAR EL NÚMERO DE FILAS Y COLUMNAS DEL NUEVO DATAFRAME
# =============================================================================
print("\n=== Dimensiones del DataFrame Transformado ===")
filas_nuevo, columnas_nuevo = df_transformado.shape
print(f"• Total de filas (Estudiantes únicos): {filas_nuevo}")
print(f"• Total de columnas resultantes: {columnas_nuevo}")

# Validación automática de la pista proporcionada
if filas_nuevo == 150:
    print(
        "\n⭐ ¡ÉXITO! El DataFrame ha alcanzado la granularidad correcta de 150 filas."
    )
else:
    print(
        f"\n⚠️ Alerta: El DataFrame resultante tiene {filas_nuevo} filas en lugar de 150."
    )
    print(
        f"Verifica si la columna '{columna_clave}' es la correcta para identificar a tus estudiantes."
    )

print("\nVista previa de los primeros 5 estudiantes transformados:")
print(df_transformado.head())

# Opcional: Si deseas guardar este resultado limpio en un nuevo archivo Excel para tu entrega
# ruta_salida = r"C:\UPMH\3er CUATRIMESTRE\03-Sabado1_APRENDISAJE AUTOMATICO NO SUPERVISADO-Marcos Yamir\Tarea\ESTABLECER LA GRANULARIDAD DE FILA CORRECTA\entertainment_agrupado.xlsx"
# df_transformado.to_excel(ruta_salida, index=False)
# print(f"\n[INFO] Archivo corregido guardado en: {ruta_salida}")