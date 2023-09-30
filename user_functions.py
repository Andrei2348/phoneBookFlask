import app

# Функция запроса списка контактов
def get_contact_list():
  try:
    cursor, db = app.connect_database()
    cursor.execute('''SELECT * FROM phone_directory''')
    contacts = cursor.fetchall()
    app.close_database(cursor, db)
    if contacts:
      contact_list = []
      for contact in contacts:
        contact_list.append({'id': contact['id'],
                            'phone_number': contact['phone_number'],
                            'firstname': contact['firstname'],
                            'lastname': contact['lastname'],
                            })
      print(f'Список контактов {contact_list}')
      return contact_list
    else:
      print('Список контактов пуст.')
      return []
  except:
    print('Ошибка при обращении к бд при запросе списка контактов.')
    
    
    
def saveData(values):
  try:
    cursor, db = app.connect_database()
    cursor.execute('''UPDATE phone_directory
                      SET phone_number = ?, 
                      firstname = ?,
                      lastname = ?
                      WHERE id = ?''', values)
    db.commit()
    app.close_database(cursor, db)
  except:
    print('Ошибка при обращении к бд при запросе редактирования контакта.')
  

def deleteData(user_id):
  try:
    cursor, db = app.connect_database()
    cursor.execute('''DELETE FROM phone_directory WHERE id = ?''', (user_id,))
    db.commit()
    app.close_database(cursor, db)
    return True
  except:
    print('Ошибка при обращении к бд при запросе удаления контакта.')
    return False

# # Поиск пользователей(OK)
# def found_friends(friend):
#   try:
#     cursor, db = app.connect_database()
#     cursor.execute("SELECT username FROM users WHERE username = ?", [friend])
#     friend = cursor.fetchone()
#     app.close_database(cursor, db)
#     print(f'Запрос поиска людей (OK)! {friend}')
#     return friend
#   except:
#     print('Ошибка при обращении к бд при запросе поиска людей')
#     return []





