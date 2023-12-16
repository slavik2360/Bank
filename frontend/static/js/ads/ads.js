function loadAds() {
    const apiUrl = 'http://127.0.0.1:8000/api/v1/ads/ad_all/';
    document.querySelector('.first-container').innerHTML = '';
    document.querySelector('.two-container').innerHTML = '';
    document.querySelector('.three-container').innerHTML = '';

    axios.get(apiUrl)
        .then(response => {
            const ads = response.data;
            
            ads.forEach(ad => {
                const card = createAdCard(ad);
                
                // В какой контейнер добавить объявление в зависимости от статуса
                if (ad.status === 0) {
                    document.querySelector('.first-container').appendChild(card);
                } else if (ad.status === 1) {
                    document.querySelector('.two-container').appendChild(card);
                } else if (ad.status === 2) {
                    document.querySelector('.three-container').appendChild(card);
                }
            });
        })
        .catch(error => {
            console.error('Ошибка при загрузке объявлений', error);
        });
};

function createAdCard(ad) {
    const cardContainer = document.createElement('div');
    cardContainer.classList.add('info-first');

    const card = document.createElement('div');
    card.classList.add('info-invis');

    let buttonLabel = 'Принять';
    if (ad.status === 1) {
        buttonLabel = 'Выполнить';
    } else if (ad.status === 2) {
        buttonLabel = 'Выполнено';
    }

    card.innerHTML = `
        <div class="info-img" style="background-image: url(${ad.image})"></div>
        <div class="info-title">
            <p class="title-">${ad.title}</p>
        </div>
        <div class="info-desc">
            <p class="desc_">${ad.description}</p>
        </div>
        <div class="info-price">
            <p class="price_">${ad.price}₸</p>
        </div>
        <button type="button" class="info-btn" onclick="handleButtonClick(${ad.id}, ${ad.status})">${buttonLabel}</button>
    `;

    cardContainer.appendChild(card);

    return cardContainer;
}

function handleButtonClick(adId, adStatus) {
    if (adStatus === 0) {
        // Принять объявление
        acceptAd(adId);
    } else if (adStatus === 1) {
        // Выполнить объявление
        completeAd(adId);
    } else if (adStatus === 2) {
        alert('Это объявление уже выполнено');
    }
}

function acceptAd(adId) {
    const acceptUrl = `http://127.0.0.1:8000/api/v1/ads/take/${adId}/`;

    tokenManager.getAccessToken()
        .then(token => {
            axios.post(acceptUrl, {}, {
                headers: {
                    'Authorization': `Nimbus ${token}`
                }
            })
            .then(response => {
                alert('Объявление принято')
                console.log('Объявление принято', response.data);
                loadAds();
            })
            .catch(error => {
                if (error.response && error.response.status === 403) {
                    alert('Нельзя принять свое собственное объявление');
                } else {
                    alert('Ошибка при принятии объявления');
                    console.error('Ошибка при принятии объявления', error);
                }
            });
        })
        .catch(error => {
            alert('Необходимо выполнить авторизацию');
        });
}

function completeAd(adId) {
    const completeUrl = `http://127.0.0.1:8000/api/v1/ads/complete/${adId}/`;

    tokenManager.getAccessToken()
        .then(token => {
            axios.post(completeUrl, {}, {
                headers: {
                    'Authorization': `Nimbus ${token}`
                }
            })
            .then(response => {
                alert('Работа успешно выполнена');
                console.log('Работа успешно выполнена', response.data);
                loadAds();
            })
            .catch(error => {
                if (error.response && error.response.status === 403 && error.response.data.error === 'Вы не являетесь заказчиком этого объявления') {
                    alert('Вы не являетесь заказчиком этого объявления');
                } else {
                    alert('Ошибка при выполнении работы');
                    console.error('Ошибка при выполнении работы', error);
                }
            });
        })
        .catch(error => {
            alert('Необходимо выполнить авторизацию');
        });
}


document.addEventListener('DOMContentLoaded', loadAds);