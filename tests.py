import os
from orm import Database

db = Database('db.sqlite.test')


class Post(db.Model):

    def __init__(self, title, text, id=None):
        self.id = id
        self.title = title
        self.text = text

    def show(self):
        return '%s %s' % (self.title, self.text)

    @classmethod
    def schema(cls):
        return '''
        drop table if exists post;
        create table post (
            id integer primary key autoincrement,
            title text not null,
            text text not null
        );
        '''

try:
    hello_world = Post('Hello', 'World').save()
    assert(hello_world.id == 1)
    hello_world.text = 'Mundo'
    hello_world.update()
    db.commit()
    assert(hello_world.show() == 'Hello Mundo')
    hello_world.delete()
    db.commit()
    objects = Post.manager()
    objects.save(Post('Hello', 'World'))
    assert(objects.get(2).public == {
        'text': 'World', 'id': 2, 'title': 'Hello'})
    db.close()
    assert(objects.all() == [])
finally:
    os.remove('db.sqlite.test')
