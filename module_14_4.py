from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import logging
from aiogram.types import FSInputFile
from crud_functions import initiate_db, get_all_products
# Логирование
logging.basicConfig(level=logging.INFO)

# Создаем класс для работы с состояниями
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# Инициализация бота и диспетчера
API_TOKEN = "------------------"
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Создаем Reply-клавиатуру для главного меню
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Рассчитать"), KeyboardButton(text="Информация")],
        [KeyboardButton(text="/start"), KeyboardButton(text="Купить")]
    ],
    resize_keyboard=True
)

# Создаем Inline-клавиатуру для выбора действий
inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")],
    [InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")]
])

# Создаем Inline-клавиатуру для продуктов
product_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Product1", callback_data="product_buying")],
    [InlineKeyboardButton(text="Product2", callback_data="product_buying")],
    [InlineKeyboardButton(text="Product3", callback_data="product_buying")],
    [InlineKeyboardButton(text="Product4", callback_data="product_buying")]
])

# --- Обработчики бота ---
# Обработчик команды /start
@dp.message(F.text == "/start")
async def start_command(message: Message):
    await message.answer(
        "Привет! Я помогу рассчитать вашу норму калорий.\n"
        "Нажмите 'Рассчитать', чтобы начать, или 'Информация', чтобы узнать больше.",
        reply_markup=keyboard
    )

# Обработчик кнопки "Информация"
@dp.message(F.text == "Информация")
async def info_command(message: Message):
    await message.answer(
        "Этот бот помогает рассчитать вашу дневную норму калорий на основе возраста, роста и веса.\n"
        "Нажмите 'Рассчитать', чтобы начать!"
    )

# Обработчик кнопки "Рассчитать" для главного меню
@dp.message(F.text == "Рассчитать")
async def main_menu(message: Message):
    await message.answer(
        "Выберите опцию:",
        reply_markup=inline_keyboard
    )

# Обработчик для кнопки "Формулы расчёта"
@dp.callback_query(F.data == "formulas")
async def get_formulas(call: CallbackQuery):
    await call.message.answer(
        "Формула Миффлина-Сан Жеора для мужчин:\n"
        "10 × вес (кг) + 6.25 × рост (см) − 5 × возраст (лет) + 5\n\n"
        "Для женщин:\n"
        "10 × вес (кг) + 6.25 × рост (см) − 5 × возраст (лет) − 161"
    )
    await call.answer()

# Обработчик для кнопки "Рассчитать норму калорий"
@dp.callback_query(F.data == "calories")
async def set_age(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите свой возраст:")
    await state.set_state(UserState.age)
    await call.answer()

# Обработчик для получения возраста и перехода к росту
@dp.message(UserState.age)
async def set_growth(message: Message, state: FSMContext):
    age = message.text
    if not age.isdigit():
        await message.answer("Возраст должен быть числом. Попробуйте ещё раз:")
        return
    await state.update_data(age=int(age))
    await message.answer("Введите свой рост (в см):")
    await state.set_state(UserState.growth)

# Обработчик для получения роста и перехода к весу
@dp.message(UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    growth = message.text
    if not growth.isdigit():
        await message.answer("Рост должен быть числом. Попробуйте ещё раз:")
        return
    await state.update_data(growth=int(growth))
    await message.answer("Введите свой вес (в кг):")
    await state.set_state(UserState.weight)

# Обработчик для получения веса и вычисления калорий
@dp.message(UserState.weight)
async def send_calories(message: Message, state: FSMContext):
    weight = message.text
    if not weight.isdigit():
        await message.answer("Вес должен быть числом. Попробуйте ещё раз:")
        return
    await state.update_data(weight=int(weight))
    data = await state.get_data()
    age = data.get("age")
    growth = data.get("growth")
    weight = data.get("weight")
    calories = 10 * weight + 6.25 * growth - 5 * age - 161
    await message.answer(f"Ваша норма калорий: {calories:.2f} ккал в день.")
    await state.clear()

# Функция для отображения списка продуктов

async def get_buying_list(message: types.Message):
    products = [
        {'title': 'Product1', 'description': 'Описание продукта 1', 'price': 100, 'image': 'product1.jpg'},
        {'title': 'Product2', 'description': 'Описание продукта 2', 'price': 200, 'image': 'product2.jpg'},
        {'title': 'Product3', 'description': 'Описание продукта 3', 'price': 300, 'image': 'product3.jpg'},
        {'title': 'Product4', 'description': 'Описание продукта 4', 'price': 400, 'image': 'product4.jpg'},
    ]

    for product in products:
        text = f"Название: {product['title']} | Описание: {product['description']} | Цена: {product['price']} ₽"
        try:
            # Используем FSInputFile для загрузки файла
            photo = FSInputFile(product['image'])
            await message.answer_photo(photo, caption=text)
        except FileNotFoundError:
            await message.answer(f"Не удалось загрузить изображение для {product['name']}.")

    # В конце отправляем Inline-клавиатуру для выбора продуктов
    await message.answer("Выберите продукт для покупки:", reply_markup=product_inline_keyboard)
# Обработчик для кнопки "Купить"
@dp.message(F.text == "Купить")
async def buy_command(message: Message):
    await get_buying_list(message)

# Callback хэндлер для покупки
@dp.callback_query(F.data == "product_buying")
async def product_buying_callback(call: CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

# Главная функция для запуска бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
