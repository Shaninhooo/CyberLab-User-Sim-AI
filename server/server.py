from NextCloud import startNextCloud
from actions import startupNewAcc, openContainer, Login

username = "user"
password = "password"

startNextCloud()

startupNewAcc(username, password)
