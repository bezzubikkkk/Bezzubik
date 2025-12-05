import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Конфигурация
TOKEN = os.getenv("TELEGRAM_TOKEN", "8138177078:AAFiOjWh0lef8PLrttaaOgX6wKwjj94H_XY")
ADMIN_ID = int(os.getenv("ADMIN_ID", "7563541835"))

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Формируем имя для приветствия
    if user.first_name and user.last_name:
        # Если есть и имя, и фамилия
        user_name = f"{user.first_name} {user.last_name}"
    elif user.first_name:
        # Если только имя
        user_name = user.first_name
    elif user.last_name:
        # Если только фамилия (редкий случай)
        user_name = user.last_name
    else:
        # Если нет ни имени, ни фамилии
        user_name = "друг"
    
    # Приветствие с именем пользователя
    welcome_text = f"👋 Приветствую, {user_name}!\n\n"
    
    welcome_text += (
        "   Я бот-предложка канала 'Нижневартовск Вэйп Барахолка(НВБ)'\n"
        "   📤  Отправьте мне свой пост одним сообщением и строго соблюдая эти критерии (иначе не опубликуется!):\n\n"
        "1. Фото товара и цена\n"
        "2. Краткое описание и ваш юзернейм для связи\n"
        "3. ❌ Скриншоты с других барахолок запрещены\n"
        "4. ❌ Фото с чеками из магазинов удаляются\n"
        "5. ❌ Продажа новых устройств, испарителей, жидкостей запрещена\n\n"

        "  🍀  Желаю вам удачных продаж и покупок!"
    )
    
    await update.message.reply_text(welcome_text)

# Обработка всех сообщений от пользователей
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Получаем информацию о пользователе
        user = update.effective_user
        
        # Формируем полное имя для отчета админу
        full_name = ""
        if user.first_name:
            full_name += user.first_name
        if user.last_name:
            if full_name:
                full_name += " "
            full_name += user.last_name
        
        user_info = f"📨 Новый пост от:\nID: {user.id}"
        if full_name:
            user_info += f"\nИмя: {full_name}"
        if user.username:
            user_info += f"\nUsername: @{user.username}"
        
        # Если это команда - игнорируем
        if update.message.text and update.message.text.startswith('/'):
            return
            
        # Уведомляем пользователя
        await update.message.reply_text("✅ Спасибо! Твой пост отправлен на модерацию.\n\nДля отправки следующего поста нажми /start")
        
        # Пересылаем сообщение администратору
        await update.message.forward(chat_id=ADMIN_ID)
        
        # Отправляем информацию о пользователе
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=user_info
        )
        
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text("❌ Произошла ошибка. Попробуй позже.")

# Основная функция
def main():
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()
    
    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    # Обрабатываем все сообщения, кроме команд
    application.add_handler(MessageHandler(
        filters.ALL & ~filters.COMMAND, 
        handle_message
    ))
    
    # Запускаем бота
    print("🤖 Бот 'Нижневартовск Вэйп Барахолка' запущен...")
    print("📱 Перейдите в Telegram и напишите /start")
    application.run_polling()

if __name__ == '__main__':
    main()
