from typing import Optional, Union
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    name: str
    price: float
    id: int
    is_offer: Union[bool, None] = None
    is_published: Optional[bool] = None


posts = [{"name": 'helo', "price": 12.22, "is_offer": True, "id": 1},
         {"name": 'name2', "price": 12.22, "is_offer": True, "id": 2}]


def find_post(id):
    for p in posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for index, p in enumerate(posts):
        print(index)
        if p['id'] == id:
            return index
        return -1


@app.get('/')
def read_root():
    return {'hello': 'world'}


@app.get('/posts')
def read_post():
    post_dict = posts[0]
    print(post_dict)
    return {'data': posts}


@app.get('/posts/{post_id}')
def read_post(post_id: int, q: Union[str, None] = None):
    print(post_id, type(post_id))
    post = find_post(int(post_id))  # no need using int.
    print(post)
    name = 'hna'
    x = name.upper()
    print(x)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found {post_id}")
    return {'post_id': post_id, 'q': q, 'post': post}


@app.get('/posts-one/{post_id}')
def read_post(post_id: int, response: Response, q: Union[str, None] = None):
    print(post_id, type(post_id))
    post = find_post(int(post_id))  # no need using int.
    print(post)
    name = 'hna'
    x = name.upper()
    print(x)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found {post_id}")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'msg': f"not found {post_id}"}
    return {'post_id': post_id, 'q': q, 'post': post}


@app.put('/posts/{post_id}')
def update_post(post_id: int, post: Post):
    return {'post_name': post.name, "post_id": post_id}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = 100
    posts.append(post_dict)
    print(post_dict)
    return {'data': post_dict}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    print(index)
    if index < 0:
        print('notherer')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"not found {id}")

    posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
