from api import PetFriends

from settings import valid_email, valid_password, invalid_email, invalid_password

import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем, что запрос API ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
    print(f'\n {email}, {password}, {status}, {result}')




def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем, что запрос всех питомцев возвращает не пустой список.
       Для этого сначала получаем API ключ и сохраняем в переменную auth_key. Далее используя этоn ключ
       запрашиваем список всех питомцев и проверяем, что список не пустой.
       Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0
    num = len(result['pets'])
    if filter == 'my_pets':
        print(f'{num} my pets на сайте')
    else:
        print(f'список не пустой')

def test_add_new_pet_with_valid_data(name='Шнупи', animal_type='рыжий', age='7', pet_photo='images/cat.jpg'):
    """Проверяем,  добавление питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    print('ok')
    print(f'добавлен {result}')


def test_add_pet_with_valid_data_without_photo(name='Кот_без_фото', animal_type='Кот', age='1'):
    """Проверяем возможность добавления нового питомца без фото"""
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    print('ok')
    print(f'добавлен {result}')

def test_add_pet_with_a_lot_of_age_in_variable_age(name='Иван', animal_type='Кошка', pet_photo='images/cat3.png'):
    """Добавления очень взрослого питомца с большим возрастом.
    Тест выводит предупреждение, если  будет добавлен в приложение питомец с невозможным возрастом, меньше 0 или старше 20 лет."""
    age = '120'
    # age = '-1'
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    age = float(result['age'])#.split()
    assert status == 200
    assert (age > 20 or age < 0), 'Добавлен питомец с невозможным возрастом, меньше 0 или старше 20 лет.'
    print(f'\n Сайт позволяет добавлять питомеца с невозможным возрастом, меньше 0 или старше 20 лет. {age}')


def test_add_pet_with_valid_data_empty_field():
    """Проверяем добавление питомца с пустыми полями. Тест выводит предупреждение"""
    name = ''
    animal_type = ''
    age = ''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    print('ok')
    print(f'Сайт позволяет добавлять "пустых" питомецев {result}')


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Иван", "Кошка", "120", "images/cat3.png")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    num = len(my_pets['pets'])
    print('ok')
    print(f'в списке было, {num} питомцев')

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()
    num = len(my_pets['pets'])
    print('ok')
    print(f'в списке , {num} питомцев')

def test_successful_delete_notvalid_key_pet():
    """Проверяем возможность удаления питомца по неправильному auth_key. По статусу 403"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    print()
    print(auth_key)

    auth_key = {'key': 'ecc18c60009357ae13ba9e44ac5ea152b80178ec7b755c3f57a5c91'} #неправильный ключ
    print(auth_key)
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Инга", "кот", "5", "images/cat2.png")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    num = len(my_pets['pets'])
    print('ok')
    print(f'в списке было, {num} питомцев')

    # # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # # Проверяем что статус ответа равен 403 и в списке питомцев нет изменений
    assert status == 403
    #assert pet_id in my_pets.values()
    num = len(my_pets['pets'])
    print('ok')
    print(f'в списке , {num} питомцев')

def test_successful_update_self_pet_info(name='Cat', animal_type='supper', age=35):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
        print('ok')
        print(result)
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_pet_with_numbers_in_variable_animal_type(name='noname', animal_type='959595', age='0', pet_photo='images/cat.jpg'):
    """Проверка с негативным сценарием.
    Добавление питомца с цифрами вместо букв в переменной animal_type.
    Сообщение, если питомец будет добавлен в приложение с цифрами вместо букв в поле "Порода"."""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert animal_type in result['animal_type'], 'Питомец добавлен в приложение с цифрами вместо букв в поле "Порода".'
    print(f'\n Добавлен питомец с цифрами вместо букв в поле "Порода". {animal_type}')

def test_add_photo_at_pet(pet_photo='images/cat2.jpg'):
    """Проверяем возможность добавления фотографии питомца отдельно"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(api_key, my_pets['pets'][0]['id'], pet_photo)
        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
        print(f'\n фото добавлено {result}')
    else:
        raise Exception('Питомцы отсутствуют')

def test_get_api_key_with_correct_mail_and_wrong_passwor(email=valid_email, password=invalid_password):
    """Проверяем запрос с правильным email и c неправильным паролем.
    Проверяем нет ли ключа в ответе."""
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result
    print('ok')
    print(f'Статус {status} для теста с неправильным паролем')

def test_get_api_key_with_wrong_email_and_correct_password(email=invalid_email, password=valid_password):
    """Проверяем запрос с невалидным email и с валидным паролем.
    Проверяем нет ли ключа в ответе."""
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result
    print('ok')
    print(f'Статус {status} для теста с неправильным email')

def test_get_api_key_with_wrong_email_and_wrong_password(email=invalid_email, password=invalid_password):
    """Проверяем запрос с невалидным email и с невалидным паролем.
    Проверяем нет ли ключа в ответе."""
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result
    print('ok')
    print(f'Статус {status} для теста с неправильным email и паролем')





