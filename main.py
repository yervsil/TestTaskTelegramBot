import telebot

from controllers.controllers import TodoBotController
from views.views import TodoBotView

bot = telebot.TeleBot("6302194812:AAHtFxvECUXx6T7Bd6BpMKAc6RWDzBhL4fE")
controller = TodoBotController()
view = TodoBotView()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.from_user.id
    controller.add_user(user_id)
    bot.reply_to(message, view.welcome_message())

@bot.message_handler(commands=['add'])
def add_task(message):
    user_id = message.from_user.id
    task_description = message.text.replace('/add ', '', 1)
    if task_description != "/add":
        controller.add_task(user_id, task_description)
        bot.reply_to(message, "Задача успешно добавлена!")
    else:
        bot.reply_to(message, "Пожалуйста, введите описание задачи после команды /add.")

@bot.message_handler(commands=['done'])
def mark_done(message):
    user_id = message.from_user.id
    try:
        task_id = int(message.text.replace('/done ', '', 1))
    except:
        bot.reply_to(message, "Пожалуйста, укажите индекс выполненной записи")
        return
    try:
        controller.mark_task_done(user_id, task_id)
    except:
        bot.reply_to(message, "Список задач пуст")
        return 
    bot.reply_to(message, "Задача отмечена как выполненная!")

@bot.message_handler(commands=['list'])
def list_tasks(message):
    user_id = message.from_user.id
    tasks = controller.get_all_tasks(user_id)
    bot.reply_to(message, view.list_tasks(tasks))

@bot.message_handler(commands=['delete'])
def delete_task(message):
    user_id = message.from_user.id
    try:
        task_id = int(message.text.replace('/delete ', '', 1))
    except:
        bot.reply_to(message, "Пожалуйста, укажите индекс удаляемой записи")
        return
    try:
        controller.delete_task(user_id, task_id)
    except:
        bot.reply_to(message, "Список задач пуст")
        return 
    bot.reply_to(message, "Задача успешно удалена!")


bot.infinity_polling()
