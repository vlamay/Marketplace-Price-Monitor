import os
import yaml
from dotenv import load_dotenv

load_dotenv()

def load_config():
    """
    Загружает конфигурацию из config.yaml.
    """
    # Получаем абсолютный путь к директории, где находится этот файл
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Строим путь к config.yaml относительно base_dir
    config_path = os.path.join(base_dir, '..', 'config', 'config.yaml')
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

# Загрузка переменных из .env
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
PROXY_SERVER = os.getenv("PROXY_SERVER")
PROXY_USER = os.getenv("PROXY_USER")
PROXY_PASS = os.getenv("PROXY_PASS")

# Загрузка конфигурации из YAML
config = load_config()
PRODUCTS = config.get("products", [])
SETTINGS = config.get("settings", {})
