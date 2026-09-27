# Базовый URL учебного сервиса
BASE_URL = 'https://qa-scooter.praktikum-services.ru'

class URLS:
    CREATE_COURIER = f"{BASE_URL}/api/v1/courier"
    LOGIN_COURIER = f"{BASE_URL}/api/v1/courier/login"  # <-- Добавили эту строчку
    DELETE_COURIER = f"{BASE_URL}/api/v1/courier"  # Ручка для удаления (к ней в коде прибавляется /:id)
    CREATE_ORDER = f"{BASE_URL}/api/v1/orders"
    GET_ORDERS = f"{BASE_URL}/api/v1/orders"