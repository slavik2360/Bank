const btn = document.getElementById('new-card-btn')

btn.addEventListener('click', convertCurrency);

function convertCurrency() {
    const amountInput = document.querySelector('.total_amount');
    const selectedCurrency = document.getElementById('currencySelector').value;
    const resultElement = document.querySelector('.result');
    const text = document.querySelector('.info-p');

    const amountInKZT = parseFloat(amountInput.value);

    if (isNaN(amountInKZT)) {
        text.style.color = 'rgb(220, 53, 69)';
        text.innerText = 'Введите числовое значение!';
    }else{
        text.style.color = 'black';
        text.innerText = 'Нажмите, чтобы конвертировать валюту!';
    }

    const rate = parseFloat(selectedCurrency);
    const amountInCurrency = (amountInKZT / rate).toFixed(3);
    
    resultElement.textContent = amountInCurrency;
}


function getOption() {
    const option = document.getElementById('currencySelector');
    const selectedOption = option.options[option.selectedIndex];
    const selectedText = selectedOption.text;
    return selectedText;
}

function changeFlag() {
    const flagElement = document.querySelector('.flag_world');
    const selectedCurrency = getOption();

    const flagMapping = {
        'USD': '/static/icons/flag/сша.png',
        'EUR': '/static/icons/flag/европа.png',
        'RUB': '/static/icons/flag/россия.png',
        'GBP': '/static/icons/flag/великобритания.png',
        'JPY': '/static/icons/flag/япония.png',
        'CNY': '/static/icons/flag/китай.png',
    };

    if (flagMapping[selectedCurrency]) {
        flagElement.style.backgroundImage = `url('${flagMapping[selectedCurrency]}')`;
    }
}

document.getElementById('currencySelector').addEventListener('change', changeFlag);



const newCardBtn = document.querySelector('#new-card-btn');
newCardBtn.addEventListener('mouseenter', () => {
    anime({
        targets: newCardBtn,
        backgroundColor: 'rgb(255, 200, 51)', 
        easing: 'easeInOutQuad',
        duration: 300,
    });
});

newCardBtn.addEventListener('mouseleave', () => {
    anime({
        targets: newCardBtn,
        backgroundColor: 'rgb(255, 170, 51)',
        easing: 'easeInOutQuad',
        duration: 300,
    });
});

newCardBtn.addEventListener('mousedown', () => {
    anime({
        targets: newCardBtn,
        backgroundColor: 'rgb(255, 140, 51)',
        easing: 'easeInOutQuad',
        duration: 100,
    });
});

newCardBtn.addEventListener('mouseup', () => {
    anime({
        targets: newCardBtn,
        backgroundColor: 'rgb(255, 200, 51)',
        easing: 'easeInOutQuad',
        duration: 100,
    });
});