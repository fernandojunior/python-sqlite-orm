"""
API simples, utilizando sqlite, para gerenciar conexoes e entidades. Exemplo de uso a seguir.

    class Entry(BaseEntity):

        def __init__(self, title, text, id=None):
            self.id = id
            self.title = title
            self.text = text

        @classmethod
        def schema(cls):
            return /"/"/"
            drop table if exists entry;

            create table entry (
                id integer primary key autoincrement,
                title text not null,
                text text not null
            );
        /"/"/"
    entry = Entry('titulo', 'texto')
    DatabaseConnection db = DatabaseConnection('file_name')	
    id = Entry.objects(db).save(entry)
    db.commit()
    db.close()

Author: Fernando Felix do Nascimento Junior
"""

import sqlite3

class DatabaseConnection(object):
    
    def __init__(self, file):
        self.file = file
        self.db = None
        self.connected = False

    def connect(self):
        self.db = sqlite3.connect(self.file)
        self.db.row_factory = sqlite3.Row
        self.connected = True

    def execute(self, sql, *args):
        if not self.connected:
            self.connect()
        return self.db.execute(sql, args)

    def executescript(self, script):
        if not self.connected:
            self.connect()
        return self.db.cursor().executescript(script)
		
    def commit(self):
       self.db.commit()
	   
    def close(self):
        """Closes the database."""
        self.db.close()
        self.connected = False

class BaseManager(object):

    def __init__(self, db, entity_cls):
        self.db = db
        self.entity_cls = entity_cls
        self.table_name = entity_cls.__name__ .lower()

        if not self.__hastable():
            self.__run_schema()
            self.db.commit()
		
    def __hastable(self):
        sql = 'select count(*) len FROM sqlite_master where type = ? AND name = ?'
        cursor = self.db.execute(sql, 'table', self.table_name)
        row = cursor.fetchone()

        if row['len'] > 0:
            return True
        return False

    def all(self):
        all = []
        cursor = self.db.execute('select * from %s order by id desc' % self.table_name)

        for row in cursor.fetchall():
            all.append(self.entity_cls(**row))

        return all

    def get(self, id):
        cursor = self.db.execute('select * from %s where id = ?' % self.table_name, id)
        row = cursor.fetchall()[0]
        return self.entity_cls(**row)

    def has(self, id):
        cursor = self.db.execute('select count(*) len from %s where id = ?' % self.table_name, id)
        row = cursor.fetchall()[0]

        if(row['len'] > 0):
            return True
        else:
            return False
		
    def save(self, obj):
	
        #copying the dictionary object without 'id' element
        d = dict((k, v) for k, v in obj.__dict__.iteritems() if k is not 'id' )
	
        #(key1, key2, ...)	
        keys = '(%s)' % ', '.join(d.keys())
		
        #(?, ?, ...)
        refs = '(%s)' % ', '.join('?' for i in range(len(d)))

        #[value1, value2, ...]
        values = d.values()
		
        sql = 'insert into %s %s values %s' % (self.table_name, keys, refs)
		
        cursor = self.db.execute(sql, *values)
		
        return cursor.lastrowid
		
    def update(self, obj):
		
        #copying the dictionary object without 'id' item
        d = dict((k, v) for k, v in obj.__dict__.iteritems() if k is not 'id' )
		
        #key1 = ?, key2 = ?, ...
        keys = '= ?, '.join(d.keys()) + '= ?'
		
        #[value1, value2, ..., id_value]
        values = d.values() + [obj.id]
		
        sql = 'UPDATE %s SET %s WHERE id = ?' % (self.table_name, keys)

        self.db.execute(sql, *values)
		
    def delete(self, id):
        sql = "DELETE from %s WHERE id = ?" % self.table_name
        self.db.execute(sql, id)
		
    def __run_schema(self):
        self.db.executescript(self.entity_cls.schema())
		
class BaseEntity(object):

    @classmethod
    def schema(cls):
        raise NotImplementedError

    @classmethod
    def objects(cls, db):
        return BaseManager(db, cls)