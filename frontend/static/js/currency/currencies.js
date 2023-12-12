// CURRENCIES
const getCurrency = document.querySelector("#new-card-btn")
const currency = document.querySelector("#currency-exchange")
const rates = document.querySelector(".money") 
const data = {};

getCurrency.addEventListener('click', (event) => {
    event.preventDefault();
            axios.post('http://127.0.0.1:8000/api/v1/bank/currency_create/', {},)
            .then(response => {
                const text = document.querySelector('.info-p');
                text.style.color = 'rgb(40, 167, 79)';
                text.innerText = response.data['data'];
                setTimeout(animateCurrency, 100);
            })
            .catch(error => {
                handleError(error);
            });
});


function animateCurrency() {
        axios.get('http://127.0.0.1:8000/api/v1/bank/get_currency/', {}, )
        .then(response => {
            data.Info = response.data;
            console.log(data);
            updateInfo();
        })
        .catch(handleError);

}

function updateInfo() {
    const currencyElements = document.querySelectorAll('.cur_cur .money');
    
    currencyElements.forEach((element, index) => {
        const rate = parseFloat(data.Info[index].rate);
        const amountInCurrency = rate;
        
        element.textContent = amountInCurrency;
    });
}


function handleError(error) {
    if (error.response) {
        const text = document.querySelector('.info-p');
        for (const field in error.response.data) {
            for (const err of error.response.data[field]) {
                if (field) {
                    text.style.color = 'rgb(220, 53, 69)';
                    text.innerText = err;
                } else {
                    text.style.color = 'rgb(220, 53, 69)';
                    text.innerText = 'Произошла ошибка при обращении к серверу';
                }
            }
        }
    }
}

animateCurrency()

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