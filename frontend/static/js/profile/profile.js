const userFullname = document.querySelector(".user-fullname")
const userEmail = document.querySelector(".user-email")
const userGender = document.querySelector(".user-gender")
const userJoin = document.querySelector(".user-join")
const profileImage = document.querySelector("#avatar")
const getCard = document.querySelector("#new-card-btn")
const eye = document.querySelector("#cvv_eye");
const cvv3 = document.querySelector("#requisite_cvv")


tokenManager.getAccessToken()
.then(token => {
    axios.get("http://127.0.0.1:8000/api/v1/auth/user/", {
        headers: {
            "Authorization" : `Nimbus ${token}`
        }
    })
    .then(response => {
        let data = response.data

        if (data.gender === 2) {
            profileImage.computedStyleMap.border = "2px solid purple"
        }
        
        userFullname.innerText = `${data.last_name} ${data.first_name}`
        userFullname.style.cssText = "font-size: 140%"

        userEmail.innerText = `${data.email}`
        userEmail.style.cssText = "color: darkgray"


        userJoin.innerText += ` ${data.datetime_created.split(" ")[0]}`
    })
})

function animationCard() {
    let num1 = document.querySelector("#nums1");
    let num2 = document.querySelector("#nums2");
    let num3 = document.querySelector("#nums3");
    let num4 = document.querySelector("#nums4");

    tokenManager.getAccessToken()
    tokenManager.getAccessToken()
    .then(token => {
        axios.request({
            method: 'get',
            url: 'http://127.0.0.1:8000/api/v1/bank/requisite/',
            headers: {
                'Authorization': `Nimbus ${token}`,
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            // Обработка успешного ответа
            console.log('Карта успешно создана:', response.data);
        })
        .catch(error => {
            console.error('Ошибка при создании карты:', error);
        });
    });

    
}

getCard.addEventListener('click', (event) => {
    event.preventDefault();

    tokenManager.getAccessToken()
    .then(token => {
        axios.request({
            method: 'post',
            url: 'http://127.0.0.1:8000/api/v1/bank/create/',
            headers: {
                'Authorization': `Nimbus ${token}`,
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            let text = document.querySelector(".info-p");
            text.style.color = "rgb(40, 167, 79)";
            text.innerText = `Карта успешно выпущена`;
            console.log('Карта успешно Выпущенна:', response.data);
        })
        .catch(error => {
            let text = document.querySelector(".info-p");
                if (error.response) {
                for (field in error.response.data) {
                    for (err of error.response.data[field]) {
                    if (field === "card") {
                        text.style.color = "rgb(220, 53, 69)";
                        text.innerText = err;
                    }else {
                        text.style.color = "rgb(220, 53, 69)";
                        text.innerText = "Произошла ошибка при обращении к серверу";
                    }
                    }
                }}
        });
    });
});

animationCard()


// eye.addEventListener("click", () => {
//     if (cvv3) {
//       cvv3.innerHTML = "****";
//       eye.className = "bi bi-eye-slash";
//     } else {
//       cvv3.innerHTML = "144";
//       eye.className = "bi bi-eye";
//     }
// });