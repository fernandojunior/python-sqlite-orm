'''
A Python object relational mapper for SQLite.

Reference: https://www.sqlite.org/lang.html

Author: Fernando Felix do Nascimento Junior
License: MIT License
Homepage: https://github.com/fernandojunior/python-sqlite-orm
'''
import sqlite3


#: Dictionary to map Python and SQLite data types
DATA_TYPES = {str: 'TEXT', int: 'INTEGER', float: 'REAL'}


def attrs(obj):
    ''' Return attribute values dictionary for an object '''
    return dict(i for i in vars(obj).items() if i[0][0] != '_')


def copy_attrs(obj, remove=None):
    ''' Copy attribute values for an object '''
    if remove is None:
        remove = []
    return dict(i for i in attrs(obj).items() if i[0] not in remove)


def render_column_definitions(model):
    ''' Create SQLite column definitions for an entity model '''
    model_attrs = attrs(model).items()
    model_attrs = {k: v for k, v in model_attrs if k != 'db'}
    return ['%s %s' % (k, DATA_TYPES[v]) for k, v in model_attrs.items()]


def render_create_table_stmt(model):
    ''' Render a SQLite statement to create a table for an entity model '''
    sql = 'CREATE TABLE {table_name} (id integer primary key autoincrement, {column_def});'  # noqa
    column_definitions = ', '.join(render_column_definitions(model))
    params = {'table_name': model.__name__, 'column_def': column_definitions}
    return sql.format(**params)


class Database(object):  # pylint: disable=R0205
    ''' Proxy class to access sqlite3.connect method '''

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._connection = None
        self.connected = False
        self.Model = type('Model%s' % str(self), (Model,), {'db': self})  # pylint: disable=C0103

    @property
    def connection(self):
        ''' Create SQL connection '''
        if self.connected:
            return self._connection
        self._connection = sqlite3.connect(*self.args, **self.kwargs)
        self._connection.row_factory = sqlite3.Row
        self.connected = True
        return self._connection

    def close(self):
        ''' Close SQL connection '''
        if self.connected:
            self.connection.close()
        self.connected = False

    def commit(self):
        ''' Commit SQL changes '''
        self.connection.commit()

    def execute(self, sql, *args):
        ''' Execute SQL '''
        return self.connection.execute(sql, args)

    def executescript(self, script):
        ''' Execute SQL script '''
        self.connection.cursor().executescript(script)
        self.commit()


class Manager(object):  # pylint: disable=R0205
    ''' Data mapper interface (generic repository) for models '''

    def __init__(self, db, model, type_check=True):
        self.db = db
        self.model = model
        self.table_name = model.__name__
        self.type_check = type_check
        if not self._hastable():
            self.db.executescript(render_create_table_stmt(self.model))

    def all(self):
        ''' Get all model objects from database '''
        result = self.db.execute('SELECT * FROM %s' % self.table_name)
        return (self.create(**row) for row in result.fetchall())

    def create(self, **kwargs):
        ''' Create a model object '''
        obj = object.__new__(self.model)
        obj.__dict__ = kwargs
        return obj

    def delete(self, obj):
        ''' Delete a model object from database '''
        sql = 'DELETE from %s WHERE id = ?'
        self.db.execute(sql % self.table_name, obj.id)

    def get(self, id):
        ''' Get a model object from database by its id '''
        sql = 'SELECT * FROM %s WHERE id = ?' % self.table_name
        result = self.db.execute(sql, id)
        row = result.fetchone()
        if not row:
            msg = 'Object%s with id does not exist: %s' % (self.model, id)
            raise ValueError(msg)
        return self.create(**row)

    def has(self, id):
        ''' Check if a model object exists in database by its id '''
        sql = 'SELECT id FROM %s WHERE id = ?' % self.table_name
        result = self.db.execute(sql, id)
        return True if result.fetchall() else False

    def save(self, obj):
        ''' Save a model object '''
        if 'id' in obj.__dict__ and self.has(obj.id):
            msg = 'Object%s id already registred: %s' % (self.model, obj.id)
            raise ValueError(msg)
        clone = copy_attrs(obj, remove=['id'])
        self.type_check and self._isvalid(clone)
        column_names = '%s' % ', '.join(clone.keys())
        column_references = '%s' % ', '.join('?' for i in range(len(clone)))
        sql = 'INSERT INTO %s (%s) VALUES (%s)'
        sql = sql % (self.table_name, column_names, column_references)
        result = self.db.execute(sql, *clone.values())
        obj.id = result.lastrowid
        return obj

    def update(self, obj):
        ''' Update a model object '''
        clone = copy_attrs(obj, remove=['id'])
        self.type_check and self._isvalid(clone)
        where_expressions = '= ?, '.join(clone.keys()) + '= ?'
        sql = 'UPDATE %s SET %s WHERE id = ?' % (self.table_name, where_expressions)  # noqa
        self.db.execute(sql, *(list(clone.values()) + [obj.id]))

    def _hastable(self):
        ''' Check if entity model already has a database table '''
        sql = 'SELECT name len FROM sqlite_master WHERE type = ? AND name = ?'
        result = self.db.execute(sql, 'table', self.table_name)
        return True if result.fetchall() else False

    def _isvalid(self, attr_values):
        ''' Check if an attr values dict are valid as specificated in model '''
        attr_types = attrs(self.model)
        value_types = {a: v.__class__ for a, v in attr_values.items()}

        for attr, value_type in value_types.items():
            if value_type is not attr_types[attr]:
                msg = "%s value should be type %s not %s"
                raise TypeError(msg % (attr, attr_types[attr], value_type))


class Model(object):  # pylint: disable=R0205
    ''' Abstract entity model with an active record interface '''

    db = None

    def delete(self, type_check=True):
        ''' Delete this model object '''
        return self.__class__.manager(type_check=type_check).delete(self)

    def save(self, type_check=True):
        ''' Save this model object '''
        return self.__class__.manager(type_check=type_check).save(self)

    def update(self, type_check=True):
        ''' Update this model object '''
        return self.__class__.manager(type_check=type_check).update(self)

    @property
    def public(self):
        ''' Return the public model attributes '''
        return attrs(self)

    def __repr__(self):
        return str(self.public)

    @classmethod
    def manager(cls, db=None, type_check=True):
        ''' Create a database managet '''
        return Manager(db if db else cls.db, cls, type_check)
