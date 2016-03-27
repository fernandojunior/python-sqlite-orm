# python-sqlite-orm

A Python object relational mapper for SQLite.


## Example

* Define a Post model.

```py
# post.py

from orm import Model

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
```

* Create a data access object (DAO) indicating a database file.

```py
>>> from orm import Database
>>> db = Database('db.sqlite')
```

* Import the Post model and link it to the database.

```py
>>> from post import Post
>>> Post.__db__ = db  # see another approach in tests.py
```

* Create an object (staging area).

```py
>>> hello_world = Post('Hello', 'World').save()
>>> print(hello_world.id)  # auto generated id
1
```

* Update the object.

```py
>>> hello_world.text = 'Mundo'
>>> objects.update(hello_world)
>>> hello_world.show()
Hello Mundo
```

* Commit all staged operations (`save` and `update`) to the database.

```py
>>> db.commit()
```

* Delete the object and commit the change.

```py
>>> objects.delete(hello_world)
>>> db.commit()
```

* Create a manager that can perform CRUD operations in the database.

```py
>>> objects = Post.manager(db)
```

Create and read a post.

```py
>>> objects.save(Post('Hello', 'World'))  # save a post
{'text': 'World', 'id': 2, 'title': 'Hello'}
>>> objects.get(2)  # get by id from database
```

* Close the database without commit the changes

```py
>>> db.close()
```

Get all posts from database.

```py
>>> objects.all()  # return a empty list
[]
```

## Contributing

See CONTRIBUTING.

## License

[![CC0](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

The MIT License.

-

Copyright (c) 2014-2016 [Fernando Felix do Nascimento Junior](https://github.com/fernandojunior/).
