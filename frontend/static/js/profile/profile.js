const userFullname = document.querySelector(".user-fullname")
const userEmail = document.querySelector(".user-email")
const userGender = document.querySelector(".user-gender")
const userJoin = document.querySelector(".user-join")
const userAvatar = document.querySelector("#avatar")
const getCard = document.querySelector("#new-card-btn")
const updateAvatar = document.getElementById('uploadAvatar')
// CARD
const eye = document.querySelector("#cvv_eye");
const cvv3 = document.querySelector("#requisite_cvv")
const num1 = document.querySelector("#requisite_nums1");
const num2 = document.querySelector("#requisite_nums2");
const num3 = document.querySelector("#requisite_nums3");
const num4 = document.querySelector("#requisite_nums4");
const req_date = document.querySelector("#requisite_date")
const req_balance = document.querySelector("#requisite_balance")
const req_fulname = document.querySelector("#requisite_fullname")

const data = {};

function getUserInfo() {
    tokenManager.getAccessToken()
        .then(token => {
            axios.get("http://127.0.0.1:8000/api/v1/auth/user/", {
                headers: {
                    "Authorization" : `Nimbus ${token}`
                }
            })
            .then(response => {
                data.userInfo = response.data;
                updateUserInfo();
            })
            .catch(handleError);
        });
}

function updateUserInfo() {
    const { avatar, last_name, first_name, email, datetime_created } = data.userInfo;
    userFullname.innerText = `${last_name} ${first_name}`;
    userFullname.style.cssText = "font-size: 140%";
    userEmail.innerText = `${email}`;
    userEmail.style.cssText = "color: darkgray";
    userAvatar.style.cssText = `background-image: url('${avatar}')`
    userJoin.innerText += ` ${datetime_created.split(" ")[0]}`;
}

function animateCard() {
    tokenManager.getAccessToken()
        .then(token => {
            axios.get('http://127.0.0.1:8000/api/v1/bank/requisite/', {
                headers: {
                    'Authorization': `Nimbus ${token}`,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => {
                data.cardInfo = response.data;
                updateCardInfo();
            })
            .catch(handleError);
        });
}

function updateCardInfo() {
    const { full_name, account_balance, card_expiry_date, card_number, card_cvv } = data.cardInfo;
    req_fulname.innerText = full_name;
    req_balance.innerText =`${account_balance}₸`;
    req_date.innerText = card_expiry_date;
    num1.innerText = card_number.slice(0, 4);
    num2.innerText = card_number.slice(4, 8);
    num3.innerText = card_number.slice(8, 12);
    num4.innerText = card_number.slice(12, 16);
    cvv3.innerText = '***';

    anime({
        targets: '#requisite_fullname',
        opacity: [0, 1],
        translateY: [20, 0],
        scaleX: [0.8, 1],
        easing: 'easeInOutQuad',
        duration: 1000,
        elasticity: 1500,
        delay: 500,
    });
    anime({
        targets: '#requisite_date',
        opacity: [0, 1],
        translateY: [20, 0],
        scaleX: [0.8, 1],
        easing: 'easeInOutQuad',
        duration: 1000,
        elasticity: 1500,
        delay: 500,
    });
    anime({
        targets: ['#requisite_nums1', '#requisite_nums2', '#requisite_nums3', '#requisite_nums4'],
        opacity: [0, 1],
        translateY: [20, 0],
        scaleX: [0.8, 1],
        easing: 'easeInOutQuad',
        duration: 1000,
        elasticity: 1500,
        delay: anime.stagger(200),
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

eye.addEventListener('click', () => {
    data.isCVVVisible = !data.isCVVVisible;
    if (data.isCVVVisible) {
        cvv3.innerText = data.cardInfo.card_cvv;
        eye.className = 'bi bi-eye';
    } else {
        cvv3.innerText = '***';
        eye.className = 'bi bi-eye-slash';
    }
});

getCard.addEventListener('click', (event) => {
    event.preventDefault();
    tokenManager.getAccessToken()
        .then(token => {
            axios.post('http://127.0.0.1:8000/api/v1/bank/create/', {}, {
                headers: {
                    'Authorization': `Nimbus ${token}`,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => {
                const text = document.querySelector('.info-p');
                text.style.color = 'rgb(40, 167, 79)';
                text.innerText = response.data['data'];
                setTimeout(animateCard, 100);
            })
            .catch(error => {
                handleError(error);
            });
        });
});
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

animateCard()
getUserInfo()

updateAvatar.addEventListener('click', function () {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.style.display = 'none';
    document.body.appendChild(fileInput);

    fileInput.addEventListener('change', function (event) {
        const formData = new FormData();
        formData.append('avatar', event.target.files[0]);

        tokenManager.getAccessToken()
            .then(token => {
                axios.patch('http://127.0.0.1:8000/api/v1/auth/update-avatar/', formData, {
                    headers: {
                        'Authorization': `Nimbus ${token}`,
                        'Content-Type': 'multipart/form-data',
                    },
                })
                .then(response => {
                    location.reload()
                })
                .catch(error => {
                    alert(error.response.data.avatar)
                });
            });

        document.body.removeChild(fileInput);
    });

    fileInput.click();
});
