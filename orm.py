'''
A Python object relational mapper for SQLite.

Author: Fernando Felix do Nascimento Junior
License: MIT License
Homepage: https://github.com/fernandojunior/python-sqlite-orm
'''
import sqlite3


def cut_attrs(obj, keys):
    return dict(i for i in obj.__dict__.items() if i[0] not in keys)


class Database(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.connected = False
        self.Model = type('Model%s' % str(self), (Model,), {'db': self})

    @property
    def connection(self):
        if self.connected:
            return self._connection
        self._connection = sqlite3.connect(*self.args, **self.kwargs)
        self._connection.row_factory = sqlite3.Row
        self.connected = True
        return self._connection

    def close(self):
        if self.connected:
            self.connection.close()
        self.connected = False

    def commit(self):
        self.connection.commit()

    def execute(self, sql, *args):
        return self.connection.execute(sql, args)

    def executescript(self, script):
        self.connection.cursor().executescript(script)
        self.commit()


class Manager(object):

    def __init__(self, db, model):
        self.db = db
        self.model = model
        self.table_name = model.__name__.lower()
        if not self._hastable():
            self.db.executescript(self.model.schema())

    def all(self):
        cursor = self.db.execute('select * from %s' % self.table_name)
        return (self.model(**row) for row in cursor.fetchall())

    def delete(self, obj):
        sql = 'DELETE from %s WHERE id = ?'
        self.db.execute(sql % self.table_name, obj.id)

    def get(self, id):
        sql = 'select * from %s where id = ?' % self.table_name
        cursor = self.db.execute(sql, id)
        row = cursor.fetchone()
        if not row:
            msg = 'Object%s with id does not exist: %s' % (self.model, id)
            raise ValueError(msg)
        return self.model(**row)

    def has(self, id):
        sql = 'select id from %s where id = ?' % self.table_name
        cursor = self.db.execute(sql, id)
        return True if cursor.fetchall() else False

    def save(self, obj):
        if obj.id and self.has(obj.id):
            msg = 'Object%s id already registred: %s' % (self.model, obj.id)
            raise ValueError(msg)
        copy_ = cut_attrs(obj, 'id')
        keys = '(%s)' % ', '.join(copy_.keys())  # (key1, ...)
        refs = '(%s)' % ', '.join('?' for i in range(len(copy_)))  # (?, ...)
        sql = 'insert into %s %s values %s' % (self.table_name, keys, refs)
        cursor = self.db.execute(sql, *copy_.values())
        obj.id = cursor.lastrowid
        return obj

    def update(self, obj):
        copy_ = cut_attrs(obj, 'id')
        keys = '= ?, '.join(copy_.keys()) + '= ?'  # key1 = ?, ...
        sql = 'UPDATE %s SET %s WHERE id = ?' % (self.table_name, keys)
        self.db.execute(sql, *(copy_.values() + [obj.id]))

    def _hastable(self):
        sql = 'select name len FROM sqlite_master where type = ? AND name = ?'
        cursor = self.db.execute(sql, 'table', self.table_name)
        return True if cursor.fetchall() else False


class Model(object):

    db = None

    def delete(self):
        return self.__class__.manager().delete(self)

    def save(self):
        return self.__class__.manager().save(self)

    def update(self):
        return self.__class__.manager().update(self)

    @property
    def public(self):
        return dict(i for i in vars(self).items() if i[0][0] is not '_')

    def __repr__(self):
        return str(self.public)

    @classmethod
    def manager(cls, db=None):
        db = db if db else cls.db
        return Manager(cls.db, cls)

    @classmethod
    def schema(cls):
        raise NotImplementedError
