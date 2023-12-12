const btn = document.getElementById('transfer-btn')

btn.addEventListener('click', function () {
    const sender = document.getElementById('sender-input').value;
    const receiver = document.getElementById('recipient-input').value;
    const amount = document.getElementById('amount-input').value;

    tokenManager.getAccessToken()
    .then(token => {
        const data = {
            sender: sender,
            receiver: receiver,
            amount: amount,
        };
        axios.post('http://127.0.0.1:8000/api/v1/bank/refill/', data, {
            headers: {
                'Authorization': `Nimbus ${token}`,
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            let text = document.getElementById('transfer-info');
            text.style.color = "rgb(40, 167, 79)";
            text.innerText = "Пополение выполнено успешно!";
        })
        .catch(error => {
            let text = document.getElementById('transfer-info');
            for (field in error.response.data) {
                for (err of error.response.data[field]) {
                    if (field === "card") {;
                        text.style.color = "rgb(220, 53, 69)";
                        text.innerText = err
                    } else if (field === "balance") {
                        text.style.color = "rgb(220, 53, 69)";
                        text.innerText = err
                    }else if (field === "amount") {
                        text.style.color = "rgb(220, 53, 69)";
                        text.innerText = err
                    }else{
                        text.style.color = "rgb(220, 53, 69)";
                        text.innerText = "Произошла ошибка при обращении к серверу";
                    }
                }
            }
        });
    });
});