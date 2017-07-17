import sqlite3
import logging

from settings import DB_NAME


logger = logging.getLogger("sql queries")


def _get_connection(db_name=DB_NAME):
    conn = sqlite3.connect(db_name)
    conn.set_trace_callback(logger.info)
    return conn


def create_db(db_name=DB_NAME):
    from db.models import tables

    conn = _get_connection(db_name)
    cursor = conn.cursor()

    cursor.execute("""PRAGMA foreign_keys=on;""")

    for table in tables:
        cursor.execute(table.create_table_sql())
        if table.get_default_data():
            cursor.executemany(*table.bulk_create())

    conn.commit()
    conn.close()


def execute(query, db_name=DB_NAME):
    conn = _get_connection(db_name)
    cursor = conn.cursor()
    if isinstance(query, tuple):
        cursor.execute(*query)
    else:
        cursor.execute(query)
    conn.commit()
    conn.close()


class SqlQuery(object):

    model = None
    query = ""
    db_name = ""

    def __init__(self, model, db_name=DB_NAME):
        self.model = model
        self.db_name = db_name

    @staticmethod
    def _dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def select(self, fields):
        if isinstance(fields, list):
            fields = ", ".join(fields)
        self.query = "SELECT {} FROM {}".format(
            fields,
            self.model.table_name,
        )
        return self

    def left_join(self, join_fk_field_name, model=None):
        model = model or self.model
        foreignkey_field_model = model.fields[join_fk_field_name].reference_model
        format_params = [
            foreignkey_field_model.table_name,
            foreignkey_field_model.primary_field,
            model.table_name,
            join_fk_field_name
        ]
        if model != self.model:
            format_params = [
                model.table_name,
                join_fk_field_name,
                foreignkey_field_model.table_name,
                foreignkey_field_model.primary_field
            ]
        self.query += " LEFT JOIN {0} ON ({0}.{1} = {2}.{3})".format(*format_params)
        return self

    def where(self, is_having=False, **kwargs):
        filter_word = "WHERE"
        if is_having:
            filter_word = "HAVING"
        values = []
        for name, value in kwargs.items():
            cmp = "="
            if "__" in name:
                cmp_dict = {
                    "gt": ">",
                    "gte": ">=",
                    "lt": "<",
                    "lte": "<=",
                    "not": "<>",
                    "in": "IN"
                }
                name, cmp_slug = name.split("__")
                cmp = cmp_dict.get(cmp_slug, "=")
            if isinstance(value, str):
                value = "'{}'".format(value)
            if isinstance(value, list):
                value = "({})".format(", ".join(map(str, value)))
            values.append("{} {} {}".format(name, cmp, value))
        self.query += " {} {}".format(filter_word, " AND ".join(values))
        return self

    def group_by(self, field):
        self.query += " GROUP BY {}".format(field)
        return self

    def order_by(self, field, sort="ASC"):
        self.query += " ORDER BY {} {}".format(field, sort)
        return self

    def fetchall(self):
        conn = _get_connection(self.db_name)
        conn.row_factory = self._dict_factory
        cursor = conn.cursor()

        if isinstance(self.query, tuple):
            cursor.execute(*self.query)
        else:
            cursor.execute(self.query)
        rows = cursor.fetchall()
        conn.close()

        qs = []
        for row in rows:
            qs.append(self.model(row))
        return qs
