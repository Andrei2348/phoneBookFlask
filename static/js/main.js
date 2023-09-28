const chatForm = document.getElementById('chat__form');
const chatInputName = document.getElementById('chat__input-name');
const chatArea = document.getElementById('chat__area');
const chatInputMessage = document.getElementById('chat__input-message');
const chatMessage = document.getElementById('chat__message');
const userMenuButton = document.querySelectorAll('.user__menu-item');
const userMenuPage = document.querySelectorAll('.user__menu-page');
const sessionName = document.getElementById('session__name').textContent;
const userList = document.querySelector('.user__list');
const userFriendsList = document.querySelector('.user__friends-list');
const findForm = document.getElementById('find__friend');
const findArea = document.getElementById('find__input-user');
const findMessage = document.querySelectorAll('.find__message');
const userBlackList = document.querySelector('.user__blacklist');

// Функция обращения на сервер без return
function requestToServer(sessionName, user, request){
  $.ajax({
    url: `/user/${sessionName}`,
    type: 'POST',
    cache: true,
    data: { 'data': request,
            'user': user},
    success: function(response) {
      const res = response
    },
    error: function(error) {
      console.log(error);
    }
  });
};

// Функция очистки сообщений
function cleanEmptyList(style){
  if(document.querySelectorAll(style)){
    document.querySelectorAll(style).forEach((eachElement) => eachElement.remove());
  };
};

// Функция скрытия элементов
function hideElements(userMenuPage){
  userMenuPage.forEach((eachElement) => eachElement.classList.remove('active'));
};

window.addEventListener('DOMContentLoaded', startNavigation)

function startNavigation(){
  requestAllInfoFriends();
  // Выбор раздела меню
  userMenuButton.forEach((eachElement, index) => 
    eachElement.addEventListener('click', function(event){
      event.preventDefault();
      hideElements(userMenuPage);
      userMenuPage[index].classList.add('active');
      if (index == 0){
        requestFindFriends();
      };
      // Переключаемся на страницу личных сообщений и делаем запрос списка друзей
      if (index == 1){
        // Очищаем поле вывода списка пользователей
        cleanEmptyList('.user__empty-style');
        cleanEmptyList('.user__friend-area');
        requestAllInfoFriends();
      };
  
      if (index == 2){
        
        // Очищаем поле вывода списка пользователей
        cleanEmptyList('.user__empty-style');
        cleanEmptyList('.user__name-style');
        requestOfFriends();
      };
  
      if (index == 4){
        // Очищаем поле вывода списка пользователей
        cleanEmptyList('.user__empty-style');
        cleanEmptyList('.user__friend-area');
        requestOfBlackUsers();
      };
    })
  );
}

// ======================= Раздел № 0 =======================================
// Функция поиска друзей
function requestFindFriends(){
  let friendName = '';
  findForm.addEventListener('submit', function(event) {
    event.preventDefault();
    hideElements(findMessage);
    friendName = findArea.value;
    findArea.value = '';
    if(friendName.length > 0){
      $.ajax({
        url: `/user/${sessionName}`,
        type: 'POST',
        cache: true,
        data: {'data': 'find',
              'user': friendName
              },
        success: function(response) {
          findArea.value = response;
          if (response.length == 0){
            findMessage[0].classList.add('active');
          } else {
            findArea.value = '';
            document.getElementById('find__message-text').innerHTML = response;
            findMessage[1].classList.add('active');
          };
        },
        error: function(error) {
          console.log(error);
        } 
      });
    };
  });
};

// Событие добавления в друзья
document.getElementById('find__add-user').addEventListener('click', function(event) {
  event.preventDefault();
  const username = document.getElementById('find__message-text').innerHTML;
  hideElements(findMessage);
  $.ajax({
    url: `/user/${sessionName}`,
    type: 'POST',
    cache: true,
    data: {'data': 'addFriend',
          'user': username
          },
    success: function(response) {
      if (response == true){
        findMessage[2].classList.add('active');
      } else {
        findMessage[3].classList.add('active');
      };
    },
    error: function(error) {
      console.log(error);
    } 
  });
});


