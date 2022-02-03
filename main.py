from email.policy import default
import uvicorn
from fastapi import FastAPI, Body, Depends
from app.model import PostSchema
from app.model import UserSchema
from app.model import UserLoginSchema
from app.auth.jwt_handler import signJWT, decodeJWT, token_response
from app.auth.jwt_bearer import jwtBearer

posts = [{"id": 1, "title": "Post Demo", "content": "This is a demo post"}]

users = []

app = FastAPI()

# get - for testing
@app.get("/", tags=["test"])
def greet():
    return {"message": "Hello World"}


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
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {"info": "Post created successfully with id: " + str(post.id)}


# creating a user
@app.post("/user/signup", tags=["user"])
def user_signup(user: UserSchema = Body(default=None)):
    # check if user already exists
    if user.email in [user.email for user in users]:
        return {"error": "User already exists"}
    else:
        users.append(user)
        return signJWT(user.email)


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
