import unittest
from controllers.template_render import Template


class EachTests(unittest.TestCase):

    def test_each_iterable_in_context(self):
        rendered = Template('{% each items %}<div>{{it}}</div>{% end %}').render(items=['alex', 'maria'])
        self.assertEqual(rendered, '<div>alex</div><div>maria</div>')

    def test_each_iterable_as_literal_list(self):
        rendered = Template('{% each [1, 2, 3] %}<div>{{it}}</div>{% end %}').render()
        self.assertEqual(rendered, '<div>1</div><div>2</div><div>3</div>')

    def test_each_parent_context(self):
        rendered = Template('{% each [1, 2, 3] %}<div>{{..name}}-{{it}}</div>{% end %}').render(name='jon doe')
        self.assertEqual(rendered, '<div>jon doe-1</div><div>jon doe-2</div><div>jon doe-3</div>')

    def test_each_space_issues(self):
        rendered = Template('{% each [1,2, 3]%}<div>{{it}}</div>{%end%}').render()
        self.assertEqual(rendered, '<div>1</div><div>2</div><div>3</div>')

    def test_each_no_tags_inside(self):
        rendered = Template('{% each [1,2,3] %}<br>{% end %}').render()
        self.assertEqual(rendered, '<br><br><br>')

    def test_nested_objects(self):
        context = {'lines': [{'name': 'l1'}], 'name': 'p1'}
        template = '<h1>{{name}}</h1>{% each lines %}<span class="{{..name}}-{{it.name}}">{{it.name}}</span>{% end %}'
        rendered = Template(template).render(**context)
        self.assertEqual(rendered, '<h1>p1</h1><span class="p1-l1">l1</span>')

    def test_nested_tag(self):
        rendered = Template('{% each items %}{% if it %}yes{% end %}{% end %}').render(items=['', None, '2'])
        self.assertEqual(rendered, 'yes')


class IfTests(unittest.TestCase):

    def test_simple_if_is_true(self):
        rendered = Template('{% if num > 5 %}<div>more than 5</div>{% end %}').render(num=6)
        self.assertEqual(rendered, '<div>more than 5</div>')

    def test_simple_if_is_false(self):
        rendered = Template('{% if num > 5 %}<div>more than 5</div>{% end %}').render(num=4)
        self.assertEqual(rendered, '')

    def test_if_else_if_branch(self):
        template = '{% if num > 5 %}<div>more than 5</div>{% else %}<div>less than 5</div>{% end %}'
        rendered = Template(template).render(num=6)
        self.assertEqual(rendered, '<div>more than 5</div>')

    def test_if_else_else_branch(self):
        template = '{% if num > 5 %}<div>more than 5</div>{% else %}<div>less or equal to 5</div>{% end %}'
        rendered = Template(template).render(num=4)
        self.assertEqual(rendered, '<div>less or equal to 5</div>')

    def test_nested_if(self):
        tmpl = '{% if num > 5 %}{% each [1, 2] %}{{it}}{% end %}{% else %}{% each [3, 4] %}{{it}}{% end %}{% end %}'
        rendered = Template(tmpl).render(num=6)
        self.assertEqual(rendered, '12')
        rendered = Template(tmpl).render(num=4)
        self.assertEqual(rendered, '34')

    def test_truthy_thingy(self):
        self.assertEqual(Template('{% if items %}we have items{% end %}').render(items=[]), '')
        self.assertEqual(Template('{% if items %}we have items{% end %}').render(items=None), '')
        self.assertEqual(Template('{% if items %}we have items{% end %}').render(items=''), '')
        self.assertEqual(Template('{% if items %}we have items{% end %}').render(items=[1]), 'we have items')


class CallTests(unittest.TestCase):

    def test_no_args(self):
        with self.assertRaises(TypeError):
            Template('{% call pow %}').render(pow=pow)

    def test_positional_args(self):
        rendered = Template('{% call pow 2 3 %}').render(pow=pow)
        self.assertEqual(rendered, '8')


if __name__ == '__main__':
    unittest.main()
