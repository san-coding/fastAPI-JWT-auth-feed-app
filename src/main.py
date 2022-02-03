from fastapi import FastAPI, Depends, HTTPException
from .auth import AuthHandler
from .schemas import AuthDetails


app = FastAPI()


auth_handler = AuthHandler()
users = []


@app.get("/", tags=["Home page"])
def home():
    return {"hello": "Welcome to feed app"}


@app.post("/register", status_code=201, tags=["User Authentication"])
def register_user(auth_details: AuthDetails):
    if any(x["username"] == auth_details.username for x in users):
        raise HTTPException(
            status_code=400,
            detail="User already registered, please login or use a different username",
        )
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.append(
        {
            "name": auth_details.name,
            "username": auth_details.username,
            "password": hashed_password,
        }
    )
    return {"info": "User registered successfully"}


@app.post("/login", tags=["User Authentication"])
def login_user(auth_details: AuthDetails):
    user = None
    for x in users:
        if x["username"] == auth_details.username:
            user = x
            break

    if (user is None) or (
        not auth_handler.verify_password(auth_details.password, user["password"])
    ):
        raise HTTPException(status_code=401, detail="Invalid username and/or password")
    token = auth_handler.encode_token(user["username"])
    return {"token": token}


@app.get("/protected", tags=["User Authentication"])
def protected(username=Depends(auth_handler.auth_wrapper)):
    # extract name from username
    for user in users:
        if user["username"] == username:
            return {"info": "Logged in as " + user["name"]}
    raise HTTPException(status_code=404, detail="User not found")
