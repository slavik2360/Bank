document.addEventListener("DOMContentLoaded", function () {
    const transactionContainer = document.getElementById("transactionContainer");
    const paginationContainer = document.getElementById("paginationContainer");

    const pageSize = 10;

    tokenManager.getAccessToken()
        .then(token => {
            function fetchTransactions(url) {
                axios.get(url, {
                    headers: {
                        "Authorization": `Nimbus ${token}`
                    }
                })
                .then(response => {
                    const transactions = response.data.results;

                    transactions.forEach(transaction => {
                        const transactionCard = createTransactionCard(transaction);
                        transactionContainer.appendChild(transactionCard);
                    });

                    const pagination = response.data.pagination;
                    if (pagination && pagination.next) {
                        const loadMoreButton = createLoadMoreButton(pagination.next);
                        paginationContainer.appendChild(loadMoreButton);
                    }
                })
                .catch(error => {
                    console.error("Ошибка транзакций:", error.message);
                });
            }

            function createTransactionCard(transaction) {
                const card = document.createElement("div");
                card.classList.add("transaction-card");

                const amountInfo = `Сумма: ${transaction.amount}`;
                const transactionType = transaction.transaction_type === "debit" ? "Списание" : "Пополнение";
                const transactionTypeInfo = `Тип транзакции: ${transactionType}`;
                const dateInfo = `Дата: ${transaction.datetime_created}`;

                const amountParagraph = createParagraph(amountInfo);
                const transactionTypeParagraph = createParagraph(transactionTypeInfo);
                const dateParagraph = createParagraph(dateInfo);

                card.appendChild(amountParagraph);
                card.appendChild(transactionTypeParagraph);
                card.appendChild(dateParagraph);

                if (parseFloat(transaction.amount) < 0) {
                    card.classList.add("amount-negative");
                }

                return card;
            }

            function createParagraph(text) {
                const paragraph = document.createElement("p");
                paragraph.textContent = text;
                return paragraph;
            }

            function createLoadMoreButton(nextPageUrl) {
                const button = document.createElement("button");
                button.classList.add("btn_trans");
                button.textContent = "Показать Еще";
                button.addEventListener("click", function () {
                    paginationContainer.removeChild(button);
                    fetchTransactions(nextPageUrl);
                });

                return button;
            }

            try {
                fetchTransactions("http://127.0.0.1:8000/api/v1/ads/history_ads/");
            } catch (error) {
                console.error("Произошла ошибка при запросе:", error.message);
            }
        });
});


// tokenManager.getAccessToken()
// .then(token => {
// axios.get('http://127.0.0.1:8000/api/v1/ads/history_ads/', {
//   headers: {
//     'Authorization': `Nimbus ${token}`,
//   },
// })
//   .then(response => {
//     console.log(response.data);
//   })
//   .catch(error => {
//     console.error("Ошибка транзакций:", error);
//   });
// })