const eye = document.querySelector("#password-eye");
const inputEmail = document.querySelector("#email-input");
const btn = document.querySelector("#btnlog");


inputEmail.addEventListener("focus", () => {
  inputEmail.style.border = "none";
});


btn.addEventListener("click", async (event) => {
  event.preventDefault();

  try {
    let formdata = new FormData();
    formdata.append("email", inputEmail.value);

    const response = await axios.post("http://127.0.0.1:8000/api/v1/auth/forgot-password/", {
      email: inputEmail.value,
    });

    inputEmail.style.border = "1px solid rgb(40, 167, 79)";

    let text = document.querySelector(".info-p");
    text.style.color = "rgb(40, 167, 79)";
    text.innerText = `Код восстановления отправлен на почту`;

    inputEmail.value = "";
  } catch (error) {
    let text = document.querySelector(".info-p");
    if (error.response) {
      for (field in error.response.data) {
        for (err of error.response.data[field]) {
          if (field === "email") {
            inputEmail.style.border = "1px solid rgb(220, 53, 69)";
            text.style.color = "rgb(220, 53, 69)";
            text.innerText = err;
          } else {
            text.style.color = "rgb(220, 53, 69)";
            text.innerText = "Произошла ошибка при обращении к серверу";
          }
        }
      }
    } else {
      // Если нет ответа от сервера
      text.style.color = "rgb(220, 53, 69)";
      text.innerText = "Произошла неизвестная ошибка";
    }
  }
});
