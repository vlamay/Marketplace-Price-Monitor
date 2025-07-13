from core.scraper import run_scraper
import time
from core.config import SETTINGS

if __name__ == "__main__":
    interval = SETTINGS.get("interval", 3600)
    while True:
        run_scraper()
        print(f"Пауза на {interval} секунд перед следующим запуском.")
        time.sleep(interval)
