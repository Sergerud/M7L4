import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

def test_add_same_user(setup_database):
    """Тест добавления существующего пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    response = add_user('testuser', 'testuser@example.com', 'password123')
    #print(response)
    assert not response, "Пользователь должен быть уникален."   

def test_authenticate_user(setup_database):
    '''Тест успешной аутентификации пользователя.'''
    authenticate_user('testuser','password123')
    well = authenticate_user('testuser','password123')
    #print(well)
    assert well, "Пользователь должен ввести верные данные."

def test_absent_user(setup_database):
    "Тест аутентификации несуществующего пользователя."  
    a = authenticate_user('absent_user','password123') 
    #print(a)
    assert not a, "Пользователь должен быть зарегистрирован"

def test_wrong_pass(setup_database):
    "Тест аутентификации пользователя с неправильным паролем."
    wrongpass = authenticate_user('testuser','pass123') 
    assert not wrongpass, "ВВедите верный пароль"

def test_display_users(setup_database):
    "Тест отображения списка пользователей."
    display_users()
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT username, email FROM users')
        for user in cursor.fetchall():
            print(f"Логин: {user[0]}, Электронная почта: {user[1]}")
            assert user[0], "Отображается пользователь"+user[0]

# Возможные варианты тестов:
"""
+Тест добавления пользователя с существующим логином.
+Тест успешной аутентификации пользователя.
+Тест аутентификации несуществующего пользователя.
+Тест аутентификации пользователя с неправильным паролем.
+Тест отображения списка пользователей.
"""