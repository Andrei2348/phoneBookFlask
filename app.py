from flask import Flask, render_template, request, redirect, url_for, jsonify
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
@app.route('/', methods = ['GET', 'POST'])
def index():
  if request.method == 'POST':
    data = request.form.get('data')
    search_data = request.form.get('search_data')
    search_value = request.form.get('search_value')
    values = [
              request.form.get('phone_number'),
              request.form.get('firstname'),
              request.form.get('lastname'),
              request.form.get('id')
    ]
    if data == 'getContacts':
      contact_list = get_contact_list()
      return jsonify(contact_list)
    
    if data == 'saveData':
      return jsonify(saveData(values))
      
    if data == 'deleteData':
      return jsonify(deleteData(values[3]))
    
    if data == 'searchData':
      return jsonify(searchData(search_value, search_data.strip()))
      
  return render_template('index.html', my_title = 'Телефонный справочник')


# Добавление записи
@app.route('/add_contact/', methods = ['GET', 'POST'])
def add_contact():
  if request.method == 'POST':
    try:
      cursor, db = connect_database()
      user_details = request.form
      
      values = [
        user_details['phone_number'].strip(),
        user_details['first_name'].strip(),
        user_details['last_name'].strip()
      ]
      
      cursor.execute("""INSERT INTO phone_directory
                    (phone_number, firstname, lastname)
                    VALUES (?, ?, ?)""", values)
    
      db.commit()
      close_database(cursor, db)
      print('Контакт успешно добавлен')
    except:
      print('Ошибка при добавлении контакта')
    return redirect(url_for('index'))
  return render_template('add_contact.html', my_title = 'Добавление контакта')


# Ошибка 404
@app.errorhandler(404)
def page_not_found(error):
  return render_template('404.html', my_title = 'Error')


if __name__ == '__main__':
  app.secret_key = os.urandom(24)
  app.run(debug = True)