function TokenManager() {
    let accessToken;
    let expireAt;

    async function setAccessToken() {
        try {
            const response = await axios.post("http://127.0.0.1:8000/api/v1/auth/login/token/");

            accessToken = response.data.access;
            expireAt = Date.now() + (4 * 60 * 1000);
            
            localStorage.setItem('access_token', accessToken);

            return accessToken;
        } catch (error) {
            console.error("Error setting access token:", error);
            throw error;
        }
    }

    async function getAccessToken() {
        const storedToken = localStorage.getItem('access_token');

        if (storedToken && Date.now() < expireAt) {
            accessToken = storedToken;
            return accessToken;
        }
        return await setAccessToken();
    }

    return { getAccessToken };
}

const tokenManager = TokenManager();

