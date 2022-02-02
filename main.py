import uvicorn
from fastapi import FastAPI
from app.model import PostSchema

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


# create a post
@app.post("/posts", tags=["posts"])
def create_post(post: PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {"info": "Post created successfully with id: " + str(post.id)}
