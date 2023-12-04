const firstNameInput = document.querySelector("#first_name")
const lastNameInput = document.querySelector("#last_name")
const emailInput = document.querySelector("#email")
const passwordInput = document.querySelector("#password")
const passwordRepeatInput = document.querySelector("#password2")

const firstNameValidator = document.querySelector("#first_name_validator")
const lastNameValidator = document.querySelector("#last_name_validator")
const emailValidator = document.querySelector("#email_validator")
const passwordValidator = document.querySelector("#password_validator")
const passwordRepeatValidator = document.querySelector("#password2_validator")

const firstNameIcon = document.querySelector("#first_name_icon")
const lastNameIcon = document.querySelector("#last_name_icon")
const emailIcon = document.querySelector("#email_icon")
const passwordIcon = document.querySelector("#password_icon")
const passwordRepeatIcon = document.querySelector("#password2_icon")

const passwordEye = document.querySelector("#password_eye")
const passwordRepeatEye = document.querySelector("#password2_eye")

const hintsContainer = document.querySelector(".hints-container")

firstNameInput.addEventListener("input", () => {
    if (firstNameInput.value.length > 0) {
        firstNameValidator.className = "bi bi-check-square"
        firstNameValidator.style.cssText = `color: rgb(255, 170, 51);
                                            font-size: medium;`
        firstNameIcon.style.cssText = "border-bottom: 1px solid rgb(255, 170, 51)"
    } else {
        firstNameIcon.style.cssText = "border-bottom: 1px solid rgb(255, 123, 0);"
        firstNameValidator.className = "bi bi-exclamation-diamond"
        firstNameValidator.style.cssText = "color: rgb(255, 123, 0);"
    }
})

lastNameInput.addEventListener("input", () => {
    if (lastNameInput.value.length > 0) {
        lastNameValidator.className = "bi bi-check-square"
        lastNameValidator.style.cssText = `color: rgb(255, 170, 51);
                                           font-size: medium;`
        lastNameIcon.style.cssText = "border-bottom: 1px solid rgb(255, 170, 51)"
    } else {
        lastNameValidator.className = "bi bi-exclamation-diamond"
        lastNameValidator.style.cssText = "color: rgb(255, 123, 0);"
        lastNameIcon.style.cssText = "border-bottom: 1px solid rgb(255, 123, 0);"
    }
})

emailInput.addEventListener("input", () => {
    const regex = /^[^\d\s]\w+@(\w+\.\w+)$/;
    const allowedDomains = ['yandex.ru', 'gmail.com', 'mail.ru',
                            'bk.ru','ok.ru', 'cloud.com']
    let text = emailInput.value
    let parts = text.split("@")

    if (
        regex.test(text) &&
        allowedDomains.includes(
            parts[parts.length-1]
        )
    ) {
        emailValidator.className = "bi bi-check-square"
        emailValidator.style.cssText = `color: rgb(255, 170, 51);
                                        font-size: medium;`
        emailIcon.style.cssText = "border-bottom: 1px solid rgb(255, 170, 51)"
    } else {
        emailValidator.className = "bi bi-exclamation-diamond"
        emailValidator.style.cssText = "color: rgb(255, 123, 0);"
        emailIcon.style.cssText = "border-bottom: 1px solid rgb(255, 123, 0);"
    }
})

