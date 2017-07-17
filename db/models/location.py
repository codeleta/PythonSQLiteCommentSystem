from db import fields
from db.models._base import BaseModel


class Region(BaseModel):

    table_name = 'regions'
    fields = {
        'id': fields.PrimaryKeyField(),
        'title': fields.TextField(required=True)
    }

    @classmethod
    def get_default_data(cls):
        return [
            (1, 'Вологодская обл.'),
            (2, 'Ленинградская обл.'),
            (3, 'Московская обл.'),
            (4, 'Краснодарский край'),
        ]


class City(BaseModel):

    table_name = 'cities'
    fields = {
        'id': fields.PrimaryKeyField(),
        'title': fields.TextField(required=True),
        'region_id': fields.ForeignKeyField(required=True, reference_model=Region)
    }

    @classmethod
    def get_default_data(cls):
        return [
            (1, 'Вологда', 1),
            (2, 'Череповец', 1),
            (3, 'Выборг', 2),
            (4, 'Кировск', 2),
            (5, 'Волоколамск', 3),
            (6, 'Клин', 3),
            (7, 'Краснодар', 4),
            (8, 'Анапа', 4),
        ]