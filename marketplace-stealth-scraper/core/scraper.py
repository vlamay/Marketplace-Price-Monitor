import time
import random
import logging
from playwright.sync_api import sync_playwright
from core.config import PROXY_SERVER, PROXY_USER, PROXY_PASS, PRODUCTS, SETTINGS
from core.notifier import send_telegram_message
from core.exporter import export_to_csv

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_price(page, selector):
    """
    Получает цену товара по селектору.
    """
    try:
        price_element = page.query_selector(selector)
        if price_element:
            return price_element.inner_text().strip()
    except Exception as e:
        logging.error(f"Ошибка при получении цены: {e}")
    return None

def scrape_product(page, product):
    """
    Скрейпит один продукт.
    """
    url = product["url"]
    name = product["name"]
    selector = product["selector"]
    threshold = product.get("threshold")

    try:
        logging.info(f"Переход на страницу: {url}")
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        time.sleep(random.uniform(3, 7))

        price = get_price(page, selector)

        if price:
            logging.info(f"Цена для '{name}' найдена: {price}")

            # Экспорт в CSV
            if SETTINGS.get("export") == "csv":
                export_to_csv({
                    "product_name": name,
                    "price": price,
                    "url": url
                })

            # Уведомление в Telegram
            if SETTINGS.get("telegram_enabled"):
                message = f"Найдена цена на {name}: <b>{price}</b>"
                if threshold and float(price.replace("$", "").replace(",", "")) < threshold:
                    message = f"🔥 <b>Deal Found!</b>\nProduct: `{name}`\nPrice: `{price}`\n<a href='{url}'>🔗 Open Product</a>"
                send_telegram_message(message)

        else:
            logging.warning(f"Не удалось найти цену для '{name}' на странице.")
            if SETTINGS.get("telegram_enabled"):
                send_telegram_message(f"Не удалось найти цену для {name} на {url}")

    except Exception as e:
        logging.error(f"Произошла ошибка при обработке '{name}': {e}")
        if SETTINGS.get("telegram_enabled"):
            send_telegram_message(f"Ошибка при парсинге {name}: {e}")

def run_scraper():
    """
    Запускает скрейпер для всех продуктов из конфигурации.
    """
    with sync_playwright() as p:
        proxy = {
            "server": PROXY_SERVER,
            "username": PROXY_USER,
            "password": PROXY_PASS
        } if PROXY_SERVER else None

        browser = p.chromium.launch(headless=True, proxy=proxy)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            locale='en-US'
        )
        page = context.new_page()

        for product in PRODUCTS:
            scrape_product(page, product)
            time.sleep(random.uniform(5, 15)) # Задержка между продуктами

        browser.close()