passwordInput.addEventListener("input", () => {
    const regexOnlyLetters = /^[a-zA-Zа-яА-ЯёЁ]+$/;
    const regexOnlyNumbers = /^[0-9]+$/;
    const regexChars = /^[а-яА-ЯёЁa-zA-Z0-9]+$/;
    let text = passwordInput.value

    if (
        regexChars.test(text) &&
        !regexOnlyNumbers.test(text) &&
        !regexOnlyLetters.test(text) &&
        text.length > 6
    ) {
        passwordIcon.className = "bi bi-lock-fill"
        passwordValidator.className = "bi bi-check-square"
        passwordValidator.style.cssText = `color: rgb(255, 170, 51);
                                           font-size: medium;`
        passwordIcon.style.cssText = "border-bottom: 1px solid rgb(255, 170, 51)"
        if (text == passwordRepeatInput.value) {
            passwordRepeatIcon.className = "bi bi-lock-fill"
            passwordRepeatValidator.className = "bi bi-check-square"
            passwordRepeatValidator.style.cssText = `color: rgb(255, 170, 51);
                                                     font-size: medium;`
            passwordRepeatIcon.style.cssText = "border-bottom: 1px solid rgb(255, 170, 51)"
        } else {
            passwordRepeatIcon.className = "bi bi-unlock-fill"
            passwordRepeatValidator.className = "bi bi-exclamation-diamond"
            passwordRepeatValidator.style.cssText = "color: rgb(255, 123, 0);"
            passwordRepeatIcon.style.cssText = "border-bottom: 1px solid rgb(255, 123, 0);"
        }
    } else {
        passwordIcon.className = "bi bi-unlock-fill"
        passwordValidator.className = "bi bi-exclamation-diamond"
        passwordValidator.style.cssText = "color: rgb(255, 123, 0);"
        passwordRepeatIcon.className = "bi bi-unlock-fill"
        passwordRepeatValidator.className = "bi bi-exclamation-diamond"
        passwordRepeatValidator.style.cssText = "color: rgb(255, 123, 0);"
        passwordIcon.style.cssText = "border-bottom: 1px solid rgb(255, 123, 0);"
        passwordRepeatIcon.style.cssText = "border-bottom: 1px solid rgb(255, 123, 0);"
    }
})

passwordRepeatInput.addEventListener("input", () => {
    const regexOnlyLetters = /^[a-zA-Zа-яА-ЯёЁ]+$/;
    const regexOnlyNumbers = /^[0-9]+$/;
    const regexChars = /^[а-яА-ЯёЁa-zA-Z0-9]+$/;
    let text = passwordRepeatInput.value

    if (
        regexChars.test(text) &&
        !regexOnlyNumbers.test(text) &&
        !regexOnlyLetters.test(text) &&
        text.length > 6 &&
        text == passwordInput.value
    ) {
        passwordRepeatIcon.className = "bi bi-lock-fill"
        passwordRepeatValidator.className = "bi bi-check-square"
        passwordRepeatValidator.style.cssText = `color: rgb(255, 170, 51);
                                                 font-size: medium;`
        passwordRepeatIcon.style.cssText = "border-bottom: 1px solid rgb(255, 170, 51)"
    } else {
        passwordRepeatIcon.className = "bi bi-unlock-fill"
        passwordRepeatValidator.className = "bi bi-exclamation-diamond"
        passwordRepeatValidator.style.cssText = "color: rgb(255, 123, 0);"
        passwordRepeatIcon.style.cssText = "border-bottom: 1px solid rgb(255, 123, 0);"
    }
})

passwordEye.addEventListener("mousedown", () => {
    passwordEye.className = "bi bi-eye"
    passwordInput.type = "text"
})

passwordRepeatEye.addEventListener("mousedown", () => {
    passwordRepeatEye.className = "bi bi-eye"
    passwordRepeatInput.type = "text"
})

passwordEye.addEventListener("mouseout", () => {
    passwordEye.className = "bi bi-eye-slash"
    passwordInput.type = "password"
})

passwordRepeatEye.addEventListener("mouseout", () => {
    passwordRepeatEye.className = "bi bi-eye-slash"
    passwordRepeatInput.type = "password"
})

passwordEye.addEventListener("mouseup", () => {
    passwordEye.className = "bi bi-eye-slash"
    passwordInput.type = "password"
})

passwordRepeatEye.addEventListener("mouseup", () => {
    passwordRepeatEye.className = "bi bi-eye-slash"
    passwordRepeatInput.type = "password"
})

firstNameInput.addEventListener("focus", () => {
    hintsContainer.innerHTML = `<p>Поле должно содержать как минимум один символ</p>
                                <p>Используйте настоящее имя</p>`;
});

