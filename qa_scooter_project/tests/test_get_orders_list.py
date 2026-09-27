import requests
import allure
from data import URLS

class TestGetOrdersList:

 @allure.title("Проверка получения списка заказов") # Проверка: в тело ответа возвращается список заказов
 def test_get_orders_list_success(self):
    # Отправляем GET-запрос на получение списка заказов
    response = requests.get(URLS.GET_ORDERS)
    
    # Проверяем, что сервер ответил успешным кодом 200 OK
    assert response.status_code == 200
    
    # Проверяем, что в JSON-ответе есть ключ "orders"
    assert "orders" in response.json()
    
    # Проверяем, что значение под ключом "orders" — это именно список (массив)
    assert isinstance(response.json()["orders"], list)