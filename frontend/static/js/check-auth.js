// Асинхронная функция для проверки аутентификации
async function checkAuthentication() {
    try {
        const response = await fetch("http://127.0.0.1:8000/api/v1/auth/is-auth/", {
            method: "GET",
            credentials: "include", // Передача куки
        });

        if (response.status !== 200) {
            throw new Error(`Проверка аутентификации не удалась со статусом: ${response.status}`);
        }

        // Продолжайте выполнение кода, если аутентификация прошла успешно
        console.log("Пользователь аутентифицирован!");
    } catch (error) {
        // Обработка ошибки, например, перенаправление на страницу входа
        console.error("Ошибка проверки Аутентификации:", error);
        window.location.href = "/login/";
    }
}

// Вызов функции для проверки аутентификации
checkAuthentication();

  