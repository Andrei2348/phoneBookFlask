import app


# Функция запроса списка контактов
def get_contact_list():
  # contact_list = []
  try:
    cursor, db = app.connect_database()
    cursor.execute('''SELECT * FROM phone_directory''')
    contacts = cursor.fetchall()
    app.close_database(cursor, db)
    if len(contacts) > 0:
      contact_list = contactsInitiaze(contacts)
    else:
      contact_list = []
      print(f'Список контактов: {contact_list}.')
    return contact_list
  except:
    print('Ошибка при обращении к бд при запросе списка контактов.')
    
    
# Функция обновления контакта
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
    print('Обновление контакта прошло успешно.')
    return True
  except:
    print('Ошибка при обращении к бд при запросе редактирования контакта.')
    return False
  
  
# Функция удаления контакта
def deleteData(user_id):
  try:
    cursor, db = app.connect_database()
    cursor.execute('''DELETE FROM phone_directory WHERE id = ?''', (user_id,))
    db.commit()
    app.close_database(cursor, db)
    print('Удаление контакта прошло успешно.')
    return True
  except:
    print('Ошибка при обращении к бд при запросе удаления контакта.')
    return False


# Поиск контактов
def searchData(search_value, search_data):
  search_data = search_data.split(' ')
  contact_list = []
  try:
    cursor, db = app.connect_database()
    for each_word in search_data:
      cursor.execute(f'SELECT * FROM phone_directory WHERE {search_value} = ?', [each_word])
      contacts = cursor.fetchall()
      for contact in contacts:
        contact_list.append(contact)
    app.close_database(cursor, db)
    contact_list = contactsInitiaze(contact_list)
    print(f'Результаты поиска: {contact_list}')
    return contact_list
  except:
    print('Ошибка при обращении к бд при запросе поиска контактов')
    return []


def contactsInitiaze(contacts):
  contact_list = []
  for contact in contacts:
    contact_list.append({'id': contact['id'],
                        'phone_number': contact['phone_number'],
                        'firstname': contact['firstname'],
                        'lastname': contact['lastname'],
                        })
  return contact_list
  



