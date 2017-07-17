from db import fields
from db.models._base import BaseModel
from db.models.location import City


class Comment(BaseModel):

    table_name = 'comments'
    fields = {
        'id': fields.PrimaryKeyField(),
        'first_name': fields.TextField(required=True),
        'last_name': fields.TextField(required=True),
        'text': fields.TextField(required=True),
        'middle_name': fields.TextField(blank=True),
        'phone': fields.PhoneField(blank=True),
        'email': fields.EmailField(blank=True),
        'city_id': fields.ForeignKeyField(reference_model=City),
    }

    @classmethod
    def get_default_data(cls):
        return [
            (1, 'Ярослав', 'Демиденко', 'Текст', 'Владимирович','+7(999)9999999', 'test@test.ru', 1),
            (2, 'Ярослав', 'Демиденко', 'Текст', 'Владимирович','+7(999)9999999', 'test@test.ru', 2),
            (3, 'Ярослав', 'Демиденко', 'Текст', 'Владимирович','+7(999)9999999', 'test@test.ru', 1),
            (4, 'Ярослав', 'Демиденко', 'Текст', 'Владимирович','+7(999)9999999', 'test@test.ru', 2),
            (5, 'Ярослав', 'Демиденко', 'Текст', 'Владимирович','+7(999)9999999', 'test@test.ru', 1),
            (6, 'Ярослав', 'Демиденко', 'Текст', 'Владимирович','+7(999)9999999', 'test@test.ru', 3),
            (7, 'Ярослав', 'Демиденко', 'Текст', 'Владимирович','+7(999)9999999', 'test@test.ru', 4),
            (8, 'Ярослав', 'Демиденко', 'Текст', 'Владимирович','+7(999)9999999', 'test@test.ru', 5),
            (9, 'Ярослав', 'Демиденко', 'Текст', 'Владимирович','+7(999)9999999', 'test@test.ru', 3),
            (10, 'Ярослав', 'Демиденко', 'Текст', 'Владимирович','+7(999)9999999', 'test@test.ru', 4),
            (11, 'Ярослав', 'Демиденко', 'Текст', 'Владимирович','+7(999)9999999', 'test@test.ru', 5),
            (12, 'Ярослав', 'Демиденко', 'Текст', 'Владимирович','+7(999)9999999', 'test@test.ru', 3),
            (13, 'Ярослав', 'Демиденко', 'Текст', 'Владимирович','+7(999)9999999', 'test@test.ru', 4),
            (14, 'Ярослав', 'Демиденко', 'Текст', 'Владимирович','+7(999)9999999', 'test@test.ru', 5),
            (15, 'Ярослав', 'Демиденко', 'Текст', 'Владимирович','+7(999)9999999', 'test@test.ru', 7),
            (16, 'Ярослав', 'Демиденко', 'Текст', 'Владимирович','+7(999)9999999', 'test@test.ru', 8),
        ]