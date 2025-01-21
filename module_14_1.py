import sqlite3


connection= sqlite3.connect('not_telegram.db')
cursor=connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER,
    balance INTEGER NOT NULL
)
''')
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
# SQL-запрос для вставки записей
cursor.executemany('''
INSERT INTO Users (username, email, age, balance)
VALUES (?, ?, ?, ?)
''', users)

# Обновляем balance у каждой второй записи начиная с первой
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

# Выполняем запрос для выборки записей, где возраст не равен 60
cursor.execute('''
SELECT username, email, age, balance
FROM Users
WHERE age != 60
''')
# Получаем все записи
records = cursor.fetchall()

# Выводим записи в консоль в заданном формате
for record in records:
    username, email, age, balance = record
    print(f"Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}")

connection.commit()

# Закрываем соединение
connection.close()