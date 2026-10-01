from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os

class SeleniumPublisher:
    def __init__(self, logger):
        self.logger = logger

    def publish_data_from_csv(self, csv_path, max_records=None):
        if not os.path.exists(csv_path):
            self.logger.error(f"[Selenium] El archivo {csv_path} no existe.")
            return

        df = pd.read_csv(csv_path)
        
        if max_records and isinstance(max_records, int):
            df_to_process = df.head(max_records)
            self.logger.info(f"[Selenium] MODO PRUEBA: Procesando solo {max_records} de {len(df)} registros.")
        else:
            df_to_process = df
            self.logger.info(f"[Selenium] MODO PRODUCCIÓN: Procesando los {len(df)} registros completos.")

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")  # Forzar resolución Full HD
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)

        try:
            driver.get("https://demoqa.com/text-box")
            self.logger.info("[Selenium] Navegando al portal de destino.")

            # Opcional: Eliminar anuncios molestos mediante JS si están presentes
            try:
                driver.execute_script("document.querySelectorAll('iframe, #fixedban').forEach(el => el.remove());")
            except Exception:
                pass

            exitosos = 0
            for index, row in df_to_process.iterrows():
                try:
                    username_input = wait.until(EC.element_to_be_clickable((By.ID, "userName")))
                    username_input.clear()
                    username_input.send_keys(f"Libro: {row['Titulo']}")

                    email_input = driver.find_element(By.ID, "userEmail")
                    email_input.clear()
                    email_input.send_keys("bot_rpa@empresa.com")

                    address_input = driver.find_element(By.ID, "currentAddress")
                    address_input.clear()
                    address_input.send_keys(f"Precio: {row['Precio']} - Pág: {row['Pagina']}")

                    # Forzar clic mediante JavaScript (Evita el ElementClickInterceptedException)
                    submit_btn = driver.find_element(By.ID, "submit")
                    driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
                    driver.execute_script("arguments[0].click();", submit_btn)

                    exitosos += 1

                    if exitosos % 50 == 0 or exitosos == len(df_to_process):
                        self.logger.info(f"[Selenium] Progreso: {exitosos}/{len(df_to_process)} registros enviados.")

                except Exception as inner_error:
                    self.logger.error(f"[Selenium] Error en registro #{index + 1}: {str(inner_error)}")
                    continue

            self.logger.info(f"[Selenium] Carga finalizada. {exitosos} registros procesados con éxito.")

        except Exception as e:
            self.logger.error(f"[Selenium] Error crítico durante la publicación: {str(e)}")
            os.makedirs("logs", exist_ok=True)
            driver.save_screenshot("logs/error_screenshot.png")

        finally:
            driver.quit()
            self.logger.info("[Selenium] Sesión finalizada.")