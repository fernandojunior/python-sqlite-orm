import os
from random import random
from orm import Database

db = Database('db.sqlite.test')


class Post(db.Model):

    random = float
    text = str

    def __init__(self, text):
        self.text = text
        self.random = random()

try:
    post = Post('Hello World').save()
    assert(post.id == 1)
    post.text = 'Hello Mundo'
    post.update()
    db.commit()
    post = Post.manager().get(id=1)
    assert(post.text == 'Hello Mundo')
    post.delete()
    db.commit()
    try:
        invalid_post = Post(None).save(type_check=False)
    except TypeError as e:
        assert(False)
    else:
        assert(True)
    objects = Post.manager()
    objects.save(Post('Hello World'))
    assert(set(objects.get(2).public.keys()) == set(['id', 'text', 'random']))
    assert(isinstance(objects.get(2).random, float))
    db.close()
    assert(list(objects.all()) == [])
finally:
    os.remove('db.sqlite.test')
