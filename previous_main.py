from email.policy import default
import uvicorn
from fastapi import FastAPI, Body, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.model import PostSchema
from app.model import UserSchema
from app.model import UserLoginSchema
from app.auth.jwt_handler import signJWT, decodeJWT, token_response
from app.auth.jwt_bearer import jwtBearer

posts = [
    {
        "id": 1,
        "title": "First Post",
        "content": "Edvora is a cool place to work",
        "author": "Sandeep Rajakrishnan",
    }
]

users = []

app = FastAPI()

# get - for testing
@app.get("/", tags=["test"])
def greet():
    return {"message": "Hello World"}


# get logged in user details
@app.get(
    "/user/me",
    tags=["user"],
    response_model=UserSchema,
    dependencies=[Depends(jwtBearer())],
)
def get_user(credentials: HTTPAuthorizationCredentials = Depends(jwtBearer())):
    return {"user": credentials.credentials}


# get posts
@app.get("/posts", tags=["posts"])
def get_all_posts():
    return {"All posts": posts}


# get posts by id
@app.get("/posts/{id}", tags=["posts"])
def get_post_by_id(id: int):
    if id > len(posts):
        return {"error": "Post not found"}
    else:
        return {"Post": posts[id - 1]}


# creating a post
@app.post("/posts", dependencies=[Depends(jwtBearer())], tags=["posts"])
def create_post(post: PostSchema):
    # check if user is logged in
    post.id = len(posts) + 1
    #    post.author = decodeJWT(token_response(jwtBearer()))["userID"]
    posts.append(post.dict())
    return {"info": decodeJWT(token_response(jwtBearer()))}


# creating a user
@app.post("/user/signup", tags=["user"])
def user_signup(user: UserSchema = Body(default=None)):
    # check if user already exists
    if user.email in [user.email for user in users]:
        return {"error": "User already exists"}
    else:
        users.append(user)
        return {"info": "User created successfully"}


def check_user_credentials(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(default=None)):
    if check_user_credentials(user):
        return signJWT(user.email)
    else:
        return {"error": "Invalid credentials"}
