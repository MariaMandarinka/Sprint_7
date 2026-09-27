import requests
import allure
import pytest
from data import URLS

# Используем параметризацию для проверки всех вариантов выбора цветов по ТЗ
@pytest.mark.parametrize("color_option", [
    ["BLACK"],           # 1. Можно указать один из цветов — BLACK
    ["GREY"],            # 2. Можно указать один из цветов — GREY
    ["BLACK", "GREY"],   # 3. Можно указать оба цвета
    []                   # 4. Можно совсем не указывать цвет
])
def test_create_order_with_different_colors_success(color_option):
    # Тело запроса со всеми обязательными полями по документации
    # Превращаем список цветов в красивую строку для заголовка отчета Allure
    color_name = ", ".join(color_option) if color_option else "без указания цвета"
    allure.dynamic.title(f"Успешное создание заказа с цветом: {color_name}")
    
    order_payload = {
        "firstName": "Naruto",
        "lastName": "Uzumaki",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 999 999 99 99",
        "rentTime": 5,
        "deliveryDate": "2026-10-10",
        "comment": "Saske, come back to village",
        "color": color_option  # Pytest по очереди должен подставить каждый вариант из списка выше
    }

    # Отправляем POST-запрос на создание заказа
    response = requests.post(URLS.CREATE_ORDER, json=order_payload)

    # Проверяем, что заказ успешно создался (код 201 Created)
    assert response.status_code == 201
    
    # Проверяем, что тело ответа содержит track
    assert "track" in response.json()
    # Проверяем, что track является числом
    assert isinstance(response.json()["track"], int)