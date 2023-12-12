// CARD
const cvv3 = document.querySelector("#requisite_cvv")
const num1 = document.querySelector("#requisite_number");
const req_date = document.querySelector("#requisite_date")
const req_balance = document.querySelector("#requisite_balance")
const req_fulname = document.querySelector("#requisite_fullname")
const data = {};

function animateRequisite() {
    tokenManager.getAccessToken()
        .then(token => {
            axios.get('http://127.0.0.1:8000/api/v1/bank/requisite/', {
                headers: {
                    'Authorization': `Nimbus ${token}`,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => {
                data.Info = response.data;
                console.log(data);
                updateInfo();
            })
            .catch(handleError);
        });
}

function updateInfo() {
    const { full_name, card_expiry_date, card_number, card_cvv } = data.Info;
    req_fulname.innerText = `Владелец: ${full_name}`;
    req_date.innerText = `Дата окончания: ${card_expiry_date}`;
    num1.innerText = `Номер карты: ${card_number}`;
    cvv3.innerText = `CVV: ${card_cvv}`;

    animateElement('#requisite_fullname');
    animateElement('#requisite_date');
    animateElement('#requisite_number');
    animateElement('#requisite_cvv');
}

function animateElement(selector) {
    anime({
        targets: selector,
        opacity: [0, 1],
        translateY: [20, 0],
        scaleX: [0.8, 1],
        easing: 'easeInOutQuad',
        duration: 1000,
        elasticity: 100,
        delay: 200,
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

animateRequisite();
