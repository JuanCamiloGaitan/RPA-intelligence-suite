[← Read in English](README.english.md)

---

# Enterprise RPA Intelligence & Scraping Suite

## Visión General del Proyecto

Esta solución de Automatización Robótica de Procesos (RPA) de nivel empresarial demuestra una arquitectura híbrida moderna para la extracción masiva de datos, procesamiento ETL (Extracción, Transformación y Carga), carga automatizada en sistemas de destino e integración con flujos de orquestación low-code.

El sistema fue diseñado para resolver los desafíos comunes en entornos corporativos: rendimiento en la extracción masiva, resiliencia ante bloqueos de red o fallos en el DOM de la interfaz gráfica, transformación estructurada de datos y notificaciones ejecutivas en tiempo real.

---

## Arquitectura de la Solución

El flujo de trabajo sigue una arquitectura por capas desacoplada en cuatro fases principales:

```text
+-----------------------------------------------------------------------------------+
| 1. EXTRACCIÓN MASIVA          2. ETL & TRANSFORMACIÓN        3. CARGA DE DATOS    |
|   (Playwright)                   (Pandas)                      (Selenium)         |
|                                                                                   |
|  Scraping asíncrono   --->     Limpieza de datos       --->    Formularios Web    |
|  de 50 páginas                 Filtrado por reglas             Manejo de DOM      |
|  (~1,000 registros)            Reporte en Excel                Intercepción JS    |
+-----------------------------------------------------------------------------------+
                                                                   |
                                                                   v
                                                        4. ORQUESTACIÓN & ALERTAS
                                                           (n8n & Webhooks)
                                                                   |
                                                                   v
                                                        Notificaciones por Email /
                                                        Monitoreo de ejecución
