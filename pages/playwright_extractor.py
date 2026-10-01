from playwright.sync_api import sync_playwright
import pandas as pd
import os

class PlaywrightExtractor:
    def __init__(self, logger):
        self.logger = logger

    def extract_books_data(self, base_url="https://books.toscrape.com/"):
        self.logger.info(f"[Playwright] Iniciando extracción masiva de 50 páginas desde: {base_url}")
        results = []
        page_number = 1

        with sync_playwright() as p:
            # Lanzamos Chromium en modo headless
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(base_url)

            while True:
                # Extraer productos de la página actual
                products = page.query_selector_all(".product_pod")
                self.logger.info(f"[Playwright] Pág. {page_number}: {len(products)} libros encontrados.")

                for item in products:
                    title = item.query_selector("h3 a").get_attribute("title")
                    price = item.query_selector(".price_color").inner_text()
                    stock = item.query_selector(".instock.availability").inner_text().strip()

                    results.append({
                        "Pagina": page_number,
                        "Titulo": title,
                        "Precio": price,
                        "Disponibilidad": stock
                    })

                # Buscar el botón de navegación a la siguiente página (li.next a)
                next_button = page.query_selector("li.next a")

                if next_button:
                    page_number += 1
                    # Clic en el botón siguiente y esperar a que la red/DOM cargue
                    next_button.click()
                    page.wait_for_selector(".product_pod")
                else:
                    self.logger.info("[Playwright] Se alcanzó la última página del catálogo.")
                    break

            browser.close()

        # Guardar en Pandas DataFrame y exportar a CSV
        os.makedirs("data", exist_ok=True)
        df = pd.DataFrame(results)
        output_path = "data/extracted_data.csv"
        df.to_csv(output_path, index=False, encoding="utf-8-sig")  # utf-8-sig evita problemas con acentos en Excel
        
        self.logger.info(f"[Playwright] Extracción masiva completada exitosamente.")
        self.logger.info(f"[Playwright] Total de libros procesados: {len(df)} en {page_number} páginas.")
        self.logger.info(f"[Playwright] Archivo final guardado en '{output_path}'.")
        
        return output_path