import csv
import os
from datetime import datetime

def export_to_csv(data):
    """
    Экспортирует данные в CSV файл.
    """
    # Получаем абсолютный путь к директории, где находится этот файл
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Строим путь к price_history.csv относительно base_dir
    file_path = os.path.join(base_dir, '..', 'price_history.csv')

    file_exists = os.path.isfile(file_path)
    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "product_name", "price", "url"])

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, data["product_name"], data["price"], data["url"]])
