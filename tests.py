from orm import *

class Post(Model):

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

db = Database('db.sqlite.test')
objects = Post.manager(db)
hello_world = objects.save(Post('Hello', 'World'))
post = objects.get(hello_world.id)  # or objects.all()
post.text = 'Mundo'
objects.update(post)
assert(post.show() == 'Hello Mundo')
db.commit()
objects.delete(post)
db.commit()
assert(str(objects.save(Post('Hello', 'World'))) == "{'text': 'World', 'id': 2, 'title': 'Hello'}")
db.close()
assert(objects.all() == [])
import os
os.remove('db.sqlite.test')
