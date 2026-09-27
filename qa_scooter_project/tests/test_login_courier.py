import requests
import allure
import pytest
from data import URLS

                                                             # 1. Проверка: курьер может авторизоваться
@allure.title("Успешная авторизация курьера и получение ID") # 2. Проверка: успешный запрос возвращает id
def test_courier_login_success(clean_courier):
    # Берем валидные данные курьера, которого нам создала фикстура clean_courier
    payload = {
        "login": clean_courier["login"],
        "password": clean_courier["password"]
    }
    
    response = requests.post(URLS.LOGIN_COURIER, json=payload)
    
    # Успешный запрос возвращает код 200
    assert response.status_code == 200
    # Тело ответа содержит id курьера, и это число
    assert "id" in response.json()
    assert isinstance(response.json()["id"], int)


                                                            # 3. Проверка: для авторизации нужно передать все обязательные поля
                                                             # 4. Проверка: если какого-то поля нет, запрос возвращает ошибку
@pytest.mark.parametrize("missing_field", ["login", "password"])
def test_courier_login_missing_field_error(clean_courier, missing_field):
    allure.dynamic.title(f"Ошибка авторизации курьера при отсутствии поля: {missing_field}")

    payload = {
        "login": clean_courier["login"],
        "password": clean_courier["password"]
    }
    
    # Поочередно удаляем одно из обязательных полей перед отправкой запроса
    del payload[missing_field]
    
    response = requests.post(URLS.LOGIN_COURIER, json=payload)
    
    # Запрос возвращает ошибку 400 Bad Request
    assert response.status_code == 400
    assert response.json()["message"] == "Недостаточно данных для входа"


                                                                 # 5. Проверка: система вернёт ошибку, если неправильно указать логин или пароль
@pytest.mark.parametrize("wrong_credentials", [
    {"login": "incorrect_login_xyz", "password": "valid_password"},  # неверный логин
    {"login": "valid_login", "password": "incorrect_password_xyz"}   # неверный пароль
])
def test_courier_login_wrong_credentials_error(clean_courier, wrong_credentials):
    error_type = "логином" if wrong_credentials["login"] != "valid_login" else "паролем"
    allure.dynamic.title(f"Ошибка авторизации курьера с неверным {error_type}")
    # Если в параметре указан "valid_login", берем настоящий логин из фикстуры, иначе фальшивый

    login = clean_courier["login"] if wrong_credentials["login"] == "valid_login" else wrong_credentials["login"]
    # Если в параметре указан "valid_password", берем настоящий пароль из фикстуры, иначе фальшивый
    password = clean_courier["password"] if wrong_credentials["password"] == "valid_password" else wrong_credentials["password"]
    
    payload = {
        "login": login,
        "password": password
    }
    
    response = requests.post(URLS.LOGIN_COURIER, json=payload)
    
    # Запрос возвращает ошибку 404 Not Found
    assert response.status_code == 404
    assert response.json()["message"] == "Учетная запись не найдена"


@allure.title("Ошибка авторизации под несуществующим пользователем") # 6. Проверка: если авторизоваться под несуществующим пользователем, запрос возвращает ошибку
def test_courier_login_non_existent_user_error():
    payload = {
        "login": "completely_non_existent_user_987654",
        "password": "some_password_123"
    }
    
    response = requests.post(URLS.LOGIN_COURIER, json=payload)
    
    # Запрос возвращает ошибку 404 Not Found
    assert response.status_code == 404
    assert response.json()["message"] == "Учетная запись не найдена"