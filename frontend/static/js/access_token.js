function TokenManager() {
    let accessToken;
    let expireAt;

    async function setAccessToken() {
        try {
            const response = await axios.post("http://127.0.0.1:8000/api/v1/auth/login/token/");

            accessToken = response.data.access;
            expireAt = Date.now() + (4 * 60 * 1000);

            // Сохраняем токен в localStorage
            localStorage.setItem('access_token', accessToken);

            return accessToken;
        } catch (error) {
            console.error("Error setting access token:", error);
            throw error;
        }
    }

    async function getAccessToken() {
        // Проверяем, есть ли токен в localStorage
        const storedToken = localStorage.getItem('access_token');

        // Если токен есть и он еще не истек, возвращаем его
        if (storedToken && Date.now() < expireAt) {
            accessToken = storedToken;
            return accessToken;
        }

        // В противном случае, получаем новый токен
        return await setAccessToken();
    }

    return { getAccessToken };
}

const tokenManager = TokenManager();

