# python-sqlite-orm

A Python object relational mapper for SQLite.


## Usage

* Define a Model.

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

* Create a data access object (DAO) incating a database file.

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
1
```

* Print the auto generated id of the object.

```py
>>> print(hello_world.id)
```

* Update the object.

```py
>>> hello_world.text = 'Mundo'
>>> objects.update(hello_world)
>>> hello_world.show() == 'Hello Mundo'
True
```

* Commit all staged operations (`save` and `update`) to database.

```py
>>> db.commit()
```

* Delete and commit the object.

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
>>> objects.save(Post('Hello', 'World'))  # id 2
{'text': 'World', 'id': 2, 'title': 'Hello'}
>>> objects.get(2)  # or objects.all()
```

* Close the database without commit the saved post with id `2`.

```py
>>> db.close()
```

Get all posts from database to return a empty list.

```py
>>> objects.all() == []
True
```

## Contributing

See CONTRIBUTING.

## License

[![CC0](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

The MIT License.

-

Copyright (c) 2014-2016 [Fernando Felix do Nascimento Junior](https://github.com/fernandojunior/).
