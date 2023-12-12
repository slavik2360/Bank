// Функция для проверки аутентификации пользователя
async function checkAuthentication() {
    try {
        const response = await fetch("http://127.0.0.1:8000/api/v1/auth/is-auth/", {
            method: "GET",
            credentials: "include", 
        });

        if (response.status !== 200) {
            throw new Error(`Проверка аутентификации не удалась со статусом: ${response.status}`);
        }
        console.log("Пользователь аутентифицирован!");
    } catch (error) {
        console.error("Ошибка проверки Аутентификации:", error);
        window.location.href = "/login/";
    }
}


checkAuthentication();

  