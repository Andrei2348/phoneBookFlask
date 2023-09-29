from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
import os
import sqlite3

from user_functions import *
from create_table import create_table


app = Flask(__name__)
create_table()

# Функция подключения к бд
def connect_database():
  db = sqlite3.connect('database.db')
  db.row_factory = sqlite3.Row
  cursor = db.cursor()
  return cursor, db


# Функция закрытия cursor и бд
def close_database(cursor, db):
  cursor.close()
  db.close()


# Главная страница проекта
@app.route('/index/', methods = ['GET', 'POST'])
# @app.route('/')
def index():
  if request.method == 'POST':
    data = request.form.get('data')
    if data == 'getContacts':
      contact_list = get_contact_list()
      return jsonify(contact_list)
  return render_template('index.html', my_title = 'Телефонный справочник')



# # Личная страница пользователя
# @app.route('/user/<string:username>/', methods = ['GET', 'POST'])
# def user(username):
#   if session:
#     if request.method == 'POST':
#       # Получение запросов от клиента(OK)
#       data = request.form.get('data')
#       user = request.form.get('user')
#       message = request.form.get('message')
#       # Запрос поиска друзей(OK)
#       if data == 'find':
#         data = found_friends(user)
#         if data != None:
#           return jsonify(data['username'])
#         else:
#           return jsonify([])

#       # Запрос добавления в друзья(OK)
#       if data == 'addFriend':
#         friends = show_my_friends(username)
#         # Проверка, есть ли уже друг в списке друзей
#         # Защита, чтобы пользователь не добавил в друзья сам себя
#         if (user not in friends) and (username != user):
#           # Пользователь успешно добавлен
#           add_friend(username, user)
#           data = True
#           # Проверка, есть ли пользователь в черном списке
#           friends = show_my_enemies(username)
#           # Если друг в чс, удаляем его из чс
#           if user in friends:
#             delete_from_enemies(username, user)
#         else:
#           data = False
#         return jsonify(data)

#       # Запрос списка друзей(OK)
#       if data == 'friends':
#         return jsonify(show_my_friends(username))
      
#       # Отправка и прием сообщений в лс
#       if data == 'privateMessages':
#         print(message)
#         messages = read_private_messages(username, user)
#         message = f'{messages} \n{username}: {message}'
#         update_private_history(username, user, message)
#         data = {
#           'message': message,
#           'user': user
#         }
#         return jsonify(message)

#       # Удаление друга из списка друзей(OK)
#       if data == 'deleteFriend':
#         return jsonify(delete_from_friends(username, user))

#       # Отображение пользователей в чс(OK)
#       if data == 'blackList':
#         return jsonify(show_my_enemies(username))

#       # Добавление в черный список(OK)
#       if data == 'addToBlackList':
#         # Удаляем из друзей
#         if delete_from_friends(username, user) and addEnemyToBlackList(username, user):
#           return jsonify(True)
#         else:
#           return jsonify(False)
      
#       # Удаление из черного списка(OK)
#       if data == 'deleteFromBD':
#         return jsonify(delete_from_enemies(username, user))

#       # Получение и обновление истории переписки лс с пользователем
#       if data == 'privateMessagesHistory':
#         messages = read_private_messages(username, user)
#         data = {
#           'message': messages,
#         }
#         return jsonify(data)
#   else:
#     return redirect(url_for('login'))
#   return render_template('user.html', my_title = 'Страница пользователя')


# Добавление записи
@app.route('/add_contact/', methods = ['GET', 'POST'])
def add_contact():
  if request.method == 'POST':
    try:
      cursor, db = connect_database()
      user_details = request.form
      
      values = [
        user_details['phone_number'],
        user_details['first_name'],
        user_details['last_name']
      ]
      
      cursor.execute("""INSERT INTO phone_directory
                    (phone_number, firstname, lastname)
                    VALUES (?, ?, ?)""", values)
    
      db.commit()
      close_database(cursor, db)
      print('Контакт успешно добавлен')
      flash('Контакт успешно добавлен')
    except:
      print('Ошибка при добавлении контакта')
    return redirect(url_for('index'))
  return render_template('add_contact.html', my_title = 'Добавление контакта')



# Ошибка 404
# @app.errorhandler(404)
# def page_not_found(error):
#   return render_template('404.html', my_title = 'Error')


if __name__ == '__main__':
  app.secret_key = os.urandom(24)
  app.run(debug = True)