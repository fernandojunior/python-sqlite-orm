import os
from orm import Database

db = Database('db.sqlite.test')


class Post(db.Model):

    def __init__(self, text, id=None):
        self.id = id
        self.text = text

    @classmethod
    def schema(cls):
        return '''
        drop table if exists post;
        create table post (
            id integer primary key autoincrement,
            text text not null
        );
        '''

try:
    post = Post('Hello World').save()
    assert(post.id == 1)
    post.text = 'Hello Mundo'
    post.update()
    db.commit()
    assert(post.text == 'Hello Mundo')
    post.delete()
    db.commit()
    objects = Post.manager()
    objects.save(Post('Hello World'))
    assert(objects.get(2).public == {'text': 'Hello World', 'id': 2})
    db.close()
    assert(list(objects.all()) == [])
finally:
    os.remove('db.sqlite.test')
