import pytest

from graphqlpy import field, params, query

class TestParams(object):

    def test_integer(self):
        assert params(1) == "1"
        assert params(1000) == "1000"

    def test_boolean(self):
        assert params(True) == "true"
        assert params(False) == "false"

    def test_list(self):
        assert params([1, True, "str"]) == '[1, true, "str"]'

    def test_dict(self):
        actual = params({
            'int': 1,
            'str': "str",
            'bool': True,
            'list': [1, True, "str"],
            'dict': {
                'list': ["one", "two", 3],
                'int': 1,
            }
        })

        expected = (
            '{int: 1, str: "str", bool: true, list: [1, true, "str"], dict: {'
            'list: ["one", "two", 3], int: 1}}'
        )

    def test_unknown(self):
        class Foo():
            pass

        with pytest.raises(TypeError) as err:
            params(Foo())

        assert str(err.value) == "Type 'Foo' is not supported."


class TestField(object):

    def test_name_only(self):
        assert field("name") == "name"

    def test_name_and_alias(self):
        assert field("alias", "name") == "alias: name"

    def test_name_and_params(self):
        assert field("name", paramOne=1) == "name(paramOne: 1)"

    def test_alias_name_and_params(self):
        assert field("alias", "name", paramOne=1) == "alias: name(paramOne: 1)"


class TestQuery(object):

    def test_string_fields(self):
        actual = query(
            {'me': (
                'id',
                'firstName',
                'lastName',
                {'birthday': (
                    'month',
                    'day',
                )},
                {'friends': (
                    'name'
                )},
            )}
        )

        expected = "me { id firstName lastName birthday { month day } friends { name } }"

        assert actual == expected

    def test_custom_fields(self):
        actual = query(
            {field("user", id=4): (
                'firstName',
                'lastName',
                {'birthday': (
                    'month',
                    'day',
                )},
            )}
        )

        expected = "user(id: 4) { firstName lastName birthday { month day } }"

        assert actual == expected
