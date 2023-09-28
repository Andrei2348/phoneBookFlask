from flask import Flask, render_template, flash, session, request, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3
import validators
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
@app.route('/index/')
@app.route('/')
def index():
  return render_template('index.html', my_title = 'Главная страница сайта')


# Удаление аккаунта
@app.route('/delete/<string:username>/', methods = ['GET', 'POST'])
def delete(username):
  if session:
    if request.method == 'POST':
      confirm_login = request.form['inputLogin']
      if confirm_login == username:
        result = delete_user(username)
        if result:
          session.clear()
      flash(f'Аккаунт {username} удален!')
      return redirect(url_for('index'))
    return render_template('delete.html', my_title = 'Удаление аккаунта')
  else:
    return redirect(url_for('login'))
      

# Смена пароля
@app.route('/password/<string:username>/', methods = ['GET', 'POST'])
def password(username):
  if session:
    if request.method == 'POST':
      old_password = request.form['old_password']
      new_password = request.form['new_password']
      repeat_password = request.form['repeat_password']
      cursor, db = connect_database()
      cursor.execute("SELECT password FROM users WHERE username = ?", [username])
      password = cursor.fetchone()
      close_database(cursor, db)
      # Сверяем старый пароль из бд и введенный пароль
      if check_password_hash(password[0], old_password):
        flag_1 = True
      else:
        flash('Неверный пароль!')
        flag_1 = False
      # Сверяем новый и повторный пароли
      if new_password == repeat_password:
        flag_2 = True
      else:
        flash('Новые пароли не совпадают!')
        flag_2 = False
      # Проверяем валидность пароля
      if validators.valid_password(new_password) == True:
        flag_3 = True
      else:
        flash('Неверный формат нового пароля!')
        flag_3 = False
      # Если все три условия выполняются, вносим изменения в бд
      if flag_1 and flag_2 and flag_3:
        values = [generate_password_hash(new_password), username]
        result = update_password(values)
        if result:
          flash('Пароль успешно изменен!')
          return redirect(url_for('user', username = username))
        else:
          flash('Ошибка при изменении пароля!')
        return redirect(url_for('user', username = username))
    return render_template('password.html', my_title = 'Изменение пароля')
  else:
    return redirect(url_for('login'))


# Редактирование личных данных пользователя
@app.route('/private/<string:username>/', methods = ['GET', 'POST'])
def private(username):
  if session:
    if request.method == 'POST':
      # Запись изменений в бд
      values = [
        request.form['firstName'],
        request.form['lastName'],
        request.form['birthDate'],
        request.form['city'],
        request.form['familyStatus'],
        request.form['biography'],
        username
      ]
      result = update_privateData(values)
      if result:
        flash('Данные успешно изменены!')
        return redirect(url_for('user', username = username))
      else:
        flash('Ошибка при изменении данных!')
    # Чтение данных из бд таблицы private_settings
    personal_data = read_privateData(username)
    return render_template('private.html', my_title = 'Личные данные пользователя', personal_data = personal_data)
  else:
    return redirect(url_for('login'))


# Личная страница пользователя
@app.route('/user/<string:username>/', methods = ['GET', 'POST'])
def user(username):
  if session:
    if request.method == 'POST':
      # Получение запросов от клиента(OK)
      data = request.form.get('data')
      user = request.form.get('user')
      message = request.form.get('message')
      # Запрос поиска друзей(OK)
      if data == 'find':
        data = found_friends(user)
        if data != None:
          return jsonify(data['username'])
        else:
          return jsonify([])

      # Запрос добавления в друзья(OK)
      if data == 'addFriend':
        friends = show_my_friends(username)
        # Проверка, есть ли уже друг в списке друзей
        # Защита, чтобы пользователь не добавил в друзья сам себя
        if (user not in friends) and (username != user):
          # Пользователь успешно добавлен
          add_friend(username, user)
          data = True
          # Проверка, есть ли пользователь в черном списке
          friends = show_my_enemies(username)
          # Если друг в чс, удаляем его из чс
          if user in friends:
            delete_from_enemies(username, user)
        else:
          data = False
        return jsonify(data)

      # Запрос списка друзей(OK)
      if data == 'friends':
        return jsonify(show_my_friends(username))
      
      # Отправка и прием сообщений в лс
      if data == 'privateMessages':
        print(message)
        messages = read_private_messages(username, user)
        message = f'{messages} \n{username}: {message}'
        update_private_history(username, user, message)
        data = {
          'message': message,
          'user': user
        }
        return jsonify(message)

      # Удаление друга из списка друзей(OK)
      if data == 'deleteFriend':
        return jsonify(delete_from_friends(username, user))

      # Отображение пользователей в чс(OK)
      if data == 'blackList':
        return jsonify(show_my_enemies(username))

      # Добавление в черный список(OK)
      if data == 'addToBlackList':
        # Удаляем из друзей
        if delete_from_friends(username, user) and addEnemyToBlackList(username, user):
          return jsonify(True)
        else:
          return jsonify(False)
      
      # Удаление из черного списка(OK)
      if data == 'deleteFromBD':
        return jsonify(delete_from_enemies(username, user))

      # Получение и обновление истории переписки лс с пользователем
      if data == 'privateMessagesHistory':
        messages = read_private_messages(username, user)
        data = {
          'message': messages,
        }
        return jsonify(data)
  else:
    return redirect(url_for('login'))
  return render_template('user.html', my_title = 'Страница пользователя')


