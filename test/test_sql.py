import os
import unittest


from db.sql import SqlQuery, create_db, execute
from db.models.comment import Comment
from db.models.location import City, Region


class TestViews(unittest.TestCase):

    def setUp(self):
        self.db_name = 'test.db'
        create_db(self.db_name)

    def _getSqlQuery(self, model):
        return SqlQuery(model, self.db_name)

    def test_filter(self):
        query = self._getSqlQuery(Comment).select("id").query
        self.assertEqual(query, "SELECT id FROM comments")
        query = self._getSqlQuery(Comment).select(["id", "first_name"]).query
        self.assertEqual(query, "SELECT id, first_name FROM comments")

    def test_left_join(self):
        query = self._getSqlQuery(Comment).select(
            ["comments.id", "cities.title AS city_title"]
        ).left_join("city_id").query
        self.assertEqual(
            query,
            "SELECT comments.id, cities.title AS city_title FROM comments LEFT JOIN cities ON \
(cities.id = comments.city_id)"
        )

    def test_left_json_models_group_by(self):
        fields = [
            'cities.id', 'COUNT(comments.id) AS comments_count'
        ]
        query = self._getSqlQuery(City).select(fields).left_join("city_id", Comment).group_by("cities.id").query
        self.assertEqual(
            query,
            "SELECT cities.id, COUNT(comments.id) AS comments_count FROM cities LEFT JOIN comments ON \
(comments.city_id = cities.id) GROUP BY cities.id"
        )

    def test_order_by(self):
        query = self._getSqlQuery(Comment).select("id").order_by("id").query
        self.assertEqual(query, "SELECT id FROM comments ORDER BY id ASC")

    def test_where(self):
        query = self._getSqlQuery(Comment).select("id").where(**{"id": 3}).query
        self.assertEqual(query, "SELECT id FROM comments WHERE id = 3")
        query = self._getSqlQuery(Comment).select("id").where(**{"id__in": [3, 4]}).query
        self.assertEqual(query, "SELECT id FROM comments WHERE id IN (3, 4)")
        query = self._getSqlQuery(Comment).select("id").where(**{"id__gte": 3}).query
        self.assertEqual(query, "SELECT id FROM comments WHERE id >= 3")
        query = self._getSqlQuery(Comment).select("id").where(**{"first_name": "test"}).query
        self.assertEqual(query, "SELECT id FROM comments WHERE first_name = 'test'")

    def test_having(self):
        fields = [
            'cities.id', 'COUNT(comments.id) AS comments_count'
        ]
        query = self._getSqlQuery(City).select(fields).left_join("city_id", Comment)
        query = query.group_by("cities.id").where(True, **{"comments_count__gt": 2}).query
        self.assertEqual(
            query,
            "SELECT cities.id, COUNT(comments.id) AS comments_count FROM cities LEFT JOIN comments ON \
(comments.city_id = cities.id) GROUP BY cities.id HAVING comments_count > 2"
        )

    def test_created_db(self):
        qs = self._getSqlQuery(Comment).select("id").fetchall()
        self.assertEqual(len(qs), len(Comment.get_default_data()))
        self.assertIsInstance(qs[0], Comment)
        qs = self._getSqlQuery(City).select("id").fetchall()
        self.assertEqual(len(qs), len(City.get_default_data()))
        qs = self._getSqlQuery(Region).select("id").fetchall()
        self.assertEqual(len(qs), len(Region.get_default_data()))

    def test_execute_insert(self):
        count_fields = len(Comment.fields)
        sql = "INSERT INTO {} VALUES ({})".format(Comment.table_name, ", ".join(["?" for x in range(count_fields)]))
        execute(
            (sql, [None, 'Ярослав', 'Демиденко', 'Текст', 'Владимирович','+7(999)9999999', 'test@test.ru', 1]),
             self.db_name
        )
        qs = self._getSqlQuery(Comment).select("id").fetchall()
        self.assertEqual(len(qs), len(Comment.get_default_data()) + 1)

    def test_execute_update(self):
        qs = self._getSqlQuery(Comment).select("*").fetchall()
        item = qs[0]
        values = []
        item.values["first_name"] = "test"
        for name, value in item.values.items():
            if name != item.primary_field:
                value = "'{}'".format(value) if isinstance(value, str) else value
                values.append("{}={}".format(name, value))
        sql = "UPDATE {} SET {} WHERE {} = {}".format(
            item.table_name,
            ", ".join(values),
            item.primary_field,
            item.values[item.primary_field]
        )
        execute(sql, self.db_name)
        qs = self._getSqlQuery(Comment).select("*").fetchall()
        updated_item = qs[0]
        self.assertEqual(updated_item.values["first_name"], item.values["first_name"])

    def tearDown(self):
        os.remove("test.db")
