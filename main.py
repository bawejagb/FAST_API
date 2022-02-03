from ast import Str
from fastapi import Body, FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import *
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str 
    published: bool = True
    rating: Optional[int] = None

id_val = 0
my_posts = []

def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p
    return None

@app.get("/")
def root():
    return {"message": "Hello User!"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

""" @app.post("/createposts")
def create_post(payload: dict = Body(...)):
    print("Output:", payload)
    return {"new_post": f"title: {payload['title']} content: {payload['content']}"} """

@app.post("/posts")
def create_post(post: Post):
    global id_val
    print("Output:", post.dict())
    post_dic = post.dict()
    post_dic["id"]=id_val
    my_posts.append(post_dic)
    id_val = id_val+1
    return {"new_post": post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    print("Output:", id)
    post = find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found!")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id {id} not found!"}
    return {"Post details": post}