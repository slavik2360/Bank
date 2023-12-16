const btn = document.getElementById('transfer-btn')

btn.addEventListener('click', function () {
    const title = document.getElementById('title-input').value;
    const description = document.getElementById('desc-input').value;
    const amount = document.getElementById('amount-input').value;

    tokenManager.getAccessToken()
        .then(token => {
            const data = {
                title: title,
                description: description,
                price: amount,
            };
            axios.post('http://127.0.0.1:8000/api/v1/ads/create/', data, {
                headers: {
                    'Authorization': `Nimbus ${token}`,
                    'Content-Type': 'application/json',
                },
            })
                .then(response => {
                    let text = document.getElementById('transfer-info');
                    text.style.color = "rgb(40, 167, 79)";
                    text.innerText = "Объявление добавлено успешно!";

                    setTimeout(() => {
                        text.style.color = "rgb(40, 167, 79)";
                        text.innerHTML = `Перейти к: <a href="/ads/" class="aaddss" >Объявлениям</a>`;
                    }, 1000);
                })
                .catch(error => {
                    try {
                        console.log(error);
                        let text = document.getElementById('transfer-info');
                        for (field in error.response.data) {
                            for (err of error.response.data[field]) {
                                if (field === "title") {;
                                    text.style.color = "rgb(220, 53, 69)";
                                    text.innerText = err
                                } else if (field === "description") {
                                    text.style.color = "rgb(220, 53, 69)";
                                    text.innerText = err
                                }else if (field === "price") {
                                    text.style.color = "rgb(220, 53, 69)";
                                    text.innerText = err
                                }else if (field === "amount") {
                                    text.style.color = "rgb(220, 53, 69)";
                                    text.innerText = err
                                }else if (field === "balance") {
                                    text.style.color = "rgb(220, 53, 69)";
                                    text.innerText = err
                                }else{
                                    text.style.color = "rgb(220, 53, 69)";
                                    text.innerText = "Произошла ошибка при обращении к серверу";
                                }
                            }
                        }
                    } catch (e) {
                        console.error("Ошибка при обработке ошибки:", e);
                    }
                });
        });
});