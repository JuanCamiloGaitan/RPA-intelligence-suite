import requests
import json

class Notifier:
    def __init__(self, logger):
        self.logger = logger

    def send_n8n_notification(self, webhook_url, stats):
        """Envia un payload JSON a un Webhook de n8n."""
        self.logger.info("[n8n] Enviando resumen de ejecución al webhook...")

        payload = {
            "evento": "RPA_Execution_Finished",
            "bot_name": "RPA Intelligence Suite",
            "status": "Success",
            "metricas": stats
        }

        try:
            # Enviamos la petición POST
            response = requests.post(webhook_url, json=payload, timeout=5)
            if response.status_code == 200:
                self.logger.info("[n8n] Notificación entregada con éxito a n8n.")
            else:
                self.logger.warning(f"[n8n] El webhook respondió con código: {response.status_code}")
        except Exception as e:
            self.logger.error(f"[n8n] No se pudo conectar con el webhook: {str(e)}")