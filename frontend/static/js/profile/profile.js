const userFullname = document.querySelector(".user-fullname")
const userEmail = document.querySelector(".user-email")
const userGender = document.querySelector(".user-gender")
const userJoin = document.querySelector(".user-join")
const profileImage = document.querySelector("#avatar")

tokenManager.getAccessToken()
.then(token => {
    axios.get("http://127.0.0.1:8000/api/v1/auth/user/", {
        headers: {
            "Authorization" : `Bearer ${token}`
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
