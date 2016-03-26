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
>>> db = DatabaseConnection('db.sqlite')
```

* Import the Post model.

```py
>>> from post import Post
```

* Create a manager to perform CRUD operations in the database.

```py
>>> objects = Post.manager(db)
```

* Create an object (staging area).

```py
>>> hello_world = objects.save(Post('Hello', 'World'))
```

* Read an object.

```py
>>> post = objects.get(hello_world.id)  # or objects.all()
```

* Update the object.

```py
>>> post.text = 'Mundo'
>>> objects.update(post)
>>> assert(post.show() == 'Hello Mundo')
True
```

* Commit all performed operations.

```py
>>> db.commit()
```

* Delete and commit.

```py
>>> objects.delete(post)
>>> db.commit()
```

* Create a object without commit to return a empty list.

```py
>>> objects.save(Post('Hello', 'World'))
>>> db.close()
>>> assert(objects.all() == [])
True
```

## Contributing

See CONTRIBUTING.

## License

[![CC0](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

The MIT License.

-

Copyright (c) 2014-2016 [Fernando Felix do Nascimento Junior](https://github.com/fernandojunior/).

