import sqlite3

# Подключение к базе данных
connection = sqlite3.connect('products.db')
cursor = connection.cursor()

# Добавление продуктов в таблицу
def __add_products():
    """
    Добавляет записи в таблицу Products, если они еще не добавлены.
    """
    products = [
        ("Продукт 1", "Описание продукта 1", 100),
        ("Продукт 2", "Описание продукта 2", 200),
        ("Продукт 3", "Описание продукта 3", 300),
        ("Продукт 4", "Описание продукта 4", 400),
    ]
    for title, description, price in products:
        cursor.execute(
            '''
            INSERT INTO Products (title, description, price)
            VALUES (?, ?, ?)
            ''',
            (title, description, price)
        )
    connection.commit()

# Проверка, существует ли пользователь
def is_included(username):
    """
    Проверяет, существует ли пользователь в таблице Users.
    """
    count = cursor.execute(
        '''
        SELECT COUNT(*)
        FROM Users
        WHERE username = ?
        ''',
        (username,)
    ).fetchone()
    return count[0] > 0

# Добавление пользователя в таблицу
def add_user(username, email, age, balance=1000):
    """
    Добавляет нового пользователя в таблицу Users.
    """
    cursor.execute(
        '''
        INSERT INTO Users (username, email, age, balance)
        VALUES (?, ?, ?, ?)
        ''',
        (username, email, age, balance)
    )
    connection.commit()

# Получение всех продуктов из таблицы
def get_all_products():
    """
    Возвращает все записи из таблицы Products.
    """
    cursor.execute('SELECT * FROM Products')
    return cursor.fetchall()

# Инициализация базы данных
def initiate_db():
    """
    Создаёт таблицы Products и Users, если они не существуют.
    Заполняет таблицу Products базовыми данными.
    """
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
    )
    ''')
    # Если таблица Products пуста, заполняем её продуктами
    if not cursor.execute('SELECT 1 FROM Products LIMIT 1').fetchone():
        __add_products()
    connection.commit()

# Вызов функции инициализации базы данных при запуске модуля
initiate_db()
