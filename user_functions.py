import app


# Поиск пользователей(OK)
def found_friends(friend):
  try:
    cursor, db = app.connect_database()
    cursor.execute("SELECT username FROM users WHERE username = ?", [friend])
    friend = cursor.fetchone()
    app.close_database(cursor, db)
    print(f'Запрос поиска людей (OK)! {friend}')
    return friend
  except:
    print('Ошибка при обращении к бд при запросе поиска людей')
    return []


# Добавление в друзья(OK)
def add_friend(username, friend):
  try:
    cursor, db = app.connect_database()
    cursor.execute("""INSERT INTO friends (username, friendName, friendKey) 
                  VALUES (?, ?, ?)""", [username, friend, (username + '&' + friend)])
    cursor.execute("""INSERT INTO friends (username, friendName, friendKey) 
                  VALUES (?, ?, ?)""", [friend, username, (username + '&' + friend)])
    # Создаем запись в таблице для приватных сообщений
    cursor.execute("""INSERT INTO privateMessages (friendKey, messages, status) 
                  VALUES (?, '', 'Active')""", [(username + '&' + friend),])
    db.commit()
    app.close_database(cursor, db)
    print(f'Запрос добавления в друзья (OK)! {friend}')
  except:
    print('Ошибка при обращении к бд при запросе добавления в друзья.')


# Отображение списка друзей(OK)
def show_my_friends(username):
  my_friends = []
  try:
    cursor, db = app.connect_database()
    cursor.execute('''SELECT friendName FROM friends WHERE username = ?''', [username])
    res = cursor.fetchall()
    app.close_database(cursor, db)
    if res:
      for row in res:
        my_friends.append(row[0])
      print(f'Запрос списка друзей (OK)! {my_friends}.')
      return my_friends
    else:
      print('Список друзей пуст.')
      return []
  except:
    print('Ошибка при обращении к бд при запросе списка друзей.')
  

# Удаление из друзей(OK)
def delete_from_friends(username, friend):
  try:
    friendKey = check_friendKey(username, friend)
    cursor, db = app.connect_database()
    cursor.execute('''DELETE FROM friends WHERE username = ? AND friendName = ?''', (username, friend))
    cursor.execute('''DELETE FROM friends WHERE username = ? AND friendName = ?''', (friend, username))
    cursor.execute('''DELETE FROM privateMessages  
                  WHERE friendKey = ?''', [friendKey])
    db.commit()
    app.close_database(cursor, db)
    print(f'Запрос удаления друзей (OK)! {friend}')
    return True
  except:
    print('Ошибка при обращении к бд при запросе удаления друзей')
    return False
        

# Отображение черного списка(OK)
def show_my_enemies(username):
  my_enemies = set()
  try:
    cursor, db = app.connect_database()
    cursor.execute('''SELECT blockUser FROM blacklist WHERE username = ?''', [username])
    res = cursor.fetchall()
    app.close_database(cursor, db)
    if res:
      for row in res:
        my_enemies.add(row[0])
      print(f'Запрос отображения чс (ОК)! {my_enemies}.')
      return list(my_enemies)
    else:
      print('Список друзей пока пуст.')
      return []
  except:
    print('Ошибка при обращении к бд при запросе отображения чс.')
  

# Добавление персонажа в чс(OK)
def addEnemyToBlackList(username, friend):
  try:
    cursor, db = app.connect_database()
    cursor.execute('''INSERT INTO blacklist (username, blockUser) 
                  VALUES (?, ?)''', (username, friend))
    db.commit()
    app.close_database(cursor, db)
    print(f'Запрос на добавление в чс (ОК)! {friend}.')
    return True
  except:
    print('Ошибка при обращении к бд при запросе на добавление в чс.')
    return False


# Удаление персонажа из чс(OK)
def delete_from_enemies(username, enemy_name):
  try:
    cursor, db = app.connect_database()
    cursor.execute('''DELETE FROM blacklist 
                  WHERE username = ? AND blockUser = ?''', (username, enemy_name))
    db.commit()
    app.close_database(cursor, db)
    print(f'Запрос на удаление из чс (ОК)! {enemy_name}')
    return True
  except:
    print('Ошибка при обращении к бд при запросе на удаление из чс.')
    return False


