const eye = document.querySelector("#password-eye");
const eye2 = document.querySelector("#password2-eye");
const inputCode = document.querySelector("#code-input");
const inputPswrd = document.querySelector("#password-input");
const inputPswrdRec = document.querySelector("#password2-input");
const btn = document.querySelector("#btnlog");


eye.addEventListener("click", () => {
  if (inputPswrd.type === "text") {
    inputPswrd.type = "password";
    eye.className = "bi bi-eye-slash";
  } else {
    inputPswrd.type = "text";
    eye.className = "bi bi-eye";
  }
});
eye2.addEventListener("click", () => {
    if (inputPswrdRec.type === "text") {
      inputPswrdRec.type = "password";
      eye2.className = "bi bi-eye-slash";
    } else {
      inputPswrdRec.type = "text";
      eye2.className = "bi bi-eye";
    }
});

inputCode.addEventListener("focus", () => {
  inputCode.style.border = "none";
});

inputPswrd.addEventListener("focus", () => {
  inputPswrd.style.border = "none";
});

inputPswrdRec.addEventListener("focus", () => {
    inputPswrd.style.border = "none";
  });




btn.addEventListener("click", async (event) => {
    event.preventDefault();
    let text = document.querySelector(".info-p");
    
    if (inputPswrd.value !== inputPswrdRec.value) {
        inputPswrd.style.border = "1px solid rgb(220, 53, 69)";
        inputPswrdRec.style.border = "1px solid rgb(220, 53, 69)";
        text.style.color = "rgb(220, 53, 69)";
        text.innerText = "Пароли должны совпадать";
        return;
    }

    try {
        let formdata = new FormData();
        let urlParts = window.location.href.split("/");
        let email = urlParts[urlParts.length-2];
        formdata.append("email", email);
        formdata.append("code", inputCode.value);
        formdata.append("password", inputPswrd.value);
        formdata.append("password2", inputPswrdRec.value);

        await axios.post("http://127.0.0.1:8000/api/v1/auth/reset-password/", {
            email: email,
            code: inputCode.value,
            password: inputPswrd.value,
            password2: inputPswrdRec.value
        });

        inputCode.style.border = "1px solid rgb(40, 167, 79)";
        inputPswrd.style.border = "1px solid rgb(40, 167, 79)";
        inputPswrdRec.style.border = "1px solid rgb(40, 167, 79)";

        text.style.color = "rgb(40, 167, 79)";
        text.innerText = "Вы успешно сменили пароль";

        setTimeout(() => {
            window.location.href = "/login/";
        }, 2000);

        inputCode.value = "";
        inputPswrd.value = "";
    } 
    catch (error) {
        let text = document.querySelector(".info-p");
        for (field in error.response.data) {
            for (err of error.response.data[field]) {
                if (field === "code") {
                    inputCode.style.border = "1px solid rgb(220, 53, 69)";
                    text.style.color = "rgb(220, 53, 69)";
                    text.innerText = err
                    inputPswrd.style.border = "1px solid grey";
                    inputPswrdRec.style.border = "1px solid grey";
                } else if (field === "password") {
                    inputPswrd.style.border = "1px solid rgb(220, 53, 69)";
                    inputPswrdRec.style.border = "1px solid rgb(220, 53, 69)";
                    text.style.color = "rgb(220, 53, 69)";
                    text.innerText = err
                    inputCode.style.border = "1px solid grey";
                }else{
                    text.style.color = "rgb(220, 53, 69)";
                    text.innerText = "Произошла ошибка при обращении к серверу";
                }
            }
        }
    }
});