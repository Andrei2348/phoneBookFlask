const phoneNumber = document.getElementById('section__person-form-phone');
const firstName = document.getElementById('section__person-form-firstName');
const lastName = document.getElementById('section__person-form-lastName');
const saveButton = document.querySelector('.section__person-form-button');
const deleteButton = document.querySelector('.section__person-delete-button');
const id = document.getElementById('hidden__id');
const personData = document.querySelector('.section__person-data');
const searchInput = document.querySelector('.section__search-input');
const returnButton = document.querySelector('.section__person-return-button');


window.addEventListener('DOMContentLoaded', startNavigation)

function startNavigation(){
  requestToServer()
}

// Функция очистки списка
function cleanPersonList(style){
  if(document.querySelectorAll(style)){
    document.querySelectorAll(style).forEach((eachElement) => eachElement.remove());
  };
};

// Функция обновления списка контактов
function refreshPersonList(){
  cleanPersonList('.section__person-item');
  cleanPersonList('.section__person-info');
      if(personData.classList.contains('visible')){
        personData.classList.remove('visible');
      }
}

// Запрос на сервер данных о контактах
function requestToServer(){
  $.ajax({
    url: '/',
    type: 'POST',
    cache: true,
    data: { 'data': 'getContacts'},
    success: function(response) {
      if (response.length == 0){
        document.querySelector('.section__person-items').insertAdjacentHTML("beforeend",
        `<li class="section__person-info">
          <p class="section__person-text">Список контактов пуст</p>
        </li>`);
      } else {
        // Выводим список контактов
        document.querySelector('.section__person-items').insertAdjacentHTML("beforeend",
        `<li class="section__person-info">
          <p class="section__person-text">Нажмите на контакт, чтобы просмотреть или редактировать данные</p>
        </li>`);
        
        for (elem in response){
          document.querySelector('.section__person-items').insertAdjacentHTML("beforeend",
          `<li class="section__person-item">
            <a class="section__person-link" href="#">${response[elem]['firstname']} ${response[elem]['lastname']}</a>
          </li>`);
        };
        selectPersonFromList(response);
      }
    },
    error: function(error) {
      console.log(error);
    }
  });
}


document.querySelector('.section__search-wrapper').addEventListener('submit', function(event){
  event.preventDefault()
  if (!returnButton.classList.contains('visible')){
    returnButton.classList.add('visible');
  }
  const searchData = searchInput.value;
  if(searchData.length > 0){
    $.ajax({
      url: '/',
      type: 'POST',
      cache: true,
      data: { 'data': 'searchData',
              'search_data': searchData
            },
      success: function(response) {
        refreshPersonList()
        if (response.length == 0){
          document.querySelector('.section__person-items').insertAdjacentHTML("beforeend",
          `<li class="section__person-info">
            <p class="section__person-text">Контакты не найдены</p>
          </li>`);
        } else {
          // Выводим результаты поиска
          document.querySelector('.section__person-items').insertAdjacentHTML("beforeend",
          `<li class="section__person-info">
            <p class="section__person-text">Результаты поиска:</p>
          </li>`);
          
          for (elem in response){
            document.querySelector('.section__person-items').insertAdjacentHTML("beforeend",
            `<li class="section__person-item">
              <a class="section__person-link" href="#">${response[elem]['firstname']} ${response[elem]['lastname']}</a>
            </li>`);
          };
        }
        selectPersonFromList(response)
      },
      error: function(error) {
        console.log(error);
      }
    });
  }
})


// Функция вывода данных о выбранном контакте
function selectPersonFromList(response){
  const clients = document.querySelectorAll('.section__person-link')
  clients.forEach((eachElement, index) => 
    eachElement.addEventListener('click', function(event){
      event.preventDefault();
      console.log('clicked')
      personData.classList.add('visible');
      phoneNumber.value = response[index]['phone_number'];
      firstName.value = response[index]['firstname'];
      lastName.value = response[index]['lastname'];
      id.innerHTML = response[index]['id'];
    })
  );
};


// Функция запроса на сохранение изменений контакта
saveButton.addEventListener('click', function(event){
  event.preventDefault()
  $.ajax({
    url: '/',
    type: 'POST',
    cache: true,
    data: { 'data': 'saveData',
            'id': id.innerHTML,
            'phone_number': phoneNumber.value,
            'firstname': firstName.value,
            'lastname': lastName.value
          },
    success: function(response) {
      if(response){
        refreshPersonList();
        requestToServer();
      }
      console.log(response);
    },
    error: function(error) {
      console.log(error);
    }
  });
})


// Функция удаления контакта
deleteButton.addEventListener('click', function(event){
  event.preventDefault()
  $.ajax({
    url: '/',
    type: 'POST',
    cache: true,
    data: { 'data': 'deleteData',
            'id': id.innerHTML
          },
    success: function(response) {
      if(response){
        refreshPersonList();
        requestToServer();
      }
      console.log(response);
    },
    error: function(error) {
      console.log(error);
    }
  });
})