lastNameInput.addEventListener("focus", () => {
    hintsContainer.innerHTML = `<p>Поле должно содержать как минимум один символ</p>
                                <p>Используйте настоящую фамилию</p>`;
});

emailInput.addEventListener("focus", () => {
    hintsContainer.innerHTML = `<p>Основная часть должна начинаться с буквы</p>
                                <p>Как минимум два символа в основной части</p>
                                <p>Разрешенные домены: yandex.ru, gmail.com, mail.ru,
                                bk.ru, ok.ru, cloud.com</p>`;
});

passwordInput.addEventListener("focus", () => {
    hintsContainer.innerHTML = `<p>Пароль должен содержать цифры и буквы</p>
                                <p>Минимальная длина - 7 символов</p>`;
});

passwordRepeatInput.addEventListener("focus", () => {
    hintsContainer.innerHTML = `<p>Пароль должен совпадать с предыдущим</p>`;
});

firstNameInput.addEventListener("blur", () => {
    if (inActive === false) {
        hintsContainer.innerHTML = `<p>Нажмите на поле для просмотра подсказок</p>`;
    }
});

lastNameInput.addEventListener("blur", () => {
    if (inActive === false) {
        hintsContainer.innerHTML = `<p>Нажмите на поле для просмотра подсказок</p>`;
    }
});

emailInput.addEventListener("blur", () => {
    if (inActive === false) {
        hintsContainer.innerHTML = `<p>Нажмите на поле для просмотра подсказок</p>`;
    }
});

passwordInput.addEventListener("blur", () => {
    if (inActive === false) {
        hintsContainer.innerHTML = `<p>Нажмите на поле для просмотра подсказок</p>`;
    }
});

passwordRepeatInput.addEventListener("blur", () => {
    if (inActive === false) {
        hintsContainer.innerHTML = `<p>Нажмите на поле для просмотра подсказок</p>`;
    }
});

const form = document.querySelector(".registration-form")
const btn = document.querySelector("#register")

btn.addEventListener("click", event => {
    event.preventDefault()

    formdata = new FormData(form)
    axios.post("http://127.0.0.1:8000/api/v1/auth/register/", formdata)
    .then(() => {
        stopLoading()

        let errStyles = "border-bottom: 1px solid rgb(132, 224, 124);"
        let successStyles = "color: rgb(132, 224, 124);"

        firstNameIcon.style.cssText = errStyles
        lastNameIcon.style.cssText = errStyles
        emailIcon.style.cssText = errStyles
        passwordIcon.style.cssText = errStyles
        passwordRepeatIcon.style.cssText = errStyles

        firstNameValidator.style.cssText = successStyles
        lastNameValidator.style.cssText = successStyles
        emailValidator.style.cssText = successStyles
        passwordValidator.style.cssText = successStyles
        passwordRepeatValidator.style.cssText = successStyles
        for (data of formdata) {
            if (data[0] == "email") {
                console.log(data[1])
                var user_email = data[1]
            }
        }
        hintsContainer.innerHTML = `<h2>Подсказки</h2>
                                    <p style='color: rgb(15, 126, 15);'>
                                    Спасибо за регистрацию</p>
                                    <p style='color: rgb(15, 126, 15);'>
                                    Пожалуйста, 
                                    <a href="/account/activate/${user_email}/"
                                        style="color: rgb(19, 139, 19);">
                                    подтвердите её</a>
                                    </p>
                                    <p style='color: rgb(15, 126, 15);'>
                                    Код был отправлен на вашу почту</p>`;
        form.reset()
    })
    .catch(errors => {
        stopLoading()

        let errorsMap = errors.response.data

        for (err in errorsMap) {

            for (newError of errorsMap[err]) {
                if (newError !== "Это поле не может быть пустым.") {
                    hintsContainer.innerHTML += `<p style="color: rgb(217, 56, 70)">
                                                    ${newError}</p>`
                }
            }

            let input = document.querySelector(`#${err}_icon`)
            input.style.cssText = "border-bottom: 1px solid rgb(217, 56, 70);"
        }
    })
})
