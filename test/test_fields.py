import unittest

from db import fields
from db.models import City


class TestViews(unittest.TestCase):

    def test_required(self):
        base_field = fields.BaseField(required=True)
        with self.assertRaises(fields.FieldValidError):
            base_field.validate(None)

    def test_int_field_validate(self):
        int_field = fields.IntField(required=True)
        self.assertEqual(int_field.validate(1), 1)
        self.assertEqual(int_field.validate([1]), 1)
        self.assertEqual(int_field.validate(["1"]), 1)
        with self.assertRaises(fields.FieldValidError):
            int_field.validate(None)
        with self.assertRaises(fields.FieldValidError):
            int_field.validate("test")
        with self.assertRaises(fields.FieldValidError):
            int_field.validate({"test": "test"})

    def test_int_field_create_sql(self):
        int_field = fields.IntField(required=True)
        self.assertEqual(int_field.create_field_sql("int_field"), "int_field INTEGER NOT NULL")

    def test_text_field_validate(self):
        text_field = fields.TextField(required=True)
        self.assertEqual(text_field.validate("test"), "test")
        with self.assertRaises(fields.FieldValidError):
            text_field.validate("")

    def test_id_field_create_sql(self):
        id_field = fields.PrimaryKeyField()
        self.assertEqual(id_field.create_field_sql("id"), "id INTEGER PRIMARY KEY AUTOINCREMENT")

    def test_id_field_reference_sql(self):
        fk_field = fields.ForeignKeyField(reference_model=City)
        self.assertEqual(fk_field.create_reference_sql("city_id"), "FOREIGN KEY (city_id) REFERENCES cities(id)")

    def test_email_field_validate(self):
        text_field = fields.EmailField(blank=True)
        self.assertEqual(text_field.validate("test@test.ru"), "test@test.ru")
        self.assertEqual(text_field.validate(""), "")
        with self.assertRaises(fields.FieldValidError):
            text_field.validate("test")
        with self.assertRaises(fields.FieldValidError):
            text_field.validate("test@test")
        with self.assertRaises(fields.FieldValidError):
            text_field.validate("test@test.r")

    def test_phone_field_validate(self):
        text_field = fields.PhoneField(blank=True)
        self.assertEqual(text_field.validate("+7(999)9999999"), "+7(999)9999999")
        self.assertEqual(text_field.validate(""), "")
        with self.assertRaises(fields.FieldValidError):
            text_field.validate("test")
        with self.assertRaises(fields.FieldValidError):
            text_field.validate("89999999999")
        with self.assertRaises(fields.FieldValidError):
            text_field.validate("+79999999999")
        with self.assertRaises(fields.FieldValidError):
            text_field.validate("+7(999)999999")
