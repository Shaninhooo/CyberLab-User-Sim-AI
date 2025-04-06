from NextCloud import startNextCloud
from actions import startupNewAcc, openContainer, Login

username = "user"
password = "password"

if(startNextCloud() == "Exists"):
    Login(username, password)
else: 
    startupNewAcc(username, password)
