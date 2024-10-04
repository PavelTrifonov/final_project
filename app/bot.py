import aiohttp
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor


# Чтение токена из файла
def read_token_from_file(filepath='app/token.txt'):
    with open(filepath, 'r') as file:
        return file.read().strip()


# Чтение API токена из файла
API_TOKEN = read_token_from_file()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Адрес сервера
SERVER_URL = 'http://localhost:5000/classify'

# Порог токсичности для предупреждения и удаления сообщения
WARNING_THRESHOLD = 0.8
DELETE_THRESHOLD = 0.9

# ID чата для приветственного сообщения
CHAT_ID = '5615077468'


# Функция для отправки приветственного сообщения
async def on_startup(dp):
    await bot.send_message(CHAT_ID, "Бот запущен и готов к работе! Отправьте сообщение для проверки на токсичность.")


# Функция для классификации токсичности через сервер
async def classify_toxicity(message: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(SERVER_URL, json={"message": message}) as response:
            if response.status == 200:
                data = await response.json()
                return data['toxicity_label'], data['score']
            return None, None


# Обработка текстовых сообщений
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_message(message: types.Message):
    user_name = message.from_user.first_name  # Имя пользователя
    text = message.text

    # Проверка токсичности через сервер
    toxicity_label, toxicity_score = await classify_toxicity(text)

    if toxicity_label == 'toxic':
        if toxicity_score >= DELETE_THRESHOLD:
            await message.delete()
            await message.answer(f"❌ {user_name}, ваше сообщение было удалено из-за слишком высокого уровня токсичности: {toxicity_score:.2f}.")
        elif toxicity_score >= WARNING_THRESHOLD:
            await message.answer(f"🔔 {user_name}, ваше сообщение имеет повышенный уровень токсичности: {toxicity_score:.2f}. Пожалуйста, будьте внимательны!")
    # Не комментируем, если уровень токсичности ниже порога WARNING_THRESHOLD

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
