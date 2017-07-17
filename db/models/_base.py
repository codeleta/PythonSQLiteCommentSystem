from db.fields import FieldValidError
from db.sql import SqlQuery, execute


class BaseModel(object):

    table_name = ''
    primary_field = 'id'
    fields = {}

    def __init__(self, values=None):
        self.errors = {}
        self.values = values or {}

    def __getitem__(self, item):
        return self.values.get(item)

    def _update(self):
        if not self.values.get(self.primary_field):
            return self._create()
        values = []
        for name, value in self.values.items():
            if name != self.primary_field:
                value = "'{}'".format(value) if isinstance(value, str) else value
                values.append("{}={}".format(name, value))
        sql = "UPDATE {} SET {} WHERE {} = {}".format(
            self.table_name,
            ", ".join(values),
            self.primary_field,
            self.values[self.primary_field]
        )
        execute(sql)
        return True

    def _create(self):
        if self.values.get(self.primary_field):
            return self._update()
        count_fields = len(self.fields)
        sql = "INSERT INTO {} VALUES ({})".format(self.table_name, ", ".join(["?" for x in range(count_fields)]))
        execute((sql, list(self.values.values())))
        return True

    def is_valid(self):
        self.errors = {}
        valid_values = {}
        for name, field in self.fields.items():
            try:
                validated_data = field.validate(self.values.get(name))
            except FieldValidError as e:
                self.errors[name] = str(e)
            else:
                valid_values[name] = validated_data
        if self.errors:
            return False
        else:
            self.values = valid_values
            return True

    def save(self):
        if self.is_valid():
            if self.values.get(self.primary_field):
                return self._update()
            return self._create()
        return False

    def delete(self):
        pass

    @classmethod
    def create_table_sql(cls):
        fields = []
        for name, field in cls.fields.items():
            fields.append(field.create_field_sql(name))
            if field.is_reference:
                fields.append(field.create_reference_sql(name))
        fields = ", ".join(fields)
        return "CREATE TABLE IF NOT EXISTS {table_name}({fields});".format(table_name=cls.table_name, fields=fields)

    @classmethod
    def get_default_data(cls):
        return []

    @classmethod
    def bulk_create(cls):
        count_fields = len(cls.fields)
        sql = "INSERT INTO {} VALUES ({})".format(cls.table_name, ", ".join(["?" for x in range(count_fields)]))
        return sql, cls.get_default_data()
