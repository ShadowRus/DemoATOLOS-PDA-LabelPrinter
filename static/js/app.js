let UserId;
function onBarcode(code, type, base64) {
    const serverIP = `${window.location.protocol}//${window.location.hostname}:${window.location.port}`;

    // Отправка запроса на сервер для поиска товара

    fetch(`${serverIP}/semat/search`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code })
    })
    .then(response => response.json())
    .then(data => {
        const popup = document.getElementById('popup');
        const popupText = document.getElementById('popupText');
        const yesBtn = document.getElementById('yesBtn');
        const noBtn = document.getElementById('noBtn');

        popupText.textContent = `Имя товара: ${data.goods_name}`;
        popup.style.display = 'block';

        // Установить фокус на кнопку "Да"
        yesBtn.focus();

        // Обработчики кнопок Да и Нет
        yesBtn.onclick = () => sendAction(data.goods_id,userId, 1);
        noBtn.onclick = () => sendAction(data.goods_id,userId, 0);
    });
}

function sendAction(goods_id,userId, action) {
    const serverIP = `${window.location.protocol}//${window.location.hostname}:${window.location.port}`;

    fetch(`${serverIP}/semat/action`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ userId, goods_id, action })
    })
    .then(response => response.json())
    .then(data => {
        const countDisplay = document.getElementById('count');
        const popup = document.getElementById('popup');
        countDisplay.textContent = `Cчет: ${data.count}`;
        popup.style.display = 'none'; // Скрытие всплывающего сообщения
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const serverIP = `${window.location.protocol}//${window.location.hostname}:${window.location.port}`;

    // Элементы для экрана регистрации
    const registerBtn = document.getElementById('registerBtn');
    const surnameInput = document.getElementById('surname');
    const nameInput = document.getElementById('name');
    const organizationInput = document.getElementById('organization');

    // Элементы для экрана игры
    const gameContent = document.getElementById('gameContent');
    const playerNameDisplay = document.getElementById('playerName');
    const countDisplay = document.getElementById('count');
    const ScanMessage = document.getElementById('ScanMessage');
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');
    const popup = document.getElementById('popup');
    const popupText = document.getElementById('popupText');
    const yesBtn = document.getElementById('yesBtn');
    const noBtn = document.getElementById('noBtn');
    const timerDisplay = document.getElementById('timer');

    // Элементы для экрана завершения игры
    const endScreen = document.getElementById('endScreen');
    const endMessage = document.getElementById('endMessage');

    const inputs = [surnameInput, nameInput, organizationInput];

    inputs.forEach((input, index) => {
        input.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                event.preventDefault();
                input.blur();
                if (index < inputs.length - 1) {
                    inputs[index + 1].focus();
                } else {
                    // Если это последнее поле ввода, скрываем клавиатуру и нажимаем кнопку
                    registerBtn.focus();
                }
            }
        });
    });

    registerBtn.addEventListener('click', () => {
        // Свернуть клавиатуру путем потери фокуса на полях ввода
        surnameInput.blur();
        nameInput.blur();
        organizationInput.blur();

        // Ваши дополнительные действия при регистрации
        console.log('Регистрация выполнена');
    });


    let timer;

    // Обработчик нажатия на кнопку "Зарегистрироваться"
    registerBtn.addEventListener('click', () => {
        const user_surname = surnameInput.value;
        const user_name = nameInput.value;
        const organization = organizationInput.value;

        // Отправка данных на сервер для регистрации
        fetch(`${serverIP}/semat/reg`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_surname, user_name, organization, "attr_1":"1" })
        })
        .then(response => response.json())
        .then(data => {
            userId = data.user_id;
            playerNameDisplay.textContent = data.name;
            countDisplay.textContent = `Cчет: ${data.count}`;
            // Скрытие экрана регистрации и отображение экрана игры
            loginScreen.style.display = 'none';
            gameContent.style.display = 'block';
            startTimer(); // Запуск таймера обратного отсчета
        });
    });

    // Обработчик нажатия на кнопку "Отправить"
    searchBtn.addEventListener('click', () => {
        const barcode = searchInput.value;

        // Отправка запроса на сервер для поиска товара
        fetch(`${serverIP}/semat/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ barcode })
        })
        .then(response => response.json())
        .then(data => {
            popupText.textContent = `Имя товара: ${data.goodsname}`;
            popup.style.display = 'block';

            // Установить фокус на кнопку "Да"
            yesBtn.focus();

            // Обработчики кнопок Да и Нет
            yesBtn.onclick = () => sendAction(data.goods_id, 1);
            noBtn.onclick = () => sendAction(data.goods_id, 0);
        });
    });

    // Запуск таймера обратного отсчета
    function startTimer() {
        let timeLeft = 120; // 2 минуты
        timerDisplay.textContent = formatTime(timeLeft);

        timer = setInterval(() => {
            timeLeft -= 1;
            timerDisplay.textContent = formatTime(timeLeft);

            if (timeLeft <= 0) {
                clearInterval(timer);
                endGame(); // Завершение игры по истечению времени
            }
        }, 1000);
    }

    // Форматирование времени в минуты:секунды
    function formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
    }

    // Завершение игры и отображение итогового экрана
    function endGame() {
        endMessage.textContent = `${playerNameDisplay.textContent}, спасибо за игру. Ваш ${countDisplay.textContent}`;
        gameContent.style.display = 'none';
        endScreen.style.display = 'flex';
        endScreen.style.alignItems = 'center';
        endScreen.style.justifyContent = 'center';
    }
});