// ======================= Раздел № 1 =======================================
function requestAllInfoFriends(){
  $.ajax({
    url: `/user/${sessionName}`,
    type: 'POST',
    cache: true,
    data:  { 'data': 'friends'},
    success: function(response) {
      // Если нет друзей
      if (response.length == 0){
        document.querySelector('.user__menu-page.active').insertAdjacentHTML("beforeend",
        `<p class="user__empty-style">Список друзей пока пуст!!!</p>`);
      } else {
        // Выводим список друзей
        for (elem in response){
          userFriendsList.insertAdjacentHTML("beforeend",
          `<li class="user__friend-area">
            <h3 class="user__friend-data">${response[elem]}</h3>
            <ul class="user__button-items">
              <li class="user__button-item">
                <a href="#" class="user__button-link form__wrapper-button user__button-blacklist">Добавить в черный список</a>
              </li>
              <li class="user__button-item">
                <a href="#" class="user__button-link form__wrapper-button user__button-delete">Удалить из друзей</a>
              </li>
            </ul>
          </li>`
          );
        };
        // Привязка кнопок
        const blackListButtons = document.querySelectorAll('.user__button-blacklist');
        const deleteButtons = document.querySelectorAll('.user__button-delete');
        addFriendToBlackList(blackListButtons, response);
        deleteFriend(deleteButtons, response);
      };
    },
    error: function(error) {
      console.log(error);
    }
  });
};


// ===================== Раздел № 2 ===================================================
// Функция запроса списка друзей из БД
function requestOfFriends(){
  $.ajax({
    url: `/user/${sessionName}`,
    type: 'POST',
    cache: true,
    data:  { 'data': 'friends' },
    success: function(response) {
      if (response.length == 0){
        userList.insertAdjacentHTML("beforeend",
        `<p class="user__empty-style">Список друзей пока пуст!!!</p>`)
      } else {
        for (elem in response){
          userList.insertAdjacentHTML("beforeend",
          `<a class="user__name-style" href="#">${response[elem]}</a>`)
        };
        selectUserForMessage(response);
      }
    },
    error: function(error) {
      console.log(error);
    }
  });
};

// Отслеживание выбора пользователя для отправки сообщений
function selectUserForMessage(elems){
  const users = document.querySelectorAll('.user__name-style')
  users.forEach((eachElement, index) => 
  eachElement.addEventListener('click', function(event){
    event.preventDefault();
    
    // Добавить запрос переписки из бд с данным пользователем!!!

    const userName = document.querySelector('.chat__username-name');
    userName.innerHTML = elems[index];
    // Делаем выборку истории переписки с выбранным пользователем
    getMessage(elems[index]);
  }));
};

// Отправка и прием приватных сообщений
chatForm.addEventListener('submit', function(event) { 
  event.preventDefault();
  let inputMessage = '';
  inputMessage = chatInputMessage.value;
  const selectedUser = document.querySelector('.chat__username-name').innerHTML;
  if (inputMessage.length > 0 && selectedUser.length > 0){
    let today = new Date();
    let timeNow = today.toLocaleTimeString('ru-RU');
    inputMessage = timeNow + '@ ' + inputMessage;
    $.ajax({
      url: `/user/${sessionName}`,
      type: 'POST',
      cache: true,
      data: { 'data': 'privateMessages',
              'message': inputMessage,
              'user': selectedUser},
      success: function(response) {
        console.log(response)
        chatArea.value = response;
      },
      error: function(error) {
        console.log(error);
      }
    });
    chatInputMessage.value = '';
  };
});

// Циклическое обновление переписки
function getMessage(selectedUser){
  $.ajax({
    url: `/user/${sessionName}`,
    type: 'POST',
    cache: true,
    data: { 'data': 'privateMessagesHistory',
            'user': selectedUser},
    success: function(response) {
      chatArea.value = response['message'];
    },
    error: function(error) {
      console.log(error);
    }
  });
};


