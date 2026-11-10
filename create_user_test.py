
import sender_stand_request
import data


# Создаём копию тела запроса и меняем имя пользователя
def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body


# Общая функция для позитивных тестов
def positive_assert(first_name):
    # Подготавливаем данные пользователя
    user_body = get_user_body(first_name)

    # Отправляем POST-запрос на создание пользователя
    user_response = sender_stand_request.post_new_user(user_body)

    # Проверяем статус 201 Created
    assert user_response.status_code == 201

    # Проверяем наличие непустого токена
    assert user_response.json()["authToken"] != ""

    # Получаем таблицу пользователей
    users_table_response = sender_stand_request.get_users_table()

    # Проверяем успешность получения таблицы
    assert users_table_response.status_code == 200

    # Составляем строку с данными созданного пользователя
    str_user = (
        user_body["firstName"] + "," +
        user_body["phone"] + "," +
        user_body["address"] + ",,," +
        user_response.json()["authToken"]
    )

    # Проверяем, что запись встречается ровно один раз
    assert users_table_response.text.count(str_user) == 1


# Общая функция для негативных тестов
def negative_assert(first_name):
    # Подготавливаем данные пользователя
    user_body = get_user_body(first_name)

    # Отправляем POST-запрос
    user_response = sender_stand_request.post_new_user(user_body)

    # Проверяем статус 400 Bad Request
    assert user_response.status_code == 400

    # Проверяем код ошибки в JSON
    assert user_response.json()["code"] == 400

    # Проверяем сообщение об ошибке
    assert (
        "Имя пользователя введено некорректно"
        in user_response.json()["message"]
    )


# ТЕСТ 1
# Допустимое количество символов — 2
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")


# ТЕСТ 2
# Допустимое количество символов — 15
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("А" * 15)


# ТЕСТ 3
# Недопустимое количество символов — 1
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert("А")


# ТЕСТ 4
# Недопустимое количество символов — 16
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert("А" * 16)


# ТЕСТ 5
# Разрешённые латинские буквы
def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("QWErty")


# ТЕСТ 6
# Разрешённые русские буквы
def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert("Мария")


# ТЕСТ 7
# Запрещённые пробелы в имени
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert("Человек и Ко")


# ТЕСТ 8
# Запрещённые спецсимволы
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert("№%@!")


# ТЕСТ 9
# Запрещённые цифры
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert("123")


# ТЕСТ 10
# Параметр firstName отсутствует
def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")

    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400
    assert (
        user_response.json()["message"]
        == "Не все необходимые параметры были переданы"
    )


# ТЕСТ 11
# Передано пустое значение firstName
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")

    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400
    assert (
        user_response.json()["message"]
        == "Не все необходимые параметры были переданы"
    )


# ТЕСТ 12
# Вместо строки передано число
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)

    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 400