# Регистрация пользователя
@app.route('/register/', methods = ['GET', 'POST'])
def register():
  if request.method == 'POST':
    user_details = request.form
    # Проверяем существование пользователя с таким же username и email
    username = user_details['username']
    usermail = user_details['mail']
    password = user_details['password']
    confirm_password = user_details['confirm__password']

    cursor, db = connect_database()
    cursor.execute("SELECT username FROM users WHERE username = ?", [username])
    user = cursor.fetchone()
    
    if user is not None:
      flash('Пользователь с таким именем уже существует!')
      return redirect(url_for('register'))
    
    # Сверяем введенный и подтвержденный пароли
    if password != confirm_password:
      flash('Пароли не совпадают! Попробуйте еще раз!')
      return redirect(url_for('register'))
    
    #Проверяем корректность пароля и почты (функции в файле validators)
    if validators.valid_mail(usermail) == True and validators.valid_password(password) == True: 
      # Готовим данные к отправке в бд
      values = [usermail,
                # Шифрование пароля
                generate_password_hash(user_details['password']),
                username]
      private_values = [''] * 6
      private_values.append(username)
    else:
      flash('Неверный формат ввода email или пароля')
      return redirect(url_for('register'))
    # Записываем данные в бд
    cursor.execute("""INSERT INTO users
                  (email, password, username)
                  VALUES (?, ?, ?)""", values)
    cursor.execute("""INSERT INTO privateData
                  (firstName, lastName, birthDate, city, familyStatus, biography, username)
                  VALUES (?, ?, ?, ?, ?, ?, ?)""", private_values)
    db.commit()
    close_database(cursor, db)
    flash('Регистрация прошла успешно! Пожалуйста войдите в свой аккаунт')
    return redirect(url_for('index'))
  return render_template('register.html', my_title = 'Регистрация пользователя')


# Вход в личный кабинет
@app.route('/login/', methods = ['GET', 'POST'])
def login():
  if request.method == 'POST':
    user_details = request.form
    username = user_details['username']
    password = user_details['password']
    cursor, db = connect_database()
    cursor.execute("SELECT * FROM users WHERE username = ?", [username])
    user = cursor.fetchone()
    close_database(cursor, db)
    # Проверка существования пользователя
    if user is None:
      flash('Такого пользователя не существует!')
    else:
      # Сверка пароля
      if not check_password_hash(user['password'], password):
        flash("Неверный пароль! Попробуйте еще раз!")
      else:
        # Создание сессии
        session['username'] = user['username']
        flash('Добро пожаловать ' + session['username'] + '!!!')
        return redirect(url_for('user', username = username))
  return render_template('login.html', my_title = 'Вход')


# Выход из личного кабинета (logout)
@app.route('/logout/')
def logout():
  if session:
    session.clear()
    flash('Вы вышли из своего аккаунта!')
  return redirect(url_for('login'))


# Ошибка 404
@app.errorhandler(404)
def page_not_found(error):
  return render_template('404.html', my_title = 'Error')


if __name__ == '__main__':
  app.secret_key = os.urandom(24)
  app.run(debug = True)