import requests
import allure
import pytest
from data import URLS
from helpers import generate_courier_payload

class TestCreateCourier:

 @allure.title("Успешное создание нового курьера") # 1. Проверка: курьера можно создать, успешный запрос возвращает 201 и {"ok":true}
 def test_create_courier_success(self):
    payload = generate_courier_payload()
    
    response = requests.post(URLS.CREATE_COURIER, json=payload)
    
    # Проверяем код ответа (201 Created)
    assert response.status_code == 201
    # Проверяем тело ответа
    assert response.json() == {"ok": True}


 @allure.title("Ошибка при создании дубликата курьера") # 2. Проверка: нельзя создать двух одинаковых курьеров (с одним логином)
 def test_create_duplicate_courier_error(self):
    payload = generate_courier_payload()
    
    # Создаем первого курьера
    first_response = requests.post(URLS.CREATE_COURIER, json=payload)
    assert first_response.status_code == 201
    
    # Пытаемся создать второго с точно таким же телом запроса
    second_response = requests.post(URLS.CREATE_COURIER, json=payload)
    
    # Проверяем код ответа ошибки (409 Conflict)
    assert second_response.status_code == 409
    # Проверяем текст ошибки в теле ответа
    assert second_response.json()["message"] == "Этот логин уже используется. Попробуйте другой."


                                                       # 3. Проверка: чтобы создать курьера, нужно передать обязательные поля (логин и пароль)
                                                       # Если одного из полей нет, запрос возвращает ошибку 400
 @pytest.mark.parametrize("missing_field", ["login", "password"])
 def test_create_courier_missing_required_field_error(self, missing_field):
     # Динамически меняем название теста в отчете в зависимости от пропущенного поля
    allure.dynamic.title(f"Ошибка создания курьера при отсутствии обязательного поля: {missing_field}")
    
    payload = generate_courier_payload()
    
    # Поочередно удаляем обязательное поле из словаря перед отправкой
    del payload[missing_field]
    
    response = requests.post(URLS.CREATE_COURIER, json=payload)
    
    # Проверяем код ответа (400 Bad Request)
    assert response.status_code == 400
    # Проверяем текст сообщения об ошибке
    assert response.json()["message"] == "Недостаточно данных для создания учетной записи"