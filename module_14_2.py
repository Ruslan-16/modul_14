import sqlite3

# Подключение к базе данных
connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

# Создание таблицы Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER,
    balance INTEGER NOT NULL
)
''')

# Очистка таблицы перед вставкой
cursor.execute('DELETE FROM Users')

# Данные для вставки
users = [
    ('User1', 'example1@gmail.com', 10, 1000),
    ('User2', 'example2@gmail.com', 20, 1000),
    ('User3', 'example3@gmail.com', 30, 1000),
    ('User4', 'example4@gmail.com', 40, 1000),
    ('User5', 'example5@gmail.com', 50, 1000),
    ('User6', 'example6@gmail.com', 60, 1000),
    ('User7', 'example7@gmail.com', 70, 1000),
    ('User8', 'example8@gmail.com', 80, 1000),
    ('User9', 'example9@gmail.com', 90, 1000),
    ('User10', 'example10@gmail.com', 100, 1000),
]

# Заполнение таблицы данными
cursor.executemany('''
INSERT INTO Users (username, email, age, balance)
VALUES (?, ?, ?, ?)
''', users)

# Обновляем balance у каждой второй записи, начиная с первой
cursor.execute('''
UPDATE Users
SET balance = 500
WHERE id % 2 = 1
''')

# Удаляем каждую третью запись начиная с первой
cursor.execute('''
DELETE FROM Users
WHERE (id - 1) % 3 = 0
''')

# Удаление пользователя с id = 6
cursor.execute('''
DELETE FROM Users
WHERE id = 6
''')

# Подсчет общего количества записей
cursor.execute('SELECT COUNT(*) FROM Users')
total_users = cursor.fetchone()[0]

# Подсчет суммы всех балансов
cursor.execute('SELECT SUM(balance) FROM Users')
all_balances = cursor.fetchone()[0]

# Расчет и вывод среднего баланса
average_balance = all_balances / total_users
print(f"Средний баланс: {average_balance}")
#print(f"общего количества: {total_users}")
# Сохранение изменений и закрытие соединения
connection.commit()

