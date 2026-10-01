import pandas as pd
import os

class DataProcessor:
    def __init__(self, logger):
        self.logger = logger

    def clean_and_analyze(self, csv_input_path):
        self.logger.info(f"[Pandas] Procesando y limpiando datos desde: {csv_input_path}")
        
        if not os.path.exists(csv_input_path):
            self.logger.error(f"[Pandas] Archivo no encontrado: {csv_input_path}")
            return None

        df = pd.read_csv(csv_input_path)

        # 1. Limpieza de Precios: Convertir '£51.77' -> 51.77 (float)
        df['Precio_Num'] = df['Precio'].str.replace('£', '', regex=False).astype(float)

        # 2. Normalización de Disponibilidad
        df['Disponible'] = df['Disponibilidad'].str.contains('In stock', case=False, na=False)

        # 3. Filtrado de Negocio: Solo libros en stock y con precio menor a £30
        df_filtered = df[(df['Disponible'] == True) & (df['Precio_Num'] < 30.0)].copy()

        # 4. Estadísticas del proceso
        stats = {
            "total_extraidos": len(df),
            "total_filtrados": len(df_filtered),
            "precio_promedio": round(df['Precio_Num'].mean(), 2),
            "libro_mas_caro": df.loc[df['Precio_Num'].idxmax()]['Titulo'],
            "precio_max": df['Precio_Num'].max()
        }

        self.logger.info(f"[Pandas] Estadísticas: Total={stats['total_extraidos']} | Filtrados (<£30)={stats['total_filtrados']} | Precio Promedio=£{stats['precio_promedio']}")

        # 5. Guardar CSV procesado para Selenium
        output_csv = "data/processed_data.csv"
        df_filtered.to_csv(output_csv, index=False, encoding="utf-8-sig")

        # 6. Exportar Reporte Ejecutivo en Excel con Pandas
        output_excel = "data/Reporte_Ejecutivo_Libros.xlsx"
        with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name="Todos los Libros", index=False)
            df_filtered.to_excel(writer, sheet_name="Oportunidades (<£30)", index=False)

        self.logger.info(f"[Pandas] Reporte generado exitosamente en '{output_excel}'.")
        return output_csv, stats