from fastapi import FastAPI, Depends, HTTPException
from .auth import AuthHandler
from .schemas import AuthDetails, PostSchema


app = FastAPI()


auth_handler = AuthHandler()
users = []

posts = [
    {
        "id": 1,
        "title": "First Post",
        "content": "Edvora is a cool place to work",
        "author": "Sandeep Rajakrishnan",
    }
]


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


@app.get("/logged_in_user", tags=["User Authentication"])
def logged_in_user(username=Depends(auth_handler.auth_wrapper)):
    # extract name from username
    for user in users:
        if user["username"] == username:
            return {"info": "Logged in as " + user["name"]}
    raise HTTPException(status_code=404, detail="User not found")


# get all the posts
@app.get("/posts", tags=["Posts"])
def get_all_posts():
    if len(posts) == 0:
        return {"info": "No posts found"}
    return {"All posts": posts}


# get posts by id
@app.get("/posts/{id}", tags=["Posts"])
def get_post_by_id(id: int):
    if id > len(posts):
        return {"error": "Post not found"}
    else:
        return {"Post": posts[id - 1]}


# create posts by authenticated users
@app.post("/create_post", tags=["Posts"])
def create_post(post: PostSchema, username=Depends(auth_handler.auth_wrapper)):
    post.id = len(posts) + 1
    post.author = username
    posts.append(post.dict())
    return {"info": "Post successfully created by " + username}
