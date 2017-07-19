from db.fields import FieldValidError
from db.sql import SqlQuery, execute


class BaseModel(object):

    table_name = ''
    primary_field = 'id'
    fields = {}

    def __init__(self, values=None):
        self.errors = {}
        self.values = self._validate_values(values or {})
        self.raw_values = values

    def __getitem__(self, item):
        value = self.values.get(item, self.raw_values.get(item))
        if isinstance(value, list):
            value = value[0]
        return value

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

    def _validate_values(self, values=None):
        valid_values = {}
        if not values and not hasattr(self, 'values'):
            return valid_values
        values = values or self.values
        for name, field in self.fields.items():
            try:
                validated_data = field.validate(values.get(name))
            except FieldValidError as e:
                self.errors[name] = str(e)
                valid_values[name] = values.get(name)
            else:
                valid_values[name] = validated_data
                if name in self.errors:
                    del self.errors[name]
        return valid_values

    def is_valid(self):
        valid_values = self._validate_values()
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
        if self.values[self.primary_field]:
            sql = "DELETE FROM {} WHERE {} = {}".format(
                self.table_name,
                self.primary_field,
                self.values[self.primary_field]
            )
            execute(sql)
            return True
        return False

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