# Функция получения личных данных из бд(ОК)
def read_privateData(username):
  try:
    cursor, db = app.connect_database()
    cursor.execute("SELECT * FROM privateData WHERE username = ?", [username])
    personal_data = cursor.fetchone()
    app.close_database(cursor, db)
    print('Данные успешно получены.')
    return personal_data
  except:
    print('Ошибка при обращении к бд при запросе чтения личных данных о пользователе.')


# Функция изменения приватных данных(ОК)
def update_privateData(values):
  try:
    cursor, db = app.connect_database()
    cursor.execute('''UPDATE privateData 
                  SET firstName = ?, 
                  lastName = ?,
                  birthDate = ?, 
                  city = ?,
                  familyStatus = ?,
                  biography = ? 
                  WHERE username = ?''', values)
    db.commit()
    app.close_database(cursor, db)
    print('Данные успешно отредактированы.')
    return True
  except:
    print('Ошибка при обращении к бд при запросе обновления данных.')
    return False


#Функция изменения пароля(ОК)
def update_password(values):
  try:
    cursor, db = app.connect_database()
    cursor.execute('''UPDATE users 
                  SET password = ? 
                  WHERE username = ?''', values)
    db.commit()
    app.close_database(cursor, db)
    print('Пароль успешно изменен.')
    return True
  except:
    print('Ошибка при изменении пароля.')
    return False


# Функция удаления пользователя(OK)
def delete_user(username):
  try:
    friendList = getFriendKeys(username)
    cursor, db = app.connect_database()
    cursor.execute("PRAGMA foreign_keys = on")
    cursor.execute('''DELETE FROM users WHERE username = ?''', (username,))
    for key in friendList:
      cursor.execute('''DELETE FROM privateMessages  
                  WHERE friendKey = ?''', (key['friendKey'],))
    db.commit()
    app.close_database(cursor, db)
    print(f'Пользователь {username} удален.')
    return True
  except:
    print('Ошибка при удалении пользователя.')
    return False


# Проверка записи username и user в бд
def check_friendKey(username, user):
  cursor, db = app.connect_database()
  cursor.execute('''SELECT EXISTS
                (SELECT friendKey FROM friends 
                WHERE friendKey=?)''', [f'{username}&{user}'])
  result = bool(cursor.fetchone()[0])
  if result:
    return (f'{username}&{user}')
  else:
    return (f'{user}&{username}')


# Чтение приватных сообщений
def read_private_messages(username, user):
  friendKey = check_friendKey(username, user)
  try:
    cursor, db = app.connect_database()
    cursor.execute('''SELECT messages FROM privateMessages 
                   WHERE status = 'Active' AND friendKey = ?''', [friendKey])
    messages = cursor.fetchone()
    app.close_database(cursor, db)
    print('Чтение приватных сообщений из бд ОК')
    return messages['messages']
  except:
    print('Ошибка при чтении приватных сообщений из бд.')
    return []
  

# Обновление приватных сообщений
def update_private_history(username, user, message):
  friendKey = check_friendKey(username, user)
  try:
    cursor, db = app.connect_database()
    cursor.execute('''UPDATE privateMessages 
                      SET messages = ? 
                      WHERE friendKey = ?''', [message, friendKey])
    db.commit()
    app.close_database(cursor, db)
    print('Приватная переписка успешно перезаписана.')
  except:
    print('Ошибка при обновлении записи приватных сообщений в бд.')
    return []


def getFriendKeys(username):
  cursor, db = app.connect_database()
  cursor.execute("SELECT friendKey FROM friends WHERE username = ?", [username])
  friendList = cursor.fetchall()
  cursor.execute("SELECT friendKey FROM friends WHERE friendName = ?", [username])
  friendList = friendList + cursor.fetchall()
  app.close_database(cursor, db)
  for key in friendList:
    print(key['friendKey'])
  return friendList