// =====================================================================================
// Удаление пользователя из друзей
function deleteFriend(deleteButtons, friendList){
  deleteButtons.forEach((eachElement, index) => 
    eachElement.addEventListener('click', function(event){
    event.preventDefault();
    // Отправка запроса на сервер
    $.ajax({
      url: `/user/${sessionName}`,
      type: 'POST',
      cache: true,
      data: { 'data': 'deleteFriend',
              'user': friendList[index]},
      success: function(response) {
        cleanEmptyList('.user__empty-style');
        cleanEmptyList('.user__friend-area');
        requestAllInfoFriends();
        if(response == true){
          document.querySelector('.user__menu-page.active').insertAdjacentHTML("afterbegin",
          `<p class="user__empty-style user__alarm-style">Пользователь ${friendList[index]} успешно удален!!!</p>`);
        } else{
          document.querySelector('.user__menu-page.active').insertAdjacentHTML("afterbegin",
          `<p class="user__empty-style user__alarm-style">Ошибка удаления пользователя: ${friendList[index]}!!!</p>`);
        }
      },
      error: function(error) {
        console.log(error);
      }
    });
  })
)};


// Добавление друзей в черный список(удалить из друзей и добавить в чс)
function addFriendToBlackList(blackListButtons, friendList){
  blackListButtons.forEach((eachElement, index) => 
    eachElement.addEventListener('click', function(event){
    event.preventDefault();
    // Отправка запроса на сервер на добавление в чс
    $.ajax({
      url: `/user/${sessionName}`,
      type: 'POST',
      cache: true,
      data: { 'data': 'addToBlackList',
              'user': friendList[index]},
      success: function(response) {
        cleanEmptyList('.user__empty-style');
        cleanEmptyList('.user__friend-area');
        requestAllInfoFriends();
        if(response == true){
          document.querySelector('.user__menu-page.active').insertAdjacentHTML("afterbegin",
          `<p class="user__empty-style user__alarm-style">Пользователь ${friendList[index]} добавлен в черный список!!!</p>`);
        } else {
          document.querySelector('.user__menu-page.active').insertAdjacentHTML("afterbegin",
          `<p class="user__empty-style user__alarm-style">Ошибка добавления пользователя: ${friendList[index]} в черный список!!!</p>`);
        }
      },
      error: function(error) {
        console.log(error);
      }
    });
  })
)};


// ===================== Раздел № 4 ===================================================
// Отображение людей в черном списке
function requestOfBlackUsers(){
  $.ajax({
    url: `/user/${sessionName}`,
    type: 'POST',
    cache: true,
    data:  {'data': 'blackList'},
    success: function(response) {
      // Если нет друзей в чс
      if (response == null){
        document.querySelector('.user__menu-page.active').insertAdjacentHTML("beforeend",
        `<p class="user__empty-style">Список пользователей в черном списке пуст!!!</p>`)
      } else {
        // Выводим список друзей в чс
        for (elem in response){
          userBlackList.insertAdjacentHTML("beforeend",
          `<li class="user__friend-area">
            <h3 class="user__friend-data">${response[elem]}</h3>
            <ul class="user__button-items">
              <li class="user__button-item">
                <a href="#" class="user__button-link form__wrapper-button user__removeFrom-blacklist">Убрать из черного списка</a>
              </li>
            </ul>
          </li>`
          );
        };
        const deleteButtonsBL = document.querySelectorAll('.user__removeFrom-blacklist');
        deleteFriendFromBlackList(deleteButtonsBL, response);
      };
    },
    error: function(error) {
      console.log(error);
    }
  });
};


// Удаление пользователя из ЧС
function deleteFriendFromBlackList(deleteButtonsBL, friendList){
  deleteButtonsBL.forEach((eachElement, index) => 
    eachElement.addEventListener('click', function(event){
    event.preventDefault();
    // Отправка запроса на сервер
    $.ajax({
      url: `/user/${sessionName}`,
      type: 'POST',
      cache: true,
      data: { 'data': 'deleteFromBD',
              'user': friendList[index]},
      success: function(response) {
        cleanEmptyList('.user__empty-style');
        cleanEmptyList('.user__friend-area');
        requestOfBlackUsers();
        if(response == true){
          document.querySelector('.user__menu-page.active').insertAdjacentHTML("afterbegin",
          `<p class="user__empty-style user__alarm-style">Пользователь ${friendList[index]} удален из черного списка!!!</p>`)
        } else {
          document.querySelector('.user__menu-page.active').insertAdjacentHTML("afterbegin",
          `<p class="user__empty-style user__alarm-style">Ошибка при удалении пользователя: ${friendList[index]} из черного списка!!!</p>`)
        }
      },
      error: function(error) {
        console.log(error);
      }
    });
  })
)};