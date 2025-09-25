function getUserInfo() {
    const token = localStorage.getItem("token")
    if (!token){
        return null;
    }
    return {
        token,
        name: localStorage.getItem("name")
    }
}
function setToken(userInfo) {
    localStorage.setItem('token', userInfo.token)
    localStorage.setItem('name', userInfo.name)
}

function cleanToken() {
    localStorage.removeItem('token')
    localStorage.removeItem('name')
}
export {getUserInfo, setToken, cleanToken}