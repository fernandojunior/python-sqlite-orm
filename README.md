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

* Create a post and save it in the staging area (without commit) of database.

```py
>>> hello_world = Post('Hello', 'World').save()
>>> print(hello_world.id)  # auto generated id
1
```

* Change the hello world post and update it in the database.

```py
>>> hello_world.text = 'Mundo'
>>> hello_world.update()
>>> hello_world.show()  # show the post content
Hello Mundo
```

* Commit all staged operations (`save` and `update`) to the database.

```py
>>> db.commit()
```

* Delete the object and commit.

```py
>>> hello_world.delete()
>>> db.commit()
```

* Create a manager that can perform CRUD operations in the database.

```py
>>> objects = Post.manager(db)
```

Save and get a post.

```py
>>> objects.save(Post('Hello', 'World'))
>>> objects.get(2)  # get by id from the staging area
{'text': 'World', 'id': 2, 'title': 'Hello'}
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
