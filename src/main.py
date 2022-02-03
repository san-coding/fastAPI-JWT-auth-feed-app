from fastapi import FastAPI, Depends, HTTPException
from .auth import AuthHandler
from .schemas import AuthDetails, PostSchema
from pymongo import MongoClient
from decouple import config

app = FastAPI()


auth_handler = AuthHandler()
users = []
posts = []
print("Connecting to mongo db")
URI = config("MONGODB_URI")
client = MongoClient(URI)

# send posts to mongo db cluster
def send_posts():

    db = client.fastapiJWT
    collection = db.posts
    # only insert if post id not in db
    for post in posts:
        if collection.find_one({"id": post["id"]}) is None:
            collection.insert_one(post)


# send users to mongo db cluster
def send_users():
    db = client.fastapiJWT
    collection = db.users
    # only insert if user id not in db
    for user in users:
        if collection.find_one({"username": user["username"]}) is None:
            collection.insert_one(user)


def update_posts():
    db = client.fastapiJWT
    collection = db.posts
    files = collection.find()
    global posts
    posts = []
    for file in files:
        posts.append(
            {
                "id": file["id"],
                "title": file["title"],
                "content": file["content"],
                "author": file["author"],
            }
        )


update_posts()


def get_users():
    db = client.fastapiJWT
    collection = db.users
    user_files = collection.find()
    global users
    users = []
    for file in user_files:
        # add only name, username, password to users
        users.append(
            {
                "name": file["name"],
                "username": file["username"],
                "password": file["password"],
            }
        )


# homepage
@app.get("/", tags=["Welcome to JWT Authenticated feed app, connected to MongoDB"])
def view_functionalities():
    # return html and json as response

    return [
        {"hello": "Welcome to feed app"},
        {
            "Functionalities": [
                {"Registration": "Users have to register"},
                {
                    "Login": "Users have to login to view and create posts / get access to protected routes"
                },
                {"Posts": "Authenticated users can create and view posts"},
                {
                    "Viewing posts": "Protected routes can be accessed by authenticated users to view all posts, search & view post by id, view posts by a particular author"
                },
            ]
        },
    ]


print(len(posts))
# user registration
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
    send_users()
    return {"info": "User registered successfully"}


# user login
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


# current logged in user details
@app.get("/logged_in_user", tags=["User Authentication"])
def logged_in_user(username=Depends(auth_handler.auth_wrapper)):
    for user in users:
        if user["username"] == username:
            return {"info": "Logged in as " + user["name"] + ". Email: " + username}
    raise HTTPException(status_code=404, detail="User not found")


# create posts by authenticated users
@app.post("/create_post", tags=["Posts"])
def create_post(post: PostSchema, username=Depends(auth_handler.auth_wrapper)):
    post.id = len(posts) + 1
    post.author = username
    # add post to posts list
    try:
        posts.append(post.dict())
    except:
        raise HTTPException(status_code=400, detail="Invalid post")

    send_posts()
    return {"info": "Post successfully created by " + username}


# get all the posts
@app.get("/posts", tags=["Posts"])
def get_all_posts(username=Depends(auth_handler.auth_wrapper)):
    update_posts()
    return {"posts": posts}


# get posts by id
@app.get("/posts/{id}", tags=["Posts"])
def get_post_by_id(id: int, username=Depends(auth_handler.auth_wrapper)):
    if id > len(posts):
        return {"error": "Post not found"}
    else:
        return {"Post": posts[id - 1]}


# get posts by username
@app.get(
    "/posts/user/{username}",
    tags=["Posts"],
)
def get_post_by_username(user: str, username=Depends(auth_handler.auth_wrapper)):
    if len(posts) == 0:
        return {"info": "No posts found"}
    user_posts = []
    for post in posts:
        if post["author"] == user:
            user_posts.append(post)
    return {" posts": user_posts}
