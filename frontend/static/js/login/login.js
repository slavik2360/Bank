const eye = document.querySelector("#password-eye");
const inputEmail = document.querySelector("#email-input");
const inputPswrd = document.querySelector("#password-input");
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

btn.addEventListener("click", (event) => {
    event.preventDefault();
  
    let formdata = new FormData();
    formdata.append("email", inputEmail.value);
    formdata.append("password", inputPswrd.value);
  
    axios
        .post("http://127.0.0.1:8000/api/v1/auth/login/", formdata)
        .then(() => {
            inputEmail.style.border = "1px solid rgb(40, 167, 79)";
            
            inputPswrd.style.border = "1px solid rgb(40, 167, 79)";

            let text = document.querySelector(".info-p");
            text.style.color = "rgb(40, 167, 79)";
            text.innerText = "Вы успешно вошли";

            inputEmail.value = "";
            inputPswrd.value = "";

            setTimeout(() => {
                window.location.href = "/account/";
            }, 2000);
        })
        .catch(handleError);
});

function handleError(error) {
    if (error.response) {
        const text = document.querySelector('.info-p');
        for (const field in error.response.data) {
            for (const err of error.response.data[field]) {
                if (field) {
                    inputEmail.style.border = "1px solid rgb(220, 53, 69)";
                    inputPswrd.style.border = "1px solid rgb(220, 53, 69)";
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