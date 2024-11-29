import os
import telebot
import sqlite3

token = '7345970043:AAEJTq21x02LBjiHAEgxMfWvkZNzmQfJ3X8'
bot = telebot.TeleBot(token)
all_com = ['/create', '/public_login', '/start', '/admin', '/next', '/delete', '/send']
now = []


@bot.message_handler(commands=['admin'])
def check_user(message):
    bot.send_message(message.chat.id, 'put your login and password')
    bot.register_next_step_handler(message, admin_right)


def admin_right(message):
    cur = str(message.text).split()
    login, password = str(cur[0]), str(cur[-1])
    admin_base = sqlite3.connect('admin.db')
    cursor = admin_base.cursor()
    cursor.execute('SELECT * FROM admin')
    users = cursor.fetchall()
    if users[0][0] == login and users[0][-1] == password:
        bot.send_message(message.chat.id, 'success')
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_adm1 = telebot.types.KeyboardButton("/to_site")
        btn_adm2 = telebot.types.KeyboardButton("/delete")
        btn_adm3 = telebot.types.KeyboardButton("/send")
        btn_adm4 = telebot.types.KeyboardButton("/back_to_user")
        markup.add(btn_adm1, btn_adm2, btn_adm3, btn_adm4)
        bot.send_message(message.chat.id, 'Вы переведены в режим модерации', reply_markup=markup)


@bot.message_handler(commands=['send'])
def click(message):
    global now
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users')
    application = cursor.fetchall()
    connection.commit()
    connection.close()
    for i in application:
        if i[-1] != '0' and i[-2] != '0':
            now.append(i)
    bot.register_next_step_handler(message, sort)
    bot.send_message(message.chat.id, 'Нажмите на /send еще раз')


def sort(message):
    if len(now) >= 1:
        bot.send_message(message.chat.id, now[0][-2])
        bot.send_message(message.chat.id, now[0][-1])
        bot.send_message(message.chat.id, 'Выберите действие: /to_site or /delete')
        bot.register_next_step_handler(message, to_site)
    else:
        bot.send_message(message.chat.id, 'Модерация завершена, других заявок нет')


def to_site(message):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    if message.text == '/to_site':
        my_file = open(f"html+/{now[0][-2] + '  ' + now[0][0]}.txt", "a+")
        my_file.write(now[0][-1])
        my_file.close()
        bot.send_message(message.chat.id, 'Добавлено')
        cursor.execute("DELETE FROM users WHERE id=?", (now[0][0],))
        now.pop(0)
        sort(message)
        connection.commit()
        connection.close()

    if message.text == '/delete':
        bot.send_message(message.chat.id, 'Удалено')
        bot.send_message(int(now[0][0]), 'Ваша статья не прошла модерацию')
        cursor.execute("DELETE FROM users WHERE id=?", (now[0][0],))
        connection.commit()
        connection.close()
        now.pop(0)
        sort(message)
    if message.text == '/send':
        bot.send_message(message.chat.id, 'Неправильная команда')
        sort(message)
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    connection.commit()
    connection.close()


@bot.message_handler(commands=['start', 'back_to_user'])
def hello(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("/public_login")
    markup.add(btn1)
    bot.send_message(message.chat.id,
                     'Привет, ты попал в наш бот, для публикации статьи на нашем сайте. Чтобы разместить статью, нажми на кнопку  \"public_login\" ',
                     reply_markup=markup)
    bot.register_next_step_handler(message, stage1)


@bot.message_handler(commands=['public_login'])
def stage1(message):
    log = message.from_user.id
    bot.send_message(message.chat.id, 'Отправь мне название своей статьи')
    bot.register_next_step_handler(message, stage2)


def stage2(message):
    if message.text not in all_com:
        id = str(message.from_user.id)
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE id = ?""", (id,))
        user = cursor.fetchone()
        if user:
            cursor.execute("""UPDATE users SET article = ? WHERE id = ?""", (message.text, id,))
        else:
            cursor.execute("""INSERT INTO users (id, article) VALUES (?, ?)""", (id, message.text))
        connection.commit()
        connection.close()
        bot.register_next_step_handler(message, stage3)
    else:
        pass
    bot.send_message(message.chat.id, 'Введите текст статьи')


def stage3(message):
    if message.text not in all_com:
        id = str(message.from_user.id)
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM users WHERE id = ?""", (id,))
        user = cursor.fetchone()
        if user:
            cursor.execute("""UPDATE users SET about = ? WHERE id = ?""", (message.text, id,))
        else:
            cursor.execute("""INSERT INTO users (id, about) VALUES (?, ?)""", (id, message.text))
        cursor.execute('SELECT * FROM users')
        all_users = cursor.fetchall()
        print(all_users)
        connection.commit()
        connection.close()
        bot.send_message(message.chat.id, 'Все успешно отправлено, ожидайте подтверждние модератора')
        bot.send_message(message.chat.id,
                         'Если вы попытаетесь отправить новую стаью до подтверждения старой, рассматриваться будет только новая,старая удалится')
        bot.send_message(message.chat.id, 'Будьте внимательны')


bot.polling(none_stop=True)
