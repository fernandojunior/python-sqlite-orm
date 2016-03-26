class DatabaseConnection(object):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.connected = False

    @property
    def connection(self):
        if self.connected:
            return self.__connection

        self.__connection = sqlite3.connect(*self.args, **self.kwargs)
        self.__connection.row_factory = sqlite3.Row
        self.connected = True
        return self.__connection

    def execute(self, sql, *args):
        return self.connection.execute(sql, args)

    def executescript(self, script):
        return self.connection.cursor().executescript(script)

    def commit(self):
        self.connection.commit()

    def close(self):
        if self.connected:
            self.connection.close()
        self.connected = False


class Manager(object):

    def __init__(self, db, entity_cls):
        self.db = db
        self.entity_cls = entity_cls
        self.table_name = entity_cls.__name__.lower()

        if not self.__hastable():
            self.__run_schema()
            self.db.commit()

    def __hastable(self):
        sql = 'select name len FROM %s where type = ? AND name = ?'
        cursor = self.db.execute(
            sql % 'sqlite_master', 'table', self.table_name)
        return True if cursor.fetchall() else False

    def all(self):
        cursor = self.db.execute('select * from %s' % self.table_name)
        return [self.entity_cls(**row) for row in cursor.fetchall()]

    def get(self, id):
        cursor = self.db.execute(
            'select * from %s where id = ?' % self.table_name, id)
        row = cursor.fetchone()
        if not row:
            raise ValueError('Object%s with id does not exist: %s' % (
                self.entity_cls, id))

        return self.entity_cls(**row)

    def has(self, id):
        cursor = self.db.execute(
            'select id from %s where id = ?' % self.table_name, id)
        return True if cursor.fetchall() else False

    def save(self, obj):
        if obj.id and self.has(obj.id):
            raise ValueError('An object%s with id already registred: %s' % (
                self.entity_cls, obj.id))

        # copying the dictionary object without 'id' element
        d = dict((k, v) for k, v in obj.__dict__.iteritems() if k is not 'id')
        keys = '(%s)' % ', '.join(d.keys())  # (key1, key2, ...)
        refs = '(%s)' % ', '.join('?' for i in range(len(d)))  # (?, ?, ...)
        values = d.values()  # [value1, value2, ...]
        sql = 'insert into %s %s values %s' % (self.table_name, keys, refs)
        cursor = self.db.execute(sql, *values)
        obj.id = cursor.lastrowid
        return obj

    def update(self, obj):
        # copying the dictionary object without 'id' item
        d = dict((k, v) for k, v in obj.__dict__.iteritems() if k is not 'id')
        keys = '= ?, '.join(d.keys()) + '= ?'  # key1 = ?, key2 = ?, ...
        values = d.values() + [obj.id]  # [value1, value2, ..., id_value]
        sql = 'UPDATE %s SET %s WHERE id = ?' % (self.table_name, keys)
        self.db.execute(sql, *values)

    def delete(self, obj):
        sql = 'DELETE from %s WHERE id = ?'
        self.db.execute(sql % self.table_name, obj.id)

    def __run_schema(self):
        self.db.executescript(self.entity_cls.schema())


class Model(object):

    def __repr__(self):
        return str(self.__dict__)

    @classmethod
    def schema(cls):
        raise NotImplementedError

    @classmethod
    def objects(cls, db):
        return Manager(db, cls)
