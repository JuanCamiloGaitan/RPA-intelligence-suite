from utils.logger import setup_logger
from utils.notifier import Notifier
from pages.playwright_extractor import PlaywrightExtractor
from pages.data_processor import DataProcessor
from pages.selenium_publisher import SeleniumPublisher

def run_pipeline():
    logger = setup_logger()
    logger.info("=========================================")
    logger.info("  INICIANDO WORKFLOW COMPLETO DE RPA     ")
    logger.info("=========================================")

    # 1. Extracción con Playwright (50 páginas)
    extractor = PlaywrightExtractor(logger)
    raw_csv = extractor.extract_books_data()

    # 2. Procesamiento y Limpieza con Pandas
    processor = DataProcessor(logger)
    processed_csv, stats = processor.clean_and_analyze(raw_csv)

    # 3. Carga de datos filtrados con Selenium (n# valores)
    publisher = SeleniumPublisher(logger)
    publisher.publish_data_from_csv(processed_csv, max_records=100)

    # 4. Notificación vía n8n (Usa tu URL de webhook o una de prueba)
    notifier = Notifier(logger)
    webhook_test_url = "http://localhost:5678/webhook-test/6adab1b3-00a4-42ec-9b0f-e844d5b1585e"  # Puedes cambiarlo por tu URL de n8n
    notifier.send_n8n_notification(webhook_test_url, stats)

    logger.info("=========================================")
    logger.info("  WORKFLOW COMPLETO FINALIZADO CON ÉXITO ")
    logger.info("=========================================")

if __name__ == "__main__":
    run_pipeline()