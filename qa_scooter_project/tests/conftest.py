import pytest
import requests
from data import URLS
from helpers import generate_courier_payload

@pytest.fixture
def clean_courier():
    """
    Фикстура для создания курьера перед тестом 
    и его автоматического удаления ПОСЛЕ завершения теста.
    """
    # [SETUP] Создаем уникального курьера
    payload = generate_courier_payload()
    register_response = requests.post(URLS.CREATE_COURIER, json=payload)
    
    courier_data = {
        "login": payload["login"],
        "password": payload["password"],
        "id": None
    }
    
    # Пытаемся сразу узнать ID курьера через логин, чтобы потом его удалить
    login_payload = {"login": payload["login"], "password": payload["password"]}
    login_response = requests.post(URLS.LOGIN_COURIER, json=login_payload)
    if login_response.status_code == 200:
        courier_data["id"] = login_response.json().get("id")

    # Передаем данные курьера в тест
    yield courier_data

    # [TEARDOWN] Этот код выполнится автоматически, когда тест закончится
    # Если ID курьера известен, удаляем его из базы Самоката
    if courier_data["id"]:
        requests.delete(f"{URLS.CREATE_COURIER}/{courier_data['id']}")
    else:
        # Если во время теста курьер не залогинился, пробуем узнать ID еще раз перед удалением
        login_response = requests.post(URLS.LOGIN_COURIER, json=login_payload)
        if login_response.status_code == 200:
            c_id = login_response.json().get("id")
            requests.delete(f"{URLS.CREATE_COURIER}/{c_id}")