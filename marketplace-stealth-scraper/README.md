# Marketplace Stealth Scraper

Инструмент для сбора цен с маркетплейсов с минимальным следом и обходом антибот-защиты. Использует Playwright, прокси, YAML-конфигурацию и Telegram-уведомления.

## 🎯 Цель проекта

- Мониторить цены на несколько товаров одновременно
- Работать незаметно для систем антибота
- Уведомлять пользователя при нахождении выгодной цены
- Хранить историю цен в CSV
- Быть готовым к запуску на VPS или в Docker

## ⚙️ Функциональность

| Возможность | Описание |
|---|---|
| 🎭 Anti-detect режим | Настроенные User-Agent, локаль, куки |
| 🌐 Прокси | Поддержка авторизованных прокси |
| 📈 Мониторинг | Сбор цен по расписанию для нескольких товаров |
| 📬 Telegram уведомления | Умные оповещения при достижении пороговой цены |
| 🔐 .env конфигурация | Все чувствительные данные хранятся отдельно |
| 📜 YAML-конфигурация | Гибкая настройка списка товаров и параметров скрейпинга |
| 📊 CSV Экспорт | Сохранение истории цен в `price_history.csv` |
| 🐳 Docker-ready | Возможность собрать и запустить в контейнере |

## 🗂 Структура проекта

```bash
marketplace-stealth-scraper/
├── config/
│   └── config.yaml         # Конфигурация товаров и настроек
├── core/
│   ├── scraper.py          # Логика скрейпинга
│   ├── notifier.py         # Отправка Telegram-уведомлений
│   ├── exporter.py         # Экспорт данных в CSV
│   └── config.py           # Загрузка конфигураций
├── .env                    # Конфиденциальные настройки
├── requirements.txt        # Зависимости
├── run.py                  # Основной файл для запуска
├── Dockerfile              # Docker-конфигурация
├── .dockerignore           # Исключения для Docker-сборки
└── README.md               # Документация
```

## 🔐 Как использовать

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
playwright install
```

### 2. Настройка .env
Заполните файл `.env` своими данными:
```ini
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
# Опционально, если используете прокси
PROXY_SERVER=http://proxy_ip:port
PROXY_USER=your_user
PROXY_PASS=your_pass
```

### 3. Настройка `config.yaml`
Отредактируйте `config/config.yaml` для добавления своих товаров:
```yaml
products:
  - name: "iPhone 14"
    url: "https://example.com/product/iphone14"
    selector: "span.price"
    threshold: 700

  - name: "MacBook Air"
    url: "https://example.com/product/macbook"
    selector: ".price-value"
    threshold: 1000

settings:
  interval: 3600 # Интервал в секундах между проверками
  telegram_enabled: true
  export: csv # или none
```

### 4. Запуск
```bash
python run.py
```
Скрипт будет запускаться каждые `interval` секунд, указанных в `config.yaml`.

### 5. Запуск в Docker
Для запуска в Docker выполните следующие команды:
```bash
# Сборка образа
docker build -t stealth-scraper .

# Запуск контейнера
docker run -d --env-file .env stealth-scraper
```

## 📦 Потенциал доработки

- **Хранение в БД:** Использовать SQLite или другую БД вместо CSV.
- **Веб-интерфейс:** Создать простой дашборд на Flask/Streamlit для отображения данных.
- **Продвинутый анти-detect:** Ротация User-Agent'ов, прокси и использование `playwright-stealth`.
