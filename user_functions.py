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
      # print(f'Список контактов: {contact_list}.')
      return contact_list
    else:
      print('Список контактов пуст.')
      return []
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


# # Поиск пользователей(OK)
def searchData(search_data):
  contact_list = []
  params = ['firstname', 'lastname']
  try:
    cursor, db = app.connect_database()
    for param in params:
      cursor.execute(f'SELECT * FROM phone_directory WHERE {param} = ?', [search_data])
      contacts = cursor.fetchall()
      if len(contacts) > 0:
        for contact in contacts:
          contact_list.append({'id': contact['id'],
                              'phone_number': contact['phone_number'],
                              'firstname': contact['firstname'],
                              'lastname': contact['lastname'],
                              })
      print(contact_list)
    app.close_database(cursor, db)
    return contact_list
  except:
    print('Ошибка при обращении к бд при запросе поиска контактов')
    return []


# def contactsInitiaze(contacts, contact_list):
#   if contacts:
#     for contact in contacts:
#       contact_list.append({'id': contact['id'],
#                           'phone_number': contact['phone_number'],
#                           'firstname': contact['firstname'],
#                           'lastname': contact['lastname'],
#                           })
    
#     return contact_list
#   else:
#     return []



