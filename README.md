# python-sqlite-orm

A Python object relational mapper for SQLite.

## Install

```sh
pip install sqlite-orm
```

## Usage

Following a basic tutorial to demonstrate how to use the ORM.

1. Define a `Post` model in a `post.py` file.

    ```py
    # post.py
    from orm import Model

    class Post(Model):

        text = str  # other datatypes: int, float

        def __init__(self, text):
            self.text = text

    ```

2. Import `Database` to create a data access object.

    ```py
    >>> from orm import Database
    >>> db = Database('db.sqlite')  # indicating a database file.
    ```

3. Import the `Post` model and link it to the database.

    ```py
    >>> from post import Post
    >>> Post.db = db  # see another approach in tests.py
    ```

4. Create a post and save it in the staging area (without commit) of database.

    ```py
    >>> post = Post('Hello World').save()
    >>> print(post.id)  # auto generated id
    1
    ```

5. Change the hello world post and update it in the database.

    ```py
    >>> post.text = 'Hello Mundo'
    >>> post.update()
    >>> post.text
    Hello Mundo
    ```

6. Commit all staged operations (`save` and `update`) to the database.

    ```py
    >>> db.commit()
    ```

7. Delete the object and commit.

    ```py
    >>> post.delete()
    >>> db.commit()
    ```

8. Create a manager that can perform CRUD operations in the database.

    ```py
    >>> objects = Post.manager(db)
    ```

9. Save and get a post.

    ```py
    >>> objects.save(Post('Hello', 'World'))
    >>> objects.get(2)  # get by id from the staging area
    {'text': 'World', 'id': 2, 'title': 'Hello'}
    ```

10. Close the database without commit the changes

    ```py
    >>> db.close()
    ```

11. Get all posts from database.

    ```py
    >>> list(objects.all())  # return a "empty" generator
    []
    ```

## Contributing

See [CONTRIBUTING](/CONTRIBUTING.md).

## License

[![CC0](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

The MIT License.

-

Copyright (c) 2014-2016 [Fernando Felix do Nascimento Junior](https://github.com/fernandojunior/).
