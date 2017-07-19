import re


class FieldValidError(Exception):
    pass


class BaseField(object):

    type = ''
    value = None
    is_reference = False
    required = False
    create_params = None
    default = None

    def __init__(self, **kwargs):
        if kwargs.get('required'):
            self.required = kwargs['required']
        if kwargs.get('default'):
            self.default = kwargs['default']

    def get_sql_field_create_params(self):
        create_params = self.create_params or []
        if self.required and "NOT NULL" not in create_params:
            create_params.append("NOT NULL")
        if self.default:
            self.default = self.validate(self.default)
            if "DEFAULT " + self.default not in create_params:
                create_params.append("DEFAULT " + self.default)
        return create_params

    def set(self, value):
        self.value = self.validate(value)

    def validate(self, value):
        if self.required and value is None:
            raise FieldValidError("This field is required")
        if not value:
            value = self.default
        return value

    def create_field_sql(self, name):
        field_params = self.get_sql_field_create_params()
        sql_field_create_params = "{} {}".format(name, self.type)
        if field_params:
            sql_field_create_params += " " + " ".join(field_params)
        return sql_field_create_params

    def create_reference_sql(self, name):
        pass


class IntField(BaseField):

    type = 'INTEGER'

    def validate(self, value):
        if value and isinstance(value, list):
            value = value[0]
        if value:
            try:
                value = int(value)
            except TypeError:
                raise FieldValidError("Wrong type")
            except ValueError:
                raise FieldValidError("Wrong value")
            except Exception as e:
                raise FieldValidError("Wrong value: {}".format(str(e)))
        return super().validate(value)


class TextField(BaseField):

    type = 'TEXT'
    pattern = None
    blank = False
    default = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if kwargs.get('blank'):
            self.blank = kwargs['blank']

    def validate(self, value):
        if not self.blank and not value:
            raise FieldValidError("This field cannot be empty")
        if value and isinstance(value, list):
            value = value[0]
        if value:
            if isinstance(value, (str, bytes)):
                if self.pattern and not re.match(self.pattern, value):
                    raise FieldValidError("Invalid value")
            else:
                raise FieldValidError("Wrong type")
        return super().validate(value)


class PrimaryKeyField(IntField):

    create_params = ["PRIMARY KEY AUTOINCREMENT"]


class ForeignKeyField(IntField):

    create_params = []
    is_reference = True
    reference_model = None
    reference_model_name = None
    reference_model_field = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        reference_model = kwargs.get('reference_model')
        if reference_model:
            self.reference_model = reference_model
            self.reference_model_name = getattr(reference_model, "table_name")
            self.reference_model_field = getattr(reference_model, "primary_field")
        else:
            raise FieldValidError("Need specify reference_model")

    def create_reference_sql(self, name):
        return "FOREIGN KEY ({}) REFERENCES {}({})".format(
            name,
            self.reference_model_name,
            self.reference_model_field
        )


class EmailField(TextField):

    pattern = r"^[\w\.\+\-]+\@[\w\.\+\-]+\.[a-z]{2,3}$"


class PhoneField(TextField):

    pattern = r"\+7\(\d{3}\)\d{7}$"
