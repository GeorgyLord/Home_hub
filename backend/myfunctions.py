from datetime import datetime

def get_current_date():
    # Получаем текущую дату и форматируем её в строку (ДД.ММ.ГГГГ)
    return datetime.now().strftime("%d.%m.%Y")

def get_current_date_format_1():
    # Получаем текущую дату и форматируем её в строку (ГГ-ММ-ДД)
    return datetime.now().strftime("%Y-%m-%d")

def format_short_date(date_str: str) -> str:
    if not date_str:
        return ""
    # 1. Парсим строку в объект даты
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    # 2. Форматируем обратно в строку: %d (день), %m (месяц), %y (две цифры года)
    return date_obj.strftime("%d.%m.%y")

# Пример вызова:
# print(get_current_date())  # Выведет, например: 18.10.2026
# print(get_current_date_format_1